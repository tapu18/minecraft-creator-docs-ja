---
author: cam-wilkerson
ms.author: v-cwilkerson
ai-usage: ai-assisted
title: カスタムバイオームチュートリアル
description: "Minecraft: Bedrock Editionでカスタムバイオームを作成するためのステップバイステップのチュートリアル（ビヘイビアパックとリソースパックの両方を含む）。"
ms.service: minecraft-bedrock-edition
ms.date: 01/20/2025
---

<a id="custom-biome-tutorial"></a>
# カスタムバイオームチュートリアル

このチュートリアルでは、サーフェス生成、フィーチャ、モブ、フォグ、環境効果を含めて、ゼロからカスタムバイオームを作成する手順を解説します。最終的に、ワールドに生成される「クリスタル洞窟」バイオームを作成します。

<a id="in-this-tutorial"></a>
## このチュートリアルで学ぶこと

次の内容を扱います:

> [!div class="checklist"]
>
> - バイオーム定義ファイルの構成方法
> - サーフェス素材と地形の設定方法
> - 鉱石や植生などのカスタムフィーチャの追加方法
> - バイオーム固有のモブスポーン設定方法
> - フォグやパーティクルで雰囲気を作る方法
> - バイオームの登録とテスト方法

<a id="prerequisites"></a>
## 前提条件

開始する前に、以下を完了していることを推奨します:

- [Biome Overview](../Biomes/BiomeOverview.md) を読む
- ビヘイビアパックおよびリソースパックの構造を理解していること
- テスト用の開発環境を準備していること

> [!TIP]
> 完成したリソースおよびビヘイビアパックのサンプルは、GitHubの [Crystal Caverns biome sample](https://github.com/microsoft/minecraft-samples/tree/main/crystal_caverns) にあります。

<a id="manifest-files"></a>
## マニフェストファイル

### ビヘイビアパックのマニフェスト

（以下のJSONはそのまま使用します）

```json
{
  "format_version": 2,
  "header": {
    "name": "Crystal Caverns Biome",
    "description": "Adds the Crystal Caverns biome to your world",
    "uuid": "YOUR-UUID-HERE-1234-abcd-1234567890ab",
    "version": [1, 0, 0],
    "min_engine_version": [1, 21, 40]
  },
  "modules": [
    {
      "type": "data",
      "uuid": "YOUR-UUID-HERE-5678-efgh-1234567890ab",
      "version": [1, 0, 0]
    }
  ],
  "dependencies": [
    {
      "uuid": "YOUR-RP-UUID-HERE-ijkl-1234567890ab",
      "version": [1, 0, 0]
    }
  ]
}
```

### リソースパックのマニフェスト

（以下のJSONはそのまま使用します）

```json
{ 
  "format_version": 2, 
  "header": { 
    "name": "Crystal Caverns Resources", 
    "description": "Resources for the Crystal Caverns biome", 
    "uuid": "YOUR-RP-UUID-HERE-ijkl-1234567890ab", 
    "version": [1, 0, 0], 
    "min_engine_version": [1, 21, 40] 
  }, 
  "modules": [ 
    { 
      "type": "resources", 
      "uuid": "YOUR-UUID-HERE-mnop-1234567890ab", 
      "version": [1, 0, 0] 
    } 
  ] 
}
```

> [!IMPORTANT]
> 各パックにはユニークなUUIDを生成してください。オンラインのUUIDジェネレーターやIDEの機能を利用できます。

<a id="configuring-the-behavior-pack"></a>
## ビヘイビアパックの設定

カスタムバイオームはビヘイビアパックとリソースパックの両方にコンテンツが必要です。ビヘイビアパック（サーバー側）には、ワールド生成やゲームプレイに影響する機能的なバイオーム定義が含まれます。

| コンテンツ | 目的 |
|---------|---------|
| **Biome definition** | バイオームの基本プロパティ（気候、サーフェス、地形形状） |
| **Features** | 生成される構造や装飾（鉱石、植物、クリスタルなど） |
| **Feature rules** | フィーチャがどこでどの頻度で出現するかのルール |
| **Spawn rules** | どのモブがどの条件でスポーンするか |

定義JSONファイルはバイオームのコアプロパティを格納する中心ファイルです。多くの気候や地形に関する設定はここで扱われるため、プロセスに慣れるとワールドのカスタマイズが容易になります。まずは次のフォルダー構成を作成します。

![Crystal caverns bp](../Media/CustomBiome/caverns_bp.png)

### バイオームJSONファイル

ビヘイビアパック内の `biomes` フォルダに **crystal_caverns.json** というファイルを作成し、以下を入れてください（コードはそのまま使用します）。

```json
{ 
  "format_version": "1.21.40", 
  "minecraft:biome": { 
    "description": { 
      "identifier": "custom:crystal_caverns" 
    }, 
    "components": { 
      "minecraft:climate": { 
        "temperature": 0.5, 
        "downfall": 0.0, 
        "snow_accumulation": [0.0, 0.0], 
        "ash": 0.0, 
        "red_spores": 0.0, 
        "white_ash": 0.0 
      }, 
      "minecraft:overworld_height": { 
        "noise_type": "lowlands" 
      }, 
      "minecraft:surface_parameters": { 
        "sea_floor_depth": 7, 
        "sea_floor_material": "minecraft:gravel", 
        "foundation_material": "minecraft:stone", 
        "mid_material": "minecraft:stone", 
        "top_material": "minecraft:stone", 
        "sea_material": "minecraft:water" 
      }, 
      "minecraft:overworld_generation_rules": { 
        "hills_transformation": "custom:crystal_caverns", 
        "generate_for_climates": [ 
          ["cold", 1], 
          ["medium", 1] 
        ] 
      }, 
      "minecraft:tags": { 
        "tags": [ 
          "overworld", 
          "custom", 
          "crystal_caverns", 
          "no_legacy_worldgen" 
        ] 
      } 
    } 
  } 
} 
```

このファイルはカスタムバイオームを定義し、識別子を通じて他のコンテンツから参照できるようにします。識別子名とファイル名を一致させておくとテスト時に見つけやすくなります。

### コンポーネント分解

先ほどの `components` セクションに多くの生成設定が含まれていることに気づいたはずです。下の表はサポートされる主なコンポーネントタイプとその役割の概要です。

| コンポーネント | 役割 |
|-----------|---------|
| `minecraft:climate` | バイオームの温度と降水設定を制御 |
| `minecraft:overworld_height` | 地形生成の形状を制御 |
| `minecraft:surface_parameters` | バイオームの表層を構成するブロックの種類を決定 |
| `minecraft:overworld_generation_rules` | バイオームがワールド内でどのように生成されるかを制御 |
| `minecraft:tags` | フィルタリングや識別を助けるタグを追加 |

次に、`minecraft:surface_parameters` を更新して、より興味深い表面にします。

```json
"minecraft:surface_parameters": {
  "sea_floor_depth": 7,
  "sea_floor_material": "minecraft:gravel",
  "foundation_material": "minecraft:deepslate",
  "mid_material": "minecraft:stone",
  "top_material": "minecraft:calcite",
  "sea_material": "minecraft:water"
}
```

ここでは基盤に `deepslate` を使用し、上層に `stone` と `calcite` を配置しています。海底は7ブロックの深さで `gravel` に設定しています。

### カスタムフィーチャの追加

表面が整ったら、バイオームに特徴を与えるフィーチャを追加します。フィーチャはバイオームで指定された場所と条件下に生成される構造や装飾です。

1. まず、表面の `deepslate`、`stone`、`calcite` の代わりに生成されるクリスタルクラスターを追加してみましょう。ビヘイビアパックの `features` フォルダに、識別子名（例: `crystal_cluster.json`）のファイルを作成します。
    
    ```json
    { 
      "format_version": "1.21.40", 
      "minecraft:ore_feature": { 
        "description": { 
          "identifier": "custom:crystal_cluster" 
        }, 
        "count": 8, 
        "replace_rules": [ 
          { 
            "places_block": "minecraft:amethyst_block", 
            "may_replace": ["minecraft:stone", "minecraft:deepslate", "minecraft:calcite"] 
          } 
        ] 
      } 
    } 
    ```

2. 次に、`glowing_mushroom.json` を作成して、バイオームに特殊なキノコを追加します。
    
    ```json
    { 
      "format_version": "1.21.40", 
      "minecraft:scatter_feature": { 
        "description": { 
          "identifier": "custom:glowing_mushroom" 
        }, 
        "iterations": 5, 
        "scatter_chance": 25, 
        "x": { 
          "distribution": "uniform", 
          "extent": [0, 15] 
        }, 
        "z": { 
          "distribution": "uniform", 
          "extent": [0, 15] 
        }, 
        "y": "query.heightmap(variable.worldx, variable.worldz)", 
        "places_feature": "custom:single_glowing_mushroom" 
      } 
    }  
    ```

    上記はキノコの分布条件を設定しますが、実際のキノコ自体は別で定義する必要があります。

3. `single_glowing_mushroom.json` を `features` フォルダに作成し、次のように記述して単一ブロックのフィーチャを定義します。
    
    ```json
    { 
      "format_version": "1.21.40", 
      "minecraft:single_block_feature": { 
        "description": { 
          "identifier": "custom:single_glowing_mushroom" 
        }, 
        "places_block": "minecraft:brown_mushroom", 
        "enforce_survivability_rules": true, 
        "enforce_placement_rules": true, 
        "may_replace": ["minecraft:air"] 
      } 
    }
    ```

### フィーチャルール

フィーチャが期待通りに出現するよう、フィーチャルールを設定します。以下は `crystal_cluster_rule` の例です。

```json
{
  "format_version": "1.21.40",
  "minecraft:feature_rules": {
    "description": {
      "identifier": "custom:crystal_cluster_rule",
      "places_feature": "custom:crystal_cluster"
    },
    "conditions": {
      "placement_pass": "underground_pass",
      "minecraft:biome_filter": {
        "test": "has_biome_tag",
        "operator": "==",
        "value": "crystal_caverns"
      }
    },
    "distribution": {
      "iterations": 10,
      "x": {
        "distribution": "uniform",
        "extent": [0, 15]
      },
      "y": {
        "distribution": "uniform",
        "extent": [0, 60]
      },
      "z": {
        "distribution": "uniform",
        "extent": [0, 15]
      }
    }
  }
}
```

以下は `glowing_mushroom_rule.json` の例です。

```json
{
  "format_version": "1.21.40",
  "minecraft:feature_rules": {
    "description": {
      "identifier": "custom:glowing_mushroom_rule",
      "places_feature": "custom:glowing_mushroom"
    },
    "conditions": {
      "placement_pass": "surface_pass",
      "minecraft:biome_filter": {
        "test": "has_biome_tag",
        "operator": "==",
        "value": "crystal_caverns"
      }
    },
    "distribution": {
      "iterations": 3,
      "x": {
        "distribution": "uniform",
        "extent": [0, 15]
      },
      "y": "query.heightmap(variable.worldx, variable.worldz)",
      "z": {
        "distribution": "uniform",
        "extent": [0, 15]
      }
    }
  }
}
```

### バイオーム固有のスポーン設定

バイオーム固有のスポーンルールを使用して、そのバイオームでのみ適用されるエンティティルールを作成できます。まずエンティティ（カスタムまたはバニラ）を選択します。

> [!NOTE]
> 例では `crystal_golem` というカスタムエンティティに基づいたルールを使用しています。実際に動作させるには同名のエンティティがパック内に存在する必要があります。

以下は `crystal_golem.json` の例です（そのまま使用できます）。

```json
{
  "format_version": "1.21.40",
  "minecraft:spawn_rules": {
    "description": {
      "identifier": "custom:crystal_golem",
      "population_control": "monster"
    },
    "conditions": [
      {
        "minecraft:spawns_on_surface": {},
        "minecraft:spawns_on_block_filter": {
          "blocks": ["minecraft:calcite", "minecraft:stone"]
        },
        "minecraft:brightness_filter": {
          "min": 0,
          "max": 7,
          "adjust_for_weather": false
        },
        "minecraft:difficulty_filter": {
          "min": "normal",
          "max": "hard"
        },
        "minecraft:biome_filter": {
          "test": "has_biome_tag",
          "operator": "==",
          "value": "crystal_caverns"
        },
        "minecraft:weight": {
          "default": 50
        },
        "minecraft:herd": {
          "min_size": 1,
          "max_size": 2
        },
        "minecraft:density_limit": {
          "surface": 3
        }
      }
    ]
  }
}
```

バニラのモブに対しては、既存のスポーンルールをオーバーライドすることで出現量を調整できます（例: コウモリをより一般的にするなど）。

<a id="configuring-the-resource-pack"></a>
## リソースパックの設定

カスタムバイオームはビヘイビアパックとリソースパックの両方のコンテンツを必要とします。リソースパック（クライアント側）には視覚・音響要素が含まれます。

| コンポーネント | 目的 |
|-----------|---------|
| フォグ設定 | 大気、視界、ボリューメトリック効果 |
| クライアントバイオーム | 水の色、環境音、音楽 |
| パーティクル | カスタムパーティクル（ある場合） |
