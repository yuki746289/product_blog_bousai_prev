from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"marker not found in {path}: {old[:80]}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


# Realtime failure states: retrieval failure must not become a false "no warning" state.
replace_once(
    "preview/bousai_home.js",
    '''    var warnings = data.warnings || {};
    var groups = Array.isArray(warnings.groups) ? warnings.groups : [];
    if (!warnings.active_count || groups.length === 0) {''',
    '''    var warnings = data.warnings;
    if (!warnings || typeof warnings !== "object") {
      var unavailable = document.createElement("p");
      unavailable.className = "realtime-none";
      unavailable.textContent = "警報・特別警報の情報を取得できていません。気象庁の公式情報を直接確認してください。";
      holder.appendChild(unavailable);
      return;
    }
    var groups = Array.isArray(warnings.groups) ? warnings.groups : [];
    if (!warnings.active_count || groups.length === 0) {''',
)
replace_once(
    "preview/bousai_home.js",
    '''    var typhoons = Array.isArray(data.typhoons) ? data.typhoons : [];
    var message = document.createElement("p");
    if (typhoons.length === 0) {''',
    '''    var message = document.createElement("p");
    if (!Array.isArray(data.typhoons)) {
      message.className = "realtime-none";
      message.textContent = "台風情報を取得できていません。気象庁の公式情報を直接確認してください。";
      holder.appendChild(message);
      return;
    }
    var typhoons = data.typhoons;
    if (typhoons.length === 0) {''',
)
replace_once(
    "preview/bousai_home.js",
    '''      if (successCount === 0) return cached;

      data.checked_at = new Date().toISOString();
      data.status = successCount === 3 ? "ok" : "partial";''',
    '''      if (successCount === 0) return cached;

      // Do not make stale cached sections look freshly checked when only part of JMA refresh succeeds.
      if (successCount === 3) {
        data.checked_at = new Date().toISOString();
      }
      data.status = successCount === 3 ? "ok" : "partial";''',
)
replace_once(
    "preview/bousai_home.js",
    '''          earthquake: null,
          warnings: { active_count: 0, groups: [] },
          typhoons: []''',
    '''          earthquake: null,
          warnings: null,
          typhoons: null''',
)

replace_once(
    "preview/about.html",
    "本サイトはリアルタイムの警報・避難情報を配信するサイトではありません。",
    "トップページでは気象庁の公開データを参考表示する場合がありますが、公式の警報・避難情報配信を代替するものではありません。取得失敗・遅延・表示差があり得るため、避難判断は気象庁・自治体等の最新情報を直接確認してください。",
)
replace_once(
    "preview/privacy.html",
    "Google AnalyticsではCookie等の技術を利用して、ページ閲覧や利用環境に関する情報がGoogleへ送信される場合があります。",
    "Google AnalyticsではCookie等の技術を利用して、ページ閲覧、閲覧ページ、商品ガイドやAmazonリンク等のクリック、利用環境に関する情報がGoogleへ送信される場合があります。クリック計測ではリンク先URLやリンク文言等をイベント情報として送信する場合があります。",
)
replace_once(
    "preview/qa.html",
    '<p>よくある疑問に先に短く答えます。質問をクリックすると同じページ内で回答が開き、回答の最後から詳しい記事へ進めます。</p>',
    '<p>よくある疑問に先に短く答えます。質問をクリックすると同じページ内で回答が開き、回答の最後から詳しい記事へ進めます。</p><p class="source-note">Q&amp;Aは概要を素早く確認するための入口です。避難・安全・保険・制度など重要な判断では、リンク先の詳しい記事と気象庁・自治体・契約先等の最新情報も確認してください。</p>',
)
