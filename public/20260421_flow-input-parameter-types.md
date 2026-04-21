---
title: Copilot Studio のエージェントフローで使える入力パラメーターの型と日付型の回避策
tags:
  - PowerPlatform
  - Microsoft365
  - PowerAutomate
  - CopilotStudio
private: true
updated_at: '2026-04-21T16:41:55+09:00'
id: 0c3a37891b9e59795612
organization_url_name: null
slide: false
ignorePublish: false
---

## はじめに

Microsoft Copilot Studio のエージェントからエージェントフローを呼び出す際、入力パラメーターで使えるデータ型には制約があります。

日付型を渡そうとして「あれ、Date 型がない…？」とハマったのが本記事を書くきっかけです。サポートされている型は **Number / String / Boolean の 3 つだけ** で、日付型やオブジェクト型は使えません。

では、日付データをフローに渡したい場合はどうするか？ということで、本記事では入力パラメーターの型の制約を整理しつつ、日付型の回避策を解説していきます。

公式ドキュメントは以下です。

[入力変数と出力変数を使った情報の受け渡し - Microsoft Copilot Studio | Microsoft Learn](https://learn.microsoft.com/ja-jp/microsoft-copilot-studio/advanced-flow-input-output)

## エージェントフローとは

エージェントフローは、Copilot Studio のエージェントからフローを呼び出す仕組みです。フロー側のトリガーには **「エージェントがフローを呼び出すとき」** を使います。

エージェントフローは Copilot Studio のトピック内から作成出来ます。トピックのノード追加で **「ツールを追加する」** を選択し、**「基本ツール」** タブから **「新しいエージェントフロー」** を選ぶと、このトリガーが設定された状態でフローが作成されます。

このトリガーに入力パラメーターを定義しておくと、Copilot Studio のトピック内のアクションノードからフローを呼び出す際に、エージェント側の変数をフローに渡すことが出来ます。フローの処理結果は **「エージェントに応答する」** アクションで出力パラメーターとしてエージェントに返す、という流れです。

<img src="https://raw.githubusercontent.com/s-shimiz/Blog/main/images/verification/20260402_flow-input-types/%E3%83%95%E3%83%AD%E3%83%BC%E3%83%88%E3%83%AA%E3%82%AC%E3%83%BC%E7%94%BB%E9%9D%A2%E3%81%AE%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88.png" alt="フロートリガー画面" width="60%">

## 使えるパラメーターの型

公式ドキュメントに記載されている、エージェントフローの入力/出力パラメーターで使える型は以下の通りです。

| 型 | サポート状況 |
| --- | --- |
| Number | ✅ サポート |
| String | ✅ サポート |
| Boolean | ✅ サポート |
| Object | ❌ 非サポート |
| Date | ❌ 非サポート |
| Timestamp | ❌ 非サポート |
| List [String] | ❌ 非サポート |
| List [Number] | ❌ 非サポート |
| List [Boolean] | ❌ 非サポート |
| List [Object] | ❌ 非サポート |
| List [Date] | ❌ 非サポート |
| List [Timestamp] | ❌ 非サポート |

見ての通り非サポートが多いです・・・
使えるのは **Number / String / Boolean** の 3 つだけで、Date や Timestamp、List 系、Object はすべて非サポートです。

実際にフローのトリガーで入力パラメーターを日付型で設定してみると、こんな感じです。

<img src="https://raw.githubusercontent.com/s-shimiz/Blog/main/images/verification/20260402_flow-input-types/%E3%83%95%E3%83%AD%E3%83%BC%E3%83%88%E3%83%AA%E3%82%AC%E3%83%BC%E3%82%92%E6%97%A5%E4%BB%98%E5%9E%8B%E3%81%A7%E8%A8%AD%E5%AE%9A.png" alt="フロートリガーを日付型で設定" width="60%">

Copilot Studio 側からこのフローを呼び出そうとすると、エラーになります。これは、フロー側で日付型として定義したパラメーターが、Copilot Studio 側では String 型として認識されてしまい、型が一致しないためです。

<img src="https://raw.githubusercontent.com/s-shimiz/Blog/main/images/verification/20260402_flow-input-types/%E3%83%95%E3%83%AD%E3%83%BC%E3%83%88%E3%83%AA%E3%82%AC%E3%83%BC%E3%82%92%E6%97%A5%E4%BB%98%E3%81%A7%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%9F%E5%A0%B4%E5%90%88%E3%81%AE%E3%82%A8%E3%83%A9%E3%83%BC%E7%94%BB%E9%9D%A2.png" alt="フロートリガーを日付型で使用した場合のエラー画面" width="60%">

ということで、日付型をそのまま使うことは出来ません。回避策は後述します。

:::note info
エージェントからフローに送れるデータ量に上限はありませんが、フローからエージェントに返せるデータは **1 アクションあたり 1 MB まで** という制限があります。
:::

## Number / String / Boolean の使い方

### String（テキスト）

最も汎用的な型です。Copilot Studio 側の変数の型が `String` であれば、そのままフローの入力パラメーター（テキスト）にマッピング出来ます。後述する日付型の回避策でも String が活躍します。

### Number（数値）

Copilot Studio 側で `Number` 型の変数をフローの入力パラメーター（数値）に渡すことが出来ます。整数・小数のどちらも扱えます。

### Boolean（はい/いいえ）

Copilot Studio 側の `Boolean` 型の変数をフローの入力パラメーター（はい/いいえ）にマッピングします。フラグ的な用途で使うことが多いです。

この 3 つの型でカバーしきれない場合に、工夫が必要になってきます。

## 日付型を渡したい場合の回避策

さて、本題の日付型です。Copilot Studio のエージェント側で日付データを取得していても、エージェントフローの入力パラメーターに Date 型は使えません。

ではどうするかというと、**日付を文字列（String）に変換してからフローに渡し、フロー側で日付データに戻す** という方法で対応出来ます。

### Copilot Studio 側: 質問ノードで日付を取得する

まず、トピック内で質問ノードを使ってユーザーから日付を取得します。質問ノードの「特定」で **日付** を選択すると、ユーザーの回答が日付型の変数として保存されます。

<img src="https://raw.githubusercontent.com/s-shimiz/Blog/main/images/verification/20260402_flow-input-types/Copilot%20Studio%20%E3%81%AE%E6%97%A5%E4%BB%98%E7%A2%BA%E8%AA%8D.png" alt="Copilot Studio の質問ノードで日付を確認" width="30%">

ここで取得した変数（例: `Topic.Date`）は日付型ですが、エージェントフローにそのまま渡すことは出来ません。そこで次のステップで文字列に変換します。

### Copilot Studio 側: 日付を文字列に変換する

Copilot Studio のアクションノードで、フローの入力パラメーターに値を渡す際、Power Fx の `Text()` 関数を使って日付型の変数を文字列に変換します。

例えば、`Topic.Date` という日付型の変数がある場合、以下のように設定します。

```power-fx
Text(Topic.Date)
```

これでフローのテキスト型の入力パラメーターに日付を文字列として渡すことが出来ます。

<img src="https://raw.githubusercontent.com/s-shimiz/Blog/main/images/verification/20260402_flow-input-types/Copilot%20Studio%20%E3%81%AE%E3%82%A2%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3%E3%83%8E%E3%83%BC%E3%83%89%E7%94%BB%E9%9D%A2.png" alt="Copilot Studio のアクションノード画面" width="30%">

### フロー側: formatDateTime() で日付データに変換する

フロー側では、テキストとして受け取った日付文字列を `formatDateTime()` 関数で任意のフォーマットに変換します。

「作成」アクションなどで以下の式を使います。

```text
formatDateTime(triggerBody()?['text_2'], 'yyyy/M/d')
```

`triggerBody()?['text_2']` の部分はトリガーで定義した入力パラメーターの内部名です。実際の名前はフローのトリガーで定義したパラメーター名に応じて変わるので、動的コンテンツから選択するのが確実です。

<img src="https://raw.githubusercontent.com/s-shimiz/Blog/main/images/verification/20260402_flow-input-types/%E3%83%95%E3%83%AD%E3%83%BC%E5%81%B4%E3%81%AE%20formatDateTime%20%E5%A4%89%E6%8F%9B%E7%94%BB%E9%9D%A2.png" alt="フロー側の formatDateTime 変換画面" width="50%">

そうすることで、エージェントから渡された日付文字列を `2026/4/21` のようなフォーマットの日付データとして扱えるようになります。

:::note warn
`Text()` で変換された文字列のフォーマットは Copilot Studio の言語設定に依存する場合があります。フロー側で `formatDateTime()` を使う際は、入力される文字列のフォーマットを意識しておくと良いです。
:::

## まとめ

Copilot Studio のエージェントフローで使える入力/出力パラメーターの型は **Number / String / Boolean** の 3 つだけです。Date や Object、List 系はサポートされていません。

日付型を渡したい場合は以下の手順で対応出来ます。

1. **Copilot Studio 側**: `Text(Topic.Date)` で日付を文字列に変換
2. **フロー側**: `formatDateTime()` で文字列を日付データに変換

ぶっちゃけていうと、テキスト型への変換でほとんどのケースはカバー出来るので、型の制約がそこまで致命的な問題にはなりません。ただ、List 型や Object 型がサポートされると、もっと柔軟にデータをやり取り出来るようになるので、今後のアップデートに期待したいところです。

普段開発をされていない方にとっては、データ型の扱いはちょっとクセがあるように感じるかもしれません。ただ、こういった細かい部分さえ押さえてしまえば、Copilot Studio はノーコードで業務を自動化できる非常に強力なツールです。ぜひ活用してみてください！
