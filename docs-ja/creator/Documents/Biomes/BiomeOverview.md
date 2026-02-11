````markdown
---
author: mammerla
ms.author: mikeam
title: Biome JSON and Overview
description: "A reference document discussing biomes and custom biomes"
ms.service: minecraft-bedrock-edition
ms.date: 04/10/2025
---

<a id="biome-json-and-overview"></a>
# バイオーム JSON と概要

> [!VIDEO https://www.youtube.com/embed/zMF3JPahrPQ]
> [!NOTE]
> このビデオは、実験的なカスタムバイオーム機能について素早く理解するのに非常に役立ちます。

バイオームとは、特定の領域でゲームがどのように振る舞うかを決定する一連のプロパティに名前を付けたものです。これには、再生される音楽や空の色といったリソースパックに関する設定、雪が積もるかどうかやどのようなモブがスポーンするかといったビヘイビアパックに関する設定が含まれます。

その領域の表面に存在するブロックは、通常そのバイオームで指定されます（例: 海では水、砂漠では砂）。ただし、特定のバイオームを視覚化したときに想像するようなブロックの多くは、[features](../FeaturesTaxonomy.md) のような他のシステムによって生成されます（例: 木の葉、花、鉄鉱石など）。
> [!NOTE]
> 構造物やエンティティはバイオームに関連付けられることがありますが、バイオーム自体の一部ではありません。

Minecraft のバイオームは、地形の特徴がまったく異なる場合があります。カスタムバイオームのデータを作成することで、次のような変更が可能です。

- 地形の全体的な形状
- バイオームの種類の出現頻度
- 表層や地下のバイオームを構成するブロックの種類
- 木や草、花などの装飾的な要素の分布
- バイオーム内でスポーンするモブ
- 気候
- …など

クライアントバイオームファイルを使用した視覚的・音響的なバイオームのカスタマイズについては、[Customizing Audio and Visual Biome Features](./../../Reference/Content/ClientBiomesReference/Examples/ClientBiomesOverview.md) のガイドを参照してください。

<a id="the-minecraft-overworld"></a>
## Minecraft のオーバーワールド

簡単に言うと、Minecraft エンジンはレベルシードとブロックの三次元座標 (X,Y,Z) を組み合わせて、滑らかに変化する一連の「ノイズ」値（例: 湿度、侵食、奇妙さなど）を生成します。ゲームはこれらのノイズ値を使って2つの異なる処理を行います。1つ目は比較的単純な世界の形状を生成するロジック（空気・水・石だけの Minecraft を想像してください）で、2つ目はその位置にどのバイオームを割り当てるかを決めるロジックです。例えば、暖かく乾いた平坦で高くない領域は Desert に割り当てられるかもしれません。

一般的な地形形状が作られ、バイオームが選ばれた後、例えば砂漠にサボテンが配置されるなど、視覚的に興味深い「features」の配置が行われます（構造物の配置や洞窟生成のような他の過程もあります）。最後にブロック生成が完了すると、その領域で適切なエンティティのスポーンや、フェンスの開閉に関わる描画用ジオメトリ生成といったゲームプレイに関わる処理が行われます。

<a id="how-does-this-compare-to-the-overworld-before-caves-cliffs-part-2"></a>
### Caves & Cliffs Part 2 前のオーバーワールドとの比較

「Caves & Cliffs Part 2」アップデートはオーバーワールド生成に大きな変更をもたらしました。関連する変更の一つは、生成ロジックが2次元アプローチから3次元アプローチへアップグレードされたことです。これにより Y 座標（高さ）を考慮できるようになり、あるバイオームのブロックや要素が別のバイオームの上に直接生成されるようになりました。例えば、平原が表層に見えていても、真下を掘ると Deep Dark や Lush Cave が現れる場合があります。

もう一つの重要な変更は、バイオームの選択タイミングです。以前はバイオームがより早い段階で選択され、バイオーム固有のブロックや要素が配置される前に地形の形状に影響を与えていました。この変更により、古い実験的なカスタムバイオームはオーバーワールドに表示されなくなる副作用が生じました。

<a id="adding-custom-biomes"></a>
## カスタムバイオームの追加

カスタムバイオームは次の2つの方法で導入できます。

1. オーバーワールドのバイオーム定義を上書きするビヘイビアパックのバイオーム定義を提供する方法。例えば、識別子が `desert` の定義を用意すれば、バニラの砂漠バイオーム定義を上書きできます。砂の代わりに土を使うといった変更が可能です。

2. 新しい [partial biome replacements](./CustomPartialbiomeReplacement.md)（実験的機能）を使う方法。この機能を使うと、既存のバニラバイオームの一部を置き換える形で新しいバイオームを挿入できます。

これらのオーバーライドの例は GitHub の [Chill Oasis sample](https://github.com/microsoft/minecraft-samples/tree/main/chill_oasis_blocks_and_features) にあります。

カスタムバイオームの大きな利点は、視覚や音響面を上書きできる点にあります。ビヘイビアパック内で地表に追加するブロックの種類を上書きする以外にも、クライアントバイオーム定義（リソースパック内）でいくつかの視覚・音響特性を上書きできます（詳細は Clientbiomes のドキュメントを参照）。

<a id="biome-json-definitions"></a>
## バイオーム JSON 定義

バイオームはビヘイビアパックの `biomes` サブフォルダ内の JSON ファイルから読み込まれます。読み込みはファイルごとに 1 つのバイオームを想定しており、ファイル名と実際のバイオーム名は一致している必要があります。新しい名前のファイルを追加するとゲームで使用可能になりますが、既存バイオームを上書きする場合は既存の名前と一致するファイルを配置します。新しいバイオームを追加する場合、ワールド生成に参加させるためのコンポーネントデータを用意しないとワールドに表示されない点に注意してください。

<a id="json-format"></a>
## JSON フォーマット

すべてのバイオームは `"format_version"` フィールドで対象とするバージョンを指定する必要があります。残りのバイオームデータは独立した JSON サブオブジェクト（コンポーネント）に分かれます。

一般に、コンポーネントはバイオームが参加するゲーム挙動を定義し、コンポーネントのフィールドはそのパラメータを指定します。

大きく分けて2つのカテゴリのコンポーネントがあります。

1. `name:` プレフィックスを持つ名前空間付きコンポーネント（ゲーム内の特定の挙動にマッピングされるもの）。メンバーフィールドでその挙動をパラメータ化します。有効なマッピングがある名前のみサポートされます。

2. `tags` によるもの。これは `"minecraft:tags"` コンポーネントの下で定義されます。タグは英数字と `.`、`_` を含むことができ、コードやデータが存在チェックを行うためにバイオームに付与されます。

<a id="biome-definitions"></a>
## バイオーム定義

バイオームを定義する説明とコンポーネントを含みます。

| Name | Type | Required | Description |
|:-----------|:-----------|:-------|:-----------|
| description| Object of type biome Description| Required| コンポーネント以外の設定（バイオーム名など）|
| components| Object of type biome Components| Required| このバイオームのコンポーネント一覧|

<a id="biome-description"></a>
## バイオーム説明

バイオームのコンポーネント以外の設定を含みます。

| Name | Type | Required | Description |
|:-----------|:-----------|:-------|:-----------|
| identifier| String| Required| バイオームの識別子。`/locate biome` のような他の機能で使用されます|

<a id="biome-json-file"></a>
## バイオーム JSON ファイル

フォーマットバージョンとバイオーム定義を含みます。

| Name | Type | Required | Description |
|:-----------|:-----------|:-------|:-----------|
| format_version| String| Required| このファイルで使用される JSON スキーマのバージョン|
| minecraft:biome| Object of type biome Definition| Required| 単一のバイオーム定義|

<a id="block-specifier"></a>
## ブロック指定子

特定のブロックを指定します（文字列のブロック名または JSON オブジェクトのどちらでも可）。

| Name | Type | Required | Description |
|:-----------|:-----------|:-------|:-----------|
| name| String| Required| ブロック名|
| states| Object| Optional| 各状態名をメンバに持ち、Boolean/整数/文字列値を設定|

<a id="biome-components"></a>
## バイオームコンポーネント

[Server Biome Components](./../../Reference/Content/BiomesReference/Examples/ComponentList.md) を参照して、ビヘイビアパック内で使用できるバイオームコンポーネントの一覧を確認してください。さらに、リソースパック内で使用できるクライアントバイオームのコンポーネントについては [Client Biomes](./../../Reference/Content/ClientBiomesReference/Examples/ClientBiomesOverview.md) のドキュメントを参照してください。

<a id="example-biome"></a>
### 例: バイオーム

```json
{
  "plains": {
    "format_version": "1.20.60",
    "minecraft:climate": {
      "downfall": 0.4,
      "snow_accumulation": [ 0.0, 0.125 ],
      "temperature": 0.8
    },
    "minecraft:overworld_height": {
      "noise_type": "lowlands"
    },
    "minecraft:surface_parameters": {
      "sea_floor_depth": 7,
      "sea_floor_material": "minecraft:gravel",
      "foundation_material": "minecraft:stone",
      "mid_material": "minecraft:dirt",
      "top_material": "minecraft:grass_block"
    },
    "minecraft:tags": {
      "tags": [
        "animal",
        "monster",
        "overworld",
        "plains"
      ]
    }
  }
}
```

<a id="troubleshooting"></a>
## トラブルシューティング

- ### バイオームの変更が反映されない

    - ファイル名がバイオーム識別子と正確に一致していることを確認してください（例: `desert.json` は `desert` の識別子と一致する必要があります）
    - 既存のチャンクが再生成されない場合は新しいワールドを作成して試してください
    - JSON 構文エラーがないかコンテンツログを確認してください
    - ビヘイビアパックが有効になっていることを確認してください

- ### 表層の素材がおかしい
    - 一部のブロックは表層素材として適切に機能しないことがあります
    - カスタムブロックを使用する前に、まずバニラのブロックでテストしてください
    - ブロック識別子に `minecraft:` プレフィックスが含まれていることを確認してください

- ### 気候が期待通りに動作しない
    - 温度は想定より広い領域に影響することを考慮してください
    - 雪が降る条件には、温度が 0.15 未満かつ downfall 値が > 0 の両方が必要です
    - 一部の気候効果は特定の条件下でのみ適用されます

<a id="next-steps"></a>
## 次のステップ

バイオームのオーバーライドに慣れたら、次の高度なトピックを参照してください。

- [Partial Biome Replacements](../Biomes/CustomPartialBiomeReplacement.md)
- [Client Biomes](./../../Reference/Content/ClientBiomesReference/Examples/ClientBiomesOverview.md)
- [Features](../FeaturesTaxonomy.md)

````
