# Copilot Instructions — M365 Copilot & Copilot Studio ブログ

## プロジェクト概要

Microsoft 365 Copilot および Copilot Studio に関する技術ブログ記事の原稿を管理するリポジトリ。
記事は主に **Qiita** に投稿する（必要に応じて Zenn にも投稿）。

## ディレクトリ構成

```
qiita/             # Qiita 用の記事 (メイン投稿先)
articles/          # Zenn 形式の記事 (必要に応じて)
images/            # 記事で使用するスクリーンショット・図
snippets/          # 記事内で参照するコードスニペット
```

## 記事の書き方

### Qiita 記事テンプレート（メイン）

```markdown
---
title: ""
tags:
  - Microsoft365
  - Copilot
  - CopilotStudio
private: true
---

## はじめに

（本文）
```

- よく使うタグ: `Microsoft365`, `Copilot`, `CopilotStudio`, `PowerPlatform`, `MicrosoftGraph`
- `private: true` で限定公開 → レビュー後に `false` へ変更して公開

### Zenn 記事テンプレート（サブ）

```markdown
---
title: ""
emoji: "🤖"
type: "tech"
topics: ["Microsoft365", "Copilot", "CopilotStudio"]
published: false
---

## はじめに

（本文）
```

- `topics` は最大 5 つ
- `published: false` で下書き保存 → レビュー後に `true` へ変更

## ファイル命名規則

- 記事ファイルは先頭に作成日を `yyyymmdd_` 形式で付与する（例: `20260217_agent-builder-vs-copilot-studio.md`）
- 日付の後にはハイフン区切りの slug を続ける

## 執筆規約

1. **言語**: 日本語で執筆する
2. **見出し**: `##` から始める（`#` は Qiita/Zenn がタイトルに使用）
3. **画像**: `images/<記事slug>/` 配下に配置し、相対パスで参照
4. **コードブロック**: 言語を必ず指定する（`power-fx`, `json`, `typescript`, `python`, `yaml` など）
5. **Microsoft 製品名**: 正式名称を使う（例: ✅ `Microsoft 365 Copilot` / ❌ `M365 Copilot`、ただし記事内で初出以降は `Copilot` と略記可）
6. **スクリーンショット**: UI 操作の手順記事では必ず添付する

## AI アシスタントへの指示

- 記事の生成・編集を依頼された場合、特に指定がなければ **Qiita テンプレート**とフロントマターを使用すること
- 技術的な正確性を重視し、公式ドキュメント（learn.microsoft.com）の情報に基づくこと
- Copilot Studio のアクション、トピック、コネクタに関する記述では、最新の UI/用語を使用すること
- コード例では Power Fx、HTTP コネクタの JSON、Graph API のリクエスト例など、実際に動作するスニペットを提供すること
- 記事の対象読者は Copilot / Power Platform に興味がある日本語話者の開発者・IT 管理者
