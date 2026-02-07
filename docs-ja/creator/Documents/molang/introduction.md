---
author: chipotle
ms.author: mikeam
title: Molang 入門
description: "Molang スクリプト言語の概要。"
ms.service: minecraft-bedrock-edition
ms.date: 08/19/2025
---


# Molang 入門

Minecraft のアドオンを開発していると、JSON ファイル内でプロパティに特定の値を設定するだけでは足りず、しかしフル機能の JavaScript は不要、という状況が出てきます。ちょっとした計算や特定のエンティティの状態を問い合わせたいときに役立つのが、Minecraft 専用のスクリプト言語である Molang です。Molang は通常、ビヘイビアパックやリソースパック内のほとんどの JSON ファイルで使えます。多くの場合は一、二行だけ使われますが、中には何ページにもわたる Molang を書いて驚くべき仕組みを作るクリエーターもいます。

このチュートリアルで学ぶこと:

> [!div class="checklist"]
>
> - Molang とは何か、どのような場面で使えるか
> - 攻撃する牛がドロップする経験値や戦利品を変更する方法
> - 攻撃する牛のアニメーションを編集してより不気味にする方法

## 前提

リソースパックとビヘイビアパックの扱いに慣れていることを想定します。必要なら以下を確認し、攻撃する牛のビヘイビアパックを用意してください。

- [アドオン開発の始め方](../GettingStarted.md)
- [リソースパック入門](../ResourcePack.md)
- [ビヘイビアパック入門](../BehaviorPack.md)

## Behavior Pack での Molang の使用

このチュートリアルは、完成済みの攻撃する牛のビヘイビアパックを前提とします。

ここでは Molang を使って、攻撃する牛が落とす経験値を増やします。また、通常の革や肉の代わりに End City の戦利品を落とすように、Molang ではない単純な JSON の編集も行います。

**cow.json** を開き、`minecraft:cow_adult` の行を探してください。

元のコードは次のようになっています。

```json
"minecraft:cow_adult": {
  "minecraft:experience_reward": {
    "on_bred": "Math.Random(1,7)",
    "on_death": "query.last_hit_by_player ? Math.Random(1,3) : 0"
  },
  "minecraft:loot": {
    "table": "loot_tables/entities/cow.json"
  }
  // ... continues ...
}
```

注目するのは、`minecraft:experience_reward` セクション内の `"on_death"` 行です。これが牛の死亡時に与えられる経験値を決定する行です。

このコードは次の意味になります。

- 牛がプレイヤーに経験値を与える方法には二通りあります。
  - 小麦を与えて繁殖させて子牛を得る（`"on_bred"`）、または
  - 牛を倒す（`"on_death"`）。

次の行：

`"on_death": "query.last_hit_by_player ? Math.Random(1,3) : 0"`

は次のように動作します。

- 牛が死亡したとき、最後に殴ったプレイヤーがいるかを問い合わせる。
- プレイヤーが見つかれば、乱数で `1`、`2`、`3` のいずれかを選び、その値を `experience_reward` として返す。
- プレイヤーが見つからなければ `0` を返す。

`"on_death"` を次のように編集してください：

`"on_death": "query.last_hit_by_player ? 300 * Math.Random(1,3) : 0"`

これにより返される経験値が 300 倍になります。

次に、牛のドロップを End City の戦利品に変更します。ここは Molang ではなく単純な JSON の編集ですが、ついでに行います。

`"minecraft:loot"` セクションの `"table"` 行を次のように変更します：

`"table": "loot_tables/chests/end_city_treasure.json"`

編集後の該当箇所は次のようになります：

```json
"minecraft:cow_adult": {
  "minecraft:experience_reward": {
      "on_bred": "Math.Random(1,7)",
      "on_death": "query.last_hit_by_player ? 300 * Math.Random(1,1) : 0"
  },
      "minecraft:loot": {
      "table": "loot_tables/chests/end_city_treasure.json"
  }
}
```

保存して動作を確認しましょう。

## Resource Pack のアニメーションで Molang を使う

次に、アニメーションファイル内の Molang を使って牛の頭を不気味に揺らす例を見ます。リソースパックに通常の `manifest.json` があることを前提とします。チュートリアルで作成したものを使っても、サンプルをダウンロードして試しても構いません。

[リソースパックのサンプル](https://github.com/microsoft/minecraft-samples/tree/main/resource_pack_sample)

準備ができたら、`manifest.json` と同じ階層に `animations` フォルダを作り、`cow.animation.json` というファイルを置いて以下を貼り付けます。

```json
{
  "format_version": "1.8.0",
  "animations": {
    "animation.cow.baby_transform": {
      "loop": true,
      "bones": {
        "head": {
          "position": [0.0, 4.0, 4.0],
          "scale": 2.0
        }
      }
    },
    "animation.cow.setup": {
      "loop": true,
      "bones": {
        "body": {
          "rotation": ["-this", 0.0, 0.0]
        },
        "head": {
          "rotation": [0, 0, "math.sin(query.life_time*360) * 40"]
        }
      }
    },
    "animation.cow.setup.v1.0": {
      "loop": true,
      "bones": {
        "body": {
          "rotation": ["90 - this", 0.0, 0.0]
        }
      }
    }
  }
}
```

Vanilla の `animations/cow.animation.json` と比較すると、違いはこの行のみです。

```json
"head": {
  "rotation": [0, 0, "math.sin(query.life_time*360) * 40"]
}
```

かっこ内の式は Molang で、正弦関数を使って頭の回転を制御しています。Minecraft を再読み込みして（あるいはワールドで）拡張された牛を確認し、値を変えて色々試してみましょう。

## 次のステップ

これで Molang を使って数学や論理式の力を利用し、ワールドの挙動を柔軟に制御できる一例を学びました。Blockbench のようなサードパーティツールを使うのも良い方法です。さらに学びたい場合は：

- [Molang Syntax Guide](./syntax-guide.md)
- [Practical Molang](./practical-molang.md)
- [Molang Query Functions](../../Reference/Content/MolangReference/Examples/MolangConcepts/QueryFunctions.md)


原文: https://github.com/MicrosoftDocs/minecraft-creator/blob/{SHA}/{PATH}
