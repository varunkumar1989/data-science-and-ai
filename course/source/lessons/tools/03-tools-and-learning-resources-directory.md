---
num: 3
title: Tools and Learning Resources Directory: How to Choose and Evaluate Tools
live: "Gap-fill lesson"
updated: "2026"
level: Beginner
duration: 75 min
summary: Use a structured directory of tools across sixteen categories, from spreadsheets and SQL to MCP and portfolio tools, and evaluate any AI or no-code tool with a repeatable sheet covering purpose, features, limits, strengths, weaknesses and alternatives.
datasets: []
outcomes:
  - Find a tool in the directory by category and learning order
  - Evaluate an AI or no-code tool with the evaluation sheet
  - Check prices and features on the official page and record the date
  - Choose between alternatives with stated criteria
---

## Why a directory and a sheet

The tool landscape changes every few months. New products appear, prices change and features move between free and paid plans. Two things keep a learner or a team from being overwhelmed: a **directory** that groups tools by the job they do, and an **evaluation sheet** that gives every tool the same questions. This lesson shows how to use both.

:::case Which tool should we use?
A small team needs to automate a weekly report and is choosing between a no-code workflow tool, a spreadsheet macro and a small Python script. Without a common sheet, the choice depends on who demonstrates best. With one, the team can compare the same facts and decide.
:::

## The sixteen categories

| # | Category | Typical tools (examples) | Course link |
|---|---|---|---|
| 1 | Excel and spreadsheets | Microsoft Excel, Google Sheets | Excel track |
| 2 | SQL and databases | PostgreSQL, DuckDB, SQL Server | SQL track |
| 3 | Power BI and BI platforms | Power BI Desktop, Tableau | Power BI and Tableau tracks |
| 4 | Python and coding environments | Python, Jupyter, VS Code | Python track |
| 5 | Statistics and mathematics | Python statistics libraries, textbooks | ML track |
| 6 | Machine learning | scikit-learn | ML track |
| 7 | Data engineering | dbt, Airflow, Spark | Data engineering track |
| 8 | Cloud platforms | AWS, Azure, Google Cloud | Data engineering track |
| 9 | Generative AI | Model provider APIs and documentation | GenAI track |
| 10 | RAG and vector databases | Embedding services, vector stores | GenAI track |
| 11 | AI agents | Agent frameworks | Agents track |
| 12 | MCP and API development | MCP servers, OpenAPI tools | Agents track |
| 13 | No-code automation | n8n, Make, Zapier | Tools track |
| 14 | Git and development | Git, GitHub | Python track |
| 15 | Product and project management | Issue trackers, document tools | Governance track |
| 16 | Portfolio and interview preparation | Portfolio sites, practice platforms | Career track |

Each entry in a full directory should record: purpose, a beginner explanation, the official site, the official documentation, the official tutorial, whether it is free or paid, the course module it supports, a learning order and one exercise.

::::warn Check the official page, and note the date
Prices, limits and features change. Before you rely on any of them, open the official page, note the date you checked, and record the plan name exactly as the vendor shows it. Third-party summaries and comparison sites often disagree with each other.
::::

## The tool evaluation sheet

Use the same twelve questions for every tool you consider:

| Question | What to write |
|---|---|
| What does it do? | One sentence in plain language |
| Why use it? | The problem it solves for your task |
| Who should use it? | The role, skill level and team size it suits |
| Main features | Three to five features that matter for your task |
| Free, freemium or paid? | Exact plan names and what each includes, with the check date |
| Limits | Usage caps, data limits, rate limits, seats |
| Strengths | Two or three, with evidence from a test |
| Weaknesses | Two or three, with evidence from a test |
| Alternatives | Two other tools in the same category |
| Practical example | One real task you ran in it |
| Official documentation | The link you used |
| Exercise | One thing you can do in 30 minutes to try it |

## Using the sheet: a worked comparison

The team above compares three ways to automate the weekly report.

| Question | No-code workflow | Spreadsheet macro | Python script |
|---|---|---|---|
| Purpose | Connects apps on a schedule | Repeats steps in one workbook | Reads data, builds the report, logs runs |
| Who | Non-coders with several apps | Analysts who know the workbook | Analysts who can code |
| Main limit | Usage caps on the free plan | Only works in that file | Needs setup on the machine that runs it |
| Weakness | Hard to test complex logic | Fragile when data moves | Someone must maintain the code |
| Test in 30 minutes | Build the trigger and one step | Record a macro on sample data | Run the script on last week's file |

Decision rule: choose the least powerful tool that meets the requirement with the lowest maintenance cost. For a single workbook, a macro is enough. For many apps on a schedule, a workflow tool. For logic that must be tested and versioned, a script.

## How to learn a new tool in order

1. Read the purpose and the beginner explanation.
2. Complete the official tutorial with sample data.
3. Build one small task from your own work.
4. Write the evaluation sheet from what you saw, not from marketing pages.
5. Decide: keep, watch, or drop, with the reason.

:::interview How do you decide between two AI tools for a team?
Start with the task and the data. Score both tools on the same evaluation sheet, run each on the same three test cases, and compare cost per completed task, the errors found and how much human checking each needs. Decide on the measured result, record the date, and plan to re-check in six months.
:::

::::key What to remember
- A directory groups tools by the job they do, across sixteen categories.
- Use one evaluation sheet for every tool so that comparisons are fair.
- Check prices and features on official pages and record the date.
- Choose the least powerful tool that meets the requirement with the lowest upkeep.
::::

:::quiz
Q: Why use the same evaluation sheet for every tool?
- It is required by law
* It makes comparisons fair and based on the same facts
- It replaces testing
- It removes the need for alternatives
> Consistent questions reduce bias from demonstrations.

Q: Where should a tool's price be checked?
- On a comparison blog
* On the official page, with the check date recorded
- In a friend's message
- In the tool's marketing video
> Official pages are the reference; third-party summaries can be out of date.

Q: The decision rule in the lesson recommends:
- The most powerful tool available
* The least powerful tool that meets the requirement at the lowest upkeep
- The newest tool
- The most expensive tool
> Simplicity and maintenance cost are part of the decision.

Q: Which category would a tool for building an API description belong to?
- Excel and spreadsheets
* MCP and API development
- Statistics
- Portfolio
> OpenAPI and related tools fall under API development.

Q: What should a learner do after the official tutorial?
- Stop and move on
* Build one small task from their own work and write the evaluation sheet
- Buy the paid plan at once
- Share the tool on social media
> Hands-on use with your own task produces the real evidence.
:::

:::exercise Evaluate one tool
Choose one AI or no-code tool you use or are considering. Complete the twelve-question evaluation sheet using its official page, one 30-minute test on your own task, and a comparison with two alternatives. End with a keep, watch or drop decision and the date you checked the official pricing.
???
Hints: keep the test small and identical for each tool. Put the check date in the free-or-paid cell. If the official page does not state a limit, write "not stated" rather than guessing.
:::
