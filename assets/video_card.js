/*
 * video_card.js
 * -------------
 * Powers the click-to-play video card built in utils.video_card().
 *
 * Dash's app.layout is rendered server-side once per session, so it has no
 * concept of per-visitor "is this card playing right now" state. This script
 * fills that gap on the client, mirroring the React VideoCard pattern:
 *   1. On first sight of a .video-card-frame, make sure it has a thumbnail:
 *      if utils.video_card() already rendered one (a local asset), leave it
 *      alone; otherwise fetch Vimeo's oEmbed thumbnail as a fallback.
 *   2. The Vimeo player iframe is only created and mounted once the visitor
 *      clicks the play button - never on page load.
 */
(function () {
  function loadThumbnail(frame) {
    var thumbSlot = frame.querySelector(".video-card-thumb");
    if (!thumbSlot || thumbSlot.querySelector("img")) return; // already have one

    var vimeoId = frame.getAttribute("data-vimeo-id");
    if (!vimeoId) return;

    fetch(
      "https://vimeo.com/api/oembed.json?url=https://vimeo.com/" +
        vimeoId +
        "&width=1280"
    )
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (!data || !data.thumbnail_url || frame.getAttribute("data-vc-playing")) {
          return;
        }
        var img = document.createElement("img");
        img.src = data.thumbnail_url;
        img.alt = "";
        img.className = "video-card-thumb-img";
        thumbSlot.innerHTML = "";
        thumbSlot.appendChild(img);
      })
      .catch(function () {
        /* leave the dark placeholder if the oEmbed lookup fails */
      });
  }

  function playVideo(frame) {
    if (frame.getAttribute("data-vc-playing")) return;
    frame.setAttribute("data-vc-playing", "1");

    var vimeoId = frame.getAttribute("data-vimeo-id");
    var title = frame.getAttribute("data-title") || "Video";

    var iframe = document.createElement("iframe");
    iframe.src =
      "https://player.vimeo.com/video/" +
      vimeoId +
      "?autoplay=1&title=0&byline=0&portrait=0&badge=0&sidedock=0";
    iframe.width = "100%";
    iframe.height = "100%";
    iframe.frameBorder = "0";
    iframe.allow = "autoplay; fullscreen; picture-in-picture";
    iframe.allowFullscreen = true;
    iframe.title = title;
    iframe.className = "video-card-player";

    frame.innerHTML = "";
    frame.appendChild(iframe);
  }

  function initCard(frame) {
    if (frame.getAttribute("data-vc-init")) return;
    frame.setAttribute("data-vc-init", "1");
    loadThumbnail(frame);
  }

  function scan() {
    document.querySelectorAll(".video-card-frame").forEach(initCard);
  }

  // Event delegation: the play button (or the whole card, once it's
  // replaced by the iframe) can be re-rendered by Dash, so bind on document
  // rather than on the button directly.
  document.addEventListener("click", function (e) {
    var btn = e.target.closest(".video-card-play-btn");
    if (!btn) return;
    var frame = btn.closest(".video-card-frame");
    if (frame) playVideo(frame);
  });

  // Dash mounts the layout after this script runs, so watch for cards
  // appearing/re-rendering instead of relying solely on DOMContentLoaded.
  var observer = new MutationObserver(scan);
  observer.observe(document.documentElement, { childList: true, subtree: true });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }
})();
