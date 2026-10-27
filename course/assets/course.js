(function () {
  var store = { get: function (k) { try { return JSON.parse(localStorage.getItem(k) || "null"); } catch (e) { return null; } },
                set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} } };
  // theme
  var th = store.get("sn-theme"); if (th) document.documentElement.setAttribute("data-theme", th);
  var tb = document.getElementById("theme");
  if (tb) tb.onclick = function () {
    var cur = document.documentElement.getAttribute("data-theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    var nx = cur === "dark" ? "light" : "dark"; document.documentElement.setAttribute("data-theme", nx); store.set("sn-theme", nx);
  };
  // copy buttons
  document.querySelectorAll(".copy").forEach(function (b) {
    b.onclick = function () { var c = b.closest(".code").querySelector("code").innerText;
      (navigator.clipboard ? navigator.clipboard.writeText(c) : Promise.reject()).then(function () { b.textContent = "Copied"; setTimeout(function () { b.textContent = "Copy"; }, 1400); }, function () {}); };
  });
  // quizzes
  document.querySelectorAll(".qq").forEach(function (q) {
    q.querySelectorAll(".opt").forEach(function (o) {
      o.onclick = function () { if (q.classList.contains("answered")) return; q.classList.add("answered");
        o.classList.add(o.dataset.ok === "1" ? "ok" : "no"); q.querySelectorAll('.opt[data-ok="1"]').forEach(function (r) { r.classList.add("ok"); }); };
    });
  });
  // progress
  var done = store.get("sn-done") || {};
  function paint() {
    document.querySelectorAll("[data-lid]").forEach(function (a) { if (a.tagName === "A") a.classList.toggle("dn", !!done[a.dataset.lid]); });
    document.querySelectorAll(".btn.done").forEach(function (b) { var d = !!done[b.dataset.lid]; b.classList.toggle("is-done", d); b.textContent = d ? "✓ Completed" : "☐ Mark as complete"; });
    document.querySelectorAll(".prog").forEach(function (p) { var t = p.dataset.track, n = +p.dataset.n, k = 0;
      Object.keys(done).forEach(function (id) { if (done[id] && id.indexOf(t + "-") === 0 && /^\d+$/.test(id.slice(t.length + 1))) k++; });
      p.querySelector("i").style.width = (100 * k / n) + "%"; p.querySelector("span").textContent = k + " / " + n + " done"; });
  }
  document.querySelectorAll(".btn.done").forEach(function (b) { b.onclick = function () { done[b.dataset.lid] = !done[b.dataset.lid]; store.set("sn-done", done); paint(); }; });
  paint();
  // toc highlight
  var links = [].slice.call(document.querySelectorAll(".toc a"));
  if (links.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (l) { l.classList.toggle("on", l.getAttribute("href") === "#" + e.target.id); }); } }); }, { rootMargin: "-70px 0px -70% 0px" });
    document.querySelectorAll(".content h2[id]").forEach(function (h) { io.observe(h); });
  }
  // search
  var q = document.getElementById("q"), box = document.getElementById("qres"), idx = window.SN_INDEX || [];
  var base = document.body.classList.contains("lesson") ? "../" : "";
  if (q && box) {
    q.oninput = function () {
      var s = q.value.trim().toLowerCase(); if (s.length < 2) { box.hidden = true; return; }
      var words = s.split(/\s+/), hits = [];
      idx.forEach(function (it) { var t = it.t.toLowerCase(), b = it.s.toLowerCase(), sc = 0;
        words.forEach(function (w) { if (t.indexOf(w) > -1) sc += 5; var p = b.indexOf(w); if (p > -1) sc += 1; });
        if (words.every(function (w) { return t.indexOf(w) > -1 || b.indexOf(w) > -1; })) hits.push([sc, it]); });
      hits.sort(function (a, b) { return b[0] - a[0]; });
      box.innerHTML = hits.slice(0, 12).map(function (h) { var it = h[1], b = it.s, p = b.toLowerCase().indexOf(words[0]);
        var snip = p > -1 ? b.slice(Math.max(0, p - 50), p + 90) : b.slice(0, 120);
        return '<a href="' + base + it.f + '"><i>' + it.k + '</i> ' + it.t + '<small>…' + snip.replace(/</g, "&lt;") + '…</small></a>'; }).join("") || '<div style="padding:10px;color:var(--mu)">No lessons found</div>';
      box.hidden = false;
    };
    document.addEventListener("click", function (e) { if (!box.contains(e.target) && e.target !== q) box.hidden = true; });
  }
})();
