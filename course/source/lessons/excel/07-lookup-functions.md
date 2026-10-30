---
num: 7
title: "Lookup Functions: VLOOKUP, XLOOKUP and INDEX-MATCH"
live: "Live classes 4–5"
updated: "Excel for Microsoft 365, 2026"
level: Intermediate
duration: 120 min
summary: Bring data together from different tables. Master VLOOKUP and HLOOKUP (exact and approximate match), the modern XLOOKUP, the flexible INDEX + MATCH combination (including two-way and reverse lookups), OFFSET, consolidating several sheets, CHOOSE, and how to troubleshoot #N/A.
datasets: [products.csv, superstore_sales.csv]
outcomes:
  - Explain why lookups are the Excel equivalent of a SQL join
  - Use VLOOKUP and HLOOKUP with exact and approximate match, and know their limits
  - Use XLOOKUP for left lookups, default values, last-match search and multiple return columns
  - Combine INDEX and MATCH for reverse (left) and two-way (matrix) lookups
  - Use CHOOSE, and fix the common causes of #N/A
---

## Why lookups matter

Business data is split across tables: orders in one, products in another, customers in a third. A **lookup** fetches a value from one table using a key that both tables share, such as a product ID or employee ID.

```python fig: A lookup takes a key from one table, finds it in another table, and returns a value from the same row.
dg.flow(["Orders table: product_id P0012", "Find P0012 in Products", "Return its price", "Use it: qty × price"], colors=[dg.SKY, dg.VIO, dg.TEAL, dg.GOLD], title="How every lookup works")
```

:::tip You are already learning SQL joins
A lookup is a **left join** for one column at a time: keep every row of the main table and bring in matching information from the other table. You will see the same idea as `JOIN` in SQL (SQL Lesson 8), `merge()` in pandas, and relationships in Power BI.
:::

We will use this lookup table on a sheet called `Prod`:

```xl title="Prod: product lookup table (A1:E7)"
Product ID{h}|Product{h}|Category{h}|Price{h}|Stock{h}
P101|Office Chair|Furniture|4500|32
P102|Standing Desk|Furniture|18500|8
P103|Laser Printer|Technology|12900|15
P104|Notebook Pack|Office Supplies|240|540
P105|Smartphone|Technology|21999|27
P106|Bookcase|Furniture|7600|0
```

## VLOOKUP

`=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])`

- **lookup_value**: what you are looking for (the key).
- **table_array**: the table to search; the key **must be in its first column**.
- **col_index_num**: which column of that table to return (1 = first column).
- **range_lookup**: `FALSE` (or 0) for an **exact** match. Use `TRUE` only for approximate matching on sorted bands.

```xl title="Order lines looking up product details with VLOOKUP" with="Prod:lookup_products.csv" errors_ok
Order{h}|Product ID{h}|Qty{h}|Product =VLOOKUP(B2,Prod!$A$2:$E$7,2,FALSE){h}|Price{h}|Amount{h}
1001|P103|2|=VLOOKUP(B2,Prod!$A$2:$E$7,2,FALSE)|=VLOOKUP(B2,Prod!$A$2:$E$7,4,FALSE){;#,##0}|=C2*E2{;#,##0}
1002|P101|6|=VLOOKUP(B3,Prod!$A$2:$E$7,2,FALSE)|=VLOOKUP(B3,Prod!$A$2:$E$7,4,FALSE){;#,##0}|=C3*E3{;#,##0}
1003|P105|1|=VLOOKUP(B4,Prod!$A$2:$E$7,2,FALSE)|=VLOOKUP(B4,Prod!$A$2:$E$7,4,FALSE){;#,##0}|=C4*E4{;#,##0}
1004|P104|20|=VLOOKUP(B5,Prod!$A$2:$E$7,2,FALSE)|=VLOOKUP(B5,Prod!$A$2:$E$7,4,FALSE){;#,##0}|=C5*E5{;#,##0}
1005|P109|3|=VLOOKUP(B6,Prod!$A$2:$E$7,2,FALSE){r}|=VLOOKUP(B6,Prod!$A$2:$E$7,4,FALSE){r}|=C6*E6{r}
```

Row 6 shows `#N/A` because P109 does not exist in the product table. That is the correct answer: the key is not there.

:::mistake The four classic VLOOKUP mistakes
1. **Forgetting FALSE**: the default is approximate match, which silently returns a *wrong* row for unsorted data.
2. **Not locking the table**: `A2:E7` copied down becomes `A3:E8`, so the last rows are missed. Use `$A$2:$E$7` or a Table name.
3. **Hard-coded column numbers**: inserting a column inside the table changes which column `4` means. Use `MATCH` for the column number, or XLOOKUP.
4. **Key not in the first column**: VLOOKUP cannot look to the left (use INDEX + MATCH or XLOOKUP).
:::

### Approximate match: bands and slabs

With `TRUE`, VLOOKUP finds the **largest value less than or equal to** the lookup value. The first column must be sorted ascending. This is perfect for tax slabs, commission tiers, discount bands and grades.

```xl title="Approximate match for commission tiers"
Sales from{h}|Commission{h}||Rep{h}|Sales{h}|Rate{h}|Commission{h}
0|0%|| Asha|85000{;#,##0}|=VLOOKUP(E2,$A$2:$B$6,2,TRUE){;0%}|=E2*F2{;#,##0}
100000|3%||Ravi|240000{;#,##0}|=VLOOKUP(E3,$A$2:$B$6,2,TRUE){;0%}|=E3*F3{;#,##0}
250000|5%||Meera|250000{;#,##0}|=VLOOKUP(E4,$A$2:$B$6,2,TRUE){;0%}|=E4*F4{;#,##0}
500000|7%||Kabir|610000{;#,##0}|=VLOOKUP(E5,$A$2:$B$6,2,TRUE){;0%}|=E5*F5{;#,##0}
1000000|10%||Zoya|1200000{;#,##0}|=VLOOKUP(E6,$A$2:$B$6,2,TRUE){;0%}|=E6*F6{;#,##0}
```

Ravi's 2,40,000 falls between 1,00,000 and 2,50,000, so he gets the 1,00,000 row: 3%. Meera's 2,50,000 matches the 2,50,000 row exactly: 5%.

### HLOOKUP

`HLOOKUP` is VLOOKUP turned sideways: it searches the **first row** and returns a value from a row below. Use it when data runs across columns (for example months as headers).

```xl title="HLOOKUP across a horizontal table"
Month{h}|Jan{h}|Feb{h}|Mar{h}|Apr{h}||Find month{h}|Mar
Target|120|130|145|150||Target →|=HLOOKUP(H1,$A$1:$E$3,2,FALSE)
Actual|118|136|139|162||Actual →|=HLOOKUP(H1,$A$1:$E$3,3,FALSE)
```

## XLOOKUP: the modern lookup (Microsoft 365 / Excel 2021+)

`=XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])`

XLOOKUP fixes every VLOOKUP limitation:

| Feature | VLOOKUP | XLOOKUP |
|---|---|---|
| Default match | Approximate (risky) | **Exact** |
| Look to the left | No | **Yes**: lookup and return arrays are separate |
| Column inserted in the table | Breaks the index number | **Safe** |
| Custom "not found" message | Needs IFERROR | Built-in 4th argument |
| Return several columns | One at a time | **Spills** many columns |
| Search last to first | No | `search_mode = -1` |
| Wildcards | Yes | `match_mode = 2` |
| Next smaller / larger match | Sorted data only | `match_mode = -1` or `1`, any order |

```xl title="XLOOKUP examples (lookup table on sheet Prod)" with="Prod:lookup_products.csv"
Need{h}|Formula{h}|Result{h}
Price of P105|'=XLOOKUP("P105",Prod!A2:A7,Prod!D2:D7)|=XLOOKUP("P105",Prod!A2:A7,Prod!D2:D7)=>>21,999
ID of "Bookcase" (left lookup)|'=XLOOKUP("Bookcase",Prod!B2:B7,Prod!A2:A7)|=XLOOKUP("Bookcase",Prod!B2:B7,Prod!A2:A7)=>>P106
Missing ID with a message|'=XLOOKUP("P109",Prod!A2:A7,Prod!B2:B7,"Not found")|=XLOOKUP("P109",Prod!A2:A7,Prod!B2:B7,"Not found")=>>Not found
Product, category and price at once|'=XLOOKUP("P103",Prod!A2:A7,Prod!B2:D7)|=XLOOKUP("P103",Prod!A2:A7,Prod!B2:D7)=>>Laser Printer~Technology~12,900
Last Furniture item in the list|'=XLOOKUP("Furniture",Prod!C2:C7,Prod!B2:B7,,0,-1)|=XLOOKUP("Furniture",Prod!C2:C7,Prod!B2:B7,,0,-1)=>>Bookcase
Product name containing "Desk"|'=XLOOKUP("*Desk*",Prod!B2:B7,Prod!D2:D7,,2)|=XLOOKUP("*Desk*",Prod!B2:B7,Prod!D2:D7,,2)=>>18,500
```

The fourth row returns three columns at once: the result spills across C5:E5.

### XLOOKUP for bands (no sorting needed)

`match_mode = -1` returns the exact match or the **next smaller** item, like VLOOKUP's TRUE, but the table does not need to be sorted:

`=XLOOKUP(E2, $A$2:$A$6, $B$2:$B$6, , -1)` gives the same commission rates as the approximate VLOOKUP above.

:::tip XMATCH
`XMATCH` is the modern version of MATCH with the same match and search modes as XLOOKUP. `=XMATCH("P105",Prod!A2:A7)` → 5.
:::

## INDEX and MATCH

Before XLOOKUP, professionals used **INDEX + MATCH**, and you will still see it everywhere. It works in every Excel version and is very flexible.

- `=INDEX(array, row_num, [col_num])` returns the value **at a position**.
- `=MATCH(lookup_value, lookup_array, [match_type])` returns the **position** of a value. Use `0` for exact match.

```xl title="INDEX returns a value at a position; MATCH returns the position of a value"
State{h}|City{h}|Population 2011 (mn){h}||Formula{h}|Result{h}
Maharashtra|Mumbai|18.4||'=INDEX(A2:C6,2,1)|=INDEX(A2:C6,2,1)
Delhi|Delhi|16.3||'=MATCH("Ahmedabad",B2:B6,0)|=MATCH("Ahmedabad",B2:B6,0)
Gujarat|Ahmedabad|6.4||'=MATCH("Population 2011 (mn)",A1:C1,0)|=MATCH("Population 2011 (mn)",A1:C1,0)
West Bengal|Kolkata|14.1||'=INDEX(C2:C6,MATCH("Kolkata",B2:B6,0))|=INDEX(C2:C6,MATCH("Kolkata",B2:B6,0))
Karnataka|Bengaluru|8.5||'=INDEX(A2:A6,MATCH("Ahmedabad",B2:B6,0))|=INDEX(A2:A6,MATCH("Ahmedabad",B2:B6,0))
```

### Reverse (left) lookup

In the table above, City is in column B and State is in column A. VLOOKUP cannot return a column to the **left** of the key, but INDEX + MATCH can: `=INDEX(A2:A6, MATCH("Ahmedabad", B2:B6, 0))` → **Gujarat**.

```python fig: INDEX + MATCH: MATCH finds the row number of the city; INDEX returns the state on that row.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(9, 3.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 4)
rows = [("Maharashtra", "Mumbai"), ("Delhi", "Delhi"), ("Gujarat", "Ahmedabad"), ("West Bengal", "Kolkata"), ("Karnataka", "Bengaluru")]
for i, (st, ci) in enumerate(rows):
    y = 3.2 - i * .6; hit = ci == "Ahmedabad"
    ax.add_patch(Rectangle((1, y), 2.2, .6, fc="#DFF5EC" if hit else "white", ec="#BBB")); ax.text(1.1, y + .3, st, va="center", fontsize=10.5, weight="bold" if hit else "normal")
    ax.add_patch(Rectangle((3.2, y), 2.2, .6, fc="#E6E0FF" if hit else "white", ec="#BBB")); ax.text(3.3, y + .3, ci, va="center", fontsize=10.5, weight="bold" if hit else "normal")
    ax.text(.6, y + .3, str(i + 1), ha="center", va="center", color="#888")
ax.text(2.1, 3.95, "A: State", ha="center", weight="bold"); ax.text(4.3, 3.95, "B: City", ha="center", weight="bold")
ax.annotate('1. MATCH("Ahmedabad", B2:B6, 0) = 3', xy=(5.4, 2.3), xytext=(5.9, 3.2), fontsize=10.5, color=dg.VIO, weight="bold", arrowprops=dict(arrowstyle="-|>", color=dg.VIO))
ax.annotate('2. INDEX(A2:A6, 3) = "Gujarat"', xy=(1.0, 2.3), xytext=(5.9, 1.0), fontsize=10.5, color=dg.TEAL, weight="bold", arrowprops=dict(arrowstyle="-|>", color=dg.TEAL, connectionstyle="arc3,rad=-.3"))
fig
```

### Two-way (matrix) lookup

INDEX can take a row **and** a column number. Use one MATCH for each to look up the intersection of a row and a column, for example an employee's salary from a table where both the employee and the field are chosen in drop-downs.

```xl title="Two-way lookup: =INDEX($B$2:$E$6, MATCH($G3,$A$2:$A$6,0), MATCH(H$2,$B$1:$E$1,0))"
EmpName{h}|DepartmentID{h}|JobTitle{h}|Salary{h}|City{h}||||
Employee_1|D10|Developer|82000|Pune||Employee{h}|JobTitle{h}|Salary{h}
Employee_2|D20|Analyst|68000|Delhi||Employee_4|=INDEX($B$2:$E$6,MATCH($G3,$A$2:$A$6,0),MATCH(H$2,$B$1:$E$1,0))|=INDEX($B$2:$E$6,MATCH($G3,$A$2:$A$6,0),MATCH(I$2,$B$1:$E$1,0))
Employee_3|D10|Tester|54000|Pune||Employee_2|=INDEX($B$2:$E$6,MATCH($G4,$A$2:$A$6,0),MATCH(H$2,$B$1:$E$1,0))|=INDEX($B$2:$E$6,MATCH($G4,$A$2:$A$6,0),MATCH(I$2,$B$1:$E$1,0))
Employee_4|D30|Manager|125000|Mumbai||||
Employee_5|D20|Developer|79000|Delhi||||
```

Because the headers in row 2 (JobTitle, Salary) are matched by MATCH, you can change a header to `City` and the formula returns cities without editing it. The XLOOKUP version nests one XLOOKUP inside another: `=XLOOKUP($G3,$A$2:$A$6,XLOOKUP(H$2,$B$1:$E$1,$B$2:$E$6))`.

### INDEX + MATCH with multiple conditions

To match on two columns at once (for example Region **and** Product), multiply the conditions inside MATCH:

`=INDEX(F2:F9, MATCH(1, (B2:B9="North")*(C2:C9="Tablet"), 0))` → returns the revenue for the North + Tablet row. In Microsoft 365 this works as a normal formula; in older Excel press `Ctrl + Shift + Enter`. With XLOOKUP: `=XLOOKUP(1,(B2:B9="North")*(C2:C9="Tablet"),F2:F9)`.

## OFFSET and consolidating worksheets

In class we also used lookups to **consolidate** data: pull values from several tables or sheets into one summary. Three tools do this job.

### OFFSET: a value or range by position

`=OFFSET(reference, rows, cols, [height], [width])` starts at `reference`, moves down `rows` and right `cols`, and returns that cell (or a range of `height` × `width`). Combined with MATCH it does the same two-way lookup as INDEX + MATCH. The table below holds month-end share prices (illustrative numbers for fictional companies).

```xl title="Two-way lookup of a share price with INDEX + MATCH and with OFFSET + MATCH"
Date{h}|Asha Foods{h}|Kiran Motors{h}|Meru Steel{h}||Company{h}|Date{h}|INDEX + MATCH{h}|OFFSET + MATCH{h}
2026-01-31|412|1180|96||Kiran Motors|2026-03-31|=INDEX($B$2:$D$6,MATCH(G2,$A$2:$A$6,0),MATCH(F2,$B$1:$D$1,0))|=OFFSET($A$1,MATCH(G2,$A$2:$A$6,0),MATCH(F2,$B$1:$D$1,0))
2026-02-28|398|1215|101||Meru Steel|2026-05-31|=INDEX($B$2:$D$6,MATCH(G3,$A$2:$A$6,0),MATCH(F3,$B$1:$D$1,0))|=OFFSET($A$1,MATCH(G3,$A$2:$A$6,0),MATCH(F3,$B$1:$D$1,0))
2026-03-31|425|1262|99||Asha Foods|2026-02-28|=INDEX($B$2:$D$6,MATCH(G4,$A$2:$A$6,0),MATCH(F4,$B$1:$D$1,0))|=OFFSET($A$1,MATCH(G4,$A$2:$A$6,0),MATCH(F4,$B$1:$D$1,0))
2026-04-30|440|1240|108||||Last 3 months avg (Asha){h}|=AVERAGE(OFFSET($B$1,COUNT($B$2:$B$6)-2,0,3,1))
2026-05-31|436|1298|112||||||
```

The last formula shows OFFSET's real strength: `OFFSET($B$1, COUNT(B2:B6)-2, 0, 3, 1)` is a range of the **last three** prices, so the average updates automatically when a new month is added. The same idea builds dynamic named ranges and charts (Lesson 9).

:::mistake OFFSET is volatile
OFFSET (like INDIRECT, TODAY and RAND) recalculates every time anything in the workbook changes. A few hundred OFFSETs are fine; tens of thousands slow a workbook down. For lookups prefer INDEX + MATCH or XLOOKUP, and for growing ranges prefer an Excel Table.
:::

### Consolidating several sheets into one

| Situation | Best tool | How |
|---|---|---|
| Same layout on every sheet (Jan, Feb, Mar…) and you need totals | 3-D reference | `=SUM(Jan:Mar!B2)` adds cell B2 on every sheet from Jan to Mar (Lesson 4) |
| Same kind of data, but rows in a different order on each sheet | **Data → Consolidate** | Choose Sum, add each sheet's range, tick *Top row* and *Left column*, optionally *Create links to source data* |
| Different tables that share a key (city code, product ID) | Lookups | Bring each column in with XLOOKUP or INDEX + MATCH, as in the class tasks below |
| Many files every month | Power Query | *Get Data → From Folder*, then Append (Lesson 12) |

### Class practice: city tables

These are the consolidation tasks from the live class. Table 1 maps cities to states and population; Table 2 maps city codes to cities.

```xl title="Consolidation tasks: state from city, population from city code, grade from marks"
City Code{h}|City{h}|State{h}|Population 2011 (mn){h}||Task{h}|Input{h}|Answer{h}
C1|Mumbai|Maharashtra|12.48||State of this city|Pune|=IFNA(INDEX($C$2:$C$7,MATCH(G2,$B$2:$B$7,0)),"Not found")
C2|Delhi|Delhi|11.01||Population of city code|C31|=IFNA(INDEX($D$2:$D$7,MATCH(G3,$A$2:$A$7,0)),"Not found")
C3|Ahmedabad|Gujarat|5.57||Population of city code|C4|=IFNA(INDEX($D$2:$D$7,MATCH(G4,$A$2:$A$7,0)),"Not found")
C4|Surat|Gujarat|4.47||City code of this city|Allahabad|=IFNA(INDEX($A$2:$A$7,MATCH(G5,$B$2:$B$7,0)),"Not found")
C31|Allahabad|Uttar Pradesh|1.11||||
C21|Pune|Maharashtra|3.12||Marks{h}|Grade (approx. match){h}|
|||||0|=VLOOKUP(F8,$F$12:$G$15,2,TRUE)|
|||||58|=VLOOKUP(F9,$F$12:$G$15,2,TRUE)|
|||||91|=VLOOKUP(F10,$F$12:$G$15,2,TRUE)|
|||||Min marks{h}|Grade{h}|
|||||0|D|
|||||40|C|
|||||60|B|
|||||80|A|
```

The state and city-code answers use INDEX + MATCH wrapped in IFNA; `=XLOOKUP(G2,B2:B7,C2:C7,"Not found")` gives the same result in Microsoft 365. The grade lookup uses **approximate match** (`TRUE`): VLOOKUP finds the largest "Min marks" that is less than or equal to the marks, so the grade table must be sorted ascending. This is the classic use of approximate match: tax slabs, commission bands and grades.

## CHOOSE, and VLOOKUP with CHOOSE

`=CHOOSE(index_num, value1, value2, …)` returns the item at a position.

```xl title="CHOOSE examples"
Input{h}|Formula{h}|Result{h}
2|'=CHOOSE(A2,"Bronze","Silver","Gold")|=CHOOSE(A2,"Bronze","Silver","Gold")
2026-04-27|'=CHOOSE(WEEKDAY(A3,2),"Mon","Tue","Wed","Thu","Fri","Sat","Sun")|=CHOOSE(WEEKDAY(A3,2),"Mon","Tue","Wed","Thu","Fri","Sat","Sun")
2026-08-15|'="Q"&CHOOSE(MONTH(A4),4,4,4,1,1,1,2,2,2,3,3,3)|="Q"&CHOOSE(MONTH(A4),4,4,4,1,1,1,2,2,2,3,3,3)
```

The last example gives the **Indian financial-year quarter** (April–June = Q1), which a plain `ROUNDUP(MONTH()/3)` cannot do.

**VLOOKUP + CHOOSE** was the old trick for a left lookup: `CHOOSE({1,2}, B2:B6, A2:A6)` builds a virtual two-column table with City first and State second, so VLOOKUP can search it:

`=VLOOKUP("Ahmedabad", CHOOSE({1,2}, B2:B6, A2:A6), 2, FALSE)` → Gujarat.

Today, prefer XLOOKUP or INDEX + MATCH: they are easier to read and faster.

## Troubleshooting #N/A

| Cause | How to check | Fix |
|---|---|---|
| The key really is missing | Search the lookup column with `Ctrl + F` | Return a message: `IFNA(…,"Not found")` or XLOOKUP's 4th argument |
| Extra spaces | `=LEN(A2)` is longer than expected | `TRIM` both sides, or `XLOOKUP(TRIM(B2),TRIM(Prod!A2:A7),…)` |
| Number vs text (`101` vs `"101"`) | `=ISTEXT(B2)` differs from the lookup column | Convert one side: `VALUE()` or `TEXT(…,"0")` |
| Approximate match on unsorted data | Wrong but no error | Use exact match (FALSE / 0) |
| Range not locked | Errors appear only in lower rows | Add `$` or use a Table |
| Invisible characters | `=CODE(RIGHT(B2))` returns 160 or 10 | `SUBSTITUTE` and `CLEAN` |

:::new Lookups in 2026
- **XLOOKUP** and **XMATCH** are now the standard; use VLOOKUP only when sharing files with very old Excel versions.
- **FILTER** returns **all** matching rows, not just the first (Lesson 6).
- For joining large tables regularly, **Power Query → Merge Queries** (Lesson 12) is faster and repeatable, and it is exactly a SQL join.
:::

## Case: pricing the Superstore order lines

Suppose the order lines arrive without a price and you must look it up from the product master (`products.csv`). This is a lookup on 6,323 rows. pandas does the same as XLOOKUP with `merge`:

```python run
import pandas as pd
orders = pd.read_csv("superstore_sales.csv")[["order_id", "product_id", "quantity"]]
products = pd.read_csv("products.csv")
priced = orders.merge(products[["product_id", "product_name", "list_price"]], on="product_id", how="left")   # = XLOOKUP for every row
priced["gross_amount"] = priced.quantity * priced.list_price
print("Rows:", len(priced), "| unmatched product IDs:", priced.list_price.isna().sum())
priced.head(5)
```

Zero unmatched IDs tells you every order line found its product: the same check you should do in Excel with `=COUNTIF(price_column,"#N/A")` or `=SUM(--ISNA(price_column))`.

## Summary

:::key
- Lookups bring columns from one table into another through a shared key, like a SQL left join.
- VLOOKUP: key in the first column, column number counted from 1, **FALSE for exact match**, lock the table with `$`.
- Approximate match (TRUE / match_mode −1) is for sorted bands: tax slabs, commissions, grades.
- XLOOKUP is exact by default, looks left, has a built-in "not found" value, returns several columns and can search from the end.
- INDEX returns a value at a position; MATCH finds the position. Together they do reverse and two-way lookups in any Excel version.
- Most #N/A errors come from missing keys, spaces, or number-vs-text mismatches.
:::

:::quiz
Q: `=VLOOKUP("P103",A2:E7,4,FALSE)` returns a value from which column of the range?
- A
- C
* D
- E
> Column index 4 counts from the first column of the table array: A=1, B=2, C=3, D=4.

Q: Why does VLOOKUP return the wrong price (not #N/A) for unsorted data?
* The fourth argument was omitted, so it used approximate match
- The table was not locked with $
- The column number was too large
- VLOOKUP cannot handle text keys
> Without FALSE, VLOOKUP uses approximate match, which assumes sorted data.

Q: Which formula returns the State for the city in H2, where State is column A and City is column B?
- `=VLOOKUP(H2,A2:B6,1,FALSE)`
* `=INDEX(A2:A6,MATCH(H2,B2:B6,0))`
- `=MATCH(H2,A2:A6,0)`
- `=HLOOKUP(H2,A2:B6,1,FALSE)`
> MATCH finds the row of the city in column B; INDEX returns column A on that row.

Q: Sales of 2,40,000 with tiers at 0, 1,00,000, 2,50,000 and 5,00,000 (approximate match). Which tier is used?
- 0
* 1,00,000
- 2,50,000
- 5,00,000
> Approximate match returns the largest tier less than or equal to the value.

Q: What does XLOOKUP's 4th argument do?
- Sets the match mode
* Returns a value when nothing is found
- Searches from last to first
- Returns several columns
> `if_not_found` replaces #N/A with your own value or message.

Q: A lookup returns #N/A even though the ID is visible in both tables. Which is NOT a likely cause?
- One side has trailing spaces
- One side is a number and the other is text
* The workbook is saved as .xlsx
- There is an invisible non-breaking space
> File format does not affect lookups. Spaces, invisible characters and type mismatches are the usual culprits.
:::

:::exercise Grade lookup
Create a grade table: 0 → F, 40 → D, 55 → C, 70 → B, 85 → A. Write a formula that returns the grade for a mark in B2 using (a) VLOOKUP, (b) XLOOKUP and (c) INDEX + MATCH.
???
With the table in E2:F6 (marks ascending):
(a) `=VLOOKUP(B2,$E$2:$F$6,2,TRUE)`
(b) `=XLOOKUP(B2,$E$2:$E$6,$F$2:$F$6,,-1)`
(c) `=INDEX($F$2:$F$6,MATCH(B2,$E$2:$E$6,1))` (match_type 1 = largest value ≤ B2, needs ascending order).
:::

:::exercise Two-way lookup
Make a table of 4 regions (rows) × 4 quarters (columns) with sales figures. Add drop-downs for region (H1) and quarter (H2) and return the matching sales value.
???
With regions in A2:A5, quarters in B1:E1 and values in B2:E5:
`=INDEX($B$2:$E$5,MATCH($H$1,$A$2:$A$5,0),MATCH($H$2,$B$1:$E$1,0))`
or `=XLOOKUP($H$1,$A$2:$A$5,XLOOKUP($H$2,$B$1:$E$1,$B$2:$E$5))`.
Make the drop-downs with Data Validation → List, source `$A$2:$A$5` and `$B$1:$E$1`.
:::

:::interview Questions you may be asked
**Q: What are the limitations of VLOOKUP and how do you overcome them?**
It cannot look left, it defaults to approximate match, it breaks when columns are inserted (hard-coded index), and it returns only the first match. Use XLOOKUP or INDEX + MATCH, and FILTER for multiple matches.

**Q: Why is INDEX + MATCH considered more flexible than VLOOKUP?**
The lookup and return ranges are separate, so it can look left, it is not affected by inserted columns, it supports two-way lookups, and it can be faster on large sheets because it only reads the columns it needs.

**Q: How would you look up a value using two criteria?**
`XLOOKUP(1,(range1=x)*(range2=y),return_range)`, `INDEX/MATCH` with the same multiplied condition, or a helper column that concatenates the two keys.
:::
