# 防災ブログ サイト横断公開監査

監査日: 2026-09-02  
対象: `preview/` 全HTML、共通CSS、固定ページ、共通フッター、公開前仕様

## 1. 結論

静的なHTML/CSS・リンク監査では、今回対象とした問題は解消済み。

- HTMLページ総数: **51**
- 既存プレビュー: **46**
- 新規固定ページ: **5**
- 静的監査PASS: **51 / 51**

ただし、ローカルブラウザでの実表示確認、本番ページ化、Google Analytics本番挿入等が未完了のため、サイト全体の `READY_TO_PUBLISH` は **NO** とする。

## 2. 新規固定ページ

| ページ | ファイル | 状態 |
|---|---|---|
| 運営方針 | `preview/about.html` | PASS |
| 免責事項 | `preview/disclaimer.html` | PASS |
| プライバシーポリシー | `preview/privacy.html` | PASS |
| 広告について | `preview/advertising.html` | PASS |
| お問い合わせ | `preview/contact.html` | PASS |

お問い合わせは実在しない連絡先を仮作成せず、現在は一般向け受付を開始していないことを明示している。

## 3. 全51ページ横断リンク監査

| チェック | 結果 |
|---|---|
| 「準備中」表記 | PASS / 0件 |
| `href="#"` | PASS / 0件 |
| `title-link--planned` | PASS / 0件 |
| `category-article-link--planned` | PASS / 0件 |
| フッター欠落 | PASS / 0件 |
| 固定ページ5リンク欠落 | PASS / 0件 |
| Amazonアソシエイト共通表示欠落 | PASS / 0件 |
| 存在しない内部HTMLへのリンク | PASS / 0件 |

監査中、以下の3カテゴリに実ページリンク済みなのにplannedクラスが残っていることを検出し、修正後に再確認した。

- `preview/category_home.html`
- `preview/category_insurance.html`
- `preview/category_post_disaster.html`

## 4. 共通フッター

全ページで次のリンクへ統一した。

- 運営方針
- 免責事項
- プライバシーポリシー
- 広告について
- お問い合わせ
- 気象庁 防災情報

さらに全ページの共通フッターへ次のAmazonアソシエイト表示を統一した。

> Amazonのアソシエイトとして、当サイトは適格販売により収入を得ています。

元々フッター自体がなかった一部記事ページにも共通フッターを追加した。

## 5. CSS semantic role 再チェック

`preview/bousai_common.css` を再確認。

| UI役割 | 状態 |
|---|---|
| 章見出し / section role | PASS |
| 要点・結論 / summary role | PASS |
| 注意 / warning role | PASS |
| 危険・禁止 / danger role | PASS |
| 出典 / info role | PASS |
| 商品紹介記事CTA / product role | PASS |
| Amazon購入CTA / purchase role | PASS |
| 関連記事 / related role | PASS |
| 表ヘッダー / table role | PASS |
| フッター補足表示 | PASS |
| CSS波括弧の対応 | PASS |

商品紹介記事CTAは紫系、章見出しは緑系、Amazon購入CTAは濃い青系として分離されている。

## 6. 仕様・チェックリスト反映

反映済み:

- `docs/BOUSAI_SITE_SPEC.md`
- `docs/SITE_STRUCTURE.md`
- `docs/ARTICLE_REVIEW_CHECKLIST.md`
- `docs/reviews/ARTICLE_CHECKLIST_TEMPLATE.md`
- `docs/SITE_RELEASE_CHECKLIST.md`
- `docs/reviews/SITE_UI_LINK_AUDIT_20260902.md`

追加した主なルール:

- 記事本数をサイト完成条件にしない
- 固定ページを記事IDとは別管理する
- 共通フッターから固定ページへ到達可能にする
- 存在しないページを `href="#"` のまま公開しない
- Amazonアソシエイト表示を共通位置へ置く
- CSSは意味上の役割ごとに色・見た目を分離する
- サイト全体の公開判定は記事別チェックとは別に行う

## 7. 残課題

### 静的監査では確認できない項目

- ローカルブラウザでの実際の色味
- hover / focus時の見え方
- PC幅のレイアウト
- スマートフォン幅のレイアウト
- 商品画像の実ロード状態
- 外部画像の403/404/ホットリンク制限
- 本番ページのGoogle Analytics
- previewの `noindex` を本番公開時に適切に扱うこと
- 本番URLへ変換後の最終リンク確認

## 8. 最終判定

- HTML/CSS静的監査: **PASS**
- 固定ページ・共通フッター: **PASS**
- CSS役割分離: **PASS**
- ローカル実ブラウザ確認: **TODO**
- 本番実装確認: **TODO**
- READY_TO_PUBLISH: **NO**
