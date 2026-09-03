# B035 記事別レビュー記録

> 共通ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 新規記事手順: `docs/NEW_ARTICLE_WORKFLOW.md`

- article_id: `B035`
- title: 高齢者の防災は何を準備する？薬・補聴器・入れ歯・避難支援を確認
- content_role: `practical`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-03
- reviewer: ChatGPT

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 物品だけでなく薬情報・生活機能・食事・避難支援まで一連で整理 |
| C02 出典・安全性 | PASS | 内閣府・広島県・農水省・厚労省の現行情報 |
| C03 画像・視覚要素 | PASS | 高齢者を過度に弱者化する画像を避け、表・チェックリストを使用 |
| C04 読みやすさ・UI | PASS | 4分類、表、分担表、保存用チェック |
| C05 内部リンク | PASS | B001/B002/B025/B030へ役割分担 |
| C06 商品導線・商品記事 | N/A | 医療・介護用品のAmazon直販誘導なし |
| C07 Q&A | PASS | 個別避難計画対象の誤解、薬の自己判断を本文で防止 |
| C08 同期・公開前 | PASS | Markdown / preview / sources / images / review / registry同期予定 |

## 2. 高リスク追加確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 高齢者全員を要支援者扱いしない | PASS | 内閣府定義に合わせる |
| 個別避難計画の自治体差を明示 | PASS | 対象基準・作成状況・手順の地域差を記載 |
| 市町村努力義務の表現 | PASS | 令和3年改正・令和8年白書 |
| 薬の追加量を自己判断させない | PASS | 医師・薬剤師確認を案内 |
| 食形態・とろみを一律指示しない | PASS | 普段の状態・専門職指示優先 |
| 本人の尊厳を損なう表現を避ける | PASS | 「高齢者=できない」と一括りにしない |

## 3. 証跡

- sources: `docs/research/B035_SOURCES.md`
- images: `docs/research/B035_IMAGES.md`
- brief: `docs/research/B035_BRIEF.md`
- audience_research: `docs/research/AUDIENCE_NEEDS_RESEARCH_20260903.md`
- production_check: GitHub Actions

## 4. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 最新の要支援者制度、個別避難計画、薬・補助具・食品の一次情報を確認し、医療・福祉の過剰一般化を回避した。
