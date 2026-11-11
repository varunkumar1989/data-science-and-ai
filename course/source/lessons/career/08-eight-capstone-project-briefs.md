---
num: 8
title: Eight Capstone Project Briefs and the Portfolio Checklist
live: "Gap-fill lesson"
updated: "2026"
level: Advanced
duration: 150 min
summary: Choose one of eight portfolio-level capstone projects covering dashboards, churn prediction, an end-to-end data pipeline, an AI data analyst, an enterprise RAG assistant, an agent for business operations, an MCP business assistant and an industry-specific project. Each brief has requirements, deliverables and an evaluation rubric, and a checklist makes every project presentable to an employer.
datasets: [telecom_churn.csv, superstore_sales.csv, daily_sales.csv]
outcomes:
  - Scope a portfolio project with clear requirements and deliverables
  - Choose a project that matches your target role
  - Prepare a project so that an employer can review it in ten minutes
  - Evaluate your own work against the rubric before you show it
---

## How to use these briefs

Choose **two** projects, not eight: one that matches your target role closely, and one that shows a different skill. Each brief has the same parts: the problem, requirements, deliverables, the data to use, and the rubric the work will be judged against. Read the rubric first; it tells you what matters most.

## Project 1: Business analytics dashboard

- **Problem:** a regional sales manager needs to see revenue, margin and returns by region, category and month, and to spot where profit is falling.
- **Requirements:** a clean star schema; at least 8 measures in one measure table; a page for trends, a page for drill-down, and a page of exceptions; a filter for date and region.
- **Deliverables:** the report file, a 1-page guide for users, and a README explaining the data source and refresh.
- **Data:** `superstore_sales.csv`.
- **Rubric:** correctness of totals against a control (30%); clarity of the first page (25%); measures documented and tested (25%); usability on a phone or small screen (20%).

## Project 2: Customer churn prediction

- **Problem:** a telecom company wants to know which customers are likely to leave in the next month, so that a retention offer can be targeted.
- **Requirements:** a defined churn label; a train and test split that respects time; a baseline model; one stronger model; evaluation with precision, recall and a business cost; an explanation of the top drivers.
- **Deliverables:** a notebook, a short model card, and a one-page recommendation with the expected value of the offer.
- **Data:** `telecom_churn.csv`.
- **Rubric:** a sound split and leakage check (30%); evaluation that matches the business cost (30%); explanation in plain language (25%); reproducibility (15%).

## Project 3: End-to-end data engineering pipeline

- **Problem:** daily sales files arrive from several sources and must become a trusted reporting table.
- **Requirements:** raw, cleaned and reporting layers (medallion layout); idempotent loads with a key; data-quality checks (nulls, duplicates, row counts, reconciliation); a scheduled run; logs and a failure alert.
- **Deliverables:** code in a repository, a diagram of the layers, the test results, and a failure drill with notes.
- **Data:** `daily_sales.csv` split into daily files, plus a second file with customer data.
- **Rubric:** correctness and re-run safety (35%); tests and checks (25%); operations: schedule, logs, alerts (25%); documentation (15%).

## Project 4: AI-powered data analyst

- **Problem:** managers ask data questions in plain English and wait days for answers.
- **Requirements:** natural-language questions turned into safe SQL against a read-only database; a row limit; the SQL shown with each answer; a test set of 30 questions with known answers; a refusal for anything outside the data.
- **Deliverables:** the working assistant, the test set and its results, and a short note on errors found.
- **Data:** `superstore_sales.csv` loaded into a database.
- **Rubric:** accuracy on the test set (35%); safety (SELECT only, limits, no personal data) (25%); transparency (SQL shown, uncertainty stated) (25%); cost per question (15%).

## Project 5: Enterprise RAG knowledge assistant

- **Problem:** staff cannot find policies, procedures and past decisions across many documents.
- **Requirements:** chunking and indexing of at least 20 documents; retrieval with citations; "not found" when the answer is absent; access control so that restricted documents are never returned to unauthorised users; an evaluation of retrieval and answers.
- **Deliverables:** the assistant, an evaluation report with retrieval hit rate and citation accuracy, and an access-control test.
- **Rubric:** retrieval quality (30%); grounded answers with correct citations (30%); access control (20%); evaluation and monitoring (20%).

## Project 6: AI agent for business operations

- **Problem:** a support team wants an agent that triages tickets, looks up orders and drafts replies, with approval for anything that changes a record.
- **Requirements:** read tools and at least one write tool behind approval; a step limit and budget; a regression suite of at least 30 tasks including forbidden actions; traces; cost per successful task.
- **Deliverables:** the agent, the suite and its results, the trace of a sample run, and a release checklist.
- **Rubric:** task completion on the suite (30%); safety tests passed (30%); traces and monitoring (20%); cost and latency (20%).

## Project 7: MCP-powered business assistant

- **Problem:** one assistant should answer questions using a CRM, a ticket system and a help centre, through a common protocol.
- **Requirements:** an MCP server with read tools for two systems (you may use sample data), scoped permissions per tool, logging of every call, and an injection test.
- **Deliverables:** the server, a tool list with roles and fields, the logs of a demo session, and the test results.
- **Rubric:** tool design and scoping (30%); security tests (30%); logging and audit (20%); documentation for other developers (20%).

## Project 8: Industry-specific capstone (choose one)

Choose an industry you know (retail, real estate, healthcare administration, logistics, education, finance operations) and combine any two earlier projects around one question in that industry. Write the problem with a named user, a decision, the data you would need and the data you can actually obtain, and deliver a working version with a clear limit statement.

- **Rubric:** relevance to the industry and the user (35%); technical quality (35%); honesty about data and limits (30%).

## Portfolio checklist (every project)

- [ ] A README with the problem, the data source, how to run the project and the result.
- [ ] Code and data in a repository, with no secrets or personal data.
- [ ] Tests or checks, with the results shown.
- [ ] One chart, table or screenshot on the first page of the README.
- [ ] A clear limitations section, including what you would do next.
- [ ] A 5-minute walkthrough (video or written) that an employer can follow.
- [ ] The rubric, filled in honestly by you before you share the work.

:::interview What makes a portfolio project credible?
A specific problem, real or realistic data, a result that is checked against something, a clear statement of limits, and evidence that you tested it. Employers can tell a project that was finished from one that was only started; the checklist is how to finish it.
:::

::::key What to remember
- Choose two projects: one for your target role and one for a different skill.
- Read the rubric first and invest most effort where the marks are.
- Include tests, a limitations section and a walkthrough.
- A finished, honest project beats an ambitious one that is not finished.
::::

:::quiz
Q: How many projects should a candidate usually prepare?
- Eight, all at once
* Two: one for the target role and one for a different skill
- None
- One hundred
> Two finished projects are more persuasive than many unfinished ones.

Q: Which rubric item is common to nearly every brief?
- The colour scheme
* Correctness or quality of the core result, checked against something
- The number of pages
- The software version
> Every brief rewards verified results.

Q: Why must a RAG assistant refuse questions outside the documents?
- To save storage
* To avoid inventing answers, which is the main risk of the approach
- Because refusals are required by law
- To make the system slower
> A grounded assistant says when the documents do not answer.

Q: What belongs in the portfolio checklist's "limitations" section?
- Praise for the tool vendor
* The data gaps, assumptions and the next steps you would take
- A list of passwords
- Only the best result
> Stating limits makes a project credible.

Q: Which project is most suited to someone targeting a data engineering role?
- The AI data analyst only
* The end-to-end data engineering pipeline
- The churn dashboard only
- The MCP assistant only
> The pipeline demonstrates reliable loading, testing and operations.
:::

:::exercise Scope one project
Choose one brief and write a one-page plan: the user and decision, the data you will use, the three deliverables, the rubric weights, and the first milestone you can finish in one week. Share the plan with someone who works in your target role and ask for one change.
???
Hints: pick data you can actually obtain. If the brief asks for an enterprise feature, scope a smaller version and state what is missing. Put the rubric weights in your plan so that you prioritise the largest one first.
:::
