import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import blog_automation as ba  # noqa: E402

GOOD = textwrap.dedent("""\
    ---
    title: "テスト記事"
    tags:
      - Copilot
    private: true
    ---

    ## はじめに

    ![画面](../images/test-slug/01_home.png)

    ```json
    {}
    ```
    """)


class BlogAutomationTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = self.tmp.name
        ba.ROOT = self.root
        os.makedirs(os.path.join(self.root, "drafts"))
        os.makedirs(os.path.join(self.root, "public"))
        os.makedirs(os.path.join(self.root, "images", "test-slug"))
        open(os.path.join(self.root, "images", "test-slug", "01_home.png"), "wb").close()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path

    def test_check_passes_for_complete_article(self):
        self.assertEqual(ba.check_article(self.write("drafts/20261123_test-slug.md", GOOD)), [])

    def test_check_reports_unfinished_items(self):
        text = GOOD.replace("```json", "```").replace("01_home.png", "02_missing.png")
        text += "\n<!-- SHOT: 03_settings.png | 設定画面 -->\nTODO あとで書く\n"
        problems = "\n".join(ba.check_article(self.write("drafts/20261123_test-slug.md", text)))
        self.assertIn("言語指定", problems)
        self.assertIn("02_missing.png", problems)
        self.assertIn("03_settings.png", problems)
        self.assertIn("仮テキスト", problems)

    def test_pick_article_ignores_shot_plan_and_images(self):
        paths = ["drafts/20261123_test-slug.md", "drafts/20261123_test-slug.shot-plan.md", "images/test-slug/01_home.png"]
        self.assertEqual(ba.pick_article(paths), "drafts/20261123_test-slug.md")
        with self.assertRaises(SystemExit):
            ba.pick_article(paths + ["drafts/20261124_other.md"])

    def test_publish_moves_article_and_rewrites_images(self):
        self.write("drafts/20261123_test-slug.md", GOOD)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        dst = ba.publish("drafts/20261123_test-slug.md", "owner/repo", "main", private=False)
        self.assertEqual(dst, "public/20261123_test-slug.md")
        self.assertFalse(os.path.exists(os.path.join(self.root, "drafts/20261123_test-slug.md")))
        with open(os.path.join(self.root, dst), encoding="utf-8") as f:
            out = f.read()
        self.assertIn("private: false", out)
        self.assertIn('<img src="https://raw.githubusercontent.com/owner/repo/main/images/test-slug/01_home.png" alt="画面" width="60%">', out)

    def test_publish_refuses_article_with_pending_shots(self):
        self.write("drafts/20261123_test-slug.md", GOOD + "\n<!-- SHOT: 02_x.png | x -->\n")
        with self.assertRaises(SystemExit):
            ba.publish("drafts/20261123_test-slug.md", "owner/repo", "main", private=True)
        self.assertTrue(os.path.exists(os.path.join(self.root, "drafts/20261123_test-slug.md")))

    def test_add_idea_inserts_next_number_before_footer(self):
        body = "## 今週のネタ候補\n\n### 1. A\n- x\n\n### 2. B\n- y\n\n---\n### 次の操作\n- `/write 番号`\n"
        new_body, number = ba.add_idea(body, "自分のネタ\n画面を多めに\n\nデモも入れる")
        self.assertEqual(number, 3)
        self.assertLess(new_body.index("### 3. 自分のネタ"), new_body.index("---\n### 次の操作"))
        self.assertIn("  > 画面を多めに\n  >\n  > デモも入れる", new_body)
        self.assertEqual(ba.add_idea("", "最初のネタ")[0], "### 1. 最初のネタ\n- **出典**: 著者のアイデア\n- **slug**: 未定（下書き作成時に決める）\n")
        with self.assertRaises(SystemExit):
            ba.add_idea(body, "  \n")


if __name__ == "__main__":
    unittest.main()
