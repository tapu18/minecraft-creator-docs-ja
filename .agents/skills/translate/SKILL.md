---
name: translate
description: ドキュメントファイルを翻訳します
---

upstreamの特定のドキュメントを翻訳するskillです。原則として、翻訳は一つのファイルずつ行ってください。
翻訳は以下の手順で行ってください。 
1. translation-assets/rules.md を閲覧し、翻訳の手順とルールを把握する
2. /docs-jaに/upstreamと対応するようにディレクトリ・ファイルを作成する
3. 翻訳した結果を /docs-ja のファイルに記載する
  - 翻訳の際は translation-assets/style-guide.md の文体に従うこと
  - 特定の語句は translation-assets/glossary.yml に対応表があることに留意する
  - 固有名詞や表記ゆれしやすいと判断する語句が原文に含まれる場合、一度ユーザーに翻訳案とともに確認を行う。確認がとれたらglossary.ymlに新たに追記する。  
