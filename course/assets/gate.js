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
  const has = () => !!get(KEY);
  const gated = a => { if (!a || a.hasAttribute("data-nogate")) return false; const h = a.getAttribute("href") || ""; return FILE.test(h); };
  let modal, pending;
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
      if (pending) { const p = pending; pending = null; window.open(p.href, "_blank", "noopener") || (location.href = p.href); }
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
  window.SNgate = { has };
})();
