---
author: chipotle
ms.author: mikeam
title: 実践的な Molang
description: "Molang のさまざまな利用方法に関するリファレンス。"
ms.service: minecraft-bedrock-edition
ms.date: 08/25/2025
---

# 実践的な Molang

既に [Molang の基本](./introduction.md) を学び、[構文や関数](./syntax-guide.md) を確認したなら、Molang を実際にどう使うか見ていきましょう。ここでは Molang がアドオンに与える実用的な利点の例を示します。

## エンティティ定義スクリプト

### 値の事前計算

エンティティ定義ファイルには、アニメーションやレンダーコントローラーが処理される直前に実行される `"pre_animation"` セクションがあります。ここで後続の参照に使う値を事前に計算して Molang 変数に保存することで、複数箇所で同じ計算を繰り返すより効率的に処理できます。

以下は、Resource Pack 内の `entity/dream_turkey.entity.json` にある `pre_animation` の例です（Chill Dreams Add-On の例）：

```json
"scripts": {
  "pre_animation": [
    "variable.wing_flap = ((math.sin(query.wing_flap_position * 57.3) + 1) * query.wing_flap_speed);"
  ]
},
```

この例では `math.sin()` を使って羽ばたきの動きを正弦波に沿わせ、より自然な動きを作っています。ここで定義した `wing_flap` 変数は Resource Pack 内のアニメーション定義ファイル `animations/dream_turkey.animation.json` で参照できます。

```json
"animation.dream_turkey.general": {
  "loop": true,
  "bones": {
    "body": {
      "rotation": ["-this", 0.0, 0.0]
    },
    "wing0": {
      "rotation": [0.0, 0.0, "variable.wing_flap - this"]
    },
    "wing1": {
      "rotation": [0.0, 0.0, "-variable.wing_flap - this"]
    }
  }
}
```

### アニメーションへのパラメーター渡し

同じ `dream_turkey.entity.json` の `scripts` ブロック内にある `animate` セクションでは、Molang を使ってアニメーションにパラメーターを渡せます。

```json
"animate": [
  "general",
  { "move": "query.modified_move_speed" },
  "look_at_target",
  { "baby_transform": "query.is_baby" }
],
```

## アニメーション

> [!IMPORTANT]
> アニメーション定義とアニメーションコントローラーのほとんどで Molang を使えますが、以下のタイプは例外です：
>
> - `material`
> - `texture`
> - `geometry`

多くのケースではクエリと数値関数で十分です。以下はアニメーションファイル内で Molang を使う例です。

```json
"animation.dream_turkey.move": {
  "anim_time_update": "query.modified_distance_moved",
  "loop": true,
  "bones": {
    "leg0": {
      "rotation": ["math.cos(query.anim_time * 38.17) *  80.0", 0.0, 0.0]
    },
    "leg1": {
      "rotation": ["math.cos(query.anim_time * 38.17) * -80.0", 0.0, 0.0]
    }
  }
}
```

より複雑な例として、ゾンビのアニメーションでは攻撃開始時間や現在アニメーションの経過時間、槍を持っているかどうかなどを考慮して計算を行っています（Bedrock Add-On Sample の例）。

### アニメーションコントローラー

[Animations vs. Animation Controllers](../../Documents/AnimationsVsControllers.md) にあるように、アニメーションコントローラーはどの条件でどのアニメーションを再生するかを定義します。以下はオオカミの例で、`query` を使って状態遷移を制御しています。

```json
"controller.animation.wolf.sitting" : {
  "initial_state" : "default",
  "states" : {
    "default" : {
      "animations" : [ "wolf_leg_default" ],
      "transitions" : [
        {
          "sitting" : "query.is_sitting"
        }
      ]
    },
    "sitting" : {
      "animations" : [ "wolf_sitting" ],
      "transitions" : [
        {
          "default" : "!query.is_sitting"
        }
      ]
    }
  }
}
```

## レンダーコントローラー

[Render controllers](../Animations/AnimationRenderController.md) はジオメトリ、マテリアル、テクスチャ、パーツの可視性を定義します。Molang は配列参照やリソース参照の式で使われます。

以下はキツネの簡単なレンダーコントローラーの例です。

```json
{
  "format_version": "1.8.0",
  "render_controllers": {
    "controller.render.fox": {
      "arrays": {
        "textures": {
          "Array.skins": [
            "Texture.red",
            "Texture.arctic"
          ]
        }
      },
      "geometry": "Geometry.default",
      "part_visibility": [
        { "leg*": "!query.is_sleeping" },
        { "head": "!query.is_sleeping" },
        { "head_sleeping": "query.is_sleeping" }
      ],
      "materials": [ { "*": "Material.default" } ],
      "textures": [ "Array.skins[query.variant]" ]
    }
  }
}
```

### 配列宣言

配列は任意の長さで宣言でき、要素は同種でなければなりません。添字が範囲外の場合はラップアラウンドや 0 番目の返却といった挙動になります。

### リソース参照

リソース参照は適切な型を返す必要があります。例えば `geometry` にはジオメトリを、`textures` にはテクスチャ名を返します。式は複雑にしても構いません。

#### サイクルアニメーション

配列内を秒単位でサイクルする例：

```json
"geometry": "array.my_geometries[query.anim_time]"
```

#### ブールに基づくジオメトリ選択

```json
"geometry": "query.is_sheared ? geometry.sheared : geometry.woolly"
```

## マテリアル

マテリアルセクションはモデルの各パーツにマテリアルを割り当てます。ワイルドカードを使って部分一致を指定できます。

## パーティクルエミッタ

パーティクルエミッタは Molang を多用します。以下はフレイムパーティクルの短い例です：

```json
{
  "format_version": "1.10.0",
  "particle_effect": {
    "description": {
      "identifier": "minecraft:basic_flame_particle",
      "basic_render_parameters": {
        "material": "particles_alpha",
        "texture": "textures/particle/particles"
      }
    },
    "components": {
      "minecraft:emitter_rate_instant": {
        "num_particles": 1
      },
      "minecraft:emitter_lifetime_expression": {
        "activation_expression": 1,
        "expiration_expression": 0
      },
      "minecraft:emitter_shape_sphere": {
        "radius": 0.025,
        "direction": [ 0, 0, 0 ]
      },
      "minecraft:particle_lifetime_expression": {
        "max_lifetime": "Math.random(0.6, 2.0)"
      },
      "minecraft:particle_appearance_billboard": {
        "size": [
          "(0.1 + variable.ParticleRandom1*0.1) - (0.1 * variable.ParticleAge)",
          "(0.1 + variable.ParticleRandom1*0.1) - (0.1 * variable.ParticleAge)"
        ],
        "facing_camera_mode": "lookat_xyz",
        "uv": {
          "texture_width": 128,
          "texture_height": 128,
          "uv": [ 0, 24 ],
          "uv_size": [ 8, 8 ]
        }
      }
    }
  }
}
```

この例では `math.random` を使ってパーティクルの寿命を決め、表示サイズの計算に Molang 式を使っています。

原文: https://github.com/MicrosoftDocs/minecraft-creator/blob/{SHA}/{PATH}
