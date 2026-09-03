# B031 記事別レビュー記録

> 共通ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 新規記事手順: `docs/NEW_ARTICLE_WORKFLOW.md`

- article_id: `B031`
- title: 非常食の賞味期限が切れたらどうする？入れ替え・消費・ローリングストック
- content_role: `detail`
- risk_level: `elevated`
- article_status: `READY_TO_PUBLISH`
- review_status: `PASS`
- last_checked_at: 2026-09-03
- reviewer: ChatGPT

## 1. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | ラッコキーワードの検索意図をクラスタリングし、既存記事との差をbriefで定義。title/H1/metaも固有 |
| C02 出典・安全性 | PASS | 消費者庁2件・農林水産省2件を確認 |
| C03 画像・視覚要素 | PASS | 写真を無理に使わず、表・カード・チェックリストを記事内容に対応 |
| C04 読みやすさ・UI | PASS | 表・カード・チェックリスト・注意枠を分散配置 |
| C05 内部リンク | PASS | 親記事・関連記事へ双方向導線を実装 |
| C06 商品導線・商品記事 | PASS | 必要性がある場合のみ文脈導線 |
| C07 Q&A | N/A | 本文で検索意図へ直接回答 |
| C08 同期・公開前 | PASS | Markdown / preview / research / review / registryを同期 |

## 2. 条件付き詳細確認

| 条件 | 状態 | 根拠・備考 |
|---|---|---|
| キーワード調査・検索意図 | PASS | `docs/research/KEYWORD_RESEARCH_REPORT_20260903.md` |
| 新規記事brief | PASS | `docs/research/B031_BRIEF.md` |
| カニバリ確認 | PASS | 親記事と扱う検索意図を分離 |
| 情報鮮度 | PASS | source_checked_at=2026-09-03 |
| 高リスク追加確認 | PASS | 期限切れ食品の一律安全保証を禁止し、消費者庁表現と整合 |

## 3. 記事固有チェック

| 記事固有の確認項目 | 状態 | 根拠・備考 |
|---|---|---|
| 主検索意図が既存記事と独立 | PASS | briefのincluded/excluded intentで確認 |
| title / meta description完全重複なし | PASS | 公開ビルド自動テスト対象 |
| 根拠のない一律基準を作っていない | PASS | 記事固有の安全表現を確認 |

## 4. 証跡

- sources: `docs/research/B031_SOURCES.md`
- images: `docs/research/B031_IMAGES.md`
- keyword_research: `docs/research/KEYWORD_RESEARCH_REPORT_20260903.md`
- cannibalization_check: `docs/research/B031_BRIEF.md`
- browser_check: 本番スモークテストで確認
- production_check: GitHub Actions

## 5. 残課題

- なし

## 6. 最終判定

- review_status: `PASS`
- READY_TO_PUBLISH: `YES`
- 判定理由: 新規記事標準手順、共通ルール、検索意図・出典・安全性・内部リンク・SEOメタデータを確認済み。
