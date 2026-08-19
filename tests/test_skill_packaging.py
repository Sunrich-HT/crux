import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillPackagingTests(unittest.TestCase):
    def test_crux_requires_explicit_invocation(self):
        metadata = (ROOT / "skills/crux/agents/openai.yaml").read_text(encoding="utf-8")
        self.assertRegex(metadata, r"(?m)^\s*allow_implicit_invocation:\s*false\s*$")
        self.assertNotRegex(metadata, r"(?m)^\s*allow_implicit_invocation:\s*true\s*$")

    def test_skill_description_reinforces_explicit_only_boundary(self):
        skill = (ROOT / "skills/crux/SKILL.md").read_text(encoding="utf-8")
        frontmatter = skill.split("---", 2)[1]
        self.assertIn("explicitly mentions $crux", frontmatter)
        self.assertIn("do not mention $crux", frontmatter)


if __name__ == "__main__":
    unittest.main()
