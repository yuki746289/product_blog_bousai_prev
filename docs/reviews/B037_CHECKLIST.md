# B037 記事別レビュー記録

> 共通サイトフレームワーク: `docs/COMMON_SITE_REVIEW_FRAMEWORK.md`
>
> 防災サイト適用プロファイル: `docs/BOUSAI_SITE_REVIEW_PROFILE.md`
>
> 共通記事ルール: `docs/CONTENT_CREATION_RULES.md`
>
> 共通記事チェック: `docs/ARTICLE_REVIEW_CHECKLIST.md`
>
> 防災サイト固有チェック: `docs/BOUSAI_SITE_REVIEW_CHECKLIST.md`

- article_id: `B037`
- title: 家が浸水した後の片付け｜清掃・乾燥・消毒の順番と注意点
- content_role: `practical`
- risk_level: `high`
- article_status: `REVIEW_REQUIRED`
- review_status: `IN_PROGRESS`
- last_checked_at: 2026-09-04
- reviewer: ChatGPT
- persona_mode: `SITUATIONAL_SEGMENT`

## 1. 適用プロファイル確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 防災サイトプロファイル確認 | PASS | 高リスク発災後記事として適用 |
| 必須専門家ロール選定 | PASS | E01〜E08,E11〜E14 |
| 条件付き専門家ロール判定 | PASS | 商品・計測はN/A |
| 詳細架空ペルソナ | N/A | 被災状況ベースで読者設定 |
| N/A項目の理由確認 | PASS | 商品販売・A/Bテスト等を行わない |

## 2. 共通チェック結果

| 共通チェック | 状態 | 根拠・備考 |
|---|---|---|
| C01 内容・情報量 | PASS | 安全確認→記録→清掃→乾燥→必要な消毒を一連で説明 |
| C02 出典・安全性 | PASS | 厚労省を主根拠、2026年更新自治体で実務差を確認 |
| C03 画像・視覚要素 | PASS | 無理な被災画像を使わず、作業フロー・表を視覚要素とする方針 |
| C04 読みやすさ・UI | PASS | 作業順と床上/床下の差を分離 |
| C05 内部リンク | TODO | B015/B005/B012等から公開時に追加 |
| C06 商品導線・商品記事 | N/A | 防護具等を販売目的で誘導しない |
| C07 Q&A | CONDITIONAL | 床下消毒等の短いQ&Aを統合時に判断 |
| C08 同期・公開前 | TODO | preview/registry/category/CI未実施 |
| C09 日付・構造化データ | TODO | registry登録・build後確認 |
| C10 デザイン・UX | TODO | preview完成後に目視 |
| C11 読者・マーケティング | PASS | post-disasterの次行動を明確化 |
| C12 アクセシビリティ | PASS/RECHECK | 順序・表をテキストで表現。HTML最終確認待ち |
| C13 技術品質・信頼性 | TODO | build/リンク/HTTP smoke未実施 |
| C14 計測・グロース | N/A | 新規計測なし |

## 3. 防災サイト固有チェック結果

| サイト固有チェック | 状態 | 根拠・備考 |
|---|---|---|
| S01 サイトプロファイル・適用判定 | PASS | 人身安全・感染症・感電等をSEOより優先 |
| S02 情報設計・ファインダビリティ | PASS/RECHECK | B015を記録、B037を清掃復旧として分離。公開導線未実装 |
| S03 法務・権利・広告表示・プライバシー | PASS | 商品画像・被災者写真を使用しない |
| S04 ブランド・トーン・コンテンツデザイン | PASS | 被害を煽らず復旧順序を説明 |
| S05 日本向けローカライゼーション | PASS | 厚労省・日本自治体の現行案内に準拠 |
| S06 運用・ガバナンス・保守性 | TODO | registry/preview/category同期後に完了 |
| S07 セキュリティ・外部依存 | PASS | 本文は外部JS/API依存なし |
| S08 数値・統計・リアルタイム要約 | PASS | 独自の消毒濃度・安全閾値を設定しない |

## 4. 高リスク追加確認

| 項目 | 状態 | 根拠・備考 |
|---|---|---|
| 消毒より清掃・乾燥を先にする | PASS | 厚労省現行案内 |
| 危険な家へ撮影・家財救出目的で入らせない | PASS | B015と整合 |
| 濡れた電気設備へ触れさせない | PASS | 安全確認を最初に配置 |
| 床下・屋外の消毒を一律必須にしない | PASS | 自治体差を明記し地域案内確認 |
| 消毒剤濃度を独自に一律化しない | PASS | 製品表示・公的資料優先 |
| 食品を見た目・臭いだけで安全判断させない | PASS | 厚労省の食品営業施設注意とも整合 |
| 医療症状をサイトで診断しない | PASS | 医療機関・相談窓口へ案内 |
| カビ・建材内部の乾燥を家庭作業だけで保証しない | PASS | 専門業者相談を明記 |

## 5. 読者・ページ設計の証跡

- target_reader: 自宅が床上/床下浸水した家庭
- usage_context: 水が引いた後〜片付け開始時
- knowledge_level: beginner/basic
- urgency_level: post-disaster
- reader_problem: 片付け・清掃・消毒の順番が分からない
- reader_goal: 安全に復旧初動を進める
- page_job: 清掃・乾燥・必要な消毒の順序を整理
- entry_path: 検索/B015/B005/B012
- next_action: 安全確認→記録→清掃→乾燥→必要な消毒
- conversion_path: 復旧行動→保険/住宅関連情報
- design_priority: 作業順を一目で理解し、危険作業を避ける

## 6. 証跡

- brief: `docs/research/B037_FLOOD_CLEANUP_BRIEF.md`
- sources: `docs/research/B037_SOURCES.md`
- images: `docs/research/B037_IMAGES.md`
- article: `content/articles/B037_flood_cleanup_dry_disinfect.md`
- browser_check: TODO
- production_check: TODO

## 7. 残課題

- preview HTML作成
- B015/B005/B012/B013/B014から内部リンク追加
- category_post_disaster掲載
- content_registry登録
- build/CI/HTTP smoke
- 本番目視後にreview_statusをPASSへ変更

## 8. 最終判定

- review_status: `IN_PROGRESS`
- READY_TO_PUBLISH: `NO`
- 判定理由: 本文・一次情報・安全レビューはPASS。公開実装・技術検証が未完了。
