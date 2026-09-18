from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_portable_metadata_contract(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        name = re.search(r"^name: (.+)$", frontmatter, re.MULTILINE).group(1)
        self.assertEqual(name, "no-slop-engineering")
        self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)
        description = re.search(r"description: >-\n((?:  .+\n)+)", frontmatter).group(1)
        self.assertGreater(len(description.strip()), 0)
        self.assertLessEqual(len(description), 1024)
        self.assertEqual(set(re.findall(r"^([a-z-]+):", frontmatter, re.MULTILINE)),
                         {"name", "description", "license"})

    def test_only_public_entry_is_discoverable(self):
        self.assertEqual(sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob("SKILL.md")), ["SKILL.md"])

    def test_supporting_markdown_is_not_a_second_skill(self):
        for path in ROOT.rglob("*.md"):
            if path == ROOT / "SKILL.md":
                continue
            text = path.read_text()
            if text.startswith("---\n"):
                frontmatter = text.split("---", 2)[1]
                self.assertFalse(re.search(r"^name:", frontmatter, re.MULTILINE)
                                 and re.search(r"^description:", frontmatter, re.MULTILINE), str(path))

    def test_stable_rule_definitions_are_complete_and_unique(self):
        rules = (ROOT / "references/rules.md").read_text()
        actual = re.findall(r"^- \*\*([HPQ]-\d\d) ", rules, re.MULTILINE)
        expected = [f"{prefix}-{number:02}" for prefix, count in (("H", 12), ("P", 6), ("Q", 8))
                    for number in range(1, count + 1)]
        self.assertEqual(actual, expected)

    def test_entry_references_exist(self):
        for name in re.findall(r"(?:references|adapters)/[a-z-]+\.md", (ROOT / "SKILL.md").read_text()):
            self.assertTrue((ROOT / name).is_file(), name)

    def test_audit_companions_do_not_reference_old_entry(self):
        for path in (ROOT / "security-audit").glob("*.md"):
            self.assertNotIn("`SKILL.md`", path.read_text(), str(path))

    def test_bundled_audit_markdown_links_resolve(self):
        for path in (ROOT / "security-audit").glob("*.md"):
            for target in re.findall(r"\]\(([^)]+\.md)\)", path.read_text()):
                self.assertTrue((path.parent / target).is_file(), f"{path.name}: {target}")
