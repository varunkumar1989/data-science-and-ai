"""Tiny notebook-like runner: executes solution code against the real case-study data,
captures printed answers, result tables and charts, and stores everything as JSON for rendering."""
import io, os, json, contextlib, traceback, html, warnings
import pandas as pd, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
HB = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HB, "site", "img", "cs")
os.makedirs(IMG, exist_ok=True)
OUT = os.path.join(HB, "solved")
os.makedirs(OUT, exist_ok=True)

PAL = ["#1F3864", "#E9A23B", "#2E8B8B", "#C8553D", "#6A4C93", "#5A8F29", "#8C8C8C", "#D17A22"]
plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 130, "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.prop_cycle": matplotlib.cycler(color=PAL),
                     "axes.titleweight": "bold", "figure.figsize": (8, 4.2)})
pd.set_option("display.width", 160)


def df_html(o, maxrows=15):
    if isinstance(o, pd.Series):
        o = o.to_frame()
    n = len(o)
    d = o.head(maxrows) if n > maxrows else o
    def fmt(x):
        if isinstance(x, (float, np.floating)):
            if np.isnan(x): return "NaN"
            return f"{x:,.2f}" if abs(x) >= 0.01 or x == 0 else f"{x:.4g}"
        return x
    try:
        d = d.map(fmt)
    except Exception:
        d = d.applymap(fmt)
    h = d.to_html(classes="tbl", border=0, escape=True)
    if n > maxrows:
        h += f'<p class="more">Showing first {maxrows} of {n:,} rows.</p>'
    return h


class Case:
    def __init__(self, cid, title, module, tool, data_dir, brief, data_desc=""):
        self.cid, self.title, self.module, self.tool = cid, title, module, tool
        self.data_dir, self.brief, self.data_desc = data_dir, brief, data_desc
        self.items = []
        self.ns = {"pd": pd, "np": np, "plt": plt}
        self.nimg = 0

    def setup(self, code):
        self.q(None, None, code, hidden_q=True)

    def q(self, num, text, code, note=None, hidden_q=False, lang="python", show=True, display=None):
        cwd = os.getcwd(); os.chdir(self.data_dir)
        buf = io.StringIO(); err = None
        self.ns.pop("out", None)
        plt.close("all")
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, f"<{self.cid}-{num}>", "exec"), self.ns)
        except Exception as e:
            err = "".join(traceback.format_exception_only(type(e), e)).strip()
        finally:
            os.chdir(cwd)
        imgs = []
        for fn in plt.get_fignums():
            fig = plt.figure(fn)
            if not fig.axes: continue
            self.nimg += 1
            name = f"{self.cid}_{self.nimg:02d}.png"
            fig.tight_layout()
            fig.savefig(os.path.join(IMG, name), bbox_inches="tight", facecolor="white")
            imgs.append("img/cs/" + name)
        plt.close("all")
        out = self.ns.get("out")
        table = None
        if isinstance(out, (pd.DataFrame, pd.Series)):
            table = df_html(out)
        elif out is not None:
            table = f"<pre class='res'>{html.escape(str(out))}</pre>"
        if callable(note):
            note = note(self.ns)
        item = dict(num=num, text=text, code=(display if display is not None else code).strip("\n"), stdout=buf.getvalue().rstrip(),
                    table=table, imgs=imgs, note=note, err=err, hidden=hidden_q, lang=lang, show=show)
        self.items.append(item)
        if err:
            print(f"!! {self.cid} Q{num}: {err}")
        return item

    def save(self):
        d = dict(cid=self.cid, title=self.title, module=self.module, tool=self.tool, brief=self.brief,
                 data_desc=self.data_desc, items=self.items)
        json.dump(d, open(os.path.join(OUT, self.cid + ".json"), "w"), indent=1, default=str)
        print(f"saved {self.cid}: {len([i for i in self.items if not i['hidden']])} questions, {self.nimg} charts,"
              f" errors={sum(1 for i in self.items if i['err'])}")
