---
num: 9
title: Date, Time & Number Functions and Named Ranges
live: "Live classes 7–8"
updated: "Excel for Microsoft 365, 2026"
level: Intermediate
duration: 120 min
summary: Work confidently with dates and times (DATE, EOMONTH, EDATE, WORKDAY, NETWORKDAYS, WEEKDAY, WEEKNUM, DATEDIF, fiscal quarters), clean up numbers with INT, MOD, ROUND, CEILING and FLOOR, and make formulas readable with static and dynamic named ranges and LET.
datasets: [superstore_sales.csv, employees_small.csv]
outcomes:
  - Explain how Excel stores dates and times, and do date arithmetic correctly
  - Extract parts of dates, find month ends, add months, and count working days with holidays
  - Calculate age, tenure and fiscal-year quarters (Indian April–March and US October–September)
  - Use INT, MOD, ROUND, ROUNDUP, ROUNDDOWN, MROUND, CEILING.MATH, FLOOR.MATH, SQRT, POWER and ABS
  - Create static and dynamic named ranges and simplify long formulas with LET
---

## Dates and times are numbers

Excel stores a date as the number of days since **1 January 1900** (that day is 1). A time is a **fraction of a day**: 12:00 noon is 0.5 and 06:00 is 0.25. A date with a time is simply a whole number plus a fraction.

```xl title="What is really stored"
You see{h}|Stored as{h}|Explanation{h}
2026-04-27|=A2{;0}|Days since 1-Jan-1900
'12:00|=TIME(12,0,0){;0.0}|Half a day
'06:30|=TIME(6,30,0){;0.0000}|6.5 hours ÷ 24
'27-04-2026 18:00|=DATE(2026,4,27)+TIME(18,0,0){;0.00}|Date + time
```

This is why date arithmetic works:

```xl title="Date arithmetic"
Order date{h}|Ship date{h}|Days to ship =B2-A2{h}|Due date (+30 days){h}|Overdue? (as of 15-Jun-2026){h}
2026-04-27|2026-05-02|=B2-A2|=A2+30{;dd-mm-yyyy}|=IF(DATE(2026,6,15)>D2,"Overdue","OK")
2026-05-20|2026-05-21|=B3-A3|=A3+30{;dd-mm-yyyy}|=IF(DATE(2026,6,15)>D3,"Overdue","OK")
2026-06-01|2026-06-08|=B4-A4|=A4+30{;dd-mm-yyyy}|=IF(DATE(2026,6,15)>D4,"Overdue","OK")
```

:::tip TODAY() and NOW()
`=TODAY()` returns today's date and `=NOW()` the date and time. They are **volatile**: they recalculate every time the workbook changes, so results move every day. For reports that must not change, type the "as of" date into a cell and refer to it, as in the overdue example above. Shortcuts: `Ctrl + ;` types today's date as a fixed value.
:::

## Building and taking apart dates

| Function | Returns | Example (A2 = 27-04-2026) | Result |
|---|---|---|---|
| `DATE(y, m, d)` | A date from parts | `=DATE(2026,4,27)` | 27-04-2026 |
| `YEAR`, `MONTH`, `DAY` | Parts of a date | `=MONTH(A2)` | 4 |
| `WEEKDAY(date, 2)` | 1 = Monday … 7 = Sunday | `=WEEKDAY(A2,2)` | 1 |
| `WEEKNUM(date, 2)` | Week of the year (weeks start Monday) | `=WEEKNUM(A2,2)` | 18 |
| `ISOWEEKNUM(date)` | ISO 8601 week number | `=ISOWEEKNUM(A2)` | 18 |
| `TEXT(date, "mmm")` | Month name as text | `=TEXT(A2,"mmmm")` | April |
| `EOMONTH(date, n)` | Last day of the month n months away | `=EOMONTH(A2,0)` | 30-04-2026 |
| `EDATE(date, n)` | Same day n months later | `=EDATE(A2,3)` | 27-07-2026 |
| `DATEVALUE(text)` | Converts date text to a real date | `=DATEVALUE("27-Apr-2026")` | 46139 |

```xl title="Date parts and month boundaries"
Date{h}|Year{h}|Month{h}|Day{h}|Weekday (Mon=1){h}|Month end{h}|First of month{h}|+3 months{h}
2026-04-27|=YEAR(A2)|=MONTH(A2)|=DAY(A2)|=WEEKDAY(A2,2)|=EOMONTH(A2,0){;dd-mm-yyyy}|=EOMONTH(A2,-1)+1{;dd-mm-yyyy}|=EDATE(A2,3){;dd-mm-yyyy}
2026-01-31|=YEAR(A3)|=MONTH(A3)|=DAY(A3)|=WEEKDAY(A3,2)|=EOMONTH(A3,0){;dd-mm-yyyy}|=EOMONTH(A3,-1)+1{;dd-mm-yyyy}|=EDATE(A3,1){;dd-mm-yyyy}
2024-02-29|=YEAR(A4)|=MONTH(A4)|=DAY(A4)|=WEEKDAY(A4,2)|=EOMONTH(A4,0){;dd-mm-yyyy}|=EOMONTH(A4,-1)+1{;dd-mm-yyyy}|=EDATE(A4,12){;dd-mm-yyyy}
```

Notice that `EDATE` handles month ends correctly: 31-Jan + 1 month = 28-Feb (2026 is not a leap year), and 29-Feb-2024 + 12 months = 28-Feb-2025.

## Working days

| Function | Use |
|---|---|
| `NETWORKDAYS(start, end, [holidays])` | Count Mon–Fri days between two dates (inclusive) minus holidays |
| `NETWORKDAYS.INTL(start, end, weekend, [holidays])` | Choose weekend days: `11` = Sunday only, `"0000011"` = Sat + Sun |
| `WORKDAY(start, days, [holidays])` | The date after adding n working days |
| `WORKDAY.INTL(start, days, weekend, [holidays])` | Same with a custom weekend |

```xl title="SLA and delivery planning (holidays in G2:G4)"
Ticket{h}|Opened{h}|Closed{h}|Working days =NETWORKDAYS(B2,C2,$G$2:$G$4){h}|Due (+5 working days){h}||Holidays{h}
T-101|2026-08-10|2026-08-18|=NETWORKDAYS(B2,C2,$G$2:$G$4)|=WORKDAY(B2,5,$G$2:$G$4){;dd-mm-yyyy}||2026-08-15
T-102|2026-10-16|2026-10-23|=NETWORKDAYS(B3,C3,$G$2:$G$4)|=WORKDAY(B3,5,$G$2:$G$4){;dd-mm-yyyy}||2026-10-20
T-103|2026-11-06|2026-11-10|=NETWORKDAYS.INTL(B4,C4,11,$G$2:$G$4)|=WORKDAY.INTL(B4,5,11,$G$2:$G$4){;dd-mm-yyyy}||2026-11-08
```

T-103 uses a **Sunday-only weekend** (code `11`), common in Indian factories and retail. The holiday on 15-Aug-2026 falls on a Saturday, so it does not change T-101's count of working days.

## Age, tenure and durations

`DATEDIF(start, end, unit)` is a hidden function (no tooltip) that returns complete years, months or days between two dates.

| Unit | Returns |
|---|---|
| `"y"` | Complete years |
| `"m"` | Complete months |
| `"d"` | Days |
| `"ym"` | Months after removing complete years |
| `"md"` | Days after removing complete months |

```xl title="Tenure as of 31-Mar-2026 (in F1)"
Employee{h}|Join date{h}|Years{h}|Months after years{h}|Tenure label{h}|2026-03-31{y}
Kavya Iyer|2016-02-28|=DATEDIF(B2,$F$1,"y")|=DATEDIF(B2,$F$1,"ym")|=C2&" yrs "&D2&" mths"|
Imran Reddy|2019-12-14|=DATEDIF(B3,$F$1,"y")|=DATEDIF(B3,$F$1,"ym")|=C3&" yrs "&D3&" mths"|
Saanvi Rao|2025-02-18|=DATEDIF(B4,$F$1,"y")|=DATEDIF(B4,$F$1,"ym")|=C4&" yrs "&D4&" mths"|
```

(Cell F1 holds the date 31-03-2026.) For fractional years use `=YEARFRAC(B2,$F$1)`, for example 10.09 years.

## Fiscal years and quarters

Calendar quarter: `="Q"&ROUNDUP(MONTH(A2)/3,0)`. Many organisations use a different financial year:

| Year type | Q1 | Formula for the quarter number |
|---|---|---|
| Calendar | Jan–Mar | `=ROUNDUP(MONTH(A2)/3,0)` |
| **India (FY Apr–Mar)** | Apr–Jun | `=ROUNDUP(MOD(MONTH(A2)-4,12)/3+0.01,0)` or `=CHOOSE(MONTH(A2),4,4,4,1,1,1,2,2,2,3,3,3)` |
| **US federal (FY Oct–Sep)** | Oct–Dec | `=CHOOSE(MONTH(A2),2,2,2,3,3,3,4,4,4,1,1,1)` |

```xl title="Calendar, Indian FY and US FY quarters"
Date{h}|Calendar Q{h}|India FY quarter{h}|India FY label{h}|US FY quarter{h}
2026-02-10|="Q"&ROUNDUP(MONTH(A2)/3,0)|="Q"&CHOOSE(MONTH(A2),4,4,4,1,1,1,2,2,2,3,3,3)|="FY"&(YEAR(A2)+(MONTH(A2)>=4))-2000|="Q"&CHOOSE(MONTH(A2),2,2,2,3,3,3,4,4,4,1,1,1)
2026-04-27|="Q"&ROUNDUP(MONTH(A3)/3,0)|="Q"&CHOOSE(MONTH(A3),4,4,4,1,1,1,2,2,2,3,3,3)|="FY"&(YEAR(A3)+(MONTH(A3)>=4))-2000|="Q"&CHOOSE(MONTH(A3),2,2,2,3,3,3,4,4,4,1,1,1)
2026-11-03|="Q"&ROUNDUP(MONTH(A4)/3,0)|="Q"&CHOOSE(MONTH(A4),4,4,4,1,1,1,2,2,2,3,3,3)|="FY"&(YEAR(A4)+(MONTH(A4)>=4))-2000|="Q"&CHOOSE(MONTH(A4),2,2,2,3,3,3,4,4,4,1,1,1)
```

In the Indian convention, 27-Apr-2026 falls in **FY27** (April 2026 – March 2027), quarter Q1.

## Times

| Function | Example | Result |
|---|---|---|
| `TIME(h, m, s)` | `=TIME(14,30,0)` | 14:30 |
| `HOUR`, `MINUTE`, `SECOND` | `=HOUR(A2)` | 14 |
| Duration in hours | `=(end-start)*24` | 8.5 |
| Duration beyond 24 h | Format `[h]:mm` | 37:30 |
| Shifts past midnight | `=MOD(end-start,1)` | Works when end is the next day |

A very common clean-up task: a system exports times as plain numbers like `1430` meaning 14:30. Convert them with `INT` and `MOD`:

```xl title="Convert 1430-style numbers into real times"
Raw{h}|Hours =INT(A2/100){h}|Minutes =MOD(A2,100){h}|Time =TIME(INT(A2/100),MOD(A2,100),0){h}|Shift length (to B6){h}
930|=INT(A2/100)|=MOD(A2,100)|=TIME(INT(A2/100),MOD(A2,100),0){;hh:mm}|=MOD(D6-D2,1)*24{;0.00}
1430|=INT(A3/100)|=MOD(A3,100)|=TIME(INT(A3/100),MOD(A3,100),0){;hh:mm}|
2245|=INT(A4/100)|=MOD(A4,100)|=TIME(INT(A4/100),MOD(A4,100),0){;hh:mm}|
5|=INT(A5/100)|=MOD(A5,100)|=TIME(INT(A5/100),MOD(A5,100),0){;hh:mm}|
1815|=INT(A6/100)|=MOD(A6,100)|=TIME(INT(A6/100),MOD(A6,100),0){;hh:mm}|
```

## Number functions

| Function | What it does | Example | Result |
|---|---|---|---|
| `INT(n)` | Rounds **down** to the integer | `=INT(-7.6)` | −8 |
| `TRUNC(n, [d])` | Cuts off decimals (towards zero) | `=TRUNC(-7.6)` | −7 |
| `ROUND(n, d)` | Normal rounding | `=ROUND(7.456,2)` | 7.46 |
| `ROUNDUP(n, d)` | Always away from zero | `=ROUNDUP(7.401,0)` | 8 |
| `ROUNDDOWN(n, d)` | Always towards zero | `=ROUNDDOWN(7.99,0)` | 7 |
| `ROUND(n, -3)` | Round to thousands | `=ROUND(123456,-3)` | 123000 |
| `MROUND(n, m)` | Nearest multiple | `=MROUND(17,5)` | 15 |
| `CEILING.MATH(n, m)` | Up to the next multiple | `=CEILING.MATH(23,7)` | 28 |
| `FLOOR.MATH(n, m)` | Down to the previous multiple | `=FLOOR.MATH(23,7)` | 21 |
| `MOD(n, d)` | Remainder | `=MOD(28,3)` | 1 |
| `QUOTIENT(n, d)` | Integer part of a division | `=QUOTIENT(28,3)` | 9 |
| `ABS(n)` | Absolute value | `=ABS(-450)` | 450 |
| `SIGN(n)` | −1, 0 or 1 | `=SIGN(-450)` | −1 |
| `SQRT(n)` | Square root | `=SQRT(144)` | 12 |
| `POWER(n, p)` | Power (same as `^`) | `=POWER(25,2)` | 625 |

```xl title="Rounding functions side by side"
Value{h}|INT{h}|ROUND 0{h}|ROUNDUP 0{h}|ROUNDDOWN 0{h}|ROUND 2{h}|CEILING.MATH to 5{h}|FLOOR.MATH to 5{h}
7.456|=INT(A2)|=ROUND(A2,0)|=ROUNDUP(A2,0)|=ROUNDDOWN(A2,0)|=ROUND(A2,2)|=CEILING.MATH(A2,5)|=FLOOR.MATH(A2,5)
-7.456|=INT(A3)|=ROUND(A3,0)|=ROUNDUP(A3,0)|=ROUNDDOWN(A3,0)|=ROUND(A3,2)|=CEILING.MATH(A3,5)|=FLOOR.MATH(A3,5)
23.5|=INT(A4)|=ROUND(A4,0)|=ROUNDUP(A4,0)|=ROUNDDOWN(A4,0)|=ROUND(A4,2)|=CEILING.MATH(A4,5)|=FLOOR.MATH(A4,5)
```

### Practical uses

- **Packaging**: boxes needed for 523 items at 24 per box = `=CEILING.MATH(523,24)/24` or `=ROUNDUP(523/24,0)` → 22.
- **Price points**: round prices up to the next 99: `=CEILING.MATH(A2,100)-1` turns 1,234 into 1,299.
- **Split profit and loss** into two columns with `ABS`:

```xl title="Profit and Loss columns"
Store{h}|Profit / Loss{h}|Profit{h}|Loss{h}
Pune|45200|=IF(B2>0,B2,0)|=IF(B2<0,ABS(B2),0)
Delhi|-12800|=IF(B3>0,B3,0)|=IF(B3<0,ABS(B3),0)
Kochi|3300|=IF(B4>0,B4,0)|=IF(B4<0,ABS(B4),0)
Patna|-7600|=IF(B5>0,B5,0)|=IF(B5<0,ABS(B5),0)
Total{b}|=SUM(B2:B5){b}|=SUM(C2:C5){b}|=SUM(D2:D5){b}
```

## Named ranges

A **name** is a label for a cell, a range, a constant or a formula. `=SUM(Sales)` is easier to read and audit than `=SUM(Data!$O$2:$O$6324)`.

### Static named ranges

| Method | How |
|---|---|
| Name Box | Select the range, click the Name Box (left of the formula bar), type `GST_Rate`, press Enter |
| Define Name | Formulas → Define Name: set the name, scope (workbook or one sheet) and comment |
| Create from Selection | Select a table with headers → Formulas → Create from Selection (`Ctrl + Shift + F3`) → Top row: one name per column |
| Name Manager | Formulas → Name Manager (`Ctrl + F3`) to edit, delete or find broken names |

Rules: names start with a letter or underscore, contain no spaces (use `_`), cannot look like a cell address (`Q1` or `FY26` are not allowed) and are not case-sensitive.

```xl title="Formulas with names (GST_Rate = F1, Qty and Price are named columns)"
Qty{h}|Price{h}|Amount =Qty*Price{h}|With GST =Qty*Price*(1+GST_Rate){h}||18%{y}
4|1250|=A2*B2|=A2*B2*(1+$F$1){;#,##0.00}||
10|299|=A3*B3|=A3*B3*(1+$F$1){;#,##0.00}||
2|8999|=A4*B4|=A4*B4*(1+$F$1){;#,##0.00}||
```

(F1, the yellow cell, is named `GST_Rate`. With names defined, the formula in D2 reads `=Qty*Price*(1+GST_Rate)`.)

### Dynamic named ranges

A static name like `=$B$2:$B$100` does not grow when you add row 101. A **dynamic** named range expands automatically, which keeps charts, validation lists and formulas up to date.

| Method | Refers to | Notes |
|---|---|---|
| **Excel Table** (best) | `=tblSales[Amount]` | Automatic, no formula needed |
| `OFFSET` + `COUNTA` | `=OFFSET(Data!$B$2,0,0,COUNTA(Data!$B:$B)-1,1)` | Classic; volatile (recalculates often) |
| `INDEX` + `COUNTA` | `=Data!$B$2:INDEX(Data!$B:$B,COUNTA(Data!$B:$B))` | Not volatile; preferred over OFFSET |
| Spill reference | `=Data!$H$2#` | Points to a dynamic-array result |

```python fig: A static range stays fixed; a dynamic range grows with the data.
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.8))
for k, ax in enumerate(axs):
    ax.axis("off"); ax.set_xlim(0, 4); ax.set_ylim(0, 8.5)
    ax.set_title(["Static: =$B$2:$B$6", "Dynamic: =$B$2:INDEX($B:$B,COUNTA($B:$B))"][k], fontsize=10.5)
    for i in range(8):
        filled = i < 7
        ax.add_patch(Rectangle((1, 7 - i), 2, 1, fc="white", ec="#CCC")); ax.text(.6, 7.5 - i, str(i + 1), ha="center", va="center", color="#888")
        if i == 0: ax.text(2, 7.5, "Sales", ha="center", va="center", weight="bold")
        elif filled: ax.text(2.9, 7.5 - i, f"{[120, 95, 140, 88, 132, 101][i - 1]}", ha="right", va="center", color="#C2410C" if i == 6 else "black")
    if k == 0: ax.add_patch(Rectangle((1, 2), 2, 5, fill=False, ec=dg.CORAL, lw=2.4)); ax.text(3.2, 1.5, "new row 7\nis missed", color=dg.CORAL, fontsize=9.5)
    else: ax.add_patch(Rectangle((1, 1), 2, 6, fill=False, ec=dg.TEAL, lw=2.4)); ax.text(3.15, 1.5, "grows to\nrow 7", color=dg.TEAL, fontsize=9.5)
fig
```

### LET: names inside one formula

`LET` (Microsoft 365) assigns names to values **inside** a formula. It makes long formulas readable and faster, because each part is calculated once.

Without LET: `=IF(SUMIFS(F:F,C:C,"Finance")/COUNTIFS(C:C,"Finance")>90000,"High","Normal")`

With LET:
```excel
=LET(
    total, SUMIFS(F:F, C:C, "Finance"),
    heads, COUNTIFS(C:C, "Finance"),
    avg,   total / heads,
    IF(avg > 90000, "High", "Normal")
)
```

`LAMBDA` goes one step further and lets you create your own reusable functions; see Lesson 12.

## Case: date analysis on Superstore

How long do orders take to ship, by ship mode, and which weekday gets the most orders? In Excel you would add columns `=ship_date-order_date` and `=TEXT(order_date,"ddd")` and pivot them. Here are the real answers:

```python run
import pandas as pd
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date", "ship_date"])
orders = s.drop_duplicates("order_id").copy()
orders["days_to_ship"] = (orders.ship_date - orders.order_date).dt.days            # =C2-B2
orders["weekday"] = orders.order_date.dt.day_name().str[:3]                         # =TEXT(B2,"ddd")
orders["fy"] = "FY" + (orders.order_date.dt.year + (orders.order_date.dt.month >= 4)).astype(str).str[2:]   # Indian FY
print(orders.groupby("ship_mode")["days_to_ship"].agg(["mean", "min", "max"]).round(1).to_string())
print()
print(orders.groupby("fy").size().rename("orders").to_string())
```

## Summary

:::key
- Dates are whole numbers (days since 1-Jan-1900); times are fractions of a day. Subtract dates to get days; multiply time differences by 24 for hours.
- `EOMONTH` and `EDATE` handle month ends correctly; `NETWORKDAYS` and `WORKDAY` (with `.INTL` for custom weekends) handle working days and holidays.
- `DATEDIF` gives complete years/months; build fiscal quarters with `CHOOSE(MONTH(…),…)`.
- `INT` rounds down, `TRUNC` cuts towards zero, `ROUNDUP`/`ROUNDDOWN` force direction, `CEILING.MATH`/`FLOOR.MATH` round to multiples, `MOD` gives remainders.
- Named ranges make formulas readable; use Tables or `INDEX`-based names for dynamic ranges, and `LET` for names inside a formula.
:::

:::quiz
Q: A1 contains 27-04-2026 and B1 contains 02-05-2026. What does `=B1-A1` return?
- 5 days as text
* 5
- 0.05
- #VALUE!
> Dates are numbers, so subtracting gives the number of days.

Q: Which formula returns the last day of the month for the date in A2?
- `=DATE(YEAR(A2),MONTH(A2),31)`
* `=EOMONTH(A2,0)`
- `=EDATE(A2,1)-1`
- `=MONTH(A2)+30`
> EOMONTH(date,0) returns the month end; the other options fail for 30-day months or February.

Q: What does `=INT(-3.2)` return?
- −3
* −4
- 3
- −3.2
> INT always rounds down (towards minus infinity). TRUNC(-3.2) would give −3.

Q: Which formula converts the number 1745 into the time 17:45?
- `=TIME(1745)`
- `=1745/24`
* `=TIME(INT(A2/100),MOD(A2,100),0)`
- `=TEXT(1745,"hh:mm")`
> INT(1745/100) = 17 hours and MOD(1745,100) = 45 minutes.

Q: Why is an INDEX-based dynamic named range often preferred to OFFSET?
- It works only in Excel 365
* OFFSET is volatile and recalculates on every change, which can slow large workbooks
- INDEX cannot refer to whole columns
- OFFSET does not grow with the data
> Both grow, but OFFSET is volatile.

Q: In the Indian financial year, which quarter is 15-January?
- Q1
- Q2
- Q3
* Q4
> FY runs April–March, so January–March is Q4.
:::

:::exercise HR date calculations
Using `employees_small.csv` and an "as of" date of 31-03-2026 in a cell: (1) tenure in complete years; (2) the probation end date (6 months after joining); (3) the first working day after the probation end; (4) the joining quarter in the Indian FY.
???
With join date in E2 and the as-of date in $J$1:
(1) `=DATEDIF(E2,$J$1,"y")`
(2) `=EDATE(E2,6)`
(3) `=WORKDAY(EDATE(E2,6)-1,1)` (the first working day on or after the probation end)
(4) `="Q"&CHOOSE(MONTH(E2),4,4,4,1,1,1,2,2,2,3,3,3)`
:::

:::interview Questions you may be asked
**Q: How does Excel store dates and times?**
Dates as serial numbers counting days from 1-Jan-1900; times as fractions of a day. This makes arithmetic, sorting and formatting consistent.

**Q: How do you count working days between two dates excluding holidays?**
`NETWORKDAYS(start, end, holidays)` or `NETWORKDAYS.INTL` with a custom weekend code.

**Q: What is a dynamic named range and when do you need one?**
A name whose range grows with the data, built with an Excel Table, `INDEX`/`COUNTA` or `OFFSET`/`COUNTA`. It keeps charts, validation lists and formulas current as data is added.
:::
