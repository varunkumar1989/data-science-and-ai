"""Diagram helpers for lesson figures (matplotlib only). Every function draws onto a new figure and returns it."""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle

INK, VIO, CORAL, TEAL, GOLD, SKY, ROSE, LIME = "#17142E", "#6C4CF5", "#FF7A59", "#12B5A6", "#E9A23B", "#3B82F6", "#E04F8A", "#5A8F29"
PAL = [VIO, CORAL, TEAL, GOLD, SKY, ROSE, LIME, "#8C8C8C"]
SOFT = {VIO: "#EEE9FF", CORAL: "#FFEDE6", TEAL: "#E2F7F4", GOLD: "#FCF1DC", SKY: "#E3EEFE", ROSE: "#FCE6EF", LIME: "#EAF3E0", "#8C8C8C": "#F0F0F0"}


def style():
    plt.rcParams.update({"figure.dpi": 110, "savefig.dpi": 120, "font.family": "Inter", "font.size": 10.5, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlesize": 12.5, "axes.titlepad": 10,
                         "axes.prop_cycle": matplotlib.cycler(color=PAL), "axes.edgecolor": "#B9B4CC", "axes.labelcolor": "#3A3650",
                         "xtick.color": "#4A4660", "ytick.color": "#4A4660", "axes.grid": True, "grid.color": "#ECE9F4", "grid.linewidth": .8,
                         "axes.axisbelow": True, "figure.figsize": (8, 4.2), "legend.frameon": False, "figure.facecolor": "white"})


style()


def _canvas(w, h, title=None):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, w); ax.set_ylim(0, h); ax.axis("off")
    if title:
        ax.text(w / 2, h - .3, title, ha="center", va="center", fontsize=13, weight="bold", color=INK)
    return fig, ax


def _box(ax, x, y, w, h, text, color=VIO, sub=None, fs=10.5, filled=False, wrap=None):
    fc = color if filled else SOFT.get(color, "#F4F2FB")
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=color, lw=1.6))
    tc = "white" if filled else INK
    t = "\n".join(textwrap.wrap(text, wrap)) if wrap else text
    if sub:
        ax.text(x + w / 2, y + h * .64, t, ha="center", va="center", fontsize=fs, weight="bold", color=tc)
        ax.text(x + w / 2, y + h * .3, "\n".join(textwrap.wrap(sub, max(12, int(w * 6.2)))), ha="center", va="center", fontsize=fs - 2, color=tc if filled else "#4A4660")
    else:
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=fs, weight="bold", color=tc)


def _arrow(ax, x1, y1, x2, y2, color="#8D88A6", text=None, style="-|>", lw=1.6, rad=0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14, color=color, lw=lw, connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + .14, text, ha="center", va="bottom", fontsize=8.5, color="#4A4660")


def flow(steps, title=None, subs=None, colors=None, w=None):
    """Left-to-right process: steps = ['Collect', 'Clean', ...]."""
    n = len(steps); bw, gap = 1.75, .45
    W = w or max(6, n * bw + (n - 1) * gap + .6); H = 2.3 if subs else 1.8
    fig, ax = _canvas(W, H + (.5 if title else 0), title)
    x0 = (W - (n * bw + (n - 1) * gap)) / 2
    for i, s in enumerate(steps):
        c = (colors or PAL)[i % len(colors or PAL)]
        x = x0 + i * (bw + gap)
        _box(ax, x, .3, bw, H - .55, s, c, sub=(subs[i] if subs else None), wrap=16)
        if i < n - 1:
            _arrow(ax, x + bw + .04, .3 + (H - .55) / 2, x + bw + gap - .04, .3 + (H - .55) / 2)
    return fig


def vflow(steps, title=None, subs=None, colors=None, width=5.2):
    n = len(steps); bh, gap = .78, .32
    H = n * bh + (n - 1) * gap + .5 + (.5 if title else 0)
    fig, ax = _canvas(width, H, title)
    y = H - (.75 if title else .25) - bh
    for i, s in enumerate(steps):
        c = (colors or PAL)[i % len(colors or PAL)]
        _box(ax, .4, y, width - .8, bh, s, c, sub=(subs[i] if subs else None), fs=10.5)
        if i < n - 1:
            _arrow(ax, width / 2, y - .02, width / 2, y - gap + .02)
        y -= bh + gap
    return fig


def cycle(steps, title=None, center=None, r=1.65):
    import math
    n = len(steps); W, H = 6.4, 4.9
    fig, ax = _canvas(W, H, title)
    cx, cy = W / 2, H / 2 - .2
    pts = [(cx + r * math.cos(math.pi / 2 - 2 * math.pi * i / n), cy + r * math.sin(math.pi / 2 - 2 * math.pi * i / n)) for i in range(n)]
    for i, (x, y) in enumerate(pts):
        x2, y2 = pts[(i + 1) % n]
        _arrow(ax, x + (x2 - x) * .28, y + (y2 - y) * .28, x + (x2 - x) * .72, y + (y2 - y) * .72, rad=-.15)
    for i, (x, y) in enumerate(pts):
        c = PAL[i % len(PAL)]
        _box(ax, x - .78, y - .3, 1.56, .6, steps[i], c, fs=9.5, wrap=16)
    if center:
        ax.add_patch(Circle((cx, cy), .62, fc=INK, ec=INK)); ax.text(cx, cy, "\n".join(textwrap.wrap(center, 10)), ha="center", va="center", color="white", fontsize=9.5, weight="bold")
    return fig


def cards(items, title=None, cols=3, colors=None, cw=2.5, ch=1.25):
    """items = [(title, description), ...] laid out in a grid."""
    import math
    rows = math.ceil(len(items) / cols); gap = .25
    W = cols * cw + (cols - 1) * gap + .5; H = rows * ch + (rows - 1) * gap + .45 + (.5 if title else 0)
    fig, ax = _canvas(W, H, title)
    for i, (t, d) in enumerate(items):
        r, c = divmod(i, cols); x = .25 + c * (cw + gap); y = H - (.7 if title else .2) - (r + 1) * ch - r * gap
        col = (colors or PAL)[i % len(colors or PAL)]
        ax.add_patch(FancyBboxPatch((x, y), cw, ch, boxstyle="round,pad=0.02,rounding_size=0.1", fc="white", ec="#E3DFF0", lw=1.2))
        ax.add_patch(Rectangle((x, y + ch - .09), cw, .09, fc=col, ec=col))
        ax.text(x + .14, y + ch - .3, t, fontsize=10.5, weight="bold", color=INK, va="center")
        ax.text(x + .14, y + ch - .52, "\n".join(textwrap.wrap(d, int(cw * 11.5))), fontsize=8.6, color="#4A4660", va="top", linespacing=1.35)
    return fig


def layers(items, title=None, width=7.5):
    """Stack of layers top -> bottom: items = [(name, description)]."""
    n = len(items); bh, gap = .7, .12
    H = n * (bh + gap) + .3 + (.5 if title else 0)
    fig, ax = _canvas(width, H, title)
    y = H - (.7 if title else .2) - bh
    for i, (name, desc) in enumerate(items):
        c = PAL[i % len(PAL)]
        ax.add_patch(FancyBboxPatch((.3, y), width - .6, bh, boxstyle="round,pad=0.01,rounding_size=0.08", fc=SOFT.get(c), ec=c, lw=1.4))
        ax.add_patch(FancyBboxPatch((.3, y), 1.9, bh, boxstyle="round,pad=0.01,rounding_size=0.08", fc=c, ec=c))
        ax.text(1.25, y + bh / 2, name, ha="center", va="center", color="white", weight="bold", fontsize=10)
        ax.text(2.4, y + bh / 2, desc, va="center", fontsize=9.6, color=INK)
        y -= bh + gap
    return fig


def compare(lt, litems, rt, ritems, title=None, lc=VIO, rc=CORAL, width=8):
    n = max(len(litems), len(ritems)); rh = .42
    H = n * rh + 1.2 + (.5 if title else 0)
    fig, ax = _canvas(width, H, title)
    top = H - (.7 if title else .2)
    for k, (t, items, c) in enumerate([(lt, litems, lc), (rt, ritems, rc)]):
        x = .25 + k * (width / 2); w = width / 2 - .5
        ax.add_patch(FancyBboxPatch((x, .2), w, top - .2, boxstyle="round,pad=0.02,rounding_size=0.12", fc=SOFT.get(c, "#F4F2FB"), ec=c, lw=1.5))
        ax.add_patch(FancyBboxPatch((x, top - .55), w, .55, boxstyle="round,pad=0.02,rounding_size=0.12", fc=c, ec=c))
        ax.text(x + w / 2, top - .28, t, ha="center", va="center", color="white", weight="bold", fontsize=11)
        for i, it in enumerate(items):
            ax.text(x + .2, top - .85 - i * rh, "• " + it, va="center", fontsize=9.4, color=INK)
    return fig


def tree(root, children, title=None, width=8.5):
    """children = {'A': ['a1','a2'], 'B': [...]} -> root at top, groups, leaves."""
    groups = list(children); n = len(groups); leaves = max(len(v) for v in children.values())
    H = 1.6 + leaves * .48 + .4 + (.5 if title else 0)
    fig, ax = _canvas(width, H, title)
    top = H - (.7 if title else .25)
    _box(ax, width / 2 - 1.2, top - .6, 2.4, .6, root, INK, filled=True)
    gw = (width - .4) / n
    for i, g in enumerate(groups):
        c = PAL[i % len(PAL)]; gx = .2 + i * gw + gw / 2
        _arrow(ax, width / 2, top - .62, gx, top - 1.12, style="-")
        _box(ax, gx - gw / 2 + .08, top - 1.62, gw - .16, .5, g, c, filled=True, fs=9.5, wrap=18)
        for j, leaf in enumerate(children[g]):
            ax.text(gx, top - 1.95 - j * .45, leaf, ha="center", va="center", fontsize=8.8, color=INK,
                    bbox=dict(boxstyle="round,pad=0.25", fc=SOFT.get(c), ec="none"))
    return fig


def join_venn(kind, title=None):
    """SQL join illustration: inner, left, right, full, left_anti, cross."""
    fig = plt.figure(figsize=(2.6, 2.0)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 2.6); ax.set_ylim(0, 2.0); ax.axis("off"); ax.set_aspect("equal")
    import numpy as np
    xs = np.linspace(0, 2.6, 400); ys = np.linspace(0, 2.0, 300); X, Y = np.meshgrid(xs, ys)
    a = (X - 1.0) ** 2 + (Y - 1.0) ** 2 < .62 ** 2; b = (X - 1.6) ** 2 + (Y - 1.0) ** 2 < .62 ** 2
    m = {"inner": a & b, "left": a, "right": b, "full": a | b, "left_anti": a & ~b, "right_anti": b & ~a, "full_anti": a ^ b}[kind]
    ax.imshow(np.where(m, 1, np.nan), extent=(0, 2.6, 0, 2.0), origin="lower", cmap=matplotlib.colors.ListedColormap([VIO]), alpha=.75)
    for cx, lab in [(1.0, "A"), (1.6, "B")]:
        ax.add_patch(Circle((cx, 1.0), .62, fill=False, ec=INK, lw=1.4)); ax.text(cx + (-.3 if lab == "A" else .3), 1.0, lab, ha="center", va="center", weight="bold", color=INK)
    if title: ax.text(1.3, .15, title, ha="center", fontsize=10, weight="bold", color=INK)
    return fig


def joins_panel(kinds=("inner", "left", "right", "full", "left_anti"), labels=None, title=None):
    import numpy as np
    n = len(kinds); fig, axs = plt.subplots(1, n, figsize=(2.15 * n, 2.3))
    xs = np.linspace(0, 2.6, 300); ys = np.linspace(0, 2.0, 220); X, Y = np.meshgrid(xs, ys)
    a = (X - 1.0) ** 2 + (Y - 1.05) ** 2 < .6 ** 2; b = (X - 1.6) ** 2 + (Y - 1.05) ** 2 < .6 ** 2
    for i, k in enumerate(kinds):
        ax = axs[i]; ax.axis("off"); ax.set_aspect("equal"); ax.set_xlim(0, 2.6); ax.set_ylim(0, 2.0)
        m = {"inner": a & b, "left": a, "right": b, "full": a | b, "left_anti": a & ~b, "right_anti": b & ~a, "full_anti": a ^ b}[k]
        ax.imshow(np.where(m, 1, np.nan), extent=(0, 2.6, 0, 2.0), origin="lower", cmap=matplotlib.colors.ListedColormap([VIO]), alpha=.75)
        for cx, lab in [(1.0, "A"), (1.6, "B")]:
            ax.add_patch(Circle((cx, 1.05), .6, fill=False, ec=INK, lw=1.3)); ax.text(cx + (-.3 if lab == "A" else .3), 1.05, lab, ha="center", va="center", weight="bold", color=INK)
        ax.set_title((labels or kinds)[i], fontsize=10.5, color=INK)
    if title: fig.suptitle(title, weight="bold")
    fig.tight_layout()
    return fig


def er(tables, rels, title=None, width=9, height=4.6):
    """tables = {name: (x, y, [cols])}; mark PK with '*', FK with '#'. rels = [(t1, t2, '1 : N')]."""
    fig, ax = _canvas(width, height, title)
    geo = {}
    for i, (name, (x, y, cols)) in enumerate(tables.items()):
        c = PAL[i % len(PAL)]; w = 2.15; rh = .3; h = .42 + rh * len(cols)
        ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.01,rounding_size=0.06", fc="white", ec=c, lw=1.5))
        ax.add_patch(FancyBboxPatch((x, y - .42), w, .42, boxstyle="round,pad=0.01,rounding_size=0.06", fc=c, ec=c))
        ax.text(x + w / 2, y - .21, name, ha="center", va="center", color="white", weight="bold", fontsize=10)
        for j, col in enumerate(cols):
            tag = "PK" if col.endswith("*") else ("FK" if col.endswith("#") else "")
            ax.text(x + .12, y - .42 - rh * (j + .5), col.rstrip("*#"), va="center", fontsize=8.8, color=INK, weight="bold" if tag == "PK" else "normal")
            if tag: ax.text(x + w - .12, y - .42 - rh * (j + .5), tag, va="center", ha="right", fontsize=7.5, color=c, weight="bold")
        geo[name] = (x, y - h, w, h)
    for t1, t2, lab in rels:
        x1, y1, w1, h1 = geo[t1]; x2, y2, w2, h2 = geo[t2]
        p1 = (x1 + w1, y1 + h1 / 2) if x1 < x2 else (x1, y1 + h1 / 2); p2 = (x2, y2 + h2 / 2) if x1 < x2 else (x2 + w2, y2 + h2 / 2)
        if abs(x1 - x2) < .5: p1 = (x1 + w1 / 2, y1); p2 = (x2 + w2 / 2, y2 + h2) if y2 < y1 else (x2 + w2 / 2, y2)
        _arrow(ax, *p1, *p2, color="#6E6886", style="-", text=lab)
    return fig


def matrix2(xlab, ylab, quads, title=None):
    """2x2 matrix. quads = [top-left, top-right, bottom-left, bottom-right] as (title, desc)."""
    fig, ax = _canvas(6.6, 5.0, title)
    cols = [GOLD, TEAL, CORAL, VIO]
    pos = [(.9, 2.35), (3.7, 2.35), (.9, .55), (3.7, .55)]
    for (x, y), (t, d), c in zip(pos, quads, cols):
        ax.add_patch(FancyBboxPatch((x, y), 2.6, 1.6, boxstyle="round,pad=0.02,rounding_size=0.1", fc=SOFT[c], ec=c, lw=1.5))
        ax.text(x + 1.3, y + 1.2, t, ha="center", weight="bold", fontsize=11, color=INK)
        ax.text(x + 1.3, y + .75, "\n".join(textwrap.wrap(d, 30)), ha="center", va="top", fontsize=8.8, color="#4A4660")
    _arrow(ax, .6, .4, 6.45, .4, color=INK); _arrow(ax, .6, .4, .6, 4.15, color=INK)
    ax.text(3.6, .12, xlab, ha="center", fontsize=9.5, color=INK, weight="bold"); ax.text(.3, 2.3, ylab, rotation=90, va="center", fontsize=9.5, color=INK, weight="bold")
    return fig


def kpi_cards(items, title=None):
    """Power BI style KPI cards: items = [(label, value, delta_text, good_bool)]."""
    n = len(items); W = n * 2.3 + .3
    fig, ax = _canvas(W, 1.65 + (.45 if title else 0), title)
    for i, (lab, val, delta, good) in enumerate(items):
        x = .2 + i * 2.3
        ax.add_patch(FancyBboxPatch((x, .15), 2.1, 1.3, boxstyle="round,pad=0.02,rounding_size=0.1", fc="white", ec="#E3DFF0", lw=1.2))
        ax.text(x + .15, 1.18, lab, fontsize=9, color="#5F5A78")
        ax.text(x + .15, .72, val, fontsize=17, weight="bold", color=INK, va="center")
        if delta: ax.text(x + .15, .35, delta, fontsize=8.8, color=(TEAL if good else CORAL), weight="bold", va="center")
    return fig


def window(title_text, rows, title=None, width=8.2, accent=VIO):
    """Generic app-window mock: rows = list of (label, value) lines shown as a settings/pane screenshot."""
    H = .9 + len(rows) * .42 + (.45 if title else 0)
    fig, ax = _canvas(width, H, title)
    top = H - (.6 if title else .15)
    ax.add_patch(FancyBboxPatch((.15, .1), width - .3, top - .1, boxstyle="round,pad=0.01,rounding_size=0.08", fc="white", ec="#CFCADF", lw=1.2))
    ax.add_patch(FancyBboxPatch((.15, top - .45), width - .3, .45, boxstyle="round,pad=0.01,rounding_size=0.08", fc=accent, ec=accent))
    for k, c in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]): ax.add_patch(Circle((.42 + k * .22, top - .225), .065, fc=c, ec="none"))
    ax.text(width / 2, top - .225, title_text, ha="center", va="center", color="white", weight="bold", fontsize=10)
    for i, (a, b) in enumerate(rows):
        y = top - .75 - i * .42
        ax.text(.45, y, a, va="center", fontsize=9.4, color=INK, weight="bold")
        ax.text(3.0, y, b, va="center", fontsize=9.2, color="#4A4660")
    return fig
