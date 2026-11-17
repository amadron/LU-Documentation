// Adds small item, pet, skill, quest, and NPC icons in front of links in tables and lists.
// The icon list (assets/icons/index.json) is written by scripts/build_media.py; doing this in the
// browser keeps ~100,000 image tags out of the Markdown sources and the site build.
(function () {
  "use strict";

  // /wiki/items/123/, /wiki/pets/123/, /wiki/skills/123/, /wiki/quests/123/,
  // /wiki/items/sources/object-123/, /wiki/quests/sources/object-123/
  var PATTERN = /\/wiki\/(items|pets|skills|quests)\/(?:(sources)\/object-)?(\d+)(?:\/|\/index\.html|\.html)?$/;
  var KIND = { items: "objects", pets: "objects", skills: "skills", quests: "missions" };
  var manifest = null;

  function siteBase() {
    var config = document.getElementById("__config");
    var base = ".";
    try {
      base = JSON.parse(config.textContent).base || ".";
    } catch (error) {
      /* fall back to the current folder */
    }
    return new URL(base.replace(/\/?$/, "/"), window.location.href);
  }

  function decorate(root) {
    if (!manifest) return;
    var base = siteBase();
    var rows = root.querySelectorAll("article table tr, article li");
    for (var r = 0; r < rows.length; r++) {
      var seen = {};
      var links = rows[r].querySelectorAll("a[href]");
      for (var l = 0; l < links.length; l++) {
        var link = links[l];
        if (link.dataset.luIcon) continue;
        var match;
        try {
          match = new URL(link.getAttribute("href"), window.location.href).pathname.match(PATTERN);
        } catch (error) {
          match = null;
        }
        if (!match) continue;
        var kind = match[2] ? "objects" : KIND[match[1]];
        var id = match[3];
        var key = kind + "/" + id;
        link.dataset.luIcon = "1";
        if (seen[key] || !manifest[kind] || !manifest[kind][id]) continue;
        seen[key] = true;
        var img = document.createElement("img");
        img.className = "lu-ti";
        img.width = 24;
        img.height = 24;
        img.loading = "lazy";
        img.alt = "";
        img.src = new URL("assets/icons/" + key + ".webp", base).href;
        link.parentNode.insertBefore(img, link);
      }
    }
  }

  function load() {
    if (manifest) {
      decorate(document);
      return;
    }
    fetch(new URL("assets/icons/index.json", siteBase()).href)
      .then(function (response) { return response.ok ? response.json() : null; })
      .then(function (data) {
        if (!data) return;
        manifest = {};
        Object.keys(data).forEach(function (kind) {
          manifest[kind] = {};
          data[kind].forEach(function (id) { manifest[kind][id] = true; });
        });
        decorate(document);
      })
      .catch(function () { /* icons are optional */ });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(load);  // Material instant navigation
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", load);
  } else {
    load();
  }
})();
