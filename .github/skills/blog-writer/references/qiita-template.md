# Qiita 記事テンプレート

## フロントマター

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

### フィールド説明

| フィールド | 説明 |
|-----------|------|
| `title` | 記事の内容が伝わる日本語のタイトル |
| `tags` | YAML 配列形式で関連タグを列挙 |
| `private` | `true` で限定公開（下書き）。レビュー後に `false` へ変更して公開 |

## ファイル命名

`public/yyyymmdd_slug.md`

例: `public/20260217_agent-builder-vs-copilot-studio.md`

## 記事テンプレート

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

（この記事で何をやるか、動機や背景を 2〜4 文で簡潔に）

## 本文

（本文）

## まとめ

（振り返りと今後の展望）
```

## Qiita 固有の記法

### 注記ブロック

```markdown
:::note info
補足情報をここに書く
:::

:::note warn
注意事項をここに書く
:::

:::note alert
警告をここに書く
:::
```

### 画像

```markdown
![代替テキスト](../images/記事のスラッグ/ファイル名.png)
```

### コードブロック

````markdown
```python:main.py
print("Hello, World!")
```
````

### アコーディオン（折りたたみ）

```markdown
<details><summary>詳細はこちら</summary>

折りたたまれた内容

</details>
```
