upstreamの特定のドキュメントを翻訳してください。原則として、翻訳は一つのファイルずつ行ってください。
翻訳は以下の手順で行ってください。 
1. translation-assets/rules.md を閲覧し、翻訳の手順とルールを把握する
2. /docs-jaに/upstreamと対応するようにディレクトリ・ファイルを作成する
3. 対象ファイルにtranslation-assets/glossary.ymlに記載のない固有名詞や表記ゆれしやすい語句が含まれる場合、translation-assets/glossary.ymlに新たに追記する
  - glossaryへの追加ルールはrules.mdに記載されているのでそれに従ってください。
4. 翻訳作業を行い、翻訳した結果を /docs-ja のファイルに記載する
  - 翻訳の際は translation-assets/style-guide.md の文体に従うこと
  - 特定の語句は translation-assets/glossary.yml に対応表があることに留意する
5. translation-assets/translated.yml と translation-assets/titles.yml に翻訳したファイルの情報を追加する