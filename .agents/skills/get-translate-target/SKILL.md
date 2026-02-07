---
name: get-translate-target
description: translation-assets/targets.yml を基に、upstream と docs-ja の差分（未翻訳ファイル、upstream が更新されたファイル）を抽出して一覧化する作業で使う。翻訳対象の洗い出し、更新検知、優先度付けのためのターゲットリスト作成時に使用する。
---

# get-translate-target

Use this skill to generate a translation target list by comparing `upstream` and `docs-ja` based on `translation-assets/targets.yml`.

## Workflow

1. Run the script from the repo root:

```powershell
python .agents/skills/get-translate-target/scripts/get-translate-target.py
```

2. Confirm `translation-assets/targets.yml` values: `base.upstream_dir`, `base.output_dir`, `include`, `exclude`.

3. Read the output: `Missing` = untranslated files, `Outdated` = upstream file timestamp is newer than the translated file.

## Notes

- The script uses file modification times to detect updates.
- If `include` patterns become more complex than `**` directory globs, extend the script’s include resolution logic.

## Script Options

- `--targets-path` (default: `translation-assets/targets.yml`)
- `--upstream-root` / `--output-root` (override values in the YAML)
- `--json` (emit JSON instead of text)
- `--out-file` (write output to a file path)
