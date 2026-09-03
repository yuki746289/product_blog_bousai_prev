# 作成ルール・チェックリスト共通化結果

作成日: 2026-09-03

## 結論

個別記事へ繰り返し追加されていたルールを共通化した。

今後の正本:

1. `docs/CONTENT_CREATION_RULES.md` — 共通記事作成ルール
2. `docs/ARTICLE_REVIEW_CHECKLIST.md` — 共通チェックリスト
3. `docs/reviews/ARTICLE_CHECKLIST_TEMPLATE.md` — 記事別レビュー記録用テンプレート
4. `docs/AFFILIATE_POLICY.md` — 商品/Amazon固有の追加条件
5. `docs/BOUSAI_SITE_SPEC.md` — サイト固有の実装条件
6. `docs/SITE_RELEASE_CHECKLIST.md` — サイト全体の公開チェック

## 共通化した旧個別ルール

| 旧ルール・監査 | 新しい共通化先 |
|---|---|
| 強調表示・視覚的な読みやすさ | CR-04 / C04 |
| 日本文脈画像レビュー | CR-03C / C03 |
| 推奨本文画像数 | CR-03 / CR-04 |
| 本文画像追加レビュー | CR-03 / C03 |
| 画像関連性再レビュー | CR-03A / C03 |
| 商品記事導線再レビュー | CR-05B / C06 |
| UI役割・旧準備中リンク監査 | CR-04C・CR-05 / C04-C05 |
| Q&A文脈導線監査 | CR-07B / C07 |
| 商品カード共通条件 | CR-06 + AFFILIATE_POLICY |
| 外部画像表示・リンク切れ対策 | CR-03E / C03 |
| HTML/Markdown/台帳同期 | CR-08 / C08 |

## 記事別チェックリストの変更

従来:

- 全共通項目を記事ごとにコピー
- 後から共通監査章を各記事へ追加
- 同じルールが複数ファイルに重複

今後:

- 共通チェックはC01〜C08のセクション判定だけ記録
- 記事固有の追加確認だけを個別ファイルへ記録
- 2記事以上で同じ固有ルールが必要になったら共通化を検討
- 既存B001〜B030の詳細チェックは履歴として残す

## 重複を削減した文書

### BOUSAI_SITE_SPEC.md

記事作成の詳細ルールを削減し、サイト固有の情報設計・GA・固定ページ・CSS実装・公開条件へ限定。

### AFFILIATE_POLICY.md

共通の読みやすさ・内部リンク・UIルールの再掲を削除。
商品選定、ASIN、価格、商品画像、リコール等のAmazon固有条件へ限定。

### ARTICLE_REVIEW_CHECKLIST.md

重複していた「読みやすさ」「強調」「UI形状」「Q&A文脈導線」等をC01〜C08へ統合。

### ARTICLE_CHECKLIST_TEMPLATE.md

共通項目の長い表を廃止し、セクション判定＋記事固有チェック方式へ変更。

### reviews/README.md

30記事の状態一覧を重複管理しない。
正式状態は `data/content_registry.json` を参照する。

## 運用ルール

新しいルールを追加するときは、まず「この1記事だけか」「他記事にも適用できるか」を判定する。

- 1記事だけ: 記事別チェックへ
- 2記事以上で共通: 共通ルールへ
- 商品固有: AFFILIATE_POLICYへ
- サイトUI・本番共通: SITE_SPEC / SITE_RELEASE_CHECKLISTへ

これにより、同じ修正ルールを30記事へコピーする運用を避ける。
