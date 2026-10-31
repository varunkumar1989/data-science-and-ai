/* Resource gate for the handbook site: PDFs, workbooks and datasets open after the visitor shares their details once.
   Details are saved as a "resource" lead on skillnavora.in (same table and alerts as the main site).
   Visitors who already filled the form on skillnavora.in arrive with ?sn=1 and are not asked again.
   This is visitor tracking, not security: files stay reachable by direct link. */
(function () {
  const KEY = "sn_access", API = "https://www.skillnavora.in/api/lead";
  const FILE = /\.(pdf|xlsx|xls|csv|zip|pptx|docx|ipynb)(?:[?#]|$)/i;
  const get = k => { try { return localStorage.getItem(k); } catch { return null; } };
  const set = (k, v) => { try { localStorage.setItem(k, v); } catch {} };
  try { if (/[?&]sn=1\b/.test(location.search)) set(KEY, get(KEY) || JSON.stringify({ t: Date.now(), via: "skillnavora" })); } catch {}
  // Signed-in admins (flag set by the admin panel, cleared on sign-out) skip the form and are not counted as visitors.
  const isAdmin = () => { try { const a = JSON.parse(get("sn_admin") || "null"); return !!a && Date.now() - a.t < 30 * 864e5; } catch { return false; } };
  const has = () => isAdmin() || !!get(KEY);
  if (isAdmin()) document.addEventListener("DOMContentLoaded", () => { const b = document.createElement("div"); b.textContent = "Admin view · details form off"; b.setAttribute("style", "position:fixed;left:12px;bottom:12px;z-index:9998;background:#17614F;color:#fff;font:600 12px/1 system-ui,sans-serif;padding:7px 11px;border-radius:999px;opacity:.9;pointer-events:none"); document.body.appendChild(b); });
  const gated = a => { if (!a || a.hasAttribute("data-nogate")) return false; const h = a.getAttribute("href") || ""; return FILE.test(h); };
  let modal, pending;
  // PDFs open inside the page (browser's own PDF viewer in a frame) so learners and admins stay on the site.
  const PDFX = /\.pdf(?:[?#]|$)/i;
  const canInline = () => navigator.pdfViewerEnabled !== false && !/Android|iPhone|iPad/i.test(navigator.userAgent);
  let viewer;
  const openPdf = (href, label) => {
    if (!viewer) {
      const st = document.createElement("style");
      st.textContent = ".snpv{position:fixed;inset:0;z-index:9999;background:rgba(15,12,30,.72);display:flex;flex-direction:column;padding:max(10px,env(safe-area-inset-top)) max(10px,env(safe-area-inset-right)) max(10px,env(safe-area-inset-bottom)) max(10px,env(safe-area-inset-left))}.snpv[hidden]{display:none}.snpv-bar{display:flex;gap:8px;align-items:center;background:#fff;color:#17142E;border-radius:10px 10px 0 0;padding:8px 12px;font:600 14px/1.3 system-ui,sans-serif}.snpv-bar b{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.snpv-bar a,.snpv-bar button{font:600 13px system-ui,sans-serif;border:1px solid #d9d3ee;background:#fff;color:#17142E;border-radius:8px;padding:6px 10px;cursor:pointer;text-decoration:none}.snpv iframe{flex:1;width:100%;border:0;background:#fff;border-radius:0 0 10px 10px}";
      document.head.appendChild(st);
      viewer = document.createElement("div"); viewer.className = "snpv"; viewer.hidden = true; viewer.setAttribute("role", "dialog"); viewer.setAttribute("aria-modal", "true");
      viewer.innerHTML = '<div class="snpv-bar"><b></b><a target="_blank" rel="noopener" data-nogate data-pdf-direct>Open in new tab ↗</a><button type="button" data-close>Close ✕</button></div><iframe title="Document"></iframe>';
      document.body.appendChild(viewer);
      const close = () => { viewer.hidden = true; viewer.querySelector("iframe").src = "about:blank"; document.documentElement.style.overflow = ""; };
      viewer.querySelector("[data-close]").addEventListener("click", close);
      viewer.addEventListener("click", e => { if (e.target === viewer) close(); });
      document.addEventListener("keydown", e => { if (e.key === "Escape" && !viewer.hidden) close(); });
    }
    viewer.querySelector("b").textContent = label || decodeURIComponent(href.split("/").pop().split(/[?#]/)[0]);
    viewer.querySelector("a").href = href; viewer.querySelector("iframe").src = href;
    viewer.hidden = false; document.documentElement.style.overflow = "hidden"; viewer.querySelector("[data-close]").focus();
  };

  // The owner's GitHub repositories: admins open them; everyone else sends an access request for the owner to approve.
  const OWNER_GH = /^https?:\/\/(www\.)?github\.com\/varunkumar1989\//i;
  const ghAdmin = () => { try { const a = JSON.parse(localStorage.getItem("sn_admin") || "null"); return !!a && Date.now() - a.t < 30 * 864e5; } catch { return false; } };
  let ghBox;
  const ghRequest = repo => {
    if (!ghBox) {
      ghBox = document.createElement("div"); ghBox.setAttribute("style", "position:fixed;inset:0;z-index:9999;background:rgba(15,12,30,.72);display:flex;align-items:center;justify-content:center;padding:16px"); ghBox.hidden = true; const ghs = document.createElement("style"); ghs.textContent = "[data-ghbox][hidden]{display:none!important}"; document.head.appendChild(ghs); ghBox.setAttribute("data-ghbox", "");
      ghBox.innerHTML = '<form style="background:#fff;color:#17142E;border-radius:14px;max-width:420px;width:100%;padding:20px;font:14px/1.45 system-ui,sans-serif" novalidate><h2 style="margin:0 0 4px;font-size:19px">Request GitHub access</h2><p style="margin:0 0 12px;color:#4A4660">The code repositories are private. Send a request and the owner will add you after approving it.</p>' +
        '<label style="display:block;font-weight:600;margin:6px 0 3px">Full name</label><input name="name" maxlength="80" style="width:100%;padding:8px;border:1px solid #d9d3ee;border-radius:8px">' +
        '<label style="display:block;font-weight:600;margin:6px 0 3px">Email</label><input name="email" type="email" maxlength="120" style="width:100%;padding:8px;border:1px solid #d9d3ee;border-radius:8px">' +
        '<label style="display:block;font-weight:600;margin:6px 0 3px">GitHub username</label><input name="gh" maxlength="40" style="width:100%;padding:8px;border:1px solid #d9d3ee;border-radius:8px">' +
        '<label style="display:block;font-weight:600;margin:6px 0 3px">Why do you need access?</label><input name="why" maxlength="200" style="width:100%;padding:8px;border:1px solid #d9d3ee;border-radius:8px">' +
        '<p data-msg style="color:#B42318;min-height:18px;margin:8px 0 0"></p><div style="display:flex;gap:8px;margin-top:8px"><button type="submit" style="flex:1;padding:10px;border:0;border-radius:9px;background:#6C4CF5;color:#fff;font-weight:700;cursor:pointer">Send request</button><button type="button" data-close style="padding:10px 14px;border:1px solid #d9d3ee;border-radius:9px;background:#fff;cursor:pointer">Cancel</button></div></form>';
      document.body.appendChild(ghBox);
      const f = ghBox.querySelector("form"), m = ghBox.querySelector("[data-msg]");
      ghBox.querySelector("[data-close]").addEventListener("click", () => ghBox.hidden = true);
      f.addEventListener("submit", async e => {
        e.preventDefault(); const v = n => f.elements[n].value.trim();
        if (!v("name")) return m.textContent = "Please enter your name.";
        if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("email"))) return m.textContent = "Please enter a valid email.";
        if (!/^[A-Za-z0-9-]{1,39}$/.test(v("gh"))) return m.textContent = "Please enter your GitHub username.";
        m.textContent = "";
        const row = { kind: "resource", first_name: v("name"), email: v("email"), role: "GitHub access request", source: "github-request",
          message: ("[GitHub access request] GitHub user: " + v("gh") + " | Repo: " + ghBox.dataset.repo + " | Reason: " + v("why") + " | Page: " + location.pathname).slice(0, 1900) };
        try { await fetch(API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(row), keepalive: true }); } catch {}
        f.reset(); ghBox.hidden = true;
        const d = document.createElement("div"); d.textContent = "Request sent. You will get access once the owner approves it."; d.setAttribute("style", "position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:10000;background:#17142E;color:#fff;padding:10px 16px;border-radius:10px;font:600 14px system-ui,sans-serif"); document.body.appendChild(d); setTimeout(() => d.remove(), 4000);
      });
    }
    ghBox.dataset.repo = repo; ghBox.hidden = false; ghBox.querySelector("input").focus();
  };
  document.addEventListener("click", e => {
    const a = e.target.closest && e.target.closest("a"); if (!a || !OWNER_GH.test(a.href) || ghAdmin()) return;
    e.preventDefault(); e.stopImmediatePropagation(); ghRequest(a.href);
  }, true);
  // Lessons and handbook pages open in the same in-page viewer when clicked from hub pages (resources, handbooks, LMS, tools, tests),
  // so learners stay on the tab they were browsing. Inside lessons themselves, links navigate normally.
  const HUB_PAGE = !/\/data-science\/(lessons|index)|\/handbooks\/pm\//.test(location.pathname) && window.self === window.top;
  const sameOriginLesson = href => { try { const u = new URL(href, location.href); return HUB_PAGE && u.origin === location.origin && /\/(data-science\/lessons\/[^/]+|handbooks\/pm\/[^/]+)\.html$/.test(u.pathname); } catch { return false; } };
  const sameOriginPdf = href => { try { const u = new URL(href, location.href); return u.origin === location.origin && PDFX.test(u.pathname); } catch { return false; } };
  document.addEventListener("click", e => {
    if (e.defaultPrevented || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
    const a = e.target.closest && e.target.closest("a"); if (!a || a.hasAttribute("data-pdf-direct")) return;
    if (sameOriginLesson(a.href)) { e.preventDefault(); openPdf(a.href, (a.textContent || "").replace(/\s+/g, " ").replace(/[↗⬇→]/g, "").trim().slice(0, 90)); return; }
    if (!sameOriginPdf(a.href) || !canInline()) return;
    if (typeof has === "function" && !has() && typeof gated === "function" && gated(a)) return;   // the details form handles it first
    e.preventDefault(); openPdf(a.href, (a.textContent || "").replace(/\s+/g, " ").replace(/[↗⬇→]/g, "").trim().slice(0, 90));
  });

  const css = `.sg-m{position:fixed;inset:0;background:rgba(20,16,40,.55);display:none;align-items:center;justify-content:center;z-index:9999;padding:16px}
.sg-m.open{display:flex}.sg-b{background:#fff;color:#1F1B2E;border-radius:14px;max-width:430px;width:100%;padding:22px 22px 18px;box-shadow:0 20px 60px rgba(0,0,0,.25);font:14px/1.45 Inter,system-ui,sans-serif;max-height:92vh;overflow:auto}
.sg-b h2{margin:0 0 4px;font-size:20px}.sg-b p{margin:0 0 12px;color:#4A4660}.sg-b label{display:block;margin:8px 0 3px;font-weight:600;font-size:13px}
.sg-b input,.sg-b select{width:100%;box-sizing:border-box;padding:9px 10px;border:1px solid #D9D3EE;border-radius:8px;font:inherit}
.sg-b .row{display:flex;gap:6px}.sg-b .row select{width:96px;flex:none}.sg-b .chk{display:flex;gap:8px;align-items:flex-start;font-weight:400;margin-top:10px}.sg-b .chk input{width:auto;margin-top:3px}
.sg-b button.go{margin-top:14px;width:100%;padding:11px;border:0;border-radius:9px;background:#7C3AED;color:#fff;font-weight:700;font-size:15px;cursor:pointer}
.sg-b .x{float:right;border:0;background:none;font-size:22px;cursor:pointer;color:#777}.sg-b .err{color:#B42318;font-size:13px;min-height:18px;margin-top:6px}
.sg-b .chip{background:#F3F0FF;border-radius:8px;padding:6px 9px;font-size:12.5px;margin-bottom:6px;word-break:break-word}
@media (prefers-color-scheme: dark){.sg-b{background:#1E1B2E;color:#EEE}.sg-b p{color:#BBB}.sg-b input,.sg-b select{background:#2A2640;color:#EEE;border-color:#3E3860}.sg-b .chip{background:#2A2640}}`;
  const build = () => {
    const st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    modal = document.createElement("div"); modal.className = "sg-m"; modal.setAttribute("role", "dialog"); modal.setAttribute("aria-modal", "true");
    modal.innerHTML = `<div class="sg-b"><button class="x" type="button" aria-label="Close">×</button><h2>Get free access</h2>
      <p>Share your details once to open every PDF, workbook and dataset in the SkillNavora handbook.</p><div class="chip" id="sg-res"></div>
      <form novalidate><label>Full name</label><input name="name" autocomplete="name" maxlength="80">
      <label>Email</label><input name="email" type="email" autocomplete="email" maxlength="120">
      <label>Phone</label><div class="row"><select name="cc"><option>+91</option><option>+971</option><option>+1</option><option>+44</option><option>+65</option><option>+61</option></select><input name="phone" inputmode="tel" maxlength="15"></div>
      <label>I am a</label><select name="role"><option value="">Choose…</option><option>Student</option><option>Working professional</option><option>Career switcher</option><option>Hiring manager / recruiter</option><option>Other</option></select>
      <label class="chk"><input type="checkbox" name="consent"><span>I agree that SkillNavora may contact me about learning resources and programs (<a href="https://www.skillnavora.in/privacy.html" target="_blank" rel="noopener" data-nogate>privacy policy</a>).</span></label>
      <div class="err" aria-live="polite"></div><button class="go" type="submit">Unlock access</button></form></div>`;
    document.body.appendChild(modal);
    const close = () => modal.classList.remove("open");
    modal.addEventListener("click", e => { if (e.target === modal || e.target.classList.contains("x")) close(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape") close(); });
    const f = modal.querySelector("form"), err = modal.querySelector(".err");
    f.addEventListener("submit", async e => {
      e.preventDefault();
      const v = n => f.elements[n].value.trim(), phone = (f.elements.cc.value + " " + v("phone")).trim();
      const say = t => (err.textContent = t);
      if (!v("name")) return say("Please enter your name.");
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v("email"))) return say("Please enter a valid email.");
      if (v("phone").replace(/\D/g, "").length < 7) return say("Please enter a valid phone number.");
      if (!v("role")) return say("Please choose who you are.");
      if (!f.elements.consent.checked) return say("Please tick the box to continue.");
      say(""); const b = f.querySelector("button.go"); b.disabled = true; b.textContent = "Unlocking…";
      const row = { kind: "resource", first_name: v("name"), email: v("email"), phone, role: v("role"), source: "data-science-handbook",
        message: ("[Resource access] Data Science & AI handbook | " + (pending ? pending.label : "") + " | Page: " + location.pathname).slice(0, 1900) };
      try { await fetch(API, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(row), keepalive: true }); } catch {}
      set(KEY, JSON.stringify({ t: Date.now(), n: v("name").split(" ")[0] }));
      b.disabled = false; b.textContent = "Unlock access"; close();
      window.dispatchEvent(new Event("sn-access"));
      if (pending && pending.href) { const p = pending; pending = null; if (sameOriginPdf(p.href) && canInline()) openPdf(p.href, p.label); else window.open(p.href, "_blank", "noopener") || (location.href = p.href); }
    });
  };
  const ask = a => {
    if (!modal) build();
    pending = { href: a.href, label: (a.textContent || a.getAttribute("href") || "").replace(/\s+/g, " ").trim().slice(0, 90) };
    modal.querySelector("#sg-res").textContent = "Opening: " + pending.label;
    modal.classList.add("open"); setTimeout(() => modal.querySelector("input[name=name]").focus(), 30);
  };
  document.addEventListener("click", e => {
    if (e.defaultPrevented || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey) return;
    const a = e.target.closest && e.target.closest("a"); if (!a || !gated(a) || has()) return;
    e.preventDefault(); ask(a);
  }, true);
  // Lessons and handbook pages lock (blurred) until the visitor gives details; admins and returning visitors skip it.
  // Pages embedded in a frame (the in-page viewer, guide pages) are not locked: the page around them decides.
  const lockPage = label => {
    if (has() || window.self !== window.top || document.getElementById("sn-lockov")) return;
    const st = document.createElement("style");
    st.textContent = "#sn-lockov{position:fixed;inset:0;z-index:9990;background:rgba(10,12,30,.55);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);display:flex;align-items:center;justify-content:center;padding:16px}#sn-lockov .c{background:#fff;color:#17142E;border-radius:16px;padding:22px 24px;max-width:460px;text-align:center;font:15px/1.5 system-ui,sans-serif;box-shadow:0 18px 50px rgba(0,0,0,.3)}#sn-lockov h2{margin:0 0 6px;font-size:20px}#sn-lockov p{margin:0 0 14px;color:#55607a}#sn-lockov button{border:0;border-radius:10px;background:#5b4ee8;color:#fff;font:700 15px system-ui,sans-serif;padding:11px 20px;cursor:pointer}";
    document.head.appendChild(st);
    const ov = document.createElement("div"); ov.id = "sn-lockov";
    ov.innerHTML = '<div class="c"><h2>Free access: enter your details to read this</h2><p>Tell us a little about you once. Then every lesson, class, tab and PDF opens.</p><button type="button">Unlock free access</button></div>';
    document.body.appendChild(ov); document.documentElement.style.overflow = "hidden";
    const open = () => { if (!modal) build(); pending = { href: "", label }; modal.querySelector("#sg-res").textContent = "Opening: " + label; modal.classList.add("open"); setTimeout(() => modal.querySelector("input[name=name]").focus(), 30); };
    ov.querySelector("button").addEventListener("click", open);
    window.addEventListener("sn-access", () => { ov.remove(); document.documentElement.style.overflow = ""; }, { once: true });
    open();
  };
  const initLock = () => { const b = document.body; if (b && (b.classList.contains("lesson") || b.hasAttribute("data-gate-lock"))) lockPage((b.getAttribute("data-gate-lock") || document.title.split("·")[0]).trim().slice(0, 80)); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initLock); else initLock();
  window.SNgate = { has };
})();
