# Production Lighthouse performance audit

実施日: 2026-09-03  
方式: GitHub Actions / Lighthouse 12.8.2 / mobile emulation  
Baseline run: 33727160529

## 判定上の注意

Lighthouseはラボ計測であり、実ユーザーのCore Web Vitalsそのものではない。
実ユーザーのLCP / INP / CLSは、CrUXやSearch ConsoleのCore Web Vitalsで別途確認する。

GoogleのCore Web Vitals基準:
- LCP: 2.5秒以下が良好、4.0秒超は不良
- INP: 200ms以下が良好、500ms超は不良
- CLS: 0.1以下が良好、0.25超は不良
- 実ユーザーデータでは75パーセンタイルで評価

参考:
- https://web.dev/articles/lcp?hl=ja
- https://web.dev/articles/cls?hl=ja
- https://web.dev/articles/defining-core-web-vitals-thresholds

## Baseline

| URL | Performance | FCP | LCP | CLS | TBT | Speed Index |
|---|---:|---:|---:|---:|---:|---:|
| トップ | 70 | 3.2s | 4.6s | 0 | 250ms | 4.9s |
| B001 防災入門 | 56 | 4.3s | 7.2s | 0 | 300ms | 5.8s |
| B028 ポータブル電源 | 68 | 4.0s | 4.9s | 0 | 220ms | 4.4s |

## 主なLighthouse指摘

### トップ
- Preconnect to required origins: 約476ms
- Reduce unused JavaScript: 約450ms
- TTFB: 約110msで大きな問題なし

### B001
- Preconnect to required origins: 約612ms
- Reduce unused JavaScript: 約490ms
- Properly size images: 約330ms / 67KiB
- Reduce unused CSS: 約240ms
- Enable text compression: 約240ms
- TTFB: 約110ms

### B028
- Reduce unused JavaScript: 約750ms
- Eliminate render-blocking resources: 約507ms
- Preconnect to required origins: 約368ms
- TTFB: 約110ms

## 初回対応

1. Wikimedia Commons画像のローカルWebP化、width/height付与、feature imageのfetchpriorityは実装済み。
2. Google Tag Manager / Google Analyticsへpreconnectを追加。
3. Google Analyticsは計測上必要なため、Lighthouseのunused JavaScriptだけを理由に削除しない。
4. CLSは3ページとも0であり、現時点では優先的な追加修正は不要。
5. サーバー側text compressionはホスティング側制約を確認せずに設定ファイルを追加しない。
6. CSSの非同期化はFOUCやレイアウト崩れのリスクがあるため、単純なmedia=print方式は採用しない。

## 残確認

- preconnect追加後のLighthouse再計測
- B001のLCP要素・画像サイズの追加分析
- Search Console / CrUXに十分なデータが出た後、実ユーザーLCP / INP / CLSを確認
