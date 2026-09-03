# B033 記事別レビュー記録

> 共通ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 新規記事手順: `docs/NEW_ARTICLE_WORKFLOW.md`

- article_id: `B033`
- title: ペットの防災は何を準備する？同行避難・備蓄・持ち出し品を整理
- content_role: `practical`
- risk_level: `standard`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-03
- reviewer: ChatGPT

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 用品だけでなく同行避難・避難所条件・訓練・健康情報・一時預け先まで網羅 |
| C02 出典・安全性 | PASS | 環境省・広島県の一次情報を確認 |
| C03 画像・視覚要素 | PASS | 不適切な海外画像流用を避け、表・分類・チェックリストで補助 |
| C04 読みやすさ・UI | PASS | 表、番号手順、保存用チェック、重要語強調を分散 |
| C05 内部リンク | PASS | B001/B002/B025/B030へ導線 |
| C06 商品導線・商品記事 | N/A | ペット専用商品記事未作成のためAmazon直リンクなし |
| C07 Q&A | PASS | 同行避難の誤解を本文で直接解消 |
| C08 同期・公開前 | PASS | Markdown / preview / sources / images / review / registry同期 |

## 2. 条件付き詳細確認

| 条件 | 状態 | 根拠・備考 |
|---|---|---|
| キーワード調査・検索意図 | PASS | `docs/research/AUDIENCE_NEEDS_RESEARCH_20260903.md` |
| 新規記事brief | PASS | `docs/research/B033_BRIEF.md` |
| カニバリ確認 | PASS | B001/B002/B025/B030との役割差をbriefで整理 |
| 情報鮮度 | PASS | source_checked_at=2026-09-03 |
| 高リスク追加確認 | N/A | 標準リスク |

## 3. 記事固有チェック

| 記事固有の確認項目 | 状態 | 根拠・備考 |
|---|---|---|
| 同行避難=同室と誤解させない | PASS | 自治体・避難所ごとのルール差を明記 |
| 備蓄日数の根拠を明示 | PASS | 広島県の5日/できれば7日以上を出典化 |
| 薬・療法食を独自指示しない | PASS | 動物病院/商品表示優先 |
| 海外風景を日本向け画像として流用しない | PASS | 画像0件の判断理由を記録 |
| practical保存用チェック | PASS | 保存用チェックリストあり |

## 4. 証跡

- sources: `docs/research/B033_SOURCES.md`
- images: `docs/research/B033_IMAGES.md`
- brief: `docs/research/B033_BRIEF.md`
- audience_research: `docs/research/AUDIENCE_NEEDS_RESEARCH_20260903.md`
- browser_check: 本番スモークテスト対象
- production_check: GitHub Actions

## 5. 残課題

- 適切な日本文脈の権利確認済み画像が見つかった場合のみ追加検討

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 検索意図、一次情報、カニバリ、安全表現、内部リンク、practical記事の実用性を確認済み。
