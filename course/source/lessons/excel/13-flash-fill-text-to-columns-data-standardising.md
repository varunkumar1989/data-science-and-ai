---
num: 13
title: Flash Fill, Text to Columns and Standardising Messy Data
live: "Gap-fill lesson"
updated: "Excel for Microsoft 365, 2026"
level: Intermediate
duration: 120 min
summary: Clean messy exports fast. Use Flash Fill to learn a pattern from examples, Text to Columns to split values, and formulas to standardise case, spacing, phone numbers and dates, then check every result before you rely on it.
datasets: [customers.csv]
outcomes:
  - Use Flash Fill to split, join and reformat values from one example
  - Split a column with Text to Columns using a delimiter or fixed widths
  - Standardise case, spacing, phone numbers and dates with formulas
  - Check cleaned data with simple tests before it reaches a report
---

## Why cleaning comes first

Most analysis time goes into cleaning. A CRM export has names in capitals, phone numbers in four formats, dates stored as text and cities with extra spaces. Every report built on that data inherits its errors. Excel has three quick tools for standardising data: **Flash Fill**, **Text to Columns** and **text formulas**. This lesson uses all three and ends with checks.

:::case A messy customer list
A sales operations team receives a list of 200 customers from a partner. Names are in one column, phone numbers are mixed, cities have stray spaces and the join date is text. The CRM import rejects the file. The task is to fix it in under an hour, and to show the steps so the next import can be repeated.
:::

## Flash Fill: learn the pattern from one example

Flash Fill watches what you type and fills the rest of the column when it spots a pattern. Type the result for the first row, then start typing the second row. When Excel shows the grey preview of the remaining rows, press **Enter**. Or press **Ctrl+E** on a selected column.

Typical uses:

- Split a full name into first and last names.
- Join first name and last name with a space.
- Pull a code out of a longer text, such as the three-letter city code from "BLR-2025-0042".
- Reformat phone numbers into one pattern.

```xl title="Flash Fill example: names"
Full name as received{h}|First name (typed once){h}|Last name (typed once){h}
  asha   RAO|Asha|Rao
Vikram  Singh |Vikram|Singh
PRIYA mehta|Priya|Mehta
```

Type the first and second rows yourself, then use Ctrl+E on the empty cells. Excel learns that the first word is the first name and the last word is the last name.

::::warn Flash Fill is a guess
Flash Fill infers a rule from your examples and applies it everywhere. If the data has mixed patterns, one unusual row can produce a wrong result without any error message. Always scan the output, and sort or filter to look at the unusual cases.
::::

## Text to Columns: split one column into several

Text to Columns is for splitting a column in a fixed rule-based way. It is faster than formulas for one-off splits.

1. Select the column.
2. Go to **Data > Text to Columns**.
3. Choose **Delimited** (a comma, space, semicolon or other character) or **Fixed width** (positions).
4. Set the destination so that the original column is not overwritten by mistake.

Example: an address stored as "Plot 12, Indiranagar, Bengaluru, Karnataka" splits cleanly on commas. A product code "FUR-CH-10001234" splits on the hyphen into category, sub-category and number.

::::tip Keep the original
Text to Columns overwrites the column to the right when you press Finish. Copy the source column first, or set the destination cell to an empty column.
::::

## Standardising case and spacing

Three functions fix most text problems:

| Problem | Formula | Result from "  rAVI   kUMAR " |
|---|---|---|
| Extra spaces inside and at the ends | `=TRIM(A2)` | "rAVI kUMAR" |
| Consistent capitals | `=PROPER(A2)` | "Ravi Kumar" |
| Upper or lower case | `=UPPER(A2)`, `=LOWER(A2)` | "RAVI KUMAR" |

Combine them so that one formula cleans the value: `=PROPER(TRIM(A2))`. Nest `TRIM` inside `PROPER` so that the spaces are removed before the capitals are set.

```xl title="Standardise names and cities"
Raw name{h}|Raw city{h}|Clean name{h}|Clean city{h}|Check{h}
  rAVI   kUMAR |  bengaluru  |=PROPER(TRIM(A2))|=PROPER(TRIM(B2))|=IF(C2=PROPER(TRIM(A2)),"ok","check")
PRIYA   mehta|Mumbai|=PROPER(TRIM(A3))|=PROPER(TRIM(B3))|=IF(C3=PROPER(TRIM(A3)),"ok","check")
 sanjay  Reddy|  delhi |=PROPER(TRIM(A4))|=PROPER(TRIM(B4))|=IF(C4=PROPER(TRIM(A4)),"ok","check")
```

`PROPER` capitalises the first letter of each word and lowers the rest, so "bengaluru" becomes "Bengaluru". For acronyms such as "IT" or "ID", `PROPER` gives "It" or "Id"; keep those in a lookup list and replace them afterwards.

::::note CLEAN() removes hidden characters
Text pasted from web pages can contain non-breaking spaces and line breaks that `TRIM` does not remove. Use `=TRIM(CLEAN(SUBSTITUTE(A2,CHAR(160)," ")))` when the data comes from a website or a PDF.
::::

## Standardising phone numbers

Phone numbers from different sources arrive as "98450 12345", "+91-98450-12345" and "(080) 2345 6789". A standard form, such as ten digits, makes matching and de-duplication reliable.

Step 1 removes the common separators with nested `SUBSTITUTE`:

```xl title="Keep only the digits of a phone number"
Raw number{h}|Without spaces and dashes{h}|Without brackets{h}|Last 10 digits{h}
+91-98450-12345|=SUBSTITUTE(SUBSTITUTE(A2,"-","")," ","")|=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(B2,"(",""),")","")," ","")|=RIGHT(C2,10)
(080) 2345 6789|=SUBSTITUTE(SUBSTITUTE(A3,"-","")," ","")|=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(B3,"(",""),")","")," ","")|=RIGHT(C3,10)
98450 12345|=SUBSTITUTE(SUBSTITUTE(A4,"-","")," ","")|=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(B4,"(",""),")","")," ","")|=RIGHT(C4,10)
```

`RIGHT(..., 10)` keeps the last ten digits, which removes the country code. Check the results: a number with fewer than ten digits after cleaning is an error to review.

## Converting text dates into real dates

A date stored as text, such as "15/03/2025" or "15-Mar-25", cannot be sorted or used in a timeline. Convert it with `DATE` (for numeric parts) or `DATEVALUE` (for recognised text), and check the result format.

```xl title="Text dates to real dates"
Text as received{h}|Day{h}|Month{h}|Year{h}|Real date{h}|Days since joining{h}
15/03/2025|=VALUE(LEFT(A2,2))|=VALUE(MID(A2,4,2))|=VALUE(RIGHT(A2,4))|=DATE(D2,C2,B2)|=TODAY()-E2
01/11/2024|=VALUE(LEFT(A3,2))|=VALUE(MID(A3,4,2))|=VALUE(RIGHT(A3,4))|=DATE(D3,C3,B3)|=TODAY()-E3
28/02/2025|=VALUE(LEFT(A4,2))|=VALUE(MID(A4,4,2))|=VALUE(RIGHT(A4,4))|=DATE(D4,C4,B4)|=TODAY()-E4
```

Splitting the parts yourself is safer than relying on the locale. A text "03/04/2025" means different months in India and the United States; explicit day, month and year parts remove that doubt.

::::warn Locale changes date meaning
Excel reads "03/04/2025" as 3 April in a day-first locale and as 4 March in a month-first locale. Use explicit parts, as above, whenever the source format is not confirmed.
::::

## Checking the clean data

Cleaning is not finished until you test it. Three simple checks catch most mistakes:

1. **Count check**: the number of rows before and after cleaning must match, unless you deliberately removed duplicates.
2. **Blank check**: `=COUNTBLANK(range)` should be zero for required columns.
3. **Pattern check**: `=SUMPRODUCT(--(LEN(range)<>10))` counts phone numbers that are not ten characters.

For duplicates, use **Data > Remove Duplicates** on a copy, or `=COUNTIF(range, A2)>1` to flag repeats before removing them.

```xl title="Quality flags on a cleaned list"
Customer{h}|Phone (clean){h}|Duplicate?{h}|Phone ok?{h}
Ravi Kumar|9845012345|=IF(COUNTIF(A$2:A$4,A2)>1,"duplicate","unique")|=IF(LEN(B2)=10,"ok","check")
Priya Mehta|9812345678|=IF(COUNTIF(A$2:A$4,A3)>1,"duplicate","unique")|=IF(LEN(B3)=10,"ok","check")
Ravi Kumar|98450|=IF(COUNTIF(A$2:A$4,A4)>1,"duplicate","unique")|=IF(LEN(B4)=10,"ok","check")
```

The third row is flagged twice: its name repeats and its number is too short. Both are reasons to contact the partner before import.

## A repeatable cleaning routine

1. Copy the raw data to a new sheet and never edit the original.
2. Trim, proper-case and remove hidden characters.
3. Split combined fields with Text to Columns or Flash Fill, checking each result.
4. Standardise phone numbers and dates with formulas, so the logic can be re-run.
5. Run the count, blank and pattern checks, and record what you found.
6. Save the final sheet with a date in the file name.

::::key What to remember
- Flash Fill (Ctrl+E) learns a pattern from examples and must be checked.
- Text to Columns splits by delimiter or position; copy the source first.
- `PROPER(TRIM(...))` is the standard text clean-up; add `CLEAN` for pasted text.
- Standardise phone numbers and dates with formulas, using explicit date parts.
- Test the result with count, blank and pattern checks before import.
::::

:::quiz
Q: Which shortcut runs Flash Fill on the selected column?
- Ctrl+F
* Ctrl+E
- Ctrl+R
- Alt+F4
> Ctrl+E is the Flash Fill shortcut.

Q: What does `=PROPER(TRIM(" rAVI   kUMAR "))` return?
- rAVI kUMAR
* Ravi Kumar
- RAVI KUMAR
- Ravi   Kumar
> TRIM removes extra spaces, then PROPER capitalises each word.

Q: Text to Columns overwrites which cells by default?
- The column on the left
* The columns to the right of the selected column
- The first row only
- Nothing; it always creates a new sheet
> Choose an empty destination to keep the original data.

Q: Why use explicit DATE(year, month, day) for text dates?
- DATE is faster than typing the value
* It removes the risk that the locale reads day and month in the wrong order
- It creates text dates
- It changes the time zone
> Explicit parts avoid day-month confusion.

Q: Which formula counts rows whose required column is blank?
- =COUNT(range)
- =COUNTA(range)
* =COUNTBLANK(range)
- =SUM(range)
> COUNTBLANK counts empty cells.
:::

:::exercise Clean a partner list
Using a sheet of 30 rows you create, with names in capitals, extra spaces, phone numbers in mixed formats and join dates as text in dd/mm/yyyy: (a) clean the names with `PROPER(TRIM())`; (b) produce a 10-digit phone column; (c) convert the dates to real dates; (d) add a flag column that marks duplicate names; (e) write a one-line summary showing how many rows failed the phone check.
???
Hints: (a) `=PROPER(TRIM(A2))`. (b) nest `SUBSTITUTE` for "-", " ", "(" and ")", then `=RIGHT(x,10)`. (c) `=DATE(RIGHT(C2,4), MID(C2,4,2), LEFT(C2,2))`. (d) `=IF(COUNTIF(A$2:A$31,A2)>1,"duplicate","unique")`. (e) `=SUMPRODUCT(--(LEN(B2:B31)<>10))`.
:::
