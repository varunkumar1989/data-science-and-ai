---
num: 5
title: Text Functions, Logical Functions & IF
live: "Live classes 3–4"
updated: "Excel for Microsoft 365, 2026"
level: Beginner
duration: 120 min
summary: Extract, clean, combine and reformat text with LEFT, RIGHT, MID, LEN, FIND, SEARCH, CONCAT, TEXTJOIN, TEXT and the new TEXTSPLIT/TEXTBEFORE/TEXTAFTER. Then make decisions with AND, OR, NOT, IF, nested IF, IFS, SWITCH and IFERROR.
datasets: [superstore_sales.csv, employees_small.csv]
outcomes:
  - Extract parts of codes, names and emails with LEFT, RIGHT, MID, FIND and SEARCH
  - Combine text with &, CONCAT and TEXTJOIN and format numbers inside text with TEXT
  - Split text with Text to Columns and the TEXTSPLIT, TEXTBEFORE and TEXTAFTER functions
  - Build conditions with AND, OR, NOT and decisions with IF, nested IF, IFS and SWITCH
  - Handle errors cleanly with IFERROR and IFNA
---

## Why text functions matter

Real data arrives as text: order IDs like `IN-2025-00042`, product codes, email addresses, "Last, First" names, addresses and free-text comments. Text functions let you pull out the part you need (the year, the region code, the domain) so you can analyse it.

## Measuring and extracting text

| Function | What it returns | Example | Result |
|---|---|---|---|
| `LEN(text)` | Number of characters | `=LEN("Pune")` | 4 |
| `LEFT(text, n)` | First n characters | `=LEFT("IN-2025-00042",2)` | IN |
| `RIGHT(text, n)` | Last n characters | `=RIGHT("IN-2025-00042",5)` | 00042 |
| `MID(text, start, n)` | n characters from position start | `=MID("IN-2025-00042",4,4)` | 2025 |
| `FIND(find, text, [start])` | Position of text (case-sensitive, no wildcards) | `=FIND("-","IN-2025-00042")` | 3 |
| `SEARCH(find, text, [start])` | Position (not case-sensitive, wildcards allowed) | `=SEARCH("pune","PUNE-411001")` | 1 |

```xl title="Extracting parts of an order ID"
Order ID{h}|Country =LEFT(A2,2){h}|Year =MID(A2,4,4){h}|Order no. =RIGHT(A2,5){h}|Length{h}|Year as number{h}
IN-2025-00042|=LEFT(A2,2)|=MID(A2,4,4)|=RIGHT(A2,5)|=LEN(A2)|=VALUE(MID(A2,4,4))
IN-2023-01519|=LEFT(A3,2)|=MID(A3,4,4)|=RIGHT(A3,5)|=LEN(A3)|=VALUE(MID(A3,4,4))
IN-2024-02988|=LEFT(A4,2)|=MID(A4,4,4)|=RIGHT(A4,5)|=LEN(A4)|=VALUE(MID(A4,4,4))
```

Text functions always return **text**. `MID(A2,4,4)` returns the text `"2025"`, not the number 2025. Wrap with `VALUE()` (or multiply by 1) to get a number you can compare or add.

### When the position changes: FIND + MID

Codes rarely have fixed lengths. Combine `FIND` with `LEFT`, `MID` and `RIGHT` to cut at a delimiter wherever it is.

```xl title="Splitting emails at the @ sign"
Email{h}|Position of @{h}|User name{h}|Domain{h}
kavya.iyer@abc.in|=FIND("@",A2)|=LEFT(A2,FIND("@",A2)-1)|=MID(A2,FIND("@",A2)+1,100)
imran@datacorp.com|=FIND("@",A3)|=LEFT(A3,FIND("@",A3)-1)|=MID(A3,FIND("@",A3)+1,100)
harpreet.k@skillnavora.in|=FIND("@",A4)|=LEFT(A4,FIND("@",A4)-1)|=MID(A4,FIND("@",A4)+1,100)
```

Using a large number like 100 in `MID` simply means "take everything to the end". Alternatively use `=RIGHT(A2,LEN(A2)-FIND("@",A2))`.

```xl title="First and last name from 'First Last'"
Full name{h}|First name{h}|Last name{h}|Initials{h}
Kavya Iyer|=LEFT(A2,FIND(" ",A2)-1)|=MID(A2,FIND(" ",A2)+1,50)|=LEFT(A2,1)&LEFT(C2,1)
Harpreet Kulkarni|=LEFT(A3,FIND(" ",A3)-1)|=MID(A3,FIND(" ",A3)+1,50)|=LEFT(A3,1)&LEFT(C3,1)
Aarav Kulkarni|=LEFT(A4,FIND(" ",A4)-1)|=MID(A4,FIND(" ",A4)+1,50)|=LEFT(A4,1)&LEFT(C4,1)
```

### FIND vs SEARCH

| | FIND | SEARCH |
|---|---|---|
| Case-sensitive | Yes: `FIND("a","Apple")` → #VALUE! | No: `SEARCH("a","Apple")` → 1 |
| Wildcards `*` `?` | No | Yes |
| Not found | `#VALUE!` | `#VALUE!` |

A common pattern to test whether text **contains** a word: `=ISNUMBER(SEARCH("chair",B2))` returns TRUE or FALSE.

## Changing and cleaning text

| Function | Purpose | Example → Result |
|---|---|---|
| `UPPER`, `LOWER`, `PROPER` | Change case | `=PROPER("new delhi")` → New Delhi |
| `TRIM` | Remove extra spaces | `=TRIM("  a   b ")` → a b |
| `CLEAN` | Remove non-printing characters | Line breaks from web data |
| `SUBSTITUTE(text, old, new, [n])` | Replace by content | `=SUBSTITUTE("2025-04-27","-","/")` → 2025/04/27 |
| `REPLACE(text, start, n, new)` | Replace by position | `=REPLACE("E101",1,1,"EMP")` → EMP101 |
| `REPT(text, n)` | Repeat text | `=REPT("★",4)` → ★★★★ |
| `EXACT(a, b)` | Case-sensitive comparison | `=EXACT("abc","ABC")` → FALSE |

:::tip Count how many times a character appears
`=LEN(A2)-LEN(SUBSTITUTE(A2,",",""))` counts commas in A2 (the length difference after removing them). Add 1 to count items in a comma-separated list.
:::

## Joining text

```xl title="Three ways to combine text"
First{h}|Last{h}|City{h}|With &{h}|CONCAT{h}|TEXTJOIN{h}
Kavya|Iyer|Mumbai|=A2&" "&B2&" ("&C2&")"|=CONCAT(A2," ",B2)|=TEXTJOIN(", ",TRUE,A2:C2)
Imran||Delhi|=A3&" "&B3&" ("&C3&")"|=CONCAT(A3," ",B3)|=TEXTJOIN(", ",TRUE,A3:C3)
```

- `&` is the quickest way to join a few pieces.
- `CONCAT` joins ranges as well as single cells (it replaces the older `CONCATENATE`).
- `TEXTJOIN(delimiter, ignore_empty, …)` puts a separator between items and can **skip blanks**, which is why row 3 shows "Imran, Delhi" without a double comma.

### Numbers and dates inside text: TEXT

Joining a number or date directly shows its raw value: `="Sales: "&A2` gives `Sales: 1234567.891`, and a date shows as `46139`. Use `TEXT(value, format)` to control how it appears.

```xl title="TEXT() inside labels"
Value{h}|Label formula result{h}
1234567.891|="Revenue: ₹"&TEXT(A2,"#,##0")
2026-04-27|="Report date: "&TEXT(A3,"dd mmm yyyy")
0.1834|="Growth: "&TEXT(A4,"0.0%")
2026-04-27|="Day: "&TEXT(A5,"dddd")
```

## Splitting text

**Text to Columns** (Lesson 2) splits once into static values. Microsoft 365 adds formula versions that update automatically:

| Function | Example | Result |
|---|---|---|
| `TEXTBEFORE(text, delimiter, [instance])` | `=TEXTBEFORE("kavya.iyer@abc.in","@")` | kavya.iyer |
| `TEXTAFTER(text, delimiter, [instance])` | `=TEXTAFTER("IN-2025-00042","-",-1)` | 00042 (−1 = last hyphen) |
| `TEXTSPLIT(text, col_delim, [row_delim])` | `=TEXTSPLIT("North,South,East",",")` | spills North / South / East across three cells |

```xl title="TEXTSPLIT spills into neighbouring cells (Microsoft 365)"
Input{h}||||
IN-2025-00042|=TEXTSPLIT(A2,"-")=>>IN~2025~00042|||
Furniture|Chairs|Apex Chair 412||
=TEXTJOIN(" > ",TRUE,A3:C3)=>>Furniture > Chairs > Apex Chair 412||||
```

The blue cells are a **spill range**: one formula fills several cells. If any of those cells already contain something, the formula shows `#SPILL!` (Lesson 6).

:::new Regular expressions in Excel (2025)
Microsoft 365 has added `REGEXTEST`, `REGEXEXTRACT` and `REGEXREPLACE`. For example `=REGEXEXTRACT(A2,"\d{6}")` pulls a 6-digit PIN code out of an address, and `=REGEXTEST(A2,"^[\w.]+@[\w.]+\.\w+$")` checks that an email looks valid. They are covered with Python regex in the Python track.
:::

## Logical functions: TRUE or FALSE

Comparisons such as `=B2>100` return TRUE or FALSE. Logical functions combine them:

| Function | Returns TRUE when | Example |
|---|---|---|
| `AND(c1, c2, …)` | **All** conditions are TRUE | `=AND(B2>=4, C2="Sales")` |
| `OR(c1, c2, …)` | **At least one** condition is TRUE | `=OR(D2="Delhi", D2="Mumbai")` |
| `NOT(c)` | The condition is FALSE | `=NOT(E2="Done")` |
| `XOR(c1, c2)` | An odd number of conditions are TRUE | Rarely needed |

```xl title="AND, OR and NOT on employee data"
Name{h}|Department{h}|City{h}|Rating{h}|Salary{h}|Sales & rating≥4{h}|Metro city{h}|Not HR{h}
Kavya Iyer|HR|Mumbai|4|97000|=AND(B2="Sales",D2>=4)|=OR(C2="Delhi",C2="Mumbai")|=NOT(B2="HR")
Isha Mehta|Sales|Delhi|3|57000|=AND(B3="Sales",D3>=4)|=OR(C3="Delhi",C3="Mumbai")|=NOT(B3="HR")
Aadhya Nair|Sales|Bengaluru|5|45000|=AND(B4="Sales",D4>=4)|=OR(C4="Delhi",C4="Mumbai")|=NOT(B4="HR")
Krishna Khan|Sales|Mumbai|3|156000|=AND(B5="Sales",D5>=4)|=OR(C5="Delhi",C5="Mumbai")|=NOT(B5="HR")
```

:::tip TRUE = 1, FALSE = 0
In arithmetic Excel treats TRUE as 1 and FALSE as 0. `=SUM(--(D2:D21>=4))` counts ratings of 4 or more (the double minus converts TRUE/FALSE to 1/0). This trick powers `SUMPRODUCT` in Lesson 6.
:::

## IF: making decisions

`=IF(logical_test, value_if_true, value_if_false)`

```python fig: IF checks a condition and returns one of two results.
dg.flow(["Salary ≥ 1,00,000 ?", "TRUE → \"High\"", "FALSE → \"Standard\""], colors=[dg.VIO, dg.TEAL, dg.CORAL], title="=IF(F2>=100000, \"High\", \"Standard\")")
```

```xl title="IF in practice"
Name{h}|Salary{h}|Rating{h}|Band{h}|Bonus (10% if rating ≥ 4){h}|Pass/Fail target 80k{h}
Kavya Iyer|97000|4|=IF(B2>=100000,"High","Standard")|=IF(C2>=4,B2*10%,0){;#,##0}|=IF(B2>=80000,"Pass","Fail")
Imran Reddy|157000|3|=IF(B3>=100000,"High","Standard")|=IF(C3>=4,B3*10%,0){;#,##0}|=IF(B3>=80000,"Pass","Fail")
Isha Mehta|57000|3|=IF(B4>=100000,"High","Standard")|=IF(C4>=4,B4*10%,0){;#,##0}|=IF(B4>=80000,"Pass","Fail")
Vikram Joshi|75000|5|=IF(B5>=100000,"High","Standard")|=IF(C5>=4,B5*10%,0){;#,##0}|=IF(B5>=80000,"Pass","Fail")
```

IF can return text, numbers, another formula's result, or `""` (an empty-looking cell).

### Combining IF with AND and OR

```xl title="IF + AND / OR"
Name{h}|Dept{h}|Rating{h}|Years{h}|Promotion: rating ≥4 AND years ≥3{h}|Review: rating ≤2 OR years <1{h}
Kavya Iyer|HR|4|10|=IF(AND(C2>=4,D2>=3),"Eligible","Not yet")|=IF(OR(C2<=2,D2<1),"Review","OK")
Saanvi Rao|HR|4|1|=IF(AND(C3>=4,D3>=3),"Eligible","Not yet")|=IF(OR(C3<=2,D3<1),"Review","OK")
Aarav Kulkarni|HR|2|1|=IF(AND(C4>=4,D4>=3),"Eligible","Not yet")|=IF(OR(C4<=2,D4<1),"Review","OK")
Neha Menon|Sales|3|0|=IF(AND(C5>=4,D5>=3),"Eligible","Not yet")|=IF(OR(C5<=2,D5<1),"Review","OK")
```

### Nested IF vs IFS

For more than two outcomes, you can put an IF inside another IF (**nested IF**), or use **IFS**, which is easier to read.

```xl title="Grading marks: nested IF and IFS give the same result"
Marks{h}|Nested IF{h}|IFS{h}
92|=IF(A2>=90,"A",IF(A2>=75,"B",IF(A2>=60,"C","Fail")))|=IFS(A2>=90,"A",A2>=75,"B",A2>=60,"C",TRUE,"Fail")
78|=IF(A3>=90,"A",IF(A3>=75,"B",IF(A3>=60,"C","Fail")))|=IFS(A3>=90,"A",A3>=75,"B",A3>=60,"C",TRUE,"Fail")
60|=IF(A4>=90,"A",IF(A4>=75,"B",IF(A4>=60,"C","Fail")))|=IFS(A4>=90,"A",A4>=75,"B",A4>=60,"C",TRUE,"Fail")
41|=IF(A5>=90,"A",IF(A5>=75,"B",IF(A5>=60,"C","Fail")))|=IFS(A5>=90,"A",A5>=75,"B",A5>=60,"C",TRUE,"Fail")
```

:::mistake Order matters in nested IF and IFS
Excel stops at the **first** TRUE condition. If you test `A2>=60` first, a mark of 92 returns "C". Always test from the highest threshold to the lowest (or lowest to highest with `<`). In IFS, end with `TRUE, "default"` so values that match nothing do not return `#N/A`.
:::

### SWITCH: matching exact values

When you compare one value against a list of exact matches, `SWITCH` is cleaner than nested IFs.

```xl title="SWITCH maps codes to names"
Region code{h}|Region name{h}
N|=SWITCH(A2,"N","North","S","South","E","East","W","West","Unknown")
W|=SWITCH(A3,"N","North","S","South","E","East","W","West","Unknown")
X|=SWITCH(A4,"N","North","S","South","E","East","W","West","Unknown")
```

For long mappings, a lookup table with XLOOKUP (Lesson 7) is better than a long formula, because the mapping can be edited without touching formulas.

## Handling errors: IFERROR and IFNA

```xl title="IFERROR replaces any error with a value you choose" errors_ok
Sales{h}|Orders{h}|Average order{h}|With IFERROR{h}
120000|40|=A2/B2{;#,##0}|=IFERROR(A2/B2,0){;#,##0}
0|0|=A3/B3|=IFERROR(A3/B3,0){;#,##0}
95000|25|=A4/B4{;#,##0}|=IFERROR(A4/B4,0){;#,##0}
```

- `IFERROR(value, value_if_error)` catches **every** error type.
- `IFNA(value, value_if_na)` catches only `#N/A`, typically from lookups, so real problems such as `#REF!` stay visible.

:::warn Do not hide problems
Wrapping every formula in IFERROR can hide genuine mistakes (a deleted column, a typo). Use it where an error is expected and meaningful (division by zero, value not found), and prefer IFNA for lookups.
:::

## Case: building columns for the Superstore data

Here is how analysts typically enrich the Superstore order table with text and logical formulas before analysis. The same logic in pandas gives us the real results on all 6,323 rows:

```python run
import pandas as pd
s = pd.read_csv("superstore_sales.csv")
s["order_year"] = s["order_id"].str[3:7].astype(int)            # =VALUE(MID(A2,4,4))
s["product_brand"] = s["product_name"].str.split(" ").str[0]     # =TEXTBEFORE(N2," ")
s["profit_flag"] = s["profit"].apply(lambda p: "Loss" if p < 0 else "Profit")       # =IF(R2<0,"Loss","Profit")
s["discount_band"] = pd.cut(s["discount"], [-0.01, 0, 0.2, 1], labels=["No discount", "Up to 20%", "Above 20%"])  # =IFS(...)
s[["order_id", "order_year", "product_name", "product_brand", "discount", "discount_band", "profit", "profit_flag"]].head(6)
```

```python run
pd.crosstab(s["discount_band"], s["profit_flag"], margins=True)
```

The crosstab already tells a business story: almost every order-line with a discount above 20% makes a loss. You will build this same view as a pivot table in Lesson 8.

| New column | Excel formula (row 2) |
|---|---|
| Order year | `=VALUE(MID(B2,4,4))` |
| Brand | `=TEXTBEFORE(N2," ")` or `=LEFT(N2,FIND(" ",N2)-1)` |
| Profit flag | `=IF(S2<0,"Loss","Profit")` |
| Discount band | `=IFS(Q2=0,"No discount",Q2<=0.2,"Up to 20%",TRUE,"Above 20%")` |

:::ai Do it with AI
Prompt: *"Column B has order IDs like IN-2025-00042. Write an Excel formula to extract the year as a number, and another to flag orders where discount (Q) is above 20% and profit (S) is negative as 'Review'. Explain each part."* Expected answer: `=VALUE(MID(B2,4,4))` and `=IF(AND(Q2>0.2,S2<0),"Review","")`.
:::

## Summary

:::key
- `LEFT`, `RIGHT`, `MID` extract text; `FIND`/`SEARCH` locate a character so you can cut at a delimiter.
- Text functions return text: wrap with `VALUE()` to get numbers.
- Join with `&`, `CONCAT` or `TEXTJOIN` (which can skip blanks); format numbers inside labels with `TEXT`.
- `TEXTSPLIT`, `TEXTBEFORE` and `TEXTAFTER` split text with formulas that update.
- `AND` needs all conditions, `OR` needs any; TRUE counts as 1 in arithmetic.
- Use `IFS` (with a final `TRUE`) instead of deep nested IFs; order conditions from strictest to loosest.
- Use `IFERROR` for expected errors and `IFNA` for lookups.
:::

:::quiz
Q: What does `=MID("SKU-7781-BLU",5,4)` return?
- SKU-
* 7781
- 781-
- BLU
> MID starts at position 5 ("7") and takes 4 characters: 7781.

Q: A2 contains `ravi.verma@xyz.com`. Which formula returns `ravi.verma`?
* `=LEFT(A2,FIND("@",A2)-1)`
- `=LEFT(A2,FIND("@",A2))`
- `=RIGHT(A2,FIND("@",A2))`
- `=MID(A2,1,FIND(".",A2))`
> FIND returns 11 (the @ position); take 10 characters from the left.

Q: Which function joins A2:D2 with ", " and skips empty cells?
- `=CONCAT(A2:D2)`
* `=TEXTJOIN(", ",TRUE,A2:D2)`
- `=A2&", "&B2&", "&C2&", "&D2`
- `=TEXT(A2:D2,", ")`
> TEXTJOIN's second argument TRUE ignores empty cells.

Q: `=IF(A2>=60,"C",IF(A2>=75,"B","A"))` is used to grade a mark of 85. What is the result?
* C
- B
- A
- #VALUE!
> The first test (85 >= 60) is TRUE, so "C" is returned immediately. The conditions are in the wrong order.

Q: Why end an IFS formula with `TRUE,"Other"`?
- It makes IFS case-insensitive
* It returns a default value instead of #N/A when no condition matches
- It is required syntax
- It speeds up the calculation
> TRUE always matches, so it acts as the "else" branch.

Q: What does `="Total: "&TEXT(1234.5,"#,##0")` return?
- Total: 1234.5
* Total: 1,235
- Total: 1,234
- Total: #,##0
> TEXT formats the number with separators and no decimals, rounding 1234.5 to 1,235.
:::

:::exercise Product codes
Codes look like `FUR-CH-10001234` (category-subcategory-number). Write formulas for: (a) the category code; (b) the sub-category code; (c) the number as a value; (d) a flag "Furniture" when the category is FUR, otherwise "Other".
???
(a) `=LEFT(A2,3)` or `=TEXTBEFORE(A2,"-")`
(b) `=MID(A2,5,2)` or `=TEXTBEFORE(TEXTAFTER(A2,"-"),"-")`
(c) `=VALUE(RIGHT(A2,8))` or `=VALUE(TEXTAFTER(A2,"-",-1))`
(d) `=IF(LEFT(A2,3)="FUR","Furniture","Other")`
:::

:::exercise Commission rules
Sales reps get: 10% commission if sales ≥ 5,00,000; 7% if ≥ 3,00,000; 4% if ≥ 1,00,000; otherwise 0. Reps in the "Trainee" grade get half. Write one formula (sales in B2, grade in C2).
???
`=B2*IFS(B2>=500000,10%,B2>=300000,7%,B2>=100000,4%,TRUE,0)*IF(C2="Trainee",0.5,1)`
:::

:::interview Questions you may be asked
**Q: Difference between FIND and SEARCH?**
FIND is case-sensitive and does not allow wildcards; SEARCH is not case-sensitive and supports `*` and `?`. Both return `#VALUE!` when the text is not found.

**Q: How would you extract the domain from an email address?**
`=MID(A2,FIND("@",A2)+1,LEN(A2))` or, in Microsoft 365, `=TEXTAFTER(A2,"@")`.

**Q: Nested IF or IFS?**
IFS for readability when testing several conditions in order; SWITCH for exact matches of one value; a lookup table when the mapping is long or changes often.
:::
