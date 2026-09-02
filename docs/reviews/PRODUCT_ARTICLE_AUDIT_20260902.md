# 商品紹介記事・商品紹介ページ 再レビュー
作成日: 2026-09-02
基準: docs/reviews/ARTICLE_CHECKLIST_TEMPLATE.md の「5.1 商品紹介記事の追加チェック」

## 1. 対象

- preview/article_b026.html
- preview/article_b027.html
- preview/article_b028.html
- preview/article_b029.html
- preview/goods_water_food.html
- preview/goods_toilet_hygiene.html
- preview/goods_light_information.html
- preview/goods_power_charging.html

## 2. 横断結果

| ページ | 商品数 | 文脈から自然に接続 | 必須カード項目 | 制作側表現なし | Amazon静的価格なし | ASIN直リンク | 商品画像 |
|---|---:|---|---|---|---|---|---|
| B026 非常食 | 4 | PASS | PASS | PASS | PASS | PASS | PASS / Amazon CDN |
| B027 防災ラジオ | 3 | PASS | PASS | PASS | PASS | PASS | PASS / YTM-R100を山善公式画像へ変更 |
| B028 ポータブル電源 | 3 | PASS | PASS | PASS | PASS | PASS | PASS / Anker・Jackery公式CDN |
| B029 車載防災用品 | 4 | PASS | PASS | PASS | PASS | PASS | PASS / Amazon CDN・公式プレス |
| 水・非常食 | 5 | PASS | PASS | PASS | PASS | PASS | RECHECK / 赤穂化成 備蓄水のみ旧Amazon画像URLが残る |
| 携帯トイレ・衛生 | 3 | PASS | PASS | PASS | PASS | PASS | PASS / Amazon CDN |
| ライト・ラジオ | 4 | PASS | PASS | PASS | PASS | PASS | PASS / GENTOS・山善公式画像を使用 |
| ポータブル電源紹介 | 3 | PASS | PASS | PASS | PASS | PASS | PASS / Anker・Jackery公式CDN |

## 3. 今回の画像修正

表示不安定要因になり得る `images-na.ssl-images-amazon.com` の旧形式URLを優先的に除去した。

変更:
- 山善 YTM-R100
  - 山善公式通販の商品画像へ変更
- GENTOS EX-1300D
  - GENTOS公式ストアの商品画像へ変更
- Jackery 600 New
  - Jackery Japan公式CDNへ変更
- Jackery 1000 New V3
  - Jackery Japan公式CDNへ変更
- 8ページの外部画像へ `referrerpolicy="no-referrer"` を付与

メーカー公式ページ上で商品画像と型番の一致を再確認した。

## 4. 残る画像課題

### 赤穂化成 備蓄水 2L×6本

`preview/goods_water_food.html` の商品画像だけ、現時点で
`images-na.ssl-images-amazon.com`
の旧形式URLが残っている。

メーカー公式ページでは同一商品（2L、ケース6本、JAN 4901291991472）と商品画像を確認できたが、公開ページへそのまま利用できる安定したメーカー公式画像URLを確定できていない。

したがって以下の順で扱う。

1. 現在URLへ `referrerpolicy="no-referrer"` を付けて表示改善
2. ローカルプレビューで表示できるか再確認
3. 表示できなければ、権利・利用条件を確認できるメーカー公式画像URLへ差し替える
4. 権利不明の通販サイト画像へ安易に差し替えない

## 5. 記事構成の再確認

全8ページで、商品カードの前に用途・必要性・判断基準の説明があり、
「商品を最後に一覧でまとめて置く」構成にはなっていない。

読者向け本文では以下を検出しなかった。

- 商品候補
- 記事内容に沿って選んだ商品候補
- 売れ筋順ではなく選定
- 当サイトが選定

商品カードには原則として以下がそろっている。

- 商品画像
- 商品名
- 価格情報
- 向く人・用途
- 主な強み
- 注意点
- Amazonリンク

## 6. 価格・Amazonリンク

- Amazonの現在価格を確認日付きで静的転記する表現は0件
- 各商品はメーカー公式価格、希望小売価格、またはAmazon以外の参考実売価格へ整理
- Amazonの現在価格・在庫はリンク先で確認する方針
- 今回の8ページでは商品カードのAmazonリンクはすべてASIN直リンク
- 商品名・型番とASINの不一致がないことを再確認

## 7. 公開前に残す確認

- メーカー公式CDN・Amazon商品画像の利用条件の最終確認
- スマートフォン実画面
- ローカルブラウザでの商品画像表示
- B028の人による安全レビュー
- 本番ページ化・GA

## 8. 判定

商品紹介の文章構成・価格・Amazonリンク・商品情報については再レビュー基準を満たす。

画像は大幅に改善済みだが、**赤穂化成 備蓄水の商品画像だけ表示確認を残す**。
この1件を除き、今回指摘された「商品画像が表示されない」原因になりやすい旧Amazon画像URLはメーカー公式CDN等へ置換した。
