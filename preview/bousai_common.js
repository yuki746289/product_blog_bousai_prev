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


  function enhanceAccessibility() {
    var main = document.querySelector("main");
    if (main) {
      if (!main.id) main.id = "main-content";
      if (!document.querySelector(".skip-link")) {
        var skip = document.createElement("a");
        skip.className = "skip-link";
        skip.href = "#" + main.id;
        skip.textContent = "本文へ移動";
        document.body.insertBefore(skip, document.body.firstChild);
      }
    }

    document.querySelectorAll(".breadcrumb").forEach(function (breadcrumb) {
      if (!breadcrumb.hasAttribute("aria-label")) {
        breadcrumb.setAttribute("aria-label", "パンくず");
      }
    });

    document.querySelectorAll(".table-wrap").forEach(function (wrapper) {
      if (!wrapper.hasAttribute("tabindex")) wrapper.setAttribute("tabindex", "0");
      if (!wrapper.hasAttribute("role")) wrapper.setAttribute("role", "region");

      if (!wrapper.hasAttribute("aria-label")) {
        var label = "表";
        var node = wrapper.previousElementSibling;
        while (node) {
          if (/^H[23]$/.test(node.tagName)) {
            label = (node.textContent || "").trim() + "の表";
            break;
          }
          node = node.previousElementSibling;
        }
        wrapper.setAttribute("aria-label", label);
      }
    });

    var currentFile = (window.location.pathname.split("/").pop() || "index.html").toLowerCase();
    var navLinks = Array.prototype.slice.call(document.querySelectorAll(".site-nav a[href]"));
    var currentMarked = false;

    navLinks.forEach(function (link) {
      var href = (link.getAttribute("href") || "").split("#")[0].split("?")[0].toLowerCase();
      if (href === currentFile) {
        link.setAttribute("aria-current", "page");
        currentMarked = true;
      }
    });

    if (!currentMarked) {
      var categoryCrumb = document.querySelector('.breadcrumb a[href^="category_"]');
      if (categoryCrumb) {
        var categoryHref = (categoryCrumb.getAttribute("href") || "").split("#")[0].split("?")[0].toLowerCase();
        navLinks.forEach(function (link) {
          var href = (link.getAttribute("href") || "").split("#")[0].split("?")[0].toLowerCase();
          if (href === categoryHref) {
            link.setAttribute("aria-current", "location");
          }
        });
      }
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


  function init() {
    enhanceAccessibility();
    bindImageFallbacks();
    bindTrackedLinks();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
}());
