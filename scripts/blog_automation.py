#!/usr/bin/env python3
"""記事作成ワークフロー（GitHub Actions / ローカル）の補助スクリプト。

サブコマンド:
  find-article  PR などで変更された記事ファイル（drafts/ または public/ の .md）を 1 つ返す
  check         公開前チェック（フロントマター・仮テキスト・画像・コードブロック・撮影プレースホルダー）
  publish       drafts/ の記事を public/ に移動し、private と画像 URL を投稿用に整える
  add-idea      ネタ候補 Issue の本文に著者のアイデアを次の番号で追加する
"""

import argparse
import os
import re
import subprocess
import sys
import urllib.parse

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ARTICLE_RE = re.compile(r"^(drafts|public)/\d{8}_[a-z0-9][a-z0-9-]*\.md$")
SHOT_RE = re.compile(r"<!--\s*SHOT:\s*([^|>]+?)\s*(?:\|\s*(.*?))?\s*-->")
PLACEHOLDER_RE = re.compile(r"TODO|TBD|〇〇|（本文）|（ここに書く）|\(ここに書く\)")
LOCAL_IMG_MD_RE = re.compile(r"!\[([^\]]*)\]\((\.\./images/[^)\s]+)\)")
LOCAL_IMG_TAG_RE = re.compile(r'(<img\s[^>]*src=")(\.\./images/[^"]+)(")')


def git_changed_files(base):
    out = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=AMR", f"{base}...HEAD"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def pick_article(paths):
    candidates = sorted({p.replace("\\", "/") for p in paths if ARTICLE_RE.match(p.replace("\\", "/"))})
    if len(candidates) != 1:
        raise SystemExit(f"記事ファイルを 1 つに特定できません: {candidates or 'なし'}")
    return candidates[0]


def split_frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def check_article(path):
    """問題点のリストを返す。空なら公開可能。"""
    problems = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    fm, body = split_frontmatter(text)
    if fm is None:
        problems.append("フロントマター（--- で囲まれたブロック）がありません")
    else:
        title = re.search(r"^title:\s*(.*)$", fm, re.M)
        if not title or title.group(1).strip() in ("", '""', "''"):
            problems.append("title が空です")
        if not re.search(r"^tags:\s*\r?\n\s+-\s+\S", fm, re.M):
            problems.append("tags が 1 つもありません")
        if not re.search(r"^private:\s*(true|false)\s*$", fm, re.M):
            problems.append("private: true / false がありません")

    in_code = False
    for no, line in enumerate(body.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code and stripped == "```":
                problems.append(f"本文 {no} 行目: コードブロックに言語指定がありません")
            in_code = not in_code
            continue
        if in_code:
            continue
        if re.match(r"^#\s", line):
            problems.append(f"本文 {no} 行目: 見出しは ## から始めてください")
        if PLACEHOLDER_RE.search(line):
            problems.append(f"本文 {no} 行目: 仮テキストが残っています: {stripped[:40]}")
        for shot in SHOT_RE.finditer(line):
            problems.append(f"本文 {no} 行目: 未撮影のスクリーンショットがあります: {shot.group(1)}")

    base_dir = os.path.dirname(os.path.abspath(path))
    for rel in [m.group(2) for m in LOCAL_IMG_MD_RE.finditer(body)] + [m.group(2) for m in LOCAL_IMG_TAG_RE.finditer(body)]:
        img = os.path.normpath(os.path.join(base_dir, urllib.parse.unquote(rel)))
        if not os.path.exists(img):
            problems.append(f"画像が見つかりません: {rel}")
    return problems


def to_raw_url(rel, repo, branch):
    # ../images/a/b.png -> https://raw.githubusercontent.com/<repo>/<branch>/images/a/b.png
    parts = urllib.parse.unquote(rel)[len("../"):].split("/")
    return f"https://raw.githubusercontent.com/{repo}/{branch}/" + "/".join(urllib.parse.quote(p) for p in parts)


def rewrite_images(body, repo, branch):
    body = LOCAL_IMG_MD_RE.sub(
        lambda m: f'<img src="{to_raw_url(m.group(2), repo, branch)}" alt="{m.group(1)}" width="60%">', body)
    return LOCAL_IMG_TAG_RE.sub(lambda m: m.group(1) + to_raw_url(m.group(2), repo, branch) + m.group(3), body)


def publish(src_rel, repo, branch, private):
    src_rel = src_rel.replace("\\", "/")
    if not src_rel.startswith("drafts/"):
        raise SystemExit(f"drafts/ 配下の記事を指定してください: {src_rel}")
    src = os.path.join(ROOT, src_rel)
    problems = check_article(src)
    if problems:
        raise SystemExit("公開前チェックで問題が見つかりました:\n- " + "\n- ".join(problems))

    with open(src, encoding="utf-8") as f:
        text = f.read()
    fm, body = split_frontmatter(text)
    fm = re.sub(r"^private:\s*(true|false)\s*$", f"private: {'true' if private else 'false'}", fm, flags=re.M)
    new_text = f"---\n{fm}\n---\n" + rewrite_images(body, repo, branch)

    dst_rel = "public/" + os.path.basename(src_rel)
    dst = os.path.join(ROOT, dst_rel)
    if os.path.exists(dst):
        raise SystemExit(f"公開先にすでにファイルがあります: {dst_rel}")
    subprocess.run(["git", "mv", src_rel, dst_rel], cwd=ROOT, check=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_text)
    return dst_rel


def add_idea(body, comment):
    """ネタ候補 Issue の本文に著者のアイデアを次の番号で追加し、(新しい本文, 番号) を返す。

    comment は `/add-idea` を除いたコメント本文。1 行目をタイトル、2 行目以降を著者メモとして扱う。
    """
    lines = comment.strip().splitlines()
    title = lines[0].strip() if lines else ""
    if not title:
        raise SystemExit("アイデアのタイトルが空です")
    note = "\n".join(lines[1:]).strip()
    numbers = [int(n) for n in re.findall(r"^###\s+(\d+)\.", body, re.M)]
    number = max(numbers, default=0) + 1
    entry = [f"### {number}. {title}", "- **出典**: 著者のアイデア", "- **slug**: 未定（下書き作成時に決める）"]
    if note:
        entry.append("- **著者メモ**:")
        entry += [f"  > {line}" if line.strip() else "  >" for line in note.splitlines()]
    entry = "\n".join(entry) + "\n"

    footer = re.search(r"^(?:---[ \t]*\r?\n\s*)?###\s+次の操作", body, re.M)
    if footer:
        head = body[:footer.start()].rstrip()
        new_body = (head + "\n\n" if head else "") + entry + "\n" + body[footer.start():]
    else:
        new_body = (body.rstrip() + "\n\n" if body.strip() else "") + entry
    return new_body, number


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("find-article")
    p.add_argument("--base", default="origin/main", help="比較元のブランチ（既定: origin/main）")

    p = sub.add_parser("check")
    p.add_argument("article")

    p = sub.add_parser("publish")
    p.add_argument("article")
    p.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "s-shimiz/Blog"))
    p.add_argument("--branch", default="main")
    p.add_argument("--private", action="store_true", help="Qiita の限定共有のまま投稿する")

    p = sub.add_parser("add-idea", help="ネタ候補 Issue の本文に著者のアイデアを追加する")
    p.add_argument("--body-file", required=True, help="現在の Issue 本文（このファイルを上書きする）")
    p.add_argument("--idea-file", required=True, help="アイデア（1 行目: タイトル、2 行目以降: メモ）")

    a = ap.parse_args()
    if a.cmd == "find-article":
        print(pick_article(git_changed_files(a.base)))
    elif a.cmd == "check":
        problems = check_article(os.path.join(ROOT, a.article))
        for prob in problems:
            print(f"- {prob}")
        print("✅ 問題は見つかりませんでした" if not problems else f"❌ {len(problems)} 件の問題があります")
        sys.exit(1 if problems else 0)
    elif a.cmd == "publish":
        print(publish(a.article, a.repo, a.branch, a.private))
    elif a.cmd == "add-idea":
        with open(a.body_file, encoding="utf-8") as f:
            body = f.read()
        with open(a.idea_file, encoding="utf-8") as f:
            new_body, number = add_idea(body, f.read())
        with open(a.body_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_body)
        print(number)


if __name__ == "__main__":
    main()
