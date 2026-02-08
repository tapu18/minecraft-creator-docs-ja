````markdown
# get-translate-target

`translation-assets/targets.yml` に基づいて `upstream` と `docs-ja` を比較し、翻訳対象リストを生成するために使用します。

## ワークフロー

1. リポジトリのルートからスクリプトを実行します:

```
python /scripts/get-translate-target.py
```

2. `translation-assets/targets.yml` の値を確認します: `base.upstream_dir`, `base.output_dir`, `include`, `exclude`。

3. 出力を確認します: `Missing` = 未翻訳のファイル、`Outdated` = upstream のファイルの更新時刻が翻訳済みファイルより新しい。

## 注意

- スクリプトはファイルの最終更新時刻を使って更新を検出します。
- `include` のパターンが `**` のディレクトリグロブより複雑になる場合は、スクリプトの include 解決ロジックを拡張してください。

## スクリプトオプション

- `--targets-path` (デフォルト: `translation-assets/targets.yml`)
- `--upstream-root` / `--output-root` (YAML の値を上書きします)
- `--json` (テキストの代わりに JSON を出力します)
- `--out-file` (出力をファイルパスに書き込みます)

````
