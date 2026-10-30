---
num: 1
title: "Getting Started with Tableau: Interface, Data Connections and Your First Views"
updated: "Tableau Desktop / Tableau Public 2026"
level: Beginner
duration: 120 min
summary: Understand the Tableau product family, install Tableau Public, connect to the Superstore India data, read the Data Source page, learn dimensions vs measures and discrete vs continuous fields, master the Marks card and shelves, build and sort your first views, and save them to Tableau Public.
datasets: [superstore_sales.csv]
outcomes:
  - Describe Tableau Desktop, Public, Cloud, Server, Prep and Pulse, and when each is used
  - Connect to a CSV, check data types and rename or hide fields on the Data Source page
  - Explain dimensions vs measures and discrete (blue) vs continuous (green) fields
  - Build bar, line and text-table views with the Columns, Rows, Marks, Filters and Pages shelves
  - Sort, label, format and save a workbook to Tableau Public
---

## What is Tableau?

**Tableau** is a visual analytics platform: you drag fields onto shelves and Tableau writes the query, aggregates the data and draws the chart. It is owned by Salesforce and, with Power BI, is one of the two BI tools most often named in Indian analyst job posts. Where Power BI leans on DAX formulas and the Microsoft stack, Tableau is known for fast visual exploration and highly customisable charts.

```python fig: The Tableau product family. You build in Desktop (or Public), share on Cloud/Server/Public, and prepare data in Prep.
dg.flow(["Data: Excel, CSV, SQL databases, cloud warehouses", "Tableau Prep Builder (clean & shape)", "Tableau Desktop / Public (build workbooks)", "Tableau Cloud / Server / Public (share, schedule, Pulse)"], colors=[dg.SKY, dg.TEAL, dg.VIO, dg.CORAL], title="Tableau products")
```

| Product | What it is | Cost (2026) |
|---|---|---|
| **Tableau Public** (desktop app + website) | Free version of Desktop; workbooks are saved **publicly** on public.tableau.com | Free |
| **Tableau Desktop** | Full authoring tool; saves locally, connects to databases | Paid (Creator licence) |
| **Tableau Cloud** | Tableau's hosted service for sharing, refresh schedules and permissions | Paid, per user |
| **Tableau Server** | The same as Cloud, but installed on your company's own servers | Paid |
| **Tableau Prep Builder** | Visual tool to clean, join and reshape data before analysis | Included with Creator |
| **Tableau Pulse / Tableau Agent** | AI features: metric digests in plain language and an assistant that helps write calculations and build views | Cloud add-ons |

:::tip Which one should you install?
Learners should install **Tableau Public** (free). It has almost every authoring feature of Desktop. The two limits: workbooks are saved to your public profile (so never use confidential data) and it connects mainly to files (Excel, CSV, text, JSON, PDF, spatial) and Google Sheets rather than company databases. Your public profile also works as a portfolio for interviews.
:::

## Install and connect

:::steps Install Tableau Public and connect to Superstore
1. Go to public.tableau.com → **Create** → download **Tableau Public** for Windows or Mac and install it; sign up for a free profile.
2. Open Tableau Public. On the **Connect** pane choose **Text file** and pick `superstore_sales.csv` (for an Excel file choose **Microsoft Excel**).
3. The **Data Source page** opens: the table appears in the canvas and a preview grid below it.
4. Check each column's **data type icon** (Abc = string, # = number, calendar = date, globe = geographic). Click an icon to change it.
5. Click **Sheet 1** at the bottom to start building.
:::

The data you connect to is the same Superstore India file used in the Excel and Power BI lessons. Check its size before you build anything:

```python run
import pandas as pd
df = pd.read_csv("superstore_sales.csv", parse_dates=["order_date", "ship_date"])
print(df.shape)
print(df.dtypes.astype(str).value_counts().to_dict())
print("Orders from", df.order_date.min().date(), "to", df.order_date.max().date())
df.head(3)
```

6,323 rows (order lines) and 19 columns: Tableau will show these as **fields** in the Data pane.

### The Data Source page

| Feature | Where | Use |
|---|---|---|
| Rename a field | Click the column header → Rename | Friendly names such as "Sub-Category" |
| Hide a field | Column menu → Hide | Remove IDs you will never use |
| Change type / geographic role | Click the type icon | Make `state` a **State/Province** so it maps |
| Split | Column menu → Split | `customer_name` → first and last name |
| Pivot | Select columns → Pivot | Turn month columns into rows |
| Data Interpreter | Left pane checkbox | Clean messy Excel sheets with titles and merged cells |
| Live vs Extract | Top right | Extract (.hyper) is a fast snapshot; Live queries the source every time |
| Filters (data source) | Top right → Add | Keep only the rows the workbook needs |

## The workspace

```python fig: The Tableau worksheet layout. Drag fields from the Data pane onto shelves and the Marks card.
dg.window("Tableau worksheet", [("Data pane (left)", "Tables and fields: dimensions above, measures below"), ("Columns / Rows shelves", "Fields here create the axes and headers"), ("Marks card", "Mark type + Color, Size, Label, Detail, Tooltip, Shape"), ("Filters shelf", "Keep or exclude data for this sheet"), ("Pages shelf", "Animate the view, one page per value"), ("Show Me (top right)", "Suggests chart types for the fields you selected"), ("Tabs (bottom)", "Data Source, sheets, dashboards, stories")], title="Workspace", accent=dg.SKY)
```

## Dimensions vs measures, discrete vs continuous

Tableau sorts every field in two ways, and the colour of a pill tells you which:

| | Meaning | Example | What it creates |
|---|---|---|---|
| **Dimension** | Categories you slice by | Region, Category, Customer Name | Groups (one mark per value) |
| **Measure** | Numbers you aggregate | Sales, Profit, Quantity | SUM, AVG, COUNT… |
| **Discrete** (blue pill) | Separate values | Region, YEAR(Order Date) as "2023, 2024" | **Headers** |
| **Continuous** (green pill) | An unbroken range | SUM(Sales), exact date | **Axes** |

```python fig: Blue (discrete) pills create headers; green (continuous) pills create axes.
dg.compare("Discrete (blue)", ["Draws headers / labels", "Region, Segment, Ship Mode", "YEAR(Order Date) as separate years", "Colour legend: distinct colours"], "Continuous (green)", ["Draws an axis", "SUM(Sales), AVG(Discount)", "MONTH(Order Date) as a timeline", "Colour legend: a gradient"], title="Pill colours", lc=dg.SKY, rc=dg.TEAL)
```

A measure dropped into the view is **aggregated** (default SUM). Right-click the pill → **Measure** to switch to Average, Median, Count, Count (Distinct), Minimum, Maximum, Standard deviation and so on.

## Your first views

### Sales by region (bar chart)

Drag **Region** to Rows and **Sales** to Columns. Tableau writes the equivalent of `SELECT region, SUM(sales) FROM superstore GROUP BY region` and draws one bar per region:

```python run
by_region = (df.groupby("region")[["sales", "profit"]].sum() / 1e7).round(2).sort_values("sales", ascending=False)
by_region.columns = ["Sales (₹ crore)", "Profit (₹ crore)"]
by_region
```

```python fig: The view you get: SUM(Sales) by Region, sorted descending, with labels.
import pandas as pd, matplotlib.pyplot as plt
d = pd.read_csv("superstore_sales.csv"); s = (d.groupby("region").sales.sum() / 1e7).sort_values()
fig, ax = plt.subplots(figsize=(7.5, 2.8)); bars = ax.barh(s.index, s.values, color="#4E79A7")
for b, v in zip(bars, s.values): ax.text(v + .2, b.get_y() + b.get_height() / 2, f"₹{v:.2f} cr", va="center", fontsize=9.5)
ax.set_xlabel("Sales (₹ crore)"); ax.spines[["top", "right"]].set_visible(False); ax.set_xlim(0, s.max() * 1.18); ax.set_title("Sales by Region", loc="left", fontsize=11, weight="bold")
fig
```

The default Tableau colours (blue #4E79A7, orange #F28E2B, red #E15759…) are the **Tableau 10** palette used in the figures in this track.

:::steps Sort, label and colour it
1. Hover the Sales axis and click the **sort** icon, or click the toolbar sort descending button.
2. Click **Label** on the Marks card → tick *Show mark labels*.
3. Drag **Profit** onto **Color**: bars are shaded by profit, so sales and margin show together.
4. Right-click the Sales axis → **Format** → Numbers → Currency (Custom) → Display units: *Crores* is not built in, so use a calculated field `[Sales]/1e7` named "Sales (₹ cr)" (Lesson 3), or show *Millions*.
5. Double-click the sheet tab and rename it "Sales by Region".
:::

### Sales over time (line chart)

Drag **Order Date** to Columns: Tableau shows **YEAR(Order Date)** as a discrete header. Click the **+** on the pill to drill down to Quarter and Month. Right-click the pill and choose the **green** "Month" (continuous) to draw a single timeline, or the **blue** "Month" (discrete) to compare the same month across years.

```python run
m = df.set_index("order_date").sales.resample("ME").sum() / 1e5
print("Months:", len(m), "| best month:", m.idxmax().strftime("%b %Y"), f"₹{m.max():.1f} lakh", "| weakest:", m.idxmin().strftime("%b %Y"), f"₹{m.min():.1f} lakh")
yearly = (df.groupby(df.order_date.dt.year).sales.sum() / 1e7).round(2); yearly
```

### Text table (crosstab)

Put **Category** on Rows, **YEAR(Order Date)** on Columns and **Sales** on **Text**. Add **Analysis → Totals → Show Row Grand Totals**. This is Tableau's pivot table:

```python run
ct = pd.crosstab(df.category, df.order_date.dt.year, values=df.sales, aggfunc="sum", margins=True, margins_name="Grand Total") / 1e5
ct.round(1)
```

## Show Me

**Show Me** (top right) highlights the chart types that fit the fields you have selected and states what it needs, e.g. "*1 date, 1 or more dimensions, 1 or more measures*" for a line chart. It is a fast start, but learn to build each chart by hand: interviewers often ask *how* you would build a view.

## Saving and sharing

| Format | What it contains |
|---|---|
| `.twb` workbook | Sheets, dashboards and the connection, **no data** |
| `.twbx` packaged workbook | Workbook **plus** a copy of the data/extract: share this one |
| `.hyper` extract | Tableau's compressed, fast data snapshot |
| Tableau Public profile | **File → Save to Tableau Public**; anyone can view and download it |

:::mistake Beginner mistakes
- Saving confidential company data to Tableau Public: everything there is public.
- Sending a `.twb` file: the receiver cannot open it without your data. Send `.twbx`.
- Leaving a date as a string ("Abc"): you lose drill-down and date functions. Change the type on the Data Source page.
- Using a measure that should be a dimension (e.g. Postal Code as SUM): right-click → Convert to Dimension.
:::

:::new Tableau in 2026
- **Tableau Agent** (formerly Einstein Copilot for Tableau) suggests calculations and builds views from a typed question in Tableau Cloud.
- **Tableau Pulse** sends plain-language metric summaries ("Sales are up 8% this week, driven by the West region") to email and Slack.
- **Tableau Next** is Salesforce's agent-based analytics layer on top of Data Cloud. Desktop and Public remain the tools you learn first.
:::

## Summary

:::key
- Tableau turns drag-and-drop into queries: shelves define the structure, the Marks card defines the look.
- Dimensions slice, measures aggregate; blue pills are discrete (headers), green pills are continuous (axes).
- Start with Tableau Public, connect to a file, fix data types on the Data Source page, then build.
- Share packaged workbooks (`.twbx`) or publish to Tableau Public/Cloud.
:::

:::quiz
Q: What does a green pill on Columns create?
* A continuous axis
- A set of headers
- A filter
- A calculated field
> Green = continuous = axis; blue = discrete = headers.

Q: You drag Sales into the view. What does Tableau show by default?
* SUM(Sales) for each combination of the dimensions in the view
- Every row's sales value
- The average sales
- The count of rows
> Measures are aggregated, and SUM is the default.

Q: Which file should you email a colleague so they can open your work with the data?
* A packaged workbook (.twbx)
- A workbook (.twb)
- A .hyper file only
- A screenshot
> .twbx bundles the workbook with its data.

Q: What is the main limitation of Tableau Public?
* Workbooks are saved publicly and it connects mainly to files
- It cannot draw maps
- It has no calculated fields
- It only works on Mac
> Never put confidential data on Tableau Public.

Q: State is shown as "Abc" and will not draw a map. What do you do?
* Assign the geographic role State/Province
- Convert it to a measure
- Delete the field
- Use a dual axis
> Geographic roles give a field latitude and longitude.

Q: Which feature suggests chart types for the selected fields?
* Show Me
- Pages shelf
- Data Interpreter
- Extract
> Show Me lists the chart types and what each needs.
:::

:::exercise Practice
Connect to `superstore_sales.csv` in Tableau Public and build three sheets: (1) Sales by Category sorted descending with labels; (2) a continuous monthly Sales line with Profit on Color; (3) a text table of Segment × Year with grand totals. Save as a packaged workbook and publish to your Tableau Public profile.
???
Sheet 1: Category on Rows, SUM(Sales) on Columns, sort descending, Label on. Sheet 2: MONTH(Order Date) continuous (green) on Columns, SUM(Sales) on Rows, SUM(Profit) on Color. Sheet 3: Segment on Rows, YEAR(Order Date) on Columns, SUM(Sales) on Text, Analysis → Totals → Show Row and Column Grand Totals. File → Save to Tableau Public.
:::

:::interview Questions you may be asked
**Q: What is the difference between a dimension and a measure?**
A dimension is a categorical field used to group the data (Region, Category); a measure is a numeric field that Tableau aggregates (SUM of Sales). Each mark represents one combination of the dimensions in the view.

**Q: Discrete vs continuous?**
Discrete fields (blue) create headers and distinct colours; continuous fields (green) create axes and colour gradients. Dates can be either: discrete YEAR gives "2023, 2024" headers, continuous MONTH gives a timeline.

**Q: .twb vs .twbx vs .hyper?**
.twb is the workbook definition without data; .twbx packages the workbook with its data or extract; .hyper is the extract file itself.

**Q: Live connection or extract?**
Live always shows current data but depends on the source's speed; an extract is a fast, compressed snapshot that you refresh on a schedule. Use extracts for speed and offline work, live for real-time needs or very large governed warehouses.
:::
