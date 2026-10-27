---
num: 3
title: Number, Custom & Conditional Formatting
live: "Live class 2"
updated: "Excel for Microsoft 365, 2026"
level: Beginner
duration: 100 min
summary: Make numbers readable and insights jump out. Learn cell and number formats, write your own custom number formats (including lakhs and crores, K and M, and colour codes), and use conditional formatting with built-in rules and your own formulas.
datasets: [superstore_sales.csv, employees_small.csv]
outcomes:
  - Apply cell formatting (fonts, alignment, borders, wrap, merge alternatives) the professional way
  - Choose the right built-in number format and know that formatting never changes the stored value
  - Write custom number formats with sections, conditions, colours, text and scaling
  - Highlight insights with conditional formatting: rules, Top/Bottom, data bars, colour scales and icon sets
  - Write custom-formula conditional formatting, such as highlighting whole rows
---

## Formatting changes how a value looks, not what it is

This is the most important idea in this lesson. When you format `0.256` as `26%`, the cell still contains `0.256`. Every formula that uses the cell sees `0.256`.

```xl title="Same stored value, different formats"
Stored value{h}|Format applied{h}|What you see{h}
0.256|Percentage, 0 decimals|=TEXT(A2,"0%")
0.256|Percentage, 1 decimal|=TEXT(A3,"0.0%")
1234567.891|Number with separator|=TEXT(A4,"#,##0.00")
46139|Date|=TEXT(A5,"dd-mmm-yyyy")
46139|Long date|=TEXT(A6,"dddd, d mmmm yyyy")
0.6875|Time|=TEXT(A7,"hh:mm")
```

Column C uses the `TEXT` function to show exactly what each format produces. (`TEXT` returns text, so use it for labels, not for numbers you still need to calculate with.)

:::warn Rounding by format vs rounding by formula
Formatting `2.456` with 1 decimal *shows* `2.5` but keeps `2.456`. Adding three such cells can show `7.4` while the visible numbers add up to `7.5`. If the rounded value must be used in calculations (invoices, tax), round it with a formula: `=ROUND(A2,1)`.
:::

## Cell formatting the professional way

Open **Format Cells** with `Ctrl + 1`. It has six tabs: Number, Alignment, Font, Border, Fill, Protection.

| Goal | How |
|---|---|
| Bold header with fill colour | Home → Bold (`Ctrl + B`) and Fill Color, or Cell Styles → Heading |
| Wrap long text | Home → Wrap Text (`Alt + H, W`) |
| Centre a title across columns **without merging** | `Ctrl + 1` → Alignment → Horizontal: **Center Across Selection** |
| Rotate header text | Alignment → Orientation |
| Thin borders around a table | Home → Borders → All Borders |
| Copy formatting | Format Painter (double-click it to paint many places) |
| Clear only formatting | Home → Clear → Clear Formats |
| Consistent look across a workbook | Page Layout → Themes, and Cell Styles |

:::mistake Avoid merged cells
Merged cells break sorting, filtering, copying, selecting columns and pivot tables. Use **Center Across Selection** instead: it looks the same and keeps every cell independent.
:::

## Built-in number formats

| Format | Example display of 1234.5 | Use for |
|---|---|---|
| General | 1234.5 | Default, no fixed format |
| Number | 1,234.50 | Quantities, amounts |
| Currency | ₹1,234.50 | Money, symbol next to the number |
| Accounting | ₹ 1,234.50 | Money in financial statements: symbol aligned at the left edge, zero shown as a dash |
| Percentage | 123450% | Rates; type `12%` or format `0.12` |
| Fraction | 1234 1/2 | Measurements |
| Scientific | 1.23E+03 | Very large or small numbers |
| Text | 1234.5 (as text) | IDs, codes, phone numbers |
| Date / Time | Various | Dates and times (stored as serial numbers) |

Shortcuts: `Ctrl + Shift + 1` number with 2 decimals, `Ctrl + Shift + 4` currency, `Ctrl + Shift + 5` percentage, `Ctrl + Shift + 3` date.

## Custom number formats

`Ctrl + 1` → Number → **Custom** lets you write your own format code. Once you understand the structure, you can make dashboards that are much easier to read.

### The four sections

A format code can have up to four parts, separated by semicolons:

```text
POSITIVE ; NEGATIVE ; ZERO ; TEXT
#,##0    ; [Red]-#,##0 ; "–" ; @
```

```python fig: A custom number format has up to four sections separated by semicolons.
dg.flow(["Positive numbers", "Negative numbers", "Zero", "Text"], subs=["#,##0", "[Red](#,##0)", '"–"', '@" (check)"'], title="POSITIVE ; NEGATIVE ; ZERO ; TEXT")
```

### Placeholder characters

| Code | Meaning | Value 7.5 → |
|---|---|---|
| `0` | Digit, shows a zero if none | `000.00` → 007.50 |
| `#` | Digit, shows nothing if none | `#.##` → 7.5 |
| `?` | Digit, shows a space (aligns decimals) | `?.??` → 7.5␣ |
| `,` (in the middle) | Thousands separator | `#,##0` |
| `,` (at the end) | Divide by 1,000 for each comma | `#,##0,` shows 12,500 as 13 |
| `%` | Multiply by 100 and add % | `0%` |
| `"text"` | Show literal text | `0" units"` |
| `@` | The cell's text | `"Dept: "@` |
| `[Red]`, `[Blue]`, `[Color10]` | Colour | `[Red]-0` |
| `[>=1000]` | Condition | `[>=1000]#,##0,"K";0` |

### Custom formats you will reuse

Each result in column C was produced by Excel's `TEXT` function with the format code in column B.

```xl title="Custom format cookbook"
Value{h}|Format code{h}|Result{h}
12500|'#,##0|=TEXT(A2,B2)
12500|#,##0,"K"|=TEXT(A3,B3)
12500|#,##0.0,"K"|=TEXT(A4,B4)
8450000|#,##0.0,,"M"|=TEXT(A5,B5)
-3200|#,##0;(#,##0)|=TEXT(A6,B6)
0|#,##0;-#,##0;"–"|=TEXT(A7,B7)
45|0" units"|=TEXT(A8,B8)
0.0725|'0.0%|=TEXT(A9,B9)
7|'000|=TEXT(A10,B10)
9876543210|00000 00000|=TEXT(A11,B11)
1500|[>=1000]#,##0.0,"K";0|=TEXT(A12,B12)
850|[>=1000]#,##0.0,"K";0|=TEXT(A13,B13)
0.25|▲ 0%;▼ 0%|=TEXT(A14,B14)
-0.12|▲ 0%;▼ 0%|=TEXT(A15,B15)
```

:::tip Up and down arrows in KPIs
`▲ 0%;▼ 0%` (add `[Color10]` for green and `[Red]` for red: `[Color10]▲ 0%;[Red]▼ 0%`) is the classic format for "change versus last month" cells in dashboards. The arrow and colour change automatically with the sign.
:::

### Indian number format: lakhs and crores

Indian reports group digits as 12,34,56,789 (crore, lakh, thousand). If your Windows region is set to English (India), the standard `#,##0` already groups this way. Otherwise use a conditional format:

```text
[>=10000000]##\,##\,##\,##0;[>=100000]##\,##\,##0;##,##0
```

```xl title="Lakhs and crores"
Value{h}|Indian grouping{h}|In lakhs{h}|In crores{h}
1234567|12,34,567|=TEXT(A2/100000,"0.00")&" L"|=TEXT(A2/10000000,"0.00")&" Cr"
98765432|9,87,65,432|=TEXT(A3/100000,"0.00")&" L"|=TEXT(A3/10000000,"0.00")&" Cr"
450000|4,50,000|=TEXT(A4/100000,"0.00")&" L"|=TEXT(A4/10000000,"0.00")&" Cr"
```

There is no "divide by 1 lakh" comma trick in Excel (each trailing comma divides by 1,000), so for lakhs either divide in a helper column (as above) or use Power BI's display units.

### Date and time format codes

| Code | Shows (for 27-04-2026 14:05) |
|---|---|
| `d`, `dd` | 27 |
| `ddd`, `dddd` | Mon, Monday |
| `m`, `mm` | 4, 04 |
| `mmm`, `mmmm` | Apr, April |
| `yy`, `yyyy` | 26, 2026 |
| `hh:mm` | 14:05 |
| `hh:mm AM/PM` | 02:05 PM |
| `[h]:mm` | Total hours beyond 24, for timesheets (e.g. 37:30) |
| `"Q"` with a formula | Quarter labels need a formula: `="Q"&ROUNDUP(MONTH(A2)/3,0)` |

## Conditional formatting: let insights jump out

**Home → Conditional Formatting** changes a cell's look based on its value. It is how you turn a wall of numbers into something a manager understands in five seconds.

```python fig: The five families of conditional formatting rules.
dg.cards([("Highlight Cells Rules", "Greater than, less than, between, equal to, text that contains, a date occurring, duplicate values"),
          ("Top/Bottom Rules", "Top 10 items or %, bottom 10, above or below average"),
          ("Data Bars", "A bar inside the cell, length proportional to the value"),
          ("Color Scales", "Two- or three-colour gradients (heat maps)"),
          ("Icon Sets", "Arrows, traffic lights, flags or ratings by thresholds"),
          ("New Rule → Use a formula", "Any TRUE/FALSE formula, e.g. highlight a whole row")], cols=3, title="Conditional formatting rule types")
```

### Highlight rules and Top/Bottom

In the table below, green marks sales **above 1,50,000** and red marks **profit below 0** (both "Highlight Cells Rules"):

```xl title="Highlight rules: sales > 1,50,000 (green), profit < 0 (red)"
Region{h}|Category{h}|Sales{h}|Profit{h}
North|Furniture|128400{;#,##0}|-3250{r;#,##0}
North|Technology|212950{g;#,##0}|28400{;#,##0}
South|Office Supplies|96300{;#,##0}|14820{;#,##0}
South|Technology|187200{g;#,##0}|19950{;#,##0}
East|Furniture|74100{;#,##0}|-8900{r;#,##0}
West|Technology|158700{g;#,##0}|22310{;#,##0}
```

### Data bars, colour scales and icon sets

These visual rules are best seen on real data. Here they are applied to monthly sales from the Superstore dataset:

```python fig: Data bars (left), a green–yellow–red colour scale (middle) and icon sets (right) applied to the same monthly sales.
import pandas as pd, numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
m = s[s.order_date.dt.year == 2025].groupby(s.order_date.dt.month)["sales"].sum() / 100000
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
fig, axs = plt.subplots(1, 3, figsize=(11, 4.6))
cmap = plt.get_cmap("RdYlGn")
lo, hi = m.min(), m.max()
for k, ax in enumerate(axs):
    ax.set_xlim(0, 3.2); ax.set_ylim(0, 13); ax.axis("off")
    ax.set_title(["Data bars", "Colour scale", "Icon set (3 arrows)"][k], fontsize=11)
    for i, (mo, v) in enumerate(zip(months, m.values)):
        y = 12 - i
        ax.add_patch(Rectangle((0, y - .5), 1, 1, fc="#F2F2F2", ec="#D9D9D9")); ax.text(.5, y, mo, ha="center", va="center", fontsize=9)
        fc = "white" if k != 1 else cmap((v - lo) / (hi - lo))
        ax.add_patch(Rectangle((1, y - .5), 2.2, 1, fc=fc, ec="#D9D9D9"))
        if k == 0: ax.add_patch(Rectangle((1.03, y - .38), 2.1 * v / hi, .76, fc="#6C9BD2", ec="none", alpha=.85))
        if k == 2:
            p = (v - lo) / (hi - lo); sym, col = ("▲", "#1E8E5A") if p > 2/3 else (("►", "#E9A23B") if p > 1/3 else ("▼", "#C0392B"))
            ax.text(1.2, y, sym, color=col, fontsize=11, va="center", family="DejaVu Sans")
        ax.text(3.1, y, f"{v:,.1f} L", ha="right", va="center", fontsize=9)
fig
```

| Rule | When to use | Watch out |
|---|---|---|
| **Data bars** | Compare magnitudes inside a table | Negative values draw leftwards; set a fixed minimum of 0 if needed |
| **Colour scales** | Heat maps: sales by region × month, attendance grids | Red/green is hard for colour-blind readers; consider blue–white–orange |
| **Icon sets** | Status at a glance: on track, at risk, off track | Default thresholds are percentages of the range (67% / 33%); set them to numbers or percentiles that match your business targets |

Under **Manage Rules → Edit Rule** you can change thresholds, choose "Show Bar Only" or "Show Icon Only", and reverse the icon order.

## Custom formula conditional formatting

**New Rule → Use a formula to determine which cells to format** is the most powerful option. Write a formula for the **top-left cell** of your selection that returns TRUE for cells you want formatted. Dollar signs matter:

- `$` before the column (`$D2`) locks the rule to column D, so **every cell in the row** checks column D → the whole row is highlighted.
- No `$` before the row number lets the row change as Excel moves down the selection.

```xl title="Highlight whole rows where Department = Finance AND Salary > 1,00,000 — rule: =AND($C2=&quot;Finance&quot;,$F2>100000)"
Emp ID{h}|Name{h}|Department{h}|City{h}|Join date{h}|Salary{h}|Rating{h}
E101|Kavya Iyer|HR|Mumbai|2016-02-28|97000{;#,##0}|4
E102{y}|Imran Reddy{y}|Finance{y}|Delhi{y}|2019-12-14{y}|157000{y;#,##0}|3{y}
E103{y}|Harpreet Kulkarni{y}|Finance{y}|Mumbai{y}|2024-10-05{y}|131000{y;#,##0}|4{y}
E104|Diya Iyer|HR|Bengaluru|2024-01-02|90000{;#,##0}|4
E110|Vikram Joshi|Finance|Chennai|2022-10-19|75000{;#,##0}|5
E119|Rohan Das|Finance|Delhi|2018-07-19|97000{;#,##0}|5
```

Rows E102 and E103 meet both conditions. E110 and E119 are in Finance but earn less than 1,00,000, so they stay white.

### More custom-formula recipes

| Goal | Select | Formula |
|---|---|---|
| Zebra stripes (every other row) | the table | `=MOD(ROW(),2)=0` |
| Overdue tasks (due date before today, status not Done) | the table | `=AND($E2<TODAY(),$F2<>"Done")` |
| Values above the column average | `C2:C100` | `=C2>AVERAGE($C$2:$C$100)` |
| Duplicate IDs | `A2:A100` | `=COUNTIF($A$2:$A$100,A2)>1` |
| Weekend dates | `A2:A100` | `=WEEKDAY(A2,2)>5` |
| Row of the employee picked in a drop-down (H1) | the table | `=$B2=$H$1` |
| Missing values | the table | `=ISBLANK(A2)` or `=A2=""` |
| Top 3 per column | `C2:C100` | `=C2>=LARGE($C$2:$C$100,3)` |

:::steps Create a whole-row highlight
1. Select the data **without** the header (for example `A2:G21`). The active cell must be in row 2.
2. Home → Conditional Formatting → New Rule → **Use a formula to determine which cells to format**.
3. Formula: `=AND($C2="Finance",$F2>100000)`.
4. Click **Format…** → Fill → choose a colour → OK.
5. To edit later: Conditional Formatting → **Manage Rules** (choose "This Worksheet" to see all rules). Rules higher in the list win; tick **Stop If True** to prevent lower rules from also applying.
:::

:::mistake The three most common conditional-formatting bugs
1. **Wrong anchor**: writing the formula for row 1 while the selection starts at row 2 shifts every result by one row.
2. **Missing `$`**: `=C2="Finance"` (no `$`) checks a different column for each cell, so only part of the row lights up.
3. **Copying cells copies rules**: pasting formatted cells many times creates hundreds of duplicate rules and slows the workbook. Clean up in Manage Rules, or paste values only.
:::

## Formatting a report: before and after

A clean report follows a few simple rules:

1. **Right-align numbers**, left-align text, and use the same number of decimals in a column.
2. Use **thousands separators**; show large values in K/M or lakh/crore with clear labels.
3. **Bold** headers and totals only; avoid using many colours.
4. Use **one highlight colour** for "needs attention" and keep everything else neutral.
5. **Freeze** the header row; make the column widths fit the content.
6. Add a title, the date range and the data source.

:::ai Do it with AI
Ask an assistant: *"Write an Excel custom number format that shows values above 1 crore as '1.25 Cr', values above 1 lakh as '4.50 L', and smaller values with Indian comma grouping."* Then test the answer with `=TEXT(value, "format")` on a few numbers before applying it. (A pure format can only scale by thousands, so a good answer will suggest a helper column or Power BI for lakhs and crores.)
:::

## Summary

:::key
- Formatting changes the **display**, never the stored value. Round with `ROUND` when it matters.
- Avoid merged cells; use **Center Across Selection**.
- Custom formats have four sections, `positive;negative;zero;text`, and support colours, conditions, text and scaling with trailing commas.
- Conditional formatting families: highlight rules, Top/Bottom, data bars, colour scales and icon sets.
- For whole-row highlights use a formula with `$` before the column: `=$C2="Finance"`.
- Manage Rules shows priority; rule order and Stop If True decide which format wins.
:::

:::quiz
Q: A cell contains 0.4567 formatted as 0%. What value does `=A1*100` return?
- 46
* 45.67
- 0.46
- 46%
> The stored value is still 0.4567, so the formula returns 45.67. Formatting only changes the display.

Q: Which custom format shows 8,450,000 as 8.5M?
- `#,##0,"M"`
* `#,##0.0,,"M"`
- `0.0"M"`
- `#,##0.0%`
> Two trailing commas divide by 1,000,000, and 0.0 shows one decimal.

Q: In the format `#,##0;[Red](#,##0);"–"`, how is -2500 shown?
- -2,500 in black
* (2,500) in red
- –
- 2,500 in red
> The second section is for negative numbers: red, in brackets, without a minus sign.

Q: You want to highlight entire rows where Status (column F) is "Late". Rows start at 2. Which rule is correct?
- `=F2="Late"`
* `=$F2="Late"`
- `=$F$2="Late"`
- `=F$2="Late"`
> Locking the column with $ makes every cell in the row test column F; leaving the row free lets each row test itself.

Q: What does "Center Across Selection" replace?
- Wrap Text
* Merge & Center
- Format Painter
- Freeze Panes
> It centres text across several cells without merging them, so sorting and selecting still work.

Q: Which conditional formatting type is best for a sales heat map of region × month?
- Icon sets
- Data bars
* Colour scales
- Highlight duplicates
> Colour scales shade each cell by value, which creates a heat map.
:::

:::exercise Dashboard number formats
Write custom formats for: (a) revenue shown in thousands with "K" and no decimals; (b) month-on-month change shown as a green up arrow with one decimal percentage when positive, and a red down arrow when negative; (c) a 6-digit PIN code that must keep leading zeros.
???
(a) `#,##0,"K"`  (b) `[Color10]▲ 0.0%;[Red]▼ 0.0%;"–"`  (c) `000000` (or store the PIN as text).
:::

:::exercise Conditional formatting practice
Using `employees_small.csv`: (1) colour-scale the salary column; (2) add an icon set to rating with green for 5, amber for 3–4 and red for 1–2; (3) highlight the whole row of anyone who joined after 1-Jan-2024.
???
(1) Select F2:F21 → Color Scales → Green–Yellow–Red. (2) Select G2:G21 → Icon Sets → 3 traffic lights → Manage Rules → Edit: green when ≥ 5 (Number), amber when ≥ 3 (Number), otherwise red. (3) Select A2:G21 → New Rule → formula `=$E2>DATE(2024,1,1)` → choose a fill.
:::

:::interview Questions you may be asked
**Q: What is the difference between formatting a number and rounding it?**
Formatting changes only how the value looks; the full value is used in calculations. `ROUND` changes the stored value. Use `ROUND` when the rounded figure must flow into other calculations, such as invoices.

**Q: How would you highlight the top 10% of customers by revenue?**
Conditional Formatting → Top/Bottom Rules → Top 10% (change 10 to any value), or a formula rule `=C2>=PERCENTILE.INC($C$2:$C$500,0.9)` for more control.

**Q: Why might a conditional format highlight the wrong rows?**
The formula was written for a different starting row than the active cell of the selection, or the `$` signs are wrong.
:::
