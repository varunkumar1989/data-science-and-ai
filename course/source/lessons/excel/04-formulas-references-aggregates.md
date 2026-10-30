---
num: 4
title: Formulas, Cell References & Aggregate Functions
live: "Live class 3"
updated: "Excel for Microsoft 365, 2026"
level: Beginner
duration: 110 min
summary: Write formulas with confidence. Understand operators and their order, relative, absolute and mixed references, and every aggregate function you need, from SUM and COUNTA to SMALL, LARGE, SUMIFS, COUNTIFS, MAXIFS, SUBTOTAL and AGGREGATE.
datasets: [employees_small.csv, superstore_sales.csv]
outcomes:
  - Explain the difference between a formula and a function and read any function's syntax
  - Predict how a formula changes when copied, and lock references with $ (F4)
  - Summarise data with SUM, COUNT, COUNTA, COUNTBLANK, AVERAGE, MIN, MAX, SMALL, LARGE, MEDIAN and MODE
  - Answer conditional questions with COUNTIF(S), SUMIF(S), AVERAGEIF(S), MAXIFS and MINIFS
  - Use SUBTOTAL and AGGREGATE for filtered data and data with errors
---

## Formula vs function

:::def Two words people mix up
A **formula** is any calculation that starts with `=`. It can use cell references, numbers, operators and functions: `=B2*C2`, `=(B2-C2)/C2`, `=SUM(B2:B10)*1.18`.
A **function** is a named, ready-made calculation inside a formula: `SUM`, `AVERAGE`, `IF`. A function has a name, brackets and **arguments** separated by commas.
:::

```python fig: Anatomy of a function call. Arguments in square brackets are optional.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 2.6)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 3)
parts = [("=", 0.4, dg.INK), ("SUMIFS", 1.35, dg.VIO), ("(", 2.15, dg.INK), ("F2:F21", 3.05, dg.TEAL), (",", 3.75, dg.INK), ("C2:C21", 4.45, dg.CORAL), (",", 5.1, dg.INK), ('"Finance"', 5.9, dg.GOLD), (")", 6.75, dg.INK)]
for t, x, c in parts: ax.text(x, 2.0, t, fontsize=20, family="DejaVu Sans Mono", color=c, ha="center", weight="bold")
for x, lab, c in [(0.4, "starts\nevery formula", dg.INK), (1.35, "function\nname", dg.VIO), (3.05, "sum_range\n(what to add)", dg.TEAL), (4.45, "criteria_range1\n(where to look)", dg.CORAL), (5.9, "criteria1\n(what to match)", dg.GOLD)]:
    ax.annotate(lab, xy=(x, 1.75), xytext=(x, .45), ha="center", fontsize=9.5, color=c, arrowprops=dict(arrowstyle="-|>", color=c))
ax.text(8.6, 2.05, "→ 6,70,000", fontsize=15, color=dg.INK, va="center"); ax.text(8.6, 1.5, "total Finance salary", fontsize=9, color="#555", ha="left")
fig
```

When you type a function name and `(`, Excel shows a tooltip with its syntax, for example `SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], …)`. Press `Ctrl + A` after the bracket to open the **Function Arguments** dialog, which explains every argument and previews the result.

## Operators and order of calculation

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+ - * /` | Add, subtract, multiply, divide | `=10+4*2` | 18 |
| `^` | Power | `=2^10` | 1024 |
| `%` | Percent | `=500*18%` | 90 |
| `&` | Join text | `="Q"&2` | Q2 |
| `= <> > < >= <=` | Comparison, returns TRUE/FALSE | `=B2>=100` | TRUE or FALSE |
| `:` | Range | `A1:A10` | 10 cells |
| `,` | Union (inside functions) | `=SUM(A1:A3,C1:C3)` | Adds both ranges |

Excel follows the usual maths order, remembered as **BODMAS/PEMDAS**: brackets, then `^`, then `*` and `/`, then `+` and `-`, then `&`, then comparisons.

```xl title="Order of operations"
Formula{h}|Result{h}|Why{h}
'=10+4*2|=10+4*2|Multiply first: 10 + 8
'=(10+4)*2|=(10+4)*2|Brackets first: 14 × 2
'=2^3^2|=2^3^2|Excel works left to right: (2^3)^2 = 64
'=-2^2|=-2^2|Negation before power in Excel: (-2)^2 = 4
'=100*(1+18%)|=100*(1+18%)|Add 18% GST
```

:::warn `-2^2` is 4 in Excel
In maths `-2²` is −4, but Excel applies the minus sign first. Write `=-(2^2)` if you mean −4. This catches people in finance formulas.
:::

## Cell references: relative, absolute and mixed

When you copy a formula, Excel adjusts its references **relative** to where you paste it. Usually that is exactly what you want. Sometimes a reference must stay fixed, for example a tax rate in one cell. A `$` sign locks the part after it.

| Reference | Copy down | Copy right | Name |
|---|---|---|---|
| `B2` | B3, B4 … | C2, D2 … | Relative |
| `$B$2` | stays `$B$2` | stays `$B$2` | Absolute |
| `B$2` | stays row 2 | C$2, D$2 … | Mixed (row locked) |
| `$B2` | B3, B4 … | stays column B | Mixed (column locked) |

Press **F4** while the cursor is on a reference to cycle `B2 → $B$2 → B$2 → $B2 → B2`.

### Absolute reference: one rate for every row

```xl title="GST rate in one input cell (G2) — formula in D2 is =B2*C2*$G$2, copied down"
Item{h}|Qty{h}|Price{h}|GST amount{h}|Total{h}||GST rate{h}
Notebook|10|45|=B2*C2*$G$2{;#,##0.00}|=B2*C2+D2{;#,##0.00}||18%{y}
Pen pack|25|60|=B3*C3*$G$2{;#,##0.00}|=B3*C3+D3{;#,##0.00}||
Stapler|4|180|=B4*C4*$G$2{;#,##0.00}|=B4*C4+D4{;#,##0.00}||
```

The GST rate lives in one input cell (yellow). Because `$G$2` is absolute, every copied formula still points to it. Change the rate once and every total updates.

### Mixed references: the multiplication table test

A classic interview question: write **one** formula in B2 that can be copied across and down to fill a multiplication table.

```xl title="One formula, =$A2*B$1, filled across and down"
×{h}|1{h}|2{h}|3{h}|4{h}|5{h}
1{h}|=$A2*B$1|=$A2*C$1|=$A2*D$1|=$A2*E$1|=$A2*F$1
2{h}|=$A3*B$1|=$A3*C$1|=$A3*D$1|=$A3*E$1|=$A3*F$1
3{h}|=$A4*B$1|=$A4*C$1|=$A4*D$1|=$A4*E$1|=$A4*F$1
4{h}|=$A5*B$1|=$A5*C$1|=$A5*D$1|=$A5*E$1|=$A5*F$1
5{h}|=$A6*B$1|=$A6*C$1|=$A6*D$1|=$A6*E$1|=$A6*F$1
```

`$A2` always uses column A (the row header) and `B$1` always uses row 1 (the column header). The same idea is used for price × discount grids, sales × commission tables, and loan EMI tables.

```xl title="The same table in formula view" formulas
×{h}|1{h}|2{h}|3{h}
1{h}|=$A2*B$1|=$A2*C$1|=$A2*D$1
2{h}|=$A3*B$1|=$A3*C$1|=$A3*D$1
3{h}|=$A4*B$1|=$A4*C$1|=$A4*D$1
```

### References to other sheets and workbooks

| Reference | Meaning |
|---|---|
| `=Sales!B2` | Cell B2 on the sheet named Sales |
| `='Sales 2026'!B2` | Quotes are needed when the sheet name has spaces |
| `=SUM(Jan:Mar!B2)` | A **3D reference**: B2 on every sheet from Jan to Mar |
| `=[Budget.xlsx]Plan!C5` | Another workbook (an external link; Data → Edit Links manages them) |

## Aggregate functions

Aggregate functions turn many values into one number. The examples below use the 20-row employee table stored on a sheet named `Emp` (columns: A emp_id, B name, C department, D city, E join_date, F salary, G rating).

```xl title="Aggregate functions on Emp (salary in F2:F21, rating in G2:G21)" with="Emp:employees_small.csv"
Question{h}|Formula{h}|Result{h}
Total salary|'=SUM(Emp!F2:F21)|=SUM(Emp!F2:F21){;#,##0}
How many numbers in salary|'=COUNT(Emp!F2:F21)|=COUNT(Emp!F2:F21)
How many non-empty names|'=COUNTA(Emp!B2:B21)|=COUNTA(Emp!B2:B21)
Empty cells in B2:B25|'=COUNTBLANK(Emp!B2:B25)|=COUNTBLANK(Emp!B2:B25)
Average salary|'=AVERAGE(Emp!F2:F21)|=AVERAGE(Emp!F2:F21){;#,##0}
Median salary|'=MEDIAN(Emp!F2:F21)|=MEDIAN(Emp!F2:F21){;#,##0}
Most common rating|'=MODE.SNGL(Emp!G2:G21)|=MODE.SNGL(Emp!G2:G21)
Lowest / highest salary|'=MIN(...) / =MAX(...)|=TEXT(MIN(Emp!F2:F21),"#,##0")&" / "&TEXT(MAX(Emp!F2:F21),"#,##0")
2nd highest salary|'=LARGE(Emp!F2:F21,2)|=LARGE(Emp!F2:F21,2){;#,##0}
3rd lowest salary|'=SMALL(Emp!F2:F21,3)|=SMALL(Emp!F2:F21,3){;#,##0}
Average rating (rounded)|'=ROUND(AVERAGE(Emp!G2:G21),2)|=ROUND(AVERAGE(Emp!G2:G21),2)
```

| Function | Counts or uses | Ignores |
|---|---|---|
| `COUNT` | Numbers (and dates) | Text, blanks, logical values typed in cells |
| `COUNTA` | Anything not empty (numbers, text, errors, `""` from formulas) | Truly empty cells |
| `COUNTBLANK` | Empty cells and cells with `""` | Everything else |
| `SUM`, `AVERAGE`, `MIN`, `MAX` | Numbers | Text and blanks in ranges |
| `MEDIAN` | Middle value of sorted numbers | Text and blanks |
| `MODE.SNGL` | Most frequent number | Text |
| `SMALL(range,k)`, `LARGE(range,k)` | k-th smallest or largest | Text and blanks |

:::tip AVERAGE ignores blanks but not zeros
A blank cell is left out of the average; a zero is counted. If "no data" is stored as 0, your average will be too low. Leave missing values blank, or use `AVERAGEIF(range,"<>0")`.
:::

:::new MEDIAN vs AVERAGE in salary data
Salaries are usually skewed by a few high earners, so the **median** describes a "typical" employee better than the average. You will meet this again in Statistics (ML track, Lesson 1).
:::

## Conditional aggregation: the IFS family

These are the most used analysis functions in Excel. They answer questions such as *"total sales in the North region for Technology in 2025"*.

| Function | Syntax |
|---|---|
| `COUNTIF` | `COUNTIF(range, criteria)` |
| `COUNTIFS` | `COUNTIFS(range1, criteria1, range2, criteria2, …)` |
| `SUMIF` | `SUMIF(range, criteria, [sum_range])` |
| `SUMIFS` | `SUMIFS(sum_range, range1, criteria1, range2, criteria2, …)` |
| `AVERAGEIF(S)` | Same pattern as SUMIF(S) |
| `MAXIFS`, `MINIFS` | `MAXIFS(max_range, range1, criteria1, …)` |

Note that `SUMIF` puts the sum range **last** while `SUMIFS` puts it **first**. Learn the `SUMIFS` pattern and use it even for one condition.

```xl title="Conditional aggregation on Emp" with="Emp:employees_small.csv"
Question{h}|Result{h}|Formula{h}
Employees in Finance|=COUNTIF(Emp!C2:C21,"Finance")|'=COUNTIF(Emp!C2:C21,"Finance")
Finance employees in Delhi|=COUNTIFS(Emp!C2:C21,"Finance",Emp!D2:D21,"Delhi")|'=COUNTIFS(Emp!C2:C21,"Finance",Emp!D2:D21,"Delhi")
Total Finance salary|=SUMIFS(Emp!F2:F21,Emp!C2:C21,"Finance"){;#,##0}|'=SUMIFS(Emp!F2:F21,Emp!C2:C21,"Finance")
Salary of people rated 4 or more|=SUMIFS(Emp!F2:F21,Emp!G2:G21,">=4"){;#,##0}|'=SUMIFS(Emp!F2:F21,Emp!G2:G21,">=4")
Average salary in HR|=AVERAGEIFS(Emp!F2:F21,Emp!C2:C21,"HR"){;#,##0}|'=AVERAGEIFS(Emp!F2:F21,Emp!C2:C21,"HR")
Highest salary in Sales|=MAXIFS(Emp!F2:F21,Emp!C2:C21,"Sales"){;#,##0}|'=MAXIFS(Emp!F2:F21,Emp!C2:C21,"Sales")
Joined in 2024 or later|=COUNTIFS(Emp!E2:E21,">="&DATE(2024,1,1))|'=COUNTIFS(Emp!E2:E21,">="&DATE(2024,1,1))
Names starting with "A"|=COUNTIF(Emp!B2:B21,"A*")|'=COUNTIF(Emp!B2:B21,"A*")
Salary between 80k and 1.2 lakh|=COUNTIFS(Emp!F2:F21,">=80000",Emp!F2:F21,"<=120000")|'=COUNTIFS(Emp!F2:F21,">=80000",Emp!F2:F21,"<=120000")
```

Let's confirm two of these with pandas, using the same file:

```python run
import pandas as pd
emp = pd.read_csv("employees_small.csv", parse_dates=["join_date"])
print("Finance headcount:", (emp.department == "Finance").sum())
print("Total Finance salary:", f"{emp.loc[emp.department == 'Finance', 'salary'].sum():,}")
print("Joined 2024 or later:", (emp.join_date >= "2024-01-01").sum())
```

### Writing criteria correctly

| Criteria | Meaning |
|---|---|
| `"Finance"` | Equal to Finance (not case-sensitive) |
| `"<>Finance"` | Not equal to Finance |
| `">=4"` | Greater than or equal to 4 (operator and number inside quotes) |
| `">="&H1` | Compare with the value in H1 (join with `&`) |
| `">="&DATE(2024,1,1)` | Compare with a date |
| `"*pune*"` | Contains "pune" |
| `"A*"` / `"*a"` | Starts with A / ends with a |
| `"?????"` | Exactly five characters |
| `""` | Blank cells |
| `"<>"` | Non-blank cells |

:::tip Build a summary table with one formula
Put departments in A2:A6 and the formula `=SUMIFS(Emp!$F$2:$F$21,Emp!$C$2:$C$21,$A2)` in B2, then copy down. The `$` signs keep the data ranges fixed while `$A2` moves to each department. In Microsoft 365 you can produce the department list itself with `=UNIQUE(Emp!C2:C21)` (Lesson 6).
:::

```xl title="Department summary built with SUMIFS and COUNTIFS" with="Emp:employees_small.csv"
Department{h}|Headcount{h}|Total salary{h}|Average salary{h}|% of payroll{h}
Finance|=COUNTIFS(Emp!$C$2:$C$21,$A2)|=SUMIFS(Emp!$F$2:$F$21,Emp!$C$2:$C$21,$A2){;#,##0}|=C2/B2{;#,##0}|=C2/$C$7{;0.0%}
HR|=COUNTIFS(Emp!$C$2:$C$21,$A3)|=SUMIFS(Emp!$F$2:$F$21,Emp!$C$2:$C$21,$A3){;#,##0}|=C3/B3{;#,##0}|=C3/$C$7{;0.0%}
IT|=COUNTIFS(Emp!$C$2:$C$21,$A4)|=SUMIFS(Emp!$F$2:$F$21,Emp!$C$2:$C$21,$A4){;#,##0}|=C4/B4{;#,##0}|=C4/$C$7{;0.0%}
Operations|=COUNTIFS(Emp!$C$2:$C$21,$A5)|=SUMIFS(Emp!$F$2:$F$21,Emp!$C$2:$C$21,$A5){;#,##0}|=C5/B5{;#,##0}|=C5/$C$7{;0.0%}
Sales|=COUNTIFS(Emp!$C$2:$C$21,$A6)|=SUMIFS(Emp!$F$2:$F$21,Emp!$C$2:$C$21,$A6){;#,##0}|=C6/B6{;#,##0}|=C6/$C$7{;0.0%}
Total{b}|=SUM(B2:B6){b}|=SUM(C2:C6){b;#,##0}|=C7/B7{b;#,##0}|=SUM(E2:E6){b;0.0%}
```

This little table is exactly what a pivot table does (Lesson 8), but with formulas you control every cell, which is useful for fixed report layouts.

## SUBTOTAL and AGGREGATE: totals for filtered data

`SUM` adds every row, including rows hidden by a filter. `SUBTOTAL` adds only **visible** rows, so the total changes as you filter.

`=SUBTOTAL(function_num, range)`

| function_num (ignores filtered rows) | 101–111 also ignore manually hidden rows | Function |
|---|---|---|
| 1 | 101 | AVERAGE |
| 2 | 102 | COUNT |
| 3 | 103 | COUNTA |
| 4 | 104 | MAX |
| 5 | 105 | MIN |
| 9 | 109 | SUM |

`AGGREGATE` does the same and can also **ignore error values**:
`=AGGREGATE(9, 6, D2:D100)` sums D2:D100 ignoring errors (option 6). `=AGGREGATE(14, 6, D2:D100, 2)` returns the 2nd largest value ignoring errors (14 = LARGE).

```xl title="AGGREGATE ignores the #DIV/0! error that breaks SUM" errors_ok
Value{h}|
120|
=10/0|
80|
SUM →|=SUM(A2:A4)
AGGREGATE(9,6,…) →|=AGGREGATE(9,6,A2:A4)
```

## Common formula errors and how to fix them

| Error | Example | Fix |
|---|---|---|
| `#DIV/0!` | `=C2/B2` with B2 = 0 | `=IFERROR(C2/B2,0)` or `=IF(B2=0,"",C2/B2)` |
| `#VALUE!` | `=A2+B2` where A2 is text | Convert text to numbers; check for spaces |
| `#REF!` | Deleted a referenced row | Undo, or rewrite the formula |
| `#NAME?` | `=SUMIFS(…,Finance)` without quotes | Put text criteria in quotes |
| Circular reference | `=SUM(A1:A10)` typed in A10 | Move the total outside the range |
| Wrong total after sorting | Mixed relative/absolute references | Lock ranges with `$` |

**Formulas → Formula Auditing** helps: **Trace Precedents** draws arrows to the cells a formula uses, **Trace Dependents** to cells that use it, **Show Formulas** (`` Ctrl + ` ``) shows every formula, and **Evaluate Formula** steps through a calculation (Lesson 11).

:::ai Do it with AI
Paste a formula into Copilot or a chat assistant and ask: *"Explain this Excel formula step by step and tell me what would make it return an error: `=SUMIFS(Sales!$F:$F,Sales!$C:$C,$A2,Sales!$E:$E,">="&$B$1)`."* Use AI to explain and draft formulas, then check the result on a few rows you can verify by hand.
:::

## Summary

:::key
- Formula = any calculation starting with `=`; function = a named calculation such as `SUM`.
- Order: brackets, power, multiply/divide, add/subtract, join, compare. In Excel `-2^2 = 4`.
- `$` locks a reference; **F4** cycles relative → absolute → mixed. Mixed references build 2-D tables with one formula.
- `COUNT` counts numbers; `COUNTA` counts non-empty; `COUNTBLANK` counts empty.
- `SUMIFS(sum_range, criteria_range, criteria, …)` and `COUNTIFS` answer most business questions.
- Criteria with operators go in quotes and join cell values with `&`: `">="&H1`.
- `SUBTOTAL(109,…)` sums only visible rows; `AGGREGATE` can also ignore errors.
:::

:::quiz
Q: You copy `=B2*$E$1` from C2 to C5. What is the formula in C5?
- `=B5*$E$4`
* `=B5*$E$1`
- `=B2*$E$1`
- `=E5*$B$1`
> B2 is relative and moves to B5; $E$1 is absolute and stays.

Q: Which formula, typed in B2 and copied across and down, builds a multiplication table with headers in row 1 and column A?
- `=A2*B1`
- `=$A$2*$B$1`
* `=$A2*B$1`
- `=A$2*$B1`
> Column A is locked for the row header, and row 1 is locked for the column header.

Q: A range contains 10, "abc", blank, 25, TRUE (typed). What does COUNT return?
* 2
- 3
- 4
- 5
> COUNT counts only numbers in a range: 10 and 25.

Q: Which formula totals Sales (D) where Region (B) is "North" AND Category (C) is "Technology"?
- `=SUMIF(B:B,"North",D:D)`
* `=SUMIFS(D:D,B:B,"North",C:C,"Technology")`
- `=SUMIFS(B:B,"North",C:C,"Technology",D:D)`
- `=COUNTIFS(B:B,"North",C:C,"Technology")`
> SUMIFS takes the sum range first, then pairs of criteria range and criteria.

Q: How do you count values in A2:A100 greater than the value in H1?
- `=COUNTIF(A2:A100,>H1)`
- `=COUNTIF(A2:A100,">H1")`
* `=COUNTIF(A2:A100,">"&H1)`
- `=COUNTIF(A2:A100,H1>)`
> The operator is text and is joined to the cell value with &.

Q: You filter a table to show only Pune. Which total updates to show only Pune's sales?
- `=SUM(D2:D500)`
* `=SUBTOTAL(109,D2:D500)`
- `=SUMIF(D2:D500,">0")`
- `=AGGREGATE(9,0,D2:D500)` with option 0
> SUBTOTAL 9/109 ignores rows hidden by a filter.
:::

:::exercise Superstore questions with formulas
Open `superstore_sales.csv` in Excel. Using only aggregate and IFS functions, find: (1) total sales; (2) number of order lines in the West region; (3) total profit for Technology in 2025; (4) average discount for Furniture; (5) the largest single order-line sale in the South.
???
Assuming columns: J region, L category, O sales, Q discount, R profit and B order_date (check your own column letters):
(1) `=SUM(O:O)`
(2) `=COUNTIFS(J:J,"West")`
(3) `=SUMIFS(R:R,L:L,"Technology",B:B,">="&DATE(2025,1,1),B:B,"<="&DATE(2025,12,31))`
(4) `=AVERAGEIFS(Q:Q,L:L,"Furniture")`
(5) `=MAXIFS(O:O,J:J,"South")`
Check your answers in Python with pandas (Python track, Lesson 22) or with a pivot table (Lesson 8): they must match exactly.
:::

:::interview Questions you may be asked
**Q: What is the difference between COUNT, COUNTA and COUNTBLANK?**
COUNT counts numeric cells, COUNTA counts every non-empty cell (including text and formulas returning ""), COUNTBLANK counts empty cells and cells containing "".

**Q: When would you use a mixed reference?**
When a formula is copied in two directions and must keep either the row or the column fixed, for example a price × quantity grid or a commission table: `=$A2*B$1`.

**Q: Why use SUMIFS instead of SUMIF?**
SUMIFS supports multiple conditions, has a consistent argument order (sum range first), and works for one condition too, so one pattern covers every case.

**Q: How do you total only visible rows after filtering?**
Use `SUBTOTAL(109, range)` or `AGGREGATE(9, 5, range)`; the Table Total Row does this automatically.
:::
