---
description: "Qiita 記事の作成・編集時に適用。Qiita フロントマター、タグ規約、命名規則を含む。Use when: Qiita 記事を書く、public/ 配下のファイルを編集"
applyTo: "public/**/*.md"
---

# Qiita 記事ルール

## フロントマター

記事の先頭には必ず以下の形式の YAML フロントマターを付ける。

```yaml
---
title: "記事のタイトル"
tags:
  - Microsoft365
  - Copilot
  - CopilotStudio
private: true
---
```

- `title`: 記事の内容が伝わる日本語のタイトル
- `tags`: 記事に関連するタグ（YAML 配列形式）
- `private`: 下書き時は `true`、公開時に `false` へ変更

## よく使うタグ

`Microsoft365`, `Copilot`, `CopilotStudio`, `PowerPlatform`, `MicrosoftGraph`, `PowerAutomate`, `PowerFx`, `AI`, `GenerativeAI`

## ファイル命名

`yyyymmdd_slug.md`（例: `20260217_agent-builder-vs-copilot-studio.md`）

- `public/` ディレクトリに配置する（Qiita CLI の管理ディレクトリ）
- 先頭に作成日を付与
- 日付の後にはハイフン区切りの slug を続ける

## Qiita 固有の記法

### 画像

```markdown
![代替テキスト](../images/記事のスラッグ/ファイル名.png)
```

### 注記

```markdown
:::note info
補足情報
:::

:::note warn
注意事項
:::

:::note alert
警告
:::
```

### リンク

通常の Markdown リンクを使用する。URL を独立行に書いてもカード化されない（Zenn とは異なる）。
