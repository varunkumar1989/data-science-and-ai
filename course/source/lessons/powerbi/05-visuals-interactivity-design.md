---
num: 5
title: Visuals, Filters, Drill-through, Tooltips, Buttons & Report Design
live: "Power BI classes 2–4"
updated: "Power BI Desktop 2026"
level: Intermediate
duration: 150 min
summary: Turn a model into an interactive, well-designed report. Choose visuals, format them (cards, matrix, charts, gauge, KPI, maps, images), use visual, page and report filters, edit interactions, drill-down and drill-through, custom tooltips, bookmarks and buttons, conditional formatting, themes and design principles.
datasets: [adventure_cycles/fact_sales.csv, adventure_cycles/dim_product.csv, adventure_cycles/dim_territory.csv, adventure_cycles/dim_customer.csv]
outcomes:
  - Pick the right visual for each question and configure its field wells and formatting
  - Apply visual, page and report-level filters, Top N, relative date filters and slicer sync
  - Control cross-filtering with Edit interactions; add drill-down, drill-through and report-page tooltips
  - Build navigation with buttons, bookmarks, page navigation and a selection pane
  - Apply themes and conditional formatting, and follow layout, colour and accessibility rules
---

## Choosing the visual

```python fig: Match the visual to the question.
dg.cards([("Compare categories", "Clustered bar/column (ranked bars for long names)"), ("Trend over time", "Line, area, or column for few periods"),
          ("Part-to-whole", "Stacked bar, 100% stacked, treemap, donut (≤ 3 parts)"), ("Relationship", "Scatter or bubble (with a play axis for time)"),
          ("Single KPI", "Card, multi-row card, KPI, gauge"), ("Detail & totals", "Table, matrix (pivot) with conditional formatting"),
          ("Geography", "Map, filled map, shape map, Azure map"), ("Flow & contribution", "Waterfall, funnel, ribbon, decomposition tree"),
          ("Explain / AI", "Key influencers, Smart narrative, Q&A, anomaly detection, Copilot narrative")], cols=3, title="Visual chooser")
```

| Visual | Fields | Good for | Watch out |
|---|---|---|---|
| **Card** / multi-row card | Values | One or few headline numbers | Format display units (K, M, Cr) and add a clear label |
| **Clustered bar / column** | Axis, Values, Legend | Comparisons | Sort descending, start at zero, ≤ 15 bars |
| **Stacked / 100% stacked** | Axis, Legend, Values | Composition | Only the bottom segment is easy to compare |
| **Line / area** | X-axis (date), Y-axis, Legend | Trends | Limit to ~5 lines; use a continuous date axis |
| **Line + clustered column** | Shared axis, column values, line values | Two measures with different scales (secondary axis) | Label both axes |
| **Waterfall** | Category, Y-axis | Bridge from start to end (profit walk) | Needs an ordered category |
| **Scatter / bubble** | X, Y, Size, Details, Play axis | Relationships and outliers | Add Details so each point is an entity |
| **Treemap** | Group, Values | Hierarchical share of total | Many tiny rectangles are unreadable |
| **Donut / pie** | Legend, Values | 2–3 parts | More than 4 slices = use a bar |
| **Matrix** | Rows, Columns, Values | Pivot tables with drill and subtotals | Use conditional formatting for heat maps |
| **Table** | Columns | Exact values, detail list | Keep it short; a table is not a dashboard |
| **KPI** / **Gauge** | Value, Target, Trend axis | Progress to a target | Gauges waste space; prefer KPI cards |
| **Funnel** | Stage, Values | Drop-off between stages | |
| **Map / Filled map** | Location, Size, Legend | Geography | Geocoding needs clean place names (`City, State, Country`) |
| **Slicer** | Field | Filter the page | Styles: list, dropdown, tiles, between (range), relative date |
| **Decomposition tree** | Analyze, Explain by | Drill into drivers | Interactive exploration |
| **Key influencers** | Analyze, Explain by | AI finds what drives a metric | Needs a binary/numeric target |
| **Smart narrative** | Auto-text | Written summary that updates | Check the wording |

## Formatting essentials

Select a visual → **Format visual** (paint-roller icon): **Visual** tab (axis, labels, colours, legend, gridlines, title) and **General** (title, size, position, background, border, alt text).

| Task | Where |
|---|---|
| Display units and decimals | Format → Callout value / Data labels → Display units: Thousands, Lakhs (not built in; use Millions) or custom format strings |
| Sort | `…` menu → Sort axis (by value or by another field) |
| Colour a highlighted series | Format → Colors → per-category colours or conditional |
| Titles that state the insight | General → Title → fx (dynamic title from a measure) |
| Accessibility | General → Alt text; keep contrast high; do not rely on colour alone |
| Copy formatting | Home → **Format painter** |
| Align / distribute | Format → Arrange → Align and distribute; hold `Shift` to multi-select |
| Group visuals | Select several → Format → Group |

:::tip Dynamic titles
Create a measure `Title Sales = "Sales by " & SELECTEDVALUE ( dim_territory[country], "all countries" ) & " in " & SELECTEDVALUE ( dim_date[year], "all years" )` and bind it in Title → fx → *Field value*. The title now reflects the user's selections.
:::

## Filters: three levels

```python fig: The three filter levels. Visual filters affect one visual, page filters one page, report filters every page.
dg.layers([("Report filters", "Apply to every page (e.g. exclude test data)"), ("Page filters", "Apply to all visuals on one page (e.g. Year = 2025)"),
           ("Visual filters", "Apply to a single visual (e.g. Top 5 products)"), ("Slicers & cross-filter", "User selections and clicks on other visuals")], title="Filter scope: broadest to narrowest")
```

Use the **Filters pane** (right side). Filter types:

| Filter type | Behaviour |
|---|---|
| **Basic** | Tick values from a list |
| **Advanced** | "contains", "starts with", "is greater than", with AND/OR |
| **Top N** | Top/Bottom N items by a measure (even one not in the visual) |
| **Relative date** | "Last 6 months", "this year", "next 7 days" |
| **Relative time** | Last 4 hours etc. |

Tips: **Require single selection** in a slicer; **Sync slicers** across pages (View → Sync slicers); the **"Include" / "Exclude"** options on a selection filter in or out; lock the filters pane or hide it for consumers.

### Edit interactions

By default clicking a bar **cross-filters** other visuals. Select the source visual → Format → **Edit interactions** → then on each target visual click the **Filter**, **Highlight** or **None** icon. Example: a KPI card for "overall sales" should ignore the clicks on the country chart (set to None), while the product chart should filter.

## Drill-down and drill-through

```python fig: Drill-down moves through a hierarchy inside one visual. Drill-through jumps to another page that is filtered by the selected item.
dg.flow(["Category: Bikes", "Drill down → Subcategory: Road Bikes", "Drill down → Product: Road Bike E-331", "Right-click → Drill through → Product detail page"], colors=[dg.VIO, dg.TEAL, dg.GOLD, dg.CORAL], title="Drill-down vs drill-through")
```

- **Drill-down**: needs a hierarchy (Lesson 2). Use the arrow buttons at the top of the visual: ↑ drill up, ↓ drill mode, ⇊ go to the next level in the hierarchy, ⇈ expand all.
- **Drill-through**: create a **detail page** → in the Visualizations pane, drag `product` into **Drill through → Add drill-through fields here** → Power BI adds a back button automatically. Users right-click a product in any visual → **Drill through → Product detail**. Use it for "customer 360", "order detail" and "product detail" pages. **Keep all filters** keeps slicer context.
- **Cross-report drill-through** links to a separate report in the Service.

## Report-page tooltips

A **tooltip page** shows a mini-report when hovering over a data point.

:::steps Build one
1. Add a new page; Format page → Page information → **Allow use as tooltip** on; Page size → **Tooltip**.
2. Add visuals (a KPI, a small trend line, top 3 products) using fields that respond to the hovered item.
3. In the main visual: Format → General → **Tooltips** → Type **Report page** → choose the page.
4. Hide the tooltip page from navigation (right-click the tab → Hide page).
:::

## Buttons, bookmarks and navigation

| Feature | What it does | Use |
|---|---|---|
| **Buttons** (Insert → Buttons) | Back, Bookmark, Page navigation, Q&A, Web URL, Apply all slicers, Clear all slicers | Menus, navigation bars, reset filter |
| **Bookmarks** (View → Bookmarks) | Save the current state (filters, slicer selections, visibility, spotlight) of a page | Story-telling views, toggle between visuals |
| **Selection pane** (View → Selection) | List, name, show or hide every object on a page | Required for bookmark toggles |
| **Page navigator** (Insert → Navigator) | Auto-generated tab buttons for pages or bookmarks | Menu |
| **Conditional visibility** | Bookmarks that show/hide visuals | "Chart ⇄ Table" toggle |

:::steps Chart / table toggle with bookmarks
1. Place a column chart and a table on top of each other.
2. Selection pane: hide the table → View → Bookmarks → **Add** → name it "Chart view"; make the table visible and hide the chart → Add → "Table view". Untick **Data** in each bookmark's options so slicers are not reset.
3. Insert two buttons and set Action → **Bookmark** → choose the matching bookmark.
:::

## Conditional formatting

| Where | How |
|---|---|
| **Table / matrix cells** | Format → Cell elements → Background colour / Font colour / **Data bars** / **Icons** / Web URL → fx → *Gradient*, *Rules* or *Field value* |
| **Column / bar colour** | Format → Colors → fx → rules (green above target, red below) |
| **Card text colour or title** | fx on the callout/title |
| **Based on a measure** | Create a measure returning a hex colour: `Margin Colour = IF ( [Profit Margin %] >= 0.35, "#1E8E5A", "#C0392B" )` then Field value |

```python fig: A matrix with conditional formatting: a heat-map background on sales and traffic-light colours on margin (rules: ≥ 36% green, otherwise amber/red).
import pandas as pd, numpy as np, matplotlib.pyplot as plt
D = "adventure_cycles/"
f = pd.read_csv(D + "fact_sales.csv"); p = pd.read_csv(D + "dim_product.csv"); t = pd.read_csv(D + "dim_territory.csv")
m = f.merge(p, on="product_key").merge(t, on="territory_key"); m["profit"] = m.sales_amount - m.total_cost
g = m.groupby("subcategory").agg(sales=("sales_amount", "sum"), profit=("profit", "sum")).sort_values("sales", ascending=False); g["margin"] = g.profit / g.sales * 100
fig, ax = plt.subplots(figsize=(8.4, 4.2)); ax.axis("off")
rows = [[i, f"{r.sales / 1e6:,.1f}", f"{r.profit / 1e6:,.1f}", f"{r.margin:.1f}%"] for i, r in g.iterrows()]
tb = ax.table(cellText=rows, colLabels=["Subcategory", "Sales (₹ M)", "Profit (₹ M)", "Margin %"], loc="center", cellLoc="center"); tb.auto_set_font_size(False); tb.set_fontsize(9.5); tb.scale(1, 1.45)
norm = (g.sales - g.sales.min()) / (g.sales.max() - g.sales.min())
for i, (idx, r) in enumerate(g.iterrows(), 1):
    tb[i, 1].set_facecolor(plt.cm.Purples(.15 + .7 * norm[idx])); tb[i, 1].get_text().set_color("white" if norm[idx] > .55 else dg.INK)
    tb[i, 3].set_facecolor("#CFEFDD" if r.margin >= 36 else ("#FFF0C2" if r.margin >= 34 else "#F9D0CB"))
for c in range(4): tb[0, c].set_facecolor(dg.INK); tb[0, c].get_text().set_color("white")
fig
```

## Themes

**View → Themes** offers built-in themes; you can download community themes or **Customize current theme** (colours, fonts, defaults). A **theme JSON file** (View → Themes → Browse for themes) applies one consistent look to every visual:

```json
{
  "name": "SkillNavora",
  "dataColors": ["#6C4CF5", "#FF7A59", "#12B5A6", "#E9A23B", "#3B82F6", "#E04F8A"],
  "background": "#FFFFFF", "foreground": "#17142E", "tableAccent": "#6C4CF5",
  "textClasses": { "title": { "fontFace": "Segoe UI Semibold", "fontSize": 14, "color": "#17142E" } }
}
```

Apply the company theme to every report so they look consistent, and edit colours in one place.

## Report design principles

```python fig: A layout that works: headline KPIs on top, the main insight chart large, supporting visuals below, filters on one side, consistent spacing.
dg.layers([("Header", "Title with the insight · date range · logo · navigation buttons"), ("KPI row", "3–5 cards: value, vs last year, vs target"), ("Hero visual", "The chart that answers the main question (largest)"),
           ("Supporting", "2–4 visuals that explain why: breakdowns, trends, tables"), ("Filters", "Slicers on the left or top; consistent across pages")], title="Report page layout")
```

1. **Start from the audience and decision**, not from the data: what will they do differently?
2. **Hierarchy**: most important top-left; big numbers first; details lower.
3. **Less is more**: 5–8 visuals per page; remove gridlines, borders and chart junk.
4. **Consistent colour logic**: one brand colour plus one highlight; red and green only for bad/good; the same colour always means the same thing.
5. **Align and space** visuals on a grid; same sizes for similar charts.
6. **Label for meaning**: insight titles, units (₹, %), clear axis titles, "as of" dates.
7. **Accessible**: contrast, alt text, tab order (Format → Tab order), do not use colour alone, test on mobile layout (View → Mobile layout).
8. **Performance**: fewer visuals, summarised data, no huge tables; check Optimize → Performance analyzer.

## Q&A, images and mobile

- **Q&A visual**: users type "total sales by country in 2025" and get a chart. Improve it with **synonyms** (Model view → Linguistic schema / Q&A setup).
- **Images and logos**: Insert → Image (or text box). For images **in data** (product photos), set the column's **Data category → Image URL**.
- **Mobile layout**: View → Mobile layout; drag key visuals into a phone-shaped canvas.
- **Accessibility and exporting**: export to PDF or PowerPoint (File → Export), analyse in Excel, subscribe in the Service.

:::new Copilot and AI visuals in 2026
Copilot can generate a report page from a prompt, suggest visuals for your fields, write summaries ("Summarise this page") and answer questions about the data. **Key influencers**, **Decomposition tree** and **Smart narrative** are built-in AI visuals; **anomaly detection** (Analytics pane) flags unusual spikes. Always verify AI-generated visuals and text against real numbers.
:::

## A mini case: the Adventure Cycles overview page

Plan the page before you build it:

| Element | Fields / measure | Visual |
|---|---|---|
| Title | Dynamic title measure | Text box |
| KPI row | `Total Sales`, `Total Profit`, `Profit Margin %`, `Orders`, each with vs-last-year | 4–5 cards |
| Hero | Monthly sales and profit margin | Line + column |
| Breakdown 1 | Sales by category (Top N subcategories) | Bar |
| Breakdown 2 | Sales by country | Map or bar |
| Drill-through | Product detail page | Table + KPIs |
| Filters | Year, Country, Category | Slicers |

```python fig: The Adventure Cycles overview page from the real data: KPI cards, monthly trend, subcategory ranking and country share.
fig = plt.figure(figsize=(12, 6.2)); fig.patch.set_facecolor("#F4F2FA"); fig.text(.02, .95, "Adventure Cycles: sales overview 2023–2025", fontsize=15, weight="bold", color=dg.INK)
from matplotlib.patches import FancyBboxPatch
tot_s, tot_p = f.sales_amount.sum(), (f.sales_amount - f.total_cost).sum()
cards = [("Total sales", f"₹{tot_s / 1e7:,.1f} Cr"), ("Total profit", f"₹{tot_p / 1e7:,.1f} Cr"), ("Profit margin", f"{tot_p / tot_s:.1%}"), ("Orders", f"{f.order_number.nunique():,}"), ("Customers", f"{f.customer_key.nunique():,}")]
for i, (l, v) in enumerate(cards):
    ax = fig.add_axes([.02 + i * .195, .79, .18, .12]); ax.axis("off"); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.06", fc="white", ec="#E3DFF0")); ax.text(.07, .68, l, fontsize=9.5, color="#5F5A78"); ax.text(.07, .22, v, fontsize=17, weight="bold", color=dg.INK)
f["order_date"] = pd.to_datetime(f.order_date); ms = f.set_index("order_date").resample("MS").agg(s=("sales_amount", "sum"), c=("total_cost", "sum"))
a1 = fig.add_axes([.06, .40, .45, .30]); a1.bar(ms.index, ms.s / 1e6, width=22, color="#C9C3E6"); a1.set_ylabel("Sales (₹ M)")
a1b = a1.twinx(); a1b.plot(ms.index, (ms.s - ms.c) / ms.s * 100, color=dg.CORAL, lw=2); a1b.set_ylabel("Margin %"); a1b.grid(False); import matplotlib.dates as mdates; a1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7])); a1.xaxis.set_major_formatter(mdates.DateFormatter("%b %y")); a1.set_title("Monthly sales and margin", fontsize=10.5, loc="left")
a2 = fig.add_axes([.72, .40, .25, .30]); sc = (g.sales / 1e6).sort_values().tail(8); a2.barh(sc.index, sc.values, color=[dg.VIO if v == sc.max() else "#C9C3E6" for v in sc.values]); a2.set_title("Top subcategories (₹ M)", fontsize=10.5, loc="left")
a3 = fig.add_axes([.08, .06, .43, .22]); ct = m.groupby("country").sales_amount.sum() / 1e6; a3.barh(ct.index, ct.values, color=[dg.TEAL, dg.GOLD, dg.SKY]); a3.set_title("Sales by country (₹ M)", fontsize=10.5, loc="left")
a4 = fig.add_axes([.66, .02, .3, .26]); a4.pie(m.groupby("category").sales_amount.sum(), labels=m.groupby("category").sales_amount.sum().index, colors=[dg.GOLD, dg.VIO, dg.CORAL, dg.TEAL], wedgeprops=dict(width=.45), textprops=dict(fontsize=8)); a4.set_title("Category mix", fontsize=10.5, loc="left")
fig
```

## Summary

:::key
- Choose visuals from the question; format with insight titles, units, sorting and accessible colours.
- Filters work at **visual, page and report** level (Basic, Advanced, Top N, Relative date); use slicers, sync them across pages, and **Edit interactions** to control cross-filtering.
- **Drill-down** needs a hierarchy; **drill-through** jumps to a detail page; **tooltip pages** show mini-reports on hover.
- **Buttons + bookmarks + the Selection pane** build navigation and chart/table toggles.
- Use **conditional formatting** (rules, gradients, field value from a measure) and **themes** for consistency.
- Design for the decision: hierarchy, few visuals, consistent colour logic, alignment, labels, accessibility and mobile layout.
:::

:::quiz
Q: Which filter level affects every page of a report?
- Visual-level
- Page-level
* Report-level (All pages)
- Slicer-level
> Report filters apply to all pages.

Q: How do you jump from a product in a chart to a detail page for that product?
- Drill-down
* Drill-through (create a drill-through page with the product field)
- Add a slicer
- Use a tooltip
> Drill-through passes the selected value as a filter to another page.

Q: What do bookmarks capture?
- Only the page name
* The state of a page: filters, slicers, visibility and more
- The data model
- The theme
> Bookmarks save a view that buttons can switch to.

Q: Which feature stops a card from reacting when you click a bar chart?
- Sync slicers
* Edit interactions → set the card to None
- Drill-through
- Alt text
> Edit interactions controls how visuals filter each other.

Q: When is a donut chart appropriate?
- With 12 categories
* With 2–3 parts of a whole
- To show a time trend
- To compare 20 products
> More than a few slices are hard to compare; use bars.

Q: What is the benefit of a theme JSON file?
* One consistent set of colours and fonts applied to all visuals and reusable across reports
- It refreshes data
- It creates relationships
- It adds measures
> Themes standardise the look and make branding quick.
:::

:::exercise Build the overview page
Using the Adventure Cycles model: (1) build the overview page above; (2) add a **Year** slicer and a **Country** slicer; (3) create a drill-through page for **Product** with sales, profit, margin and a monthly trend; (4) add a bookmarked toggle between "Sales" and "Profit" using a field parameter or bookmarks; (5) apply conditional formatting to the margin in a matrix and write a dynamic title.
???
(1) Cards for the five measures; line + clustered column for monthly sales and margin; bar for top subcategories; bar for country; donut for category mix. (2) Slicer visuals with `dim_date[year]` (tile style) and `dim_territory[country]` (dropdown). (3) New page → drag `dim_product[product]` into Drill through; add a back button. (4) Modeling → New parameter → Fields → add `Total Sales`, `Total Profit`; use the parameter on the chart values; place its slicer as a toggle. (5) Matrix of `subcategory` × `country` with `Profit Margin %`; Cell elements → Background colour → Rules; title measure with `SELECTEDVALUE`.
:::

:::interview Questions you may be asked
**Q: How do you design an effective Power BI dashboard?**
Start from the audience and decision; put headline KPIs top-left; use few visuals with insight titles; consistent colour and spacing; allow drill-down/through; test with users; check performance and accessibility.

**Q: Drill-down vs drill-through?**
Drill-down navigates levels of a hierarchy within a visual; drill-through navigates to another page filtered by the selected item.

**Q: What are the filter levels and how do slicers differ?**
Visual, page and report filters are set by the author in the Filters pane; slicers are on-canvas controls that users change, and they can be synced across pages.

**Q: How would you let users toggle between a chart and a table?**
Two bookmarks that show/hide the visuals through the Selection pane, and two buttons linked to those bookmarks.
:::
