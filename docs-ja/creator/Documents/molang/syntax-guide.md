---
author: chipotle
ms.author: mikeam
title: Molang 構文ガイド
description: "Molang の構文、概念、関数に関するリファレンス。"
ms.service: minecraft-bedrock-edition
ms.date: 08/13/2025
---

# Molang 構文ガイド

> [!NOTE]
> まだ [Molang 入門](./introduction.md) を読んでいない場合は、先にそちらを確認してください。

Molang は Minecraft の JSON ファイルに埋め込むためのシンプルな式言語です。ランタイムでの値計算を高速に行い、ゲーム内の値やシステムに直接アクセスできます。Molang によって、アニメーションなどの低レイヤーなシステムで柔軟なデータ駆動の挙動を高パフォーマンスで実現できます。

## 構文

Molang は C ライクな簡単な構文を持ちます。式は単純な値、数学計算やクエリ関数、または複雑なサブ式の組み合わせで構成できます。

C と同様に文はセミコロン (`;`) で終端しますが、単純な場合は末尾の `;` を省略でき、単一の式の評価結果がそのまま返されます。

```text
math.sin(query.anim_time * 1.23)
```

複数文の複雑なケースでは、各文に `;` が必要です。複雑なサブ式では最後に `return` 文で最終値を返してください。

```text
temp.moo = math.sin(query.anim_time * 1.23);
temp.baa = math.cos(query.life_time + 2.0);
return temp.moo * temp.moo + temp.baa;
```

`return` を忘れると戻り値は `0.0` になります。

> [!NOTE]
> Molang のほとんどの識別子は大文字小文字を区別しません（文字列は例外で、入力されたケースをそのまま保持します）。

## キーワード

以下は Molang の主な構文要素です。

| キーワード | 説明 |
|:-----------|:-----------|
| `1.23` | 数値リテラル |
| `! || && < <= >= > == !=` | 論理演算子 |
| `* / + -` | 基本的な算術演算子 |
| `(` `)` | 優先順位を制御する括弧 |
| `{` `}` | 実行スコープ |
| `??` | null 合体演算子 |
| `geometry.texture_name` | エンティティ定義で名付けられたジオメトリ参照 |
| `material.texture_name` | マテリアル参照 |
| `texture.texture_name` | テクスチャ参照 |
| `math.function_name` | 数学関数 |
| `query.function_name` | エンティティのプロパティ参照 |
| `temp.variable_name` | 一時変数 |
| `variable.variable_name` | エンティティ変数 |
| `context.variable_name` | ゲームが提供する読み取り専用のコンテキスト変数 |
| `<test> ? <if true> : <if false>` | 三項条件演算子 |
| `<test> ? <if true>` | 二項条件演算子 |
| `this` | 現在評価される値（文脈依存） |
| `return` | 複雑な式での戻り値 |
| `->` | 別のエンティティからのデータアクセス |
| `loop` | 繰り返し実行 |
| `for_each` | エンティティ配列の繰り返し |
| `break` / `continue` | ループ制御 |
| `[` `]` | 配列アクセス |

## 変数

変数には主に三つの寿命（有効範囲）があります。

- **一時変数 (temp)**: スコープ内で有効。実行効率のため、式実行の間はグローバルに生存する場合があります。
- **エンティティ変数 (variable)**: そのエンティティの寿命にわたって値を保持します（現在は保存されないためワールド再読み込みで初期化されます）。
- **コンテキスト変数 (context)**: 読み取り専用でゲーム側が提供します。

## public変数

エンティティの変数は原則プライベートです。他エンティティから読み取り専用でアクセス可能にするには、その変数に `public` 設定を行ってください。

### 例

```json
{
  "format_version": "1.10.0",
  "minecraft:client_entity": {
    "description": {
      "scripts": {
        "variables": {
          "variable.oink": "public"
        },
        "initialize": [
          "variable.oink = 0;"
        ],
      },
    }
  }
}
```

## 値の型

- 数値はすべて浮動小数点です。
- ブール値は `0.0` または `1.0` として扱われます。
- 配列インデックスは浮動小数点を整数にキャストし、負値は `0` にクランプ、範囲外はラップします。
- エラー（ゼロ除算や欠損変数など）は通常 `0.0` を返します。

サポートされる型には以下が含まれます：Geometry, Texture, Material, Actor Reference, Actor Reference Array, String, Struct。

## クエリ関数

`query.*` 系関数はゲームデータを参照します。引数が無い場合は括弧を省略します。詳細は [クエリ関数](../../Reference/Content/MolangReference/Examples/MolangConcepts/QueryFunctions.md) を参照してください。

## エイリアス

打鍵量を減らすための省略形が使えます。例：`query.moo` → `q.moo`、`variable.moo` → `v.moo`。

### エイリアスマッピング

| フルネーム | エイリアス |
|:-------|:-------|
| `context.moo` | `c.moo` |
| `query.moo` | `q.moo` |
| `temp.moo` | `t.moo` |
| `variable.moo` | `v.moo` |

## 構造体 (Structs)

構造体は使用時に暗黙的に定義されます。複雑な入れ子構造を使えますが、過度に深いネストは避けてください。

## 文字列

文字列はシングルクォートで囲います（例：`'minecraft:pig'`）。空文字は `''` です。現在文字列操作は `==` と `!=` の比較のみをサポートします。

> [!NOTE]
> 文字列中にシングルクォートを含めることはできません（エスケープ未対応）。

## 数学関数

豊富な数学関数が用意されています。詳細は Math Functions リファレンスを参照してください。

## ブレースによるスコープ

複数文を `{` `}` でまとめることで一つのグループとして扱えます。ループや条件内で使います。

## 条件文

`?` 演算子は簡潔な分岐を提供します。`A ? B` は `A` が真なら `B` を実行し、`A ? B : C` は三項演算子です。

## ループ

`loop(<count>, <expression>);` で繰り返し実行します。最大カウントは安全のため 1024 です。

### break / continue

`break` は最内ループを抜け、`continue` は次の反復に移ります。ネスト時の挙動はドキュメント内の例を参照してください。

## Null 合体演算子

`a ?? b` は `a` が解決可能なら `a`、そうでなければ `b` を返します。リソース型（material, texture, geometry）には使えません。

> [!IMPORTANT]
> 無効な操作は `0.0` を返し、非公開ビルドではコンテンツエラーを発生させることがあります。Marketplace へのアップロード前に式が安全か確認してください。

## バージョン差分

Molang はパックの `manifest.json` にある `min_engine_version` を参照して適用するルールを決定します。変更は式ごとに適用されるため、複数パックをロードした場合でも個別に処理されます。

原文: https://github.com/MicrosoftDocs/minecraft-creator/blob/{SHA}/{PATH}
