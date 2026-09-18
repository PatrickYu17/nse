import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts/install.py"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="nse-install-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.project = self.base / "project with spaces"
        self.project.mkdir()
        self.home = self.base / "home"
        self.home.mkdir()
        self.env = {key: value for key, value in os.environ.items()
                    if key not in ("XDG_CONFIG_HOME", "PI_CODING_AGENT_DIR")}
        self.env["HOME"] = str(self.home)
        self.env["USERPROFILE"] = str(self.home)

    def run_install(self, *args, env=None):
        return subprocess.run([sys.executable, "-B", str(INSTALL), *args], cwd=self.base,
                              env=env or self.env, text=True, capture_output=True)

    def test_project_targets_copy_complete_portable_package(self):
        targets = {
            "shared": ".agents/skills", "codex": ".agents/skills",
            "claude-code": ".claude/skills", "pi": ".pi/skills",
            "opencode": ".opencode/skills", "kilo": ".kilo/skills",
            "cursor": ".cursor/skills", "gemini": ".gemini/skills",
            "copilot": ".github/skills",
        }
        for harness, parent in targets.items():
            with self.subTest(harness=harness):
                project = self.project / harness
                project.mkdir()
                result = self.run_install("--harness", harness, "--project", str(project))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                destination = project / parent / "no-slop-engineering"
                for relative in ("SKILL.md", "references/rules.md", "adapters/activation.md",
                                 "scripts/setup_formal.py", "security-audit/GUIDE.md",
                                 "vendor/leanfmt/lakefile.toml", "LICENSE"):
                    self.assertEqual((destination / relative).read_bytes(), (ROOT / relative).read_bytes())
                self.assertEqual(list(destination.rglob("SKILL.md")), [destination / "SKILL.md"])
                self.assertFalse((project / "AGENTS.md").exists())
                self.assertFalse((project / "CLAUDE.md").exists())

    def test_global_defaults_resolve_in_isolated_home_without_writes(self):
        targets = {
            "shared": ".agents/skills", "codex": ".agents/skills",
            "claude-code": ".claude/skills", "pi": ".pi/agent/skills",
            "opencode": ".config/opencode/skills", "kilo": ".kilo/skills",
            "cursor": ".cursor/skills", "gemini": ".gemini/skills",
            "copilot": ".copilot/skills",
        }
        for harness, parent in targets.items():
            with self.subTest(harness=harness):
                result = self.run_install("--harness", harness, "--global", "--dry-run")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(str(self.home / parent / "no-slop-engineering"), result.stdout)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_global_install_uses_isolated_home(self):
        result = self.run_install("--harness", "codex", "--global")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.home / ".agents/skills/no-slop-engineering/SKILL.md").is_file())

    def test_relocated_package_can_scaffold_using_its_bundled_resources(self):
        destination = self.base / "portable resources" / "no-slop-engineering"
        result = self.run_install("--destination", str(destination))
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run(
            [sys.executable, "-B", str(destination / "scripts/setup_formal.py"),
             "--scaffold-only", str(self.project)],
            cwd=self.base, env=self.env, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((self.project / "formal/Formal/Proofs.lean").is_file())
        self.assertEqual((self.project / "vendor/leanfmt/lean-toolchain").read_bytes(),
                         (destination / "vendor/leanfmt/lean-toolchain").read_bytes())

    def test_config_directory_overrides(self):
        cases = (("opencode", "XDG_CONFIG_HOME", "opencode/skills"),
                 ("pi", "PI_CODING_AGENT_DIR", "skills"))
        for harness, variable, suffix in cases:
            with self.subTest(harness=harness):
                custom = self.base / "custom configuration"
                result = self.run_install("--harness", harness, "--global", "--dry-run",
                                          env={**self.env, variable: str(custom)})
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(str(custom / suffix / "no-slop-engineering"), result.stdout)
                self.assertFalse(custom.exists())

    def test_custom_destination_and_existing_user_files(self):
        destination = self.base / "custom" / "no-slop-engineering"
        result = self.run_install("--destination", str(destination))
        self.assertEqual(result.returncode, 0, result.stderr)
        entry = destination / "SKILL.md"
        entry.write_text("user customized instructions\n")
        result = self.run_install("--destination", str(destination))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stderr)
        self.assertEqual(entry.read_text(), "user customized instructions\n")

    def test_rejects_bad_name_missing_project_and_recursive_destination(self):
        cases = (
            ("--destination", str(self.base / "wrong-name")),
            ("--harness", "codex", "--project", str(self.base / "missing")),
            ("--destination", str(ROOT / "no-slop-engineering"), "--dry-run"),
        )
        for args in cases:
            with self.subTest(args=args):
                result = self.run_install(*args)
                self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_rejects_ambiguous_arguments(self):
        for args in (("--global",), ("--harness", "unknown", "--global"),
                     ("--harness", "codex", "--destination", str(self.base / "no-slop-engineering"))):
            with self.subTest(args=args):
                self.assertNotEqual(self.run_install(*args).returncode, 0)

    def test_dangling_destination_symlink_is_not_followed(self):
        destination = self.base / "no-slop-engineering"
        outside = self.base / "missing-target"
        destination.symlink_to(outside, target_is_directory=True)
        result = self.run_install("--destination", str(destination))
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(destination.is_symlink())
        self.assertFalse(outside.exists())
