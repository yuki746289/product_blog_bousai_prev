/* Created: 2026-09-02 / common preview behavior */
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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bindImageFallbacks);
  } else {
    bindImageFallbacks();
  }
}());
