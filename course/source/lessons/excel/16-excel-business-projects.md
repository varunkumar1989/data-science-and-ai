---
num: 16
title: Excel Business Projects: Complaints, Finance, Productivity and Segmentation
live: "Gap-fill lesson"
updated: "Excel for Microsoft 365, 2026"
level: Advanced
duration: 180 min
summary: Four portfolio-ready Excel projects, each from a business brief. Analyse customer complaints, build a financial performance tracker, measure employee productivity, and segment customers with a sales performance dashboard, using the skills from the course.
datasets: [hr_employees.csv, superstore_sales.csv, customer_reviews.csv]
outcomes:
  - Turn a business question into a clear analysis plan with a metric and a deliverable
  - Clean, model and analyse a dataset with formulas, pivot tables and Power Query
  - Build a one-page dashboard that answers the brief
  - Write a short recommendation that a manager can act on
---

## How to run a business project

Every project in this lesson follows the same five steps. Use them for any brief you meet in an interview or on the job.

1. **Brief**: write the business question in one sentence and name the decision it supports.
2. **Data**: list the sources and check their quality (see the cleaning lesson).
3. **Analyse**: calculate the metrics, using pivot tables and formulas.
4. **Visualise**: put the answer on one dashboard sheet with at most four charts.
5. **Recommend**: write three sentences: what you found, what to do, and how to measure it.

:::case Four briefs, one method
Each of the four briefs below came from a real team. Work through them in order. For each, produce the workbook, a dashboard sheet and a half-page note, which together make a portfolio piece.
:::

## Project 1: Customer complaint analysis

**Brief:** The customer experience head wants to know which complaint themes cost the most customer trust, and where to fix them first.

**Data:** a list of reviews with a rating (1 to 5) and a theme tag. The sample below is small so you can see the logic.

```xl title="Complaint table with a severity score"
Theme{h}|Average rating{h}|Mentions{h}|Share of mentions{h}|Priority score{h}
Delivery delay|2|42|=C2/SUM(C$2:C$5)|=C2*(5-B2)
Damaged item|1|18|=C3/SUM(C$2:C$5)|=C3*(5-B3)
Wrong product|2|25|=C4/SUM(C$2:C$5)|=C4*(5-B4)
Poor support|3|35|=C5/SUM(C$2:C$5)|=C5*(5-B5)
```

**Method:**

- Count mentions per theme with a pivot table, and average the rating per theme.
- Priority score combines frequency and severity: many complaints with low ratings score highest. The formula weights each mention by how far the rating falls below 5.
- Sort by priority score and show the top two themes on the dashboard.

**Deliverable:** the top two themes, their share of mentions, and one fix for each. Say how you would measure whether the fix worked: for example, delivery-delay mentions per 100 orders next quarter.

::::tip Frequency is not severity
A theme with many mentions and high ratings is annoying; a theme with fewer mentions and one-star ratings can cost more customers. The priority score keeps both in view. Explain the weighting to the manager, because it is a judgement.
::::

## Project 2: Financial performance tracker

**Brief:** The finance manager wants one sheet that tracks budget against actual spend by month, flags overspend, and shows the year-to-date position.

**Method:**

- Set up three tables: budget by category, actual spend by month, and a monthly summary.
- Use `SUMIFS` to total actuals by category and month, so the tracker updates when new rows are added.
- Flag overspend with conditional formatting, and show the variance in both rupees and percent.

```xl title="Budget against actual for one quarter"
Category{h}|Budget{h}|Actual{h}|Variance{h}|Variance %{h}|Status{h}
Salaries|300000|298500|=B2-C2|=D2/B2|=IF(C2>B2,"Over","Within")
Software|60000|66200|=B3-C3|=D3/B3|=IF(C3>B3,"Over","Within")
Travel|45000|38900|=B4-C4|=D4/B4|=IF(C4>B4,"Over","Within")
Marketing|90000|97400|=B5-C5|=D5/B5|=IF(C5>B5,"Over","Within")
Total|=SUM(B2:B5)|=SUM(C2:C5)|=B6-C6|=D6/B6|=IF(C6>B6,"Over","Within")
```

**Deliverable:** the categories over budget, the total variance, and two actions (for example, review the software licences and set a marketing cap). Show the year-to-date position and a forecast for the rest of the year using the monthly run rate, labelled as an estimate.

::::warn Variance sign
Decide the sign convention before you build the tracker and state it on the sheet. Here, a positive variance means under budget. Mixing conventions is a common reason a manager misreads a finance report.
::::

## Project 3: Employee productivity dashboard

**Brief:** The HR director wants to understand what drives performance and attrition across departments, so that retention plans target the right teams. The data is the HR employee file.

**Method:**

- Load the file into Power Query, check for blanks and set the data types.
- Use a pivot table to compare departments on average performance rating, average monthly income, overtime share and attrition rate.
- Calculate the attrition rate with `COUNTIFS` (employees who left divided by all employees in each group).
- Compare overtime and satisfaction, which often explain attrition, using a pivot chart.

```xl title="Attrition and overtime by department (sample rows)"
Department{h}|Employees{h}|Left{h}|Attrition rate{h}|Overtime share{h}
Operations|300|84|=C2/B2|0.42
IT|280|42|=C3/B3|0.18
Sales|310|77|=C4/B4|0.36
Finance|180|27|=C5/B5|0.15
```

**Deliverable:** the department with the highest attrition, whether its overtime share is the likely driver, and a retention action with a measurable target (for example, cut overtime above 40 hours per month by half).

::::note Correlation is not a cause
Overtime and attrition can move together for several reasons. Say "associated with" rather than "caused by", and suggest a test: pilot a change in one team and compare it with another.
::::

## Project 4: Customer segmentation and sales performance dashboard

**Brief:** The commercial head wants to know which customer groups generate the most profit, which are at risk, and where the sales team should focus next quarter. The data is the retail sales file.

**Method:**

- Load the superstore data into Power Query, keep one row per order line, and build a customer summary: total sales, total profit, number of orders and last order date.
- Segment customers with a formula: for example, "Champion" when recent and high spend, "At risk" when no order in the last 180 days, and "Regular" otherwise.
- Build a pivot table of sales and profit by segment and region, and a slicer for year.
- Add a KPI row: total sales, profit margin, number of active customers and the share of profit from the top 20% of customers.

```xl title="Segment rules applied to a customer summary"
Customer{h}|Lifetime profit{h}|Days since last order{h}|Orders{h}|Segment{h}
C0765|15200|40|9|=IF(AND(B2>10000,C2<=180),"Champion",IF(C2>180,"At risk","Regular"))
C0112|1800|210|2|=IF(AND(B3>10000,C3<=180),"Champion",IF(C3>180,"At risk","Regular"))
C0498|9400|95|5|=IF(AND(B4>10000,C4<=180),"Champion",IF(C4>180,"At risk","Regular"))
```

**Deliverable:** the profit share of each segment, the number of customers at risk with their combined past profit, and one campaign for the at-risk group with its target and measurement. Be clear that the thresholds (10,000 profit, 180 days) are choices you made and can change.

::::tip Make the thresholds visible
Put segment thresholds in input cells, not inside formulas. A manager can then change 180 days to 120 and see the result immediately, without editing any formula.
::::

## Presenting the four projects

For a portfolio or interview, each project needs:

- the brief in one sentence,
- a dashboard with the answer in the first screen,
- the method in three or four bullet points,
- the recommendation with a measure of success,
- the limits of the data, stated plainly.

Stating the limits is what makes a project credible. Say which data was missing, which assumptions were made and what would change the answer.

::::key What to remember
- Start every project with the brief and the decision it supports.
- Build priority, budget and segment logic in formulas with visible thresholds.
- Use pivot tables and slicers for interactive answers; keep the dashboard to the question.
- Distinguish association from cause, and state the limits of the data.
- Every recommendation needs a target and a way to measure it.
::::

:::quiz
Q: In the complaint priority score, why multiply frequency by (5 minus the average rating)?
- To make the number bigger
* To give more weight to themes that are frequent and have low ratings
- To remove duplicates
- To convert ratings into percentages
> The score is high when a theme is common and poorly rated.

Q: Which function totals actual spend for a category and month that can change as rows are added?
- SUM on a fixed range
* SUMIFS over a range that covers the data
- COUNTA
- AVERAGE
> SUMIFS adds values that meet several conditions.

Q: A department's attrition rate is 84 leavers out of 300 employees. The rate is:
- 84%
* 28%
- 36%
- 300%
> 84 divided by 300 is 0.28, or 28%.

Q: Why put segment thresholds in input cells rather than in formulas?
- Formulas cannot use numbers
* A manager can change a threshold without editing every formula
- Input cells are faster
- It hides the logic
> Visible inputs make the model easy to test and change.

Q: Which statement is the most careful about overtime and attrition?
- Overtime causes attrition
* Overtime is associated with attrition; a pilot would show whether reducing it helps
- Attrition causes overtime
- Overtime has no relationship with attrition
> Association does not prove cause; test the change.
:::

:::exercise Pick one project and present it
Choose one of the four projects and build it end to end: a cleaned data sheet, the analysis in formulas and pivot tables, a dashboard sheet with at most four visuals, and a half-page note with the brief, the answer, one recommendation with a target, and the limits of the data.
???
Hints: start with the brief and write the recommendation first, then build only what the recommendation needs. Check that every number on the dashboard can be traced back to a formula or pivot table on the data sheet, and that the thresholds sit in visible input cells.
:::
