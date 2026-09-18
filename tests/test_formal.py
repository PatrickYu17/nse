import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "scripts" / "setup-formal.sh"
spec = importlib.util.spec_from_file_location("proof_checker", ROOT / "scripts" / "check-proofs.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="nse-test-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve() / 'project with spaces "and quotes"'
        self.project.mkdir()

    def run_setup(self, *options, env=None):
        return subprocess.run(
            ["bash", str(SETUP), *options, str(self.project)],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env,
        )

    def create(self):
        result = self.run_setup("--scaffold-only")
        self.assertEqual(result.returncode, 0, result.stdout)
        return self.project / "formal"

    def assert_refused_without_changes(self):
        before = {str(p.relative_to(self.project)): p.read_bytes()
                  for p in self.project.rglob("*") if p.is_file()}
        result = self.run_setup("--scaffold-only")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        after = {str(p.relative_to(self.project)): p.read_bytes()
                 for p in self.project.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_fresh_layout_and_explicit_target(self):
        formal = self.create()
        for line in (formal / "Formal.lean").read_text().splitlines():
            module = line.removeprefix("import ")
            self.assertTrue((formal / (module.replace(".", "/") + ".lean")).is_file())
        self.assertIn('defaultTargets = ["Formal"]', (formal / "lakefile.toml").read_text())
        self.assertEqual((formal / "lean-toolchain").read_bytes(),
                         (ROOT / "vendor/leanfmt/lean-toolchain").read_bytes())

    def test_rerun_preserves_user_proofs_and_inventory(self):
        formal = self.create()
        proof = formal / "Formal/Proofs.lean"
        proof.write_text("theorem user_proof : True := True.intro\n")
        (formal / "theorems.txt").write_text("Formal.user_proof\n")
        result = self.run_setup("--scaffold-only")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(proof.read_text(), "theorem user_proof : True := True.intro\n")
        self.assertEqual((formal / "theorems.txt").read_text(), "Formal.user_proof\n")

    def test_existing_lean_configuration_is_not_overwritten(self):
        formal = self.project / "formal"
        formal.mkdir()
        (formal / "lakefile.lean").write_text("-- existing package\n")
        (formal / "Formal.lean").write_text("-- user work\n")
        self.assert_refused_without_changes()
        self.assertFalse((self.project / "vendor").exists())

    def test_orphan_sources_are_not_overwritten(self):
        formal = self.project / "formal"
        formal.mkdir()
        (formal / "Spec.lean").write_text("-- retain me\n")
        self.assert_refused_without_changes()

    def test_modified_configuration_requires_manual_integration(self):
        formal = self.create()
        with (formal / "lakefile.toml").open("a") as target:
            target.write('\n[[require]]\nname = "other"\n')
        self.assert_refused_without_changes()

    def test_incomplete_scaffold_is_not_silently_repaired(self):
        formal = self.create()
        (formal / "Formal/Spec.lean").unlink()
        self.assert_refused_without_changes()

    def test_changed_vendor_is_rejected(self):
        self.create()
        (self.project / "vendor/leanfmt/lean-toolchain").write_text("different-version\n")
        self.assert_refused_without_changes()

    def test_vendor_build_cache_does_not_break_rerun(self):
        self.create()
        cache = self.project / "vendor/leanfmt/.lake"
        cache.mkdir()
        (cache / "generated").write_text("build output")
        result = self.run_setup("--scaffold-only")
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_symlinked_formal_directory_is_rejected(self):
        outside = self.project.parent / "outside"
        outside.mkdir()
        (self.project / "formal").symlink_to(outside, target_is_directory=True)
        result = self.run_setup("--scaffold-only")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / "vendor").exists())

    def test_symlinked_vendor_parent_is_rejected(self):
        outside = self.project.parent / "outside"
        outside.mkdir()
        (self.project / "vendor").symlink_to(outside, target_is_directory=True)
        result = self.run_setup("--scaffold-only")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / "formal").exists())

    def test_symlinked_managed_file_is_rejected(self):
        formal = self.create()
        proof = formal / "Formal/Proofs.lean"
        proof.unlink()
        outside = self.project.parent / "outside.lean"
        outside.write_text("-- retain\n")
        proof.symlink_to(outside)
        result = self.run_setup("--scaffold-only")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(outside.read_text(), "-- retain\n")

    def test_empty_inventory_fails_before_build(self):
        formal = self.create()
        result = subprocess.run([sys.executable, str(formal / "check-proofs.py")],
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no guarantee theorems", result.stdout)

    def test_setup_propagates_build_failure_with_mocked_lake(self):
        tools = self.project.parent / "tools"
        tools.mkdir()
        for name, body in {"elan": "exit 0", "lake": 'if [ "$1" = build ]; then exit 13; fi'}.items():
            path = tools / name
            path.write_text("#!/bin/sh\n" + body + "\n")
            path.chmod(0o755)
        result = self.run_setup(env={**os.environ, "PATH": f"{tools}:{os.environ['PATH']}"})
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("Scaffold build passed", result.stdout)
        self.assertIn("13", result.stdout)


class AxiomPolicyTests(unittest.TestCase):
    def test_closed_proof_and_standard_axioms(self):
        self.assertEqual(checker.check_axioms("Formal.ok", "'Formal.ok' does not depend on any axioms"), set())
        self.assertEqual(checker.check_axioms("Formal.ok", "'Formal.ok' depends on axioms: [propext,\nClassical.choice, Quot.sound]"), checker.ALLOWED_AXIOMS)

    def test_sorry_and_project_axioms_fail(self):
        for axiom in ("sorryAx", "Formal.assumeCorrect"):
            with self.subTest(axiom=axiom), self.assertRaisesRegex(ValueError, "unapproved axioms"):
                checker.check_axioms("Formal.bad", f"'Formal.bad' depends on axioms: [{axiom}]")

    def test_unknown_wrong_and_duplicate_output_fail_closed(self):
        outputs = ["new Lean output format", "'Other.ok' does not depend on any axioms",
                   "'Formal.ok' does not depend on any axioms\n'Formal.ok' depends on axioms: [sorryAx]"]
        for output in outputs:
            with self.subTest(output=output), self.assertRaises(ValueError):
                checker.check_axioms("Formal.ok", output)

    def test_inventory_rejects_code_injection_and_duplicates(self):
        with tempfile.TemporaryDirectory(prefix="nse-inventory-") as directory:
            path = Path(directory) / "theorems.txt"
            for content in ("", "# only a comment\n", "Formal.ok\nFormal.ok\n", "Formal.ok; #eval 1\n"):
                path.write_text(content)
                with self.subTest(content=content), self.assertRaises(ValueError):
                    checker.read_theorems(path)


@unittest.skipUnless(os.environ.get("NSE_LIVE_LEAN") == "1", "set NSE_LIVE_LEAN=1 with the pinned Lean toolchain provisioned")
class LiveLeanTests(unittest.TestCase):
    def test_build_proof_and_reject_incomplete_or_assumed_proofs(self):
        self.assertIsNotNone(shutil.which("lake"), "live tests require lake")
        with tempfile.TemporaryDirectory(prefix="nse-live-") as directory:
            project = Path(directory).resolve()
            result = subprocess.run(["bash", str(SETUP), str(project)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            formal = project / "formal"
            proofs = formal / "Formal/Proofs.lean"
            inventory = formal / "theorems.txt"
            cases = [
                ("theorem checked (n : Nat) : n = n := rfl", 0, "PASS Formal.checked"),
                ("set_option warningAsError false in\ntheorem checked : False := by sorry", 1, "sorryAx"),
                ("axiom assumed : False\ntheorem checked : False := assumed", 1, "Formal.assumed"),
            ]
            inventory.write_text("Formal.checked\n")
            for source, expected, evidence in cases:
                with self.subTest(source=source):
                    proofs.write_text(f"import Formal.Impl\nnamespace Formal\n{source}\nend Formal\n")
                    result = subprocess.run([sys.executable, "check-proofs.py"], cwd=formal,
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                    self.assertIn(evidence, result.stdout + result.stderr)
            proofs.write_text("import Formal.Impl\n\nnamespace Formal\ntheorem checked (n : Nat) : n = n := rfl\nend Formal\n")
            for command in (
                ["lake", "exe", "fmt", "-r", "Formal.lean", "Formal"],
                ["lake", "exe", "fmt", "--check", "-r", "Formal.lean", "Formal"],
                [sys.executable, "check-proofs.py"],
            ):
                result = subprocess.run(command, cwd=formal, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            with proofs.open("a") as target:
                target.write("\n\n\n")
            before = proofs.read_bytes()
            result = subprocess.run(["lake", "exe", "fmt", "--check", "-r", "Formal.lean", "Formal"],
                                    cwd=formal, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(proofs.read_bytes(), before, "format check must not rewrite files")
