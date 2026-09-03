# トップページ「現在の防災情報」運用仕様

更新日: 2026-09-03

## 目的

静的な記事一覧だけでなく、トップページで現在の防災状況を簡潔に確認できる入口を提供する。

表示対象:
- 最新の地震情報
- 主な警報・特別警報
- 台風情報

避難判断の一次情報にはしない。常に気象庁・自治体等の公式情報へのリンクを併記する。

## 情報源

気象庁「防災情報XMLフォーマット」PULL型配信を使用する。

- 公式案内: https://xml.kishou.go.jp/xmlpull.html
- 高頻度/随時: https://www.data.jma.go.jp/developer/xml/feed/extra.xml
- 高頻度/地震火山: https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml
- 長期/随時: https://www.data.jma.go.jp/developer/xml/feed/extra_l.xml
- 長期/地震火山: https://www.data.jma.go.jp/developer/xml/feed/eqvol_l.xml

気象庁の高頻度Atomフィードは毎分更新・直近少なくとも10分の入電を掲載する。長期フィードは毎時更新・数日間の入電を掲載する。

## 更新構成

```text
気象庁 PULL XML
       ↓
GitHub Actions（10分間隔）
       ↓
scripts/update_realtime.py
       ↓
realtime.json
       ↓
FTPSで /realtime/realtime.json のみ更新
       ↓
トップページJSが表示
```

通常の記事・画像・CSS等を10分ごとに再デプロイしない。

## 状態再構築

高頻度フィードは直近約10分のため、それだけでは以前から継続している警報等を復元できない。

そのため:
- 初回
- 前回確認から20分以上空いた場合
- 6時間ごとの定期再同期

では長期フィードを使用して状態を再構築する。

通常の10分更新では高頻度フィードを使い、前回の `realtime.json` の内部状態へ差分を反映する。

## 取得失敗

取得エラーを「情報なし」として扱わない。

- 一部取得失敗: `partial`
- 全対象取得失敗: `degraded`
- 前回データを保持
- トップページに遅延/取得失敗の警告を表示
- 気象庁への公式リンクを維持

ブラウザ側でも `checked_at` が30分以上古い場合は遅延警告を表示する。

## ブラウザ側更新

トップページを開いた時に `realtime/realtime.json` を取得する。

開いたままの場合は5分間隔でJSONのみ再取得する。

## 警報表示

「注意報」はトップの簡潔表示から除外し、「警報」「特別警報」を表示対象にする。

警報情報はXMLの府県予報区等のHeadline情報を優先し、種類ごとに地域をまとめる。

この表示は簡易サマリーであり、全市町村の詳細表示を目的としない。

## 台風表示

台風関連XMLをEventID単位で管理する。

「熱帯低気圧に変わった」「温帯低気圧に変わった」「消滅」等の終了情報を受けたEventIDは表示対象から外す。

最終情報が24時間以上更新されないEventIDもトップ表示から外す。

## GitHub Actions利用量

リポジトリがprivateの場合、GitHub-hosted runnerはアカウントのActions利用枠を消費し、超過時は課金対象となる可能性がある。

リアルタイム更新は軽量な `ubuntu-slim` を使用し、タイムアウトを3分に制限する。

10分間隔では理論上1日144回のworkflow実行になるため、GitHub ActionsのUsageは定期的に確認する。

必要に応じて、
- 15分
- 30分
- 60分

へ更新間隔を変更できる。

## 関連ファイル

- `scripts/update_realtime.py`
- `.github/workflows/update-realtime.yml`
- `preview/realtime/realtime.json`
- `preview/index.html`
- `preview/bousai_common.js`
- `preview/bousai_common.css`
- `tests/test_realtime_update.py`
