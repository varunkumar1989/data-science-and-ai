"""Reusable 'screenshot-style' illustrations drawn with matplotlib (Excel window, Power BI canvas, SSMS, Jupyter...)."""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
import dg

def _ann(ax, xy, xytext, text, color="#FF7A59"):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=9.5, weight="bold", color=color, ha="center",
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5), bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.2))

def excel_window():
    fig = plt.figure(figsize=(10, 6.2)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 10); ax.set_ylim(0, 6.2); ax.axis("off")
    G = "#1E7145"
    ax.add_patch(Rectangle((0.6, 0.5), 8.8, 5.2, fc="white", ec="#9AA5A0", lw=1.2))
    ax.add_patch(Rectangle((0.6, 5.35), 8.8, .35, fc=G, ec=G)); ax.text(5, 5.52, "Sales_2026.xlsx  -  Excel", color="white", ha="center", va="center", fontsize=9.5, weight="bold")
    tabs = ["File", "Home", "Insert", "Page Layout", "Formulas", "Data", "Review", "View"]
    for i, t in enumerate(tabs): ax.text(0.8 + i * .78, 5.2, t, fontsize=8.2, color=G if t == "Home" else "#333", weight="bold" if t == "Home" else "normal", va="center")
    ax.add_patch(Rectangle((0.6, 4.55), 8.8, .5, fc="#F3F3F3", ec="#DADADA"))
    for i, g in enumerate(["Clipboard", "Font", "Alignment", "Number", "Styles", "Cells", "Editing"]):
        ax.add_patch(FancyBboxPatch((0.75 + i * 1.24, 4.62), 1.1, .36, boxstyle="round,pad=0.01,rounding_size=0.04", fc="white", ec="#D0D0D0")); ax.text(1.3 + i * 1.24, 4.8, g, fontsize=7.4, ha="center", va="center", color="#444")
    ax.add_patch(Rectangle((0.6, 4.18), 1.1, .3, fc="white", ec="#BDBDBD")); ax.text(1.15, 4.33, "C4", fontsize=9, ha="center", va="center")
    ax.text(1.95, 4.33, "fx", fontsize=9, style="italic", va="center", color="#666")
    ax.add_patch(Rectangle((2.2, 4.18), 7.2, .3, fc="white", ec="#BDBDBD")); ax.text(2.3, 4.33, "=B4*12", fontsize=9, va="center", family="DejaVu Sans Mono")
    cols = "ABCDEFG"; cw = 1.12; x0 = 1.0; y0 = 3.95; rh = .36
    for j, c in enumerate(cols):
        ax.add_patch(Rectangle((x0 + j * cw, y0), cw, .22, fc="#EFEFEF" if c != "C" else "#D6EADF", ec="#CFCFCF")); ax.text(x0 + j * cw + cw / 2, y0 + .11, c, fontsize=8, ha="center", va="center", color="#444")
    data = [["Month", "Monthly", "Yearly"], ["Apr", 1200, ""], ["May", 1350, ""], ["Jun", 1500, 18000], ["Jul", 1420, ""], ["Aug", 1610, ""], ["", "", ""], ["", "", ""]]
    for i in range(8):
        y = y0 - (i + 1) * rh
        ax.add_patch(Rectangle((0.6, y), .4, rh, fc="#EFEFEF" if i != 3 else "#D6EADF", ec="#CFCFCF")); ax.text(.8, y + rh / 2, str(i + 1), fontsize=8, ha="center", va="center", color="#444")
        for j in range(7):
            sel = (i == 3 and j == 2)
            ax.add_patch(Rectangle((x0 + j * cw, y), cw, rh, fc="white", ec="#1E7145" if sel else "#E3E3E3", lw=2.2 if sel else .6))
            if j < 3 and data[i][j] != "": ax.text(x0 + j * cw + (cw - .08 if isinstance(data[i][j], int) else .08), y + rh / 2, f"{data[i][j]:,}" if isinstance(data[i][j], int) else data[i][j], fontsize=8.6, va="center", ha="right" if isinstance(data[i][j], int) else "left", weight="bold" if i == 0 else "normal")
    ax.add_patch(Rectangle((0.6, .5), 8.8, .3, fc="#F3F3F3", ec="#DADADA"))
    for k, s in enumerate(["Sales", "Targets", "Sheet3", "+"]):
        ax.add_patch(Rectangle((0.8 + k * .95, .53), .88, .24, fc="white" if k == 0 else "#F3F3F3", ec="#CFCFCF")); ax.text(1.24 + k * .95, .65, s, fontsize=8, ha="center", va="center", color=G if k == 0 else "#555", weight="bold" if k == 0 else "normal")
    ax.text(7.6, .65, "Average: 1,416   Count: 5   Sum: 7,080", fontsize=7.6, va="center", color="#555")
    _ann(ax, (5.2, 5.2), (6.9, 5.95), "Ribbon tabs", dg.VIO)
    ax.annotate("Name Box\n(active cell)", xy=(1.0, 4.2), xytext=(0.35, 2.4), fontsize=9, weight="bold", color=dg.CORAL, ha="center", arrowprops=dict(arrowstyle="-|>", color=dg.CORAL, lw=1.5), bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=dg.CORAL))
    _ann(ax, (4.5, 4.33), (5.6, 3.45 - .0), "Formula bar", dg.TEAL)
    _ann(ax, (3.8, 2.65), (6.9, 2.3), "Active cell C4", dg.GOLD)
    _ann(ax, (1.25, .65), (2.9, 1.25), "Sheet tabs", dg.SKY)
    _ann(ax, (8.4, .65), (8.4, 1.5), "Status bar quick stats", dg.ROSE)
    _ann(ax, (2.25, 4.05), (3.4, 5.95), "Column header", dg.LIME)
    return fig
