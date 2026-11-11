---
num: 15
title: Office Scripts, Power Automate and AI-Assisted Excel Formulas
live: "Gap-fill lesson"
updated: "Excel for Microsoft 365, 2026"
level: Advanced
duration: 120 min
summary: Automate Excel on the web with Office Scripts written in TypeScript, run them on a schedule with Power Automate, and use AI assistants to draft formulas, with a checklist for testing every formula before you rely on it.
datasets: [superstore_sales.csv]
outcomes:
  - Explain how Office Scripts differ from VBA macros
  - Record and edit an Office Script in Excel on the web
  - Trigger a script from Power Automate on a schedule
  - Test an AI-written formula on edge cases before using it
---

## Office Scripts: automation for Excel on the web

Office Scripts are automations written in **TypeScript** that run in Excel on the web and in Microsoft 365. They do not need a desktop macro, so they work on any device with a browser, and they can be started by Power Automate. Use them when the file lives in SharePoint or OneDrive and the team works in the browser.

| | VBA macro | Office Script |
|---|---|---|
| Language | VBA | TypeScript |
| Runs in | Excel desktop | Excel on the web and desktop (Microsoft 365) |
| Started by | Button, shortcut, Alt+F8 | Button, Power Automate, Excel on the web |
| File type | .xlsm | Normal .xlsx |
| Good for | Desktop-only tasks | Shared team files and scheduled runs |

:::case A Monday summary for the team
A team lead wants a summary sheet rebuilt every Monday from the shared sales file: totals by region, a sort by sales and a timestamp. The file is in SharePoint and edited by five people. A script runs at 7 a.m. through Power Automate, so the summary is ready before the team arrives.
:::

## Step 1: record and open a script

1. Open the workbook in Excel on the web.
2. Go to **Automate > Record Actions**.
3. Format a table, add a total row and sort it. Click **Stop**.
4. Open **Automate > Code Editor** to see the script.

The recorded script uses the Office Scripts API. It is written as a function, with the workbook passed in as `workbook`:

```typescript
function main(workbook: ExcelScript.Workbook) {
    let sheet = workbook.getActiveWorksheet();
    let range = sheet.getRange("A1:F1");
    range.getFormat().getFont().setBold(true);
    range.getFormat().getFill().setColor("#1E8E5A");
}
```

As with VBA, recorded code uses fixed addresses. Replace them with values that come from the data.

## Step 2: make the script adapt

This version finds the used range and totals the sales column, whatever its size:

```typescript
function main(workbook: ExcelScript.Workbook) {
    const sheet = workbook.getActiveWorksheet();
    const used = sheet.getUsedRange();
    const rowCount = used.getRowCount();

    // Column E holds sales; rows 2 to the last data row
    const sales = sheet.getRange(`E2:E${rowCount}`);
    const total = sales.getValues().reduce((sum, row) => sum + Number(row[0] || 0), 0);

    // Write the total in a labelled cell below the data
    sheet.getRange(`D${rowCount + 2}:E${rowCount + 2}`).setValues([["Total sales", total]]);
    sheet.getRange(`E${rowCount + 2}`).getFormat().setColumnWidth(110);
}
```

The `reduce` call adds up the numbers in JavaScript. Writing a total as a value is fine for a report; if the total must update as data changes, write a formula with `setFormula("=SUM(E2:E...)")` instead.

::::tip Prefer formulas for live totals
A script that writes a value stops being correct the moment the data changes. A script that writes a formula stays correct. Use values for a snapshot (for example, a Monday report that must not change later) and formulas for anything that people will keep editing.
::::

## Step 3: run it on a schedule with Power Automate

Office Scripts can be called from a Power Automate flow:

1. Create a flow with the trigger **Recurrence**, set to every Monday at 7:00.
2. Add the action **Excel Online (Business) > Run script**.
3. Choose the workbook from SharePoint or OneDrive, and the script name.
4. Optional: add **Send an email** to notify the team after the run.

Test the flow once by running it manually, and open the workbook to check the result before you rely on the schedule.

::::warn Scheduled runs need care
A scheduled script runs without anyone watching. Make sure it cannot overwrite the source data, works on a copy if the file is shared, and sends a notice when it fails. Keep the raw data on a separate sheet from the output.
::::

## AI-assisted formulas

AI tools inside Excel, such as Copilot, and general AI assistants can write formulas from a plain-language request. This is useful for drafting, and dangerous when the result is trusted without checking.

A good request names the columns, the logic and the output:

> "In column F, show 'High' if sales in column E are above 5000 and the region in column C is 'North' or 'South', otherwise 'Standard'. Use one formula."

A reasonable answer is:

```
=IF(AND(E2>5000, OR(C2="North", C2="South")), "High", "Standard")
```

Read the formula before you use it. Ask: does it match the rule, the column letters and the case of the text?

## Testing an AI-written formula

Every formula from an AI tool should pass four tests before it enters a report:

1. **Known answer**: pick three rows where you know the right result by hand and check them.
2. **Boundary values**: test exactly 5000 (is it "above"?), blank cells and zeros.
3. **Unexpected text**: test "north" in lower case, extra spaces and misspellings.
4. **Totals**: compare the total of the new column with an independent calculation, such as a pivot table.

```xl title="Test cases for the High/Standard formula"
Sales{h}|Region{h}|Expected{h}|Formula result{h}|Pass?{h}
6000|North|High|=IF(AND(A2>5000,OR(B2="North",B2="South")),"High","Standard")|=IF(D2=C2,"yes","NO")
5000|North|Standard|=IF(AND(A3>5000,OR(B3="North",B3="South")),"High","Standard")|=IF(D3=C3,"yes","NO")
7000|north|High|=IF(AND(A4>5000,OR(B4="North",B4="South")),"High","Standard")|=IF(D4=C4,"yes","NO")
```

All three rows pass. The third row passes because Excel's text comparison (`=`) ignores case, so "north" matches "North". That is the behaviour you want here, but you should know it is a choice, not an accident. If a future rule needed case-sensitive matching, the test would catch the difference only if you had written a case-sensitive expectation.

::::note Case sensitivity in Excel
Excel comparisons with `=` ignore case, so "north" equals "North". Use `EXACT(a, b)` only when case must matter.
::::

## Choosing the right tool

- **Repeated steps on a shared file in the browser**: Office Scripts, run by hand or by Power Automate.
- **Repeated steps on a desktop file**: a VBA macro.
- **Combining and cleaning many files**: Power Query, which refreshes with one click.
- **A one-off formula**: write it yourself, or check an AI draft with the four tests.

::::key What to remember
- Office Scripts are TypeScript automations for Excel on the web; they run without desktop macros.
- Power Automate can run a script on a schedule; test the flow manually first.
- Prefer formulas over values for totals that must keep updating.
- Test every AI-written formula with a known answer, boundary values, unexpected text and a total check.
::::

:::quiz
Q: What language are Office Scripts written in?
- VBA
- Python
* TypeScript
- C#
> Office Scripts use TypeScript and the Office Scripts API.

Q: Which tool can run an Office Script every Monday without someone opening the file?
- Power Query
* Power Automate with a Recurrence trigger
- Goal Seek
- Conditional Formatting
> A Recurrence trigger starts the flow on a schedule, and the flow runs the script.

Q: Why should a script that writes a total use a formula rather than a value if people keep editing the data?
- Values cannot be stored
* The value stops being correct when the data changes, while a formula updates
- Formulas are faster to write
- Scripts cannot write values
> Formulas recalculate; a pasted value does not.

Q: An AI-written formula gives the right result for the rows you tested. What should you do next?
- Use it in the report immediately
* Test boundary values, blanks and unexpected text before relying on it
- Delete it
- Convert it to a macro
> Passing one set of rows does not prove the formula handles every case.

Q: Does `=` in Excel distinguish "North" from "north"?
* No, text comparison with = ignores case
- Yes, always
- Only in pivot tables
- Only on Excel for the web
> Use EXACT if case must matter.
:::

:::exercise A scheduled summary
Record an Office Script that takes a sheet of sales lines, creates a new sheet called "Summary" with total sales by region using formulas (`=SUMIF`), and writes the run time in a labelled cell. Then write the Power Automate flow that runs it every weekday at 8:00. List the four tests you would run on the summary before the team sees it.
???
Hints: in the script, use `workbook.addWorksheet("Summary")` and `setFormula` with `=SUMIF(Data!C:C, A2, Data!E:E)`. For the timestamp, write `=NOW()` or the script's `new Date()` value with a label. Test with a known total, a region that has no sales, a blank row in the data, and a changed source value to see whether the summary updates.
:::
