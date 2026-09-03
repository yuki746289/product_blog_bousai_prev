/* Created: 2026-09-02 / Updated: 2026-09-03 / common preview behavior */
(function () {
  function markImageError(img) {
    if (!img || img.dataset.fallbackHandled === "1") return;
    img.dataset.fallbackHandled = "1";

    /* Product cards already have a product-specific fallback. */
    if (img.closest(".product-recommendation__image")) return;

    var holder = img.closest(
      "figure, .official-link-visual, .card-thumb, .topic-card__thumb, .pickup-card__visual--image"
    );

    if (!holder) {
      img.hidden = true;
      return;
    }

    holder.classList.add("is-image-error");
    img.remove();

    if (!holder.querySelector(".image-error-note")) {
      var note = document.createElement("p");
      note.className = "image-error-note";
      note.textContent = "画像を読み込めません。本文・出典リンクの情報をご確認ください。";
      holder.appendChild(note);
    }
  }

  function bindImageFallbacks() {
    document.querySelectorAll("img").forEach(function (img) {
      img.addEventListener("error", function () {
        markImageError(img);
      }, { once: true });

      if (img.complete && img.naturalWidth === 0) {
        markImageError(img);
      }
    });
  }

  function sendAnalyticsEvent(name, parameters) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", name, parameters);
  }

  function normalizedLinkText(link) {
    return (link.textContent || "").replace(/\s+/g, " ").trim().slice(0, 120);
  }

  function isAmazonHost(hostname) {
    var host = hostname.toLowerCase();
    return host === "amzn.to" || host === "amazon.co.jp" || host.endsWith(".amazon.co.jp");
  }

  function bindTrackedLinks() {
    document.addEventListener("click", function (event) {
      var target = event.target;
      if (!target || typeof target.closest !== "function") return;

      var link = target.closest("a[href]");
      if (!link) return;

      var url;
      try {
        url = new URL(link.href, window.location.href);
      } catch (error) {
        return;
      }

      var common = {
        link_url: url.href,
        link_text: normalizedLinkText(link),
        page_path: window.location.pathname,
        transport_type: "beacon"
      };

      if (isAmazonHost(url.hostname)) {
        sendAnalyticsEvent("amazon_click", common);
        return;
      }

      if (
        url.origin === window.location.origin &&
        /^\/goods\/.+\.html$/.test(url.pathname) &&
        !/\/goods\/index\.html$/.test(url.pathname) &&
        !/^\/goods\//.test(window.location.pathname)
      ) {
        sendAnalyticsEvent("product_guide_click", common);
      }
    }, { passive: true });
  }


  function formatRealtimeDate(value) {
    if (!value) return "";
    var date = new Date(value);
    if (Number.isNaN(date.getTime())) return "";
    return new Intl.DateTimeFormat("ja-JP", {
      month: "numeric",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    }).format(date);
  }

  function isRealtimeStale(value) {
    if (!value) return true;
    var date = new Date(value);
    if (Number.isNaN(date.getTime())) return true;
    return Date.now() - date.getTime() > 30 * 60 * 1000;
  }

  function renderRealtimeEarthquake(root, data) {
    var main = root.querySelector("[data-realtime-earthquake]");
    var sub = root.querySelector("[data-realtime-earthquake-sub]");
    if (!main || !sub) return;

    var quake = data.earthquake;
    if (!quake) {
      main.textContent = "直近の地震情報を取得できていません。";
      sub.textContent = "";
      return;
    }

    var parts = [];
    if (quake.time) parts.push(formatRealtimeDate(quake.time));
    if (quake.area) parts.push(quake.area);
    if (quake.max_intensity) parts.push("最大震度" + quake.max_intensity);
    main.textContent = parts.join(" / ") || quake.title || "地震情報";

    var details = [];
    if (quake.magnitude) details.push("M" + quake.magnitude);
    if (quake.headline && !quake.max_intensity) details.push(quake.headline);
    sub.textContent = details.join("　");
  }

  function renderRealtimeWarnings(root, data) {
    var holder = root.querySelector("[data-realtime-warnings]");
    if (!holder) return;
    holder.textContent = "";

    var warnings = data.warnings || {};
    var groups = Array.isArray(warnings.groups) ? warnings.groups : [];
    if (!warnings.active_count || groups.length === 0) {
      var none = document.createElement("p");
      none.className = "realtime-none";
      none.textContent = "取得データでは、現在表示対象の警報・特別警報は確認されていません。";
      holder.appendChild(none);
      return;
    }

    var list = document.createElement("ul");
    list.className = "realtime-list";
    groups.forEach(function (group) {
      var item = document.createElement("li");
      var areas = Array.isArray(group.areas) ? group.areas : [];
      var visible = areas.slice(0, 3);
      var suffix = areas.length > 3 ? " ほか" + (areas.length - 3) + "地域" : "";
      item.textContent = group.kind + "：" + visible.join("、") + suffix;
      list.appendChild(item);
    });
    holder.appendChild(list);
  }

  function renderRealtimeTyphoons(root, data) {
    var holder = root.querySelector("[data-realtime-typhoon]");
    if (!holder) return;
    holder.textContent = "";

    var typhoons = Array.isArray(data.typhoons) ? data.typhoons : [];
    if (typhoons.length === 0) {
      var none = document.createElement("p");
      none.className = "realtime-none";
      none.textContent = "直近24時間の取得データでは、表示対象の台風情報はありません。";
      holder.appendChild(none);
      return;
    }

    var list = document.createElement("ul");
    list.className = "realtime-list";
    typhoons.forEach(function (typhoon) {
      var item = document.createElement("li");
      var text = typhoon.headline || typhoon.title || "台風情報";
      if (text.length > 110) text = text.slice(0, 107) + "…";
      item.textContent = text;
      list.appendChild(item);
    });
    holder.appendChild(list);
  }

  function renderRealtimePanel(root, data) {
    var updated = root.querySelector("[data-realtime-updated]");
    var status = root.querySelector("[data-realtime-status]");
    var checkedAt = data.checked_at;
    var stale = isRealtimeStale(checkedAt);

    if (updated) {
      updated.textContent = checkedAt
        ? "気象庁XML確認 " + formatRealtimeDate(checkedAt)
        : "更新時刻を確認できません";
    }

    renderRealtimeEarthquake(root, data);
    renderRealtimeWarnings(root, data);
    renderRealtimeTyphoons(root, data);

    if (status) {
      status.classList.remove("is-stale", "is-error");
      if (data.status === "degraded" || data.status === "partial") {
        status.classList.add("is-error");
        status.textContent = "一部の情報取得に失敗しています。表示内容が最新でない可能性があります。避難判断には気象庁・自治体などの最新情報を確認してください。";
      } else if (stale) {
        status.classList.add("is-stale");
        status.textContent = "情報更新が遅延している可能性があります。避難判断には気象庁・自治体などの最新情報を確認してください。";
      } else {
        status.textContent = data.note || "当サイトの表示には遅延する場合があります。避難判断には気象庁・自治体などの最新情報を確認してください。";
      }
    }
  }

  function loadRealtimePanel(root) {
    fetch("realtime/realtime.json?t=" + Date.now(), { cache: "no-store" })
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.json();
      })
      .then(function (data) {
        renderRealtimePanel(root, data);
      })
      .catch(function () {
        var updated = root.querySelector("[data-realtime-updated]");
        var status = root.querySelector("[data-realtime-status]");
        if (updated) updated.textContent = "最新情報を取得できません";
        if (status) {
          status.classList.add("is-error");
          status.textContent = "防災情報を取得できませんでした。気象庁・自治体などの公式情報を直接確認してください。";
        }
      });
  }

  function initRealtimePanel() {
    var root = document.querySelector("[data-realtime-root]");
    if (!root) return;
    loadRealtimePanel(root);
    window.setInterval(function () {
      loadRealtimePanel(root);
    }, 5 * 60 * 1000);
  }

  function init() {
    bindImageFallbacks();
    bindTrackedLinks();
    initRealtimePanel();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}());
