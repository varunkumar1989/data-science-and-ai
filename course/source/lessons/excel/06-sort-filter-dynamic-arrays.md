---
num: 6
title: Sorting, Filtering & Dynamic Arrays
live: "Live class 4"
updated: "Excel for Microsoft 365, 2026"
level: Beginner–Intermediate
duration: 110 min
summary: Organise data with single and multi-level sorts and custom orders, find what matters with AutoFilter and Advanced Filter, and then let formulas do it for you with the dynamic array functions UNIQUE, SORT, SORTBY, FILTER and SEQUENCE, plus the power tool SUMPRODUCT.
datasets: [superstore_sales.csv]
outcomes:
  - Sort by one or many levels, by custom lists, by colour and left to right
  - Filter text, numbers and dates, and use Advanced Filter with AND/OR criteria ranges
  - Explain spill ranges, the # operator and the #SPILL! error
  - Build live lists with UNIQUE, SORT, SORTBY, FILTER and SEQUENCE
  - Answer multi-condition questions with SUMPRODUCT
---

## The sample table

We will use this small sales table (sheet `Reps`, range `A1:F9`) so every result is easy to check by hand. Revenue is `=D2*E2`.

```xl title="Reps: sample sales table"
Rep{h}|Region{h}|Product{h}|Units{h}|Price{h}|Revenue{h}
Asha|North|Laptop|5|55000{;#,##0}|=D2*E2{;#,##0}
Ravi|West|Phone|12|18000{;#,##0}|=D3*E3{;#,##0}
Meera|South|Laptop|3|55000{;#,##0}|=D4*E4{;#,##0}
Kabir|North|Tablet|8|25000{;#,##0}|=D5*E5{;#,##0}
Zoya|East|Phone|15|18000{;#,##0}|=D6*E6{;#,##0}
Farhan|West|Laptop|4|55000{;#,##0}|=D7*E7{;#,##0}
Neha|South|Tablet|10|25000{;#,##0}|=D8*E8{;#,##0}
Rohan|North|Phone|9|18000{;#,##0}|=D9*E9{;#,##0}
```

## Sorting

### Quick sort

Click any cell in a column and use **Data → Sort A to Z** or **Sort Z to A** (or Home → Sort & Filter). Excel detects the table around the cell and keeps each row together.

:::warn Never sort a single selected column
If you select only one column and sort, Excel asks whether to "expand the selection". Choosing "Continue with the current selection" sorts that column alone and scrambles your data: names no longer match their revenue. Always click a single cell inside the table, or select the whole table.
:::

### Multi-level (level-wise) sort

**Data → Sort** opens the Sort dialog, where you add levels. Excel sorts by the first level, then breaks ties with the next.

```python fig: The Sort dialog with two levels: Region A to Z, then Revenue largest to smallest.
dg.window("Sort", [("☑ My data has headers", ""), ("Sort by", "Region        Cell Values        A to Z"), ("Then by", "Revenue       Cell Values        Largest to Smallest"),
                   ("Buttons", "Add Level · Delete Level · Copy Level · Options… (case sensitive, left to right)")], width=8.6)
```

```xl title="Result: Region A→Z, then Revenue high→low"
Rep{h}|Region{h}|Product{h}|Revenue{h}
Zoya|East{p}|Phone|270000{;#,##0}
Asha|North{p}|Laptop|275000{;#,##0}
Kabir|North{p}|Tablet|200000{;#,##0}
Rohan|North{p}|Phone|162000{;#,##0}
Neha|South{p}|Tablet|250000{;#,##0}
Meera|South{p}|Laptop|165000{;#,##0}
Farhan|West{p}|Laptop|220000{;#,##0}
Ravi|West{p}|Phone|216000{;#,##0}
```

### Other sort options

| Option | Where | Example |
|---|---|---|
| **Custom list** | Order → Custom List | Sort months Jan, Feb, Mar instead of alphabetically; sort sizes S, M, L, XL; sort priority High, Medium, Low |
| **Sort by colour** | Sort On → Cell Color / Font Color / Conditional Formatting Icon | Put all red-flagged rows on top |
| **Left to right** | Options → Sort left to right | Reorder columns by a header row |
| **Case sensitive** | Options | Rarely needed |
| **Random order** | Add a column `=RAND()` and sort by it | Draw a random sample |

:::tip Keep the original order
Before sorting raw data, add an `Index` column with 1, 2, 3 … (type 1 and 2, double-click the fill handle). You can always sort by Index to get back to the original order.
:::

## Filtering

### AutoFilter

Click inside the data and press `Ctrl + Shift + L` (Data → Filter). Every header gets a drop-down arrow.

| Filter type | Options |
|---|---|
| **Text filters** | Equals, does not equal, begins with, ends with, contains, does not contain, custom (with `*` and `?`) |
| **Number filters** | Greater than, between, Top 10 (items or percent), above/below average |
| **Date filters** | Today, this week, last month, next quarter, year to date, between, and grouped tick-boxes by year → month → day |
| **By colour** | Filter by cell colour, font colour or icon |
| **Search box** | Type part of a value to tick only matching items |

Filters on several columns combine with **AND**: Region = North **and** Product = Laptop. Within one column, ticking several items is **OR**: North **or** South.

:::tip Filtered totals
When you filter, the status bar shows "8 of 6,323 records found". Use `SUBTOTAL(109, …)` (Lesson 4) or the Table Total Row for totals that follow the filter. To copy only the visible rows, select them, press `Alt + ;` (visible cells only), then copy.
:::

Here is the same idea on the full Superstore file: filter to Technology orders in the West with a discount above 20%.

```python run
import pandas as pd
s = pd.read_csv("superstore_sales.csv")
f = s[(s.category == "Technology") & (s.region == "West") & (s.discount > 0.2)]
print(f"{len(f)} of {len(s):,} records found  |  visible sales total: {f.sales.sum():,.0f}  |  visible profit total: {f.profit.sum():,.0f}")
f[["order_id", "city", "sub_category", "sales", "discount", "profit"]].head(5)
```

### Advanced Filter: complex AND/OR in one go

**Data → Advanced** filters with a **criteria range**: a small table with the same headers as your data.

- Conditions on the **same row** are combined with **AND**.
- Conditions on **different rows** are combined with **OR**.

```xl title="Criteria range: (North AND Revenue > 1,80,000) OR (Product = Phone)"
Region{h}|Product{h}|Revenue{h}
North||>180000
|Phone|
```

Rows that match: Asha (North, 2,75,000), Kabir (North, 2,00,000), and every Phone row: Ravi, Zoya and Rohan. Rohan is in the North but has only 1,62,000; he still appears because he sells phones.

:::steps Run an Advanced Filter
1. Type the criteria range above your data or on another sheet (headers must match exactly).
2. Click inside the data → Data → **Advanced**.
3. List range: your data. Criteria range: the criteria table including headers.
4. Choose **Copy to another location** and pick an output cell to keep the original intact.
5. Tick **Unique records only** to get a list without duplicates (a quick alternative to Remove Duplicates).
:::

Advanced Filter results are static: run it again after the data changes. For live results use `FILTER`.

## Dynamic arrays: formulas that spill

In Microsoft 365, a formula can return **many values**. They **spill** into the cells below and to the right. The whole result is called the **spill range**; it has a blue border, and you can refer to it with the `#` operator.

```python fig: One formula in H2 spills into H2:H5. Refer to the whole result with H2#.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(8.5, 3.2)); ax.axis("off"); ax.set_xlim(0, 9); ax.set_ylim(0, 3.6)
vals = ["North", "West", "South", "East"]
ax.text(0.2, 3.2, "H2:  =UNIQUE(B2:B9)", fontsize=13, family="DejaVu Sans Mono", color=dg.INK, weight="bold")
for i, v in enumerate(vals):
    ax.add_patch(Rectangle((0.3, 2.3 - i * .55), 2.2, .55, fc="#EEF6FF" if i else "#DCEBFF", ec="#9CC2F7"))
    ax.text(0.45, 2.57 - i * .55, v, va="center", fontsize=11)
ax.add_patch(Rectangle((0.3, 2.85 - 4 * .55), 2.2, 4 * .55, fill=False, ec="#2563EB", lw=2.2, ls="--"))
ax.annotate("spill range H2:H5\n(one formula)", xy=(2.5, 1.7), xytext=(4.2, 2.2), fontsize=10.5, color="#2563EB", arrowprops=dict(arrowstyle="-|>", color="#2563EB"))
ax.text(4.2, 1.0, "=COUNTA(H2#)  →  4", fontsize=12, family="DejaVu Sans Mono", color=dg.INK)
ax.text(4.2, .45, "Add a new region in column B and the list grows by itself.", fontsize=10, color="#555")
fig
```

:::warn #SPILL!
If any cell in the area the result needs is not empty, the formula returns `#SPILL!`. Click the error to see which cell is blocking, and clear it. Spilling formulas also cannot be used inside an Excel Table; put them next to the table instead.
:::

### UNIQUE

`=UNIQUE(array, [by_col], [exactly_once])`

```xl title="UNIQUE examples (formulas in H2 and J2)" with="Reps:reps_small.csv"
|||Region list =UNIQUE(B2:B9){h}||Product list =UNIQUE(C2:C9){h}
|||=UNIQUE(Reps!B2:B9)=>>North;West;South;East||=UNIQUE(Reps!C2:C9)=>>Laptop;Phone;Tablet
```

- `=COUNTA(UNIQUE(C2:C9))` → **3** distinct products. (Before dynamic arrays this needed `=SUMPRODUCT(1/COUNTIF(C2:C9,C2:C9))`.)
- `=UNIQUE(B2:C9)` returns unique **combinations** of Region and Product.
- `=UNIQUE(B2:B9,,TRUE)` returns values that appear **exactly once**: East.

### SORT and SORTBY

`=SORT(array, [sort_index], [sort_order], [by_col])` sorts by a column **position** in the array. `-1` means descending.
`=SORTBY(array, by_array1, [order1], …)` sorts by **other ranges**, which do not have to be shown.

```xl title="Top performers: =SORT(A2:F9,6,-1) and =SORTBY(A2:A9,F2:F9,-1)" with="Reps:reps_small.csv"
Rep{h}|Region{h}|Product{h}|Units{h}|Price{h}|Revenue{h}||SORTBY names{h}
=SORT(Reps!A2:F9,6,-1)=>>Asha~North~Laptop~5~55000~275000;Zoya~East~Phone~15~18000~270000;Neha~South~Tablet~10~25000~250000;Farhan~West~Laptop~4~55000~220000;Ravi~West~Phone~12~18000~216000;Kabir~North~Tablet~8~25000~200000;Meera~South~Laptop~3~55000~165000;Rohan~North~Phone~9~18000~162000|||||||=SORTBY(Reps!A2:A9,Reps!F2:F9,-1)=>>Asha;Zoya;Neha;Farhan;Ravi;Kabir;Meera;Rohan
```

Combine functions: `=SORT(UNIQUE(B2:B9))` gives the regions alphabetically: East, North, South, West. `=TAKE(SORT(A2:F9,6,-1),3)` returns only the top 3 rows.

### FILTER

`=FILTER(array, include, [if_empty])`

The `include` argument is a TRUE/FALSE test with one result per row. Combine conditions with `*` for AND and `+` for OR.

```xl title="FILTER examples" with="Reps:reps_small.csv"
North reps{h}||Laptops with ≥4 units{h}||North OR Phone{h}||No match{h}
=FILTER(Reps!A2:A9,Reps!B2:B9="North")=>>Asha;Kabir;Rohan||=FILTER(Reps!A2:A9,(Reps!C2:C9="Laptop")*(Reps!D2:D9>=4))=>>Asha;Farhan||=FILTER(Reps!A2:A9,(Reps!B2:B9="North")+(Reps!C2:C9="Phone"))=>>Asha;Ravi;Kabir;Zoya;Rohan||=FILTER(Reps!A2:A9,Reps!B2:B9="Central","None found")=>>None found
```

| Logic | Write it as | Why it works |
|---|---|---|
| AND | `(cond1)*(cond2)` | TRUE×TRUE = 1; anything × FALSE = 0 |
| OR | `(cond1)+(cond2)` | Any TRUE makes the sum ≥ 1 |
| NOT | `(cond)=FALSE` or `NOT(cond)` | Reverses the test |

:::tip An interactive report in two cells
Put a Data Validation drop-down of regions in `H1` (source `=SORT(UNIQUE(B2:B9))`), then `=FILTER(A2:F9,B2:B9=H1)` below it. Choosing a region instantly shows its reps. This is the formula version of a slicer.
:::

### SEQUENCE and friends

| Function | Example | Result |
|---|---|---|
| `SEQUENCE(rows, [cols], [start], [step])` | `=SEQUENCE(5)` | 1, 2, 3, 4, 5 down a column |
| | `=SEQUENCE(1,12,1,1)` | 1 to 12 across a row |
| | `=SEQUENCE(7,1,DATE(2026,4,27),1)` | Seven consecutive dates |
| `RANDARRAY(rows, cols, min, max, integer)` | `=RANDARRAY(5,1,1,100,TRUE)` | Five random whole numbers |
| `TAKE(array, rows)` / `DROP(array, rows)` | `=TAKE(SORT(F2:F9,,-1),3)` | Top 3 revenues |
| `VSTACK` / `HSTACK` | `=VSTACK(Jan!A2:C50,Feb!A2:C50)` | Stack two ranges into one |
| `CHOOSECOLS(array, 1, 6)` | | Only columns 1 and 6 |
| `GROUPBY(row_fields, values, function)` | `=GROUPBY(B2:B9,F2:F9,SUM)` | A summary by region, like a pivot table, in one formula (newer Microsoft 365) |

## SUMPRODUCT: the original array function

`SUMPRODUCT` multiplies arrays element by element and adds the results. It works in **every** version of Excel and is the classic way to do multi-condition sums before SUMIFS existed, plus things SUMIFS cannot do.

```xl title="SUMPRODUCT on the Reps table" with="Reps:reps_small.csv"
Question{h}|Formula{h}|Result{h}
Total revenue (units × price)|'=SUMPRODUCT(D2:D9,E2:E9)|=SUMPRODUCT(Reps!D2:D9,Reps!E2:E9){;#,##0}
Revenue in North|'=SUMPRODUCT((B2:B9="North")*D2:D9*E2:E9)|=SUMPRODUCT((Reps!B2:B9="North")*Reps!D2:D9*Reps!E2:E9){;#,##0}
Phone units in West or East|'=SUMPRODUCT((C2:C9="Phone")*((B2:B9="West")+(B2:B9="East"))*D2:D9)|=SUMPRODUCT((Reps!C2:C9="Phone")*((Reps!B2:B9="West")+(Reps!B2:B9="East"))*Reps!D2:D9)
Rows where units > 8|'=SUMPRODUCT(--(D2:D9>8))|=SUMPRODUCT(--(Reps!D2:D9>8))
Weighted average price|'=SUMPRODUCT(D2:D9,E2:E9)/SUM(D2:D9)|=SUMPRODUCT(Reps!D2:D9,Reps!E2:E9)/SUM(Reps!D2:D9){;#,##0.00}
```

Check: Phone units in West or East = Ravi 12 + Zoya 15 = 27. Rows with more than 8 units: Ravi, Zoya, Neha, Rohan = 4.

:::note Why the double minus `--`?
`(D2:D9>8)` produces TRUE/FALSE values. SUMPRODUCT ignores logical values unless they are converted to numbers. `--` (minus minus) turns TRUE into 1 and FALSE into 0. Multiplying by another array (`*`) also converts them, which is why the other formulas do not need it.
:::

## Putting it together: a self-updating region summary

```xl title="Region summary with UNIQUE + SUMIFS + SORT" with="Reps:reps_small.csv"
Region =SORT(UNIQUE(B2:B9)){h}|Revenue =SUMIFS(F2:F9,B2:B9,H2#){h}|Share{h}
=SORT(UNIQUE(Reps!B2:B9))=>>East;North;South;West|=SUMIFS(Reps!F2:F9,Reps!B2:B9,"East")=>>270,000;637,000;415,000;436,000{;#,##0}|=B2/SUM(Reps!F2:F9)=>>15.4%;36.2%;23.6%;24.8%{;0.0%}
```

In Microsoft 365 the second column is a single formula, `=SUMIFS(F2:F9,B2:B9,H2#)`: because `H2#` refers to the whole spilled list, SUMIFS spills one total per region. Add a new region to the data and the summary grows automatically.

Let's confirm the numbers with pandas:

```python run
reps = pd.DataFrame({"rep": ["Asha","Ravi","Meera","Kabir","Zoya","Farhan","Neha","Rohan"],
                     "region": ["North","West","South","North","East","West","South","North"],
                     "units": [5,12,3,8,15,4,10,9], "price": [55000,18000,55000,25000,18000,55000,25000,18000]})
reps["revenue"] = reps.units * reps.price
summary = reps.groupby("region")["revenue"].sum().to_frame()
summary["share"] = (summary.revenue / summary.revenue.sum()).round(3)
summary
```

## Summary

:::key
- Click **one cell** inside the table before sorting; use the Sort dialog for multi-level, custom-list and colour sorts.
- AutoFilter: AND across columns, OR within a column. Advanced Filter: AND on one row, OR across rows of a criteria range.
- Dynamic arrays **spill**; refer to the result with `#`; clear blocking cells to fix `#SPILL!`.
- `UNIQUE`, `SORT`, `SORTBY`, `FILTER`, `SEQUENCE`, `TAKE`, `VSTACK`, `GROUPBY` replace many manual steps with live formulas.
- In FILTER and SUMPRODUCT, `*` means AND and `+` means OR.
- `SUMPRODUCT` handles weighted sums and complex conditions in any Excel version.
:::

:::quiz
Q: You select only the Revenue column and sort it, choosing "Continue with the current selection". What happens?
- The whole table is sorted correctly
* Only Revenue is reordered, so revenues no longer match their reps
- Excel refuses to sort
- The table is sorted by Rep name
> Sorting a single column separates it from the rest of the row. Always sort the whole table.

Q: In an Advanced Filter criteria range, two conditions on the same row mean:
* AND
- OR
- NOT
- XOR
> Same row = AND; different rows = OR.

Q: `=FILTER(A2:A9,(B2:B9="North")+(C2:C9="Phone"))` returns reps who are:
- In the North and sell phones
* In the North or sell phones (or both)
- Not in the North
- In the North but not selling phones
> Adding conditions works as OR.

Q: A formula returns #SPILL!. What is the most likely cause?
- A typo in the function name
* A cell in the spill area is not empty
- The data has duplicates
- The workbook is in manual calculation mode
> Dynamic arrays need empty cells to spill into.

Q: What does `=SUMPRODUCT(--(D2:D9>8))` calculate?
- The sum of values greater than 8
* The number of values greater than 8
- The average of values greater than 8
- The largest value
> `--` turns TRUE/FALSE into 1/0, and SUMPRODUCT adds them up: a count.

Q: Which formula lists each region once, sorted A to Z?
- `=UNIQUE(SORT(B2:B9),TRUE)`
* `=SORT(UNIQUE(B2:B9))`
- `=SORTBY(B2:B9,B2:B9)`
- `=FILTER(B2:B9,B2:B9<>"")`
> UNIQUE removes duplicates and SORT orders the result.
:::

:::exercise Superstore with dynamic arrays
In a copy of `superstore_sales.csv` (as a Table named `S`): (1) list the distinct sub-categories, sorted; (2) show all orders from Kochi with profit below zero; (3) show the 5 largest order lines by sales (order ID, city, sales); (4) count distinct customers.
???
(1) `=SORT(UNIQUE(S[sub_category]))`
(2) `=FILTER(S,(S[city]="Kochi")*(S[profit]<0),"None")`
(3) `=TAKE(SORTBY(CHOOSECOLS(S,2,9,16),S[sales],-1),5)` (check the column numbers in your file: here 2 = order_id, 9 = city, 16 = sales)
(4) `=COUNTA(UNIQUE(S[customer_id]))`
:::

:::interview Questions you may be asked
**Q: How would you get a list of unique values in Excel?**
`UNIQUE` in Microsoft 365; otherwise Remove Duplicates on a copy, Advanced Filter with "Unique records only", or a pivot table.

**Q: Explain AND/OR logic in FILTER or SUMPRODUCT.**
Each condition becomes an array of TRUE/FALSE. Multiplying arrays gives 1 only when all are TRUE (AND); adding gives at least 1 when any is TRUE (OR).

**Q: How do you sort by a custom order such as High, Medium, Low?**
Sort dialog → Order → Custom List, and add the list; or use `SORTBY` with `MATCH(range,{"High","Medium","Low"},0)` as the sort key.
:::
