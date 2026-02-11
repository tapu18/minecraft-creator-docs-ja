# AI Translation Prompt

翻訳作業を行ってください。
以下の手順で行ってください。
1. 翻訳対象の取得
    - githubのissueのうちaiラベルが付いたものを取得してください
    - issueが複数ある場合は一番古い物を取ってください
2. 翻訳作業
    - ./translate.mdに従って翻訳作業を行ってください。
    - 作業するブランチは`AItranslate/#{issue番号}`としてください
3. PRの作成 
    - 翻訳作業が完了したらPRを作成してください
    - PR作成の際にはaiラベルと、glossary.ymlに変更がある場合はglossaryラベルを付けてください
    - PR本文にはマージされた際にissueをクローズ出来るように、`Closes #{issue番号}`を記載してください