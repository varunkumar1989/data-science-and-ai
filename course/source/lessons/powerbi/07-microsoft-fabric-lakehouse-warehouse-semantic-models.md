---
num: 7
title: Microsoft Fabric: Lakehouse, Warehouse, Dataflows and Semantic Models
live: "Gap-fill lesson"
updated: "Microsoft Fabric 2026"
level: Advanced
duration: 150 min
summary: Understand Microsoft Fabric as one platform. Load data into a lakehouse, shape it in a warehouse or dataflow, publish a semantic model that Power BI reports read from, and keep the whole chain governed and refreshed.
datasets: [adventure_cycles/fact_sales.csv, adventure_cycles/dim_customer.csv, adventure_cycles/dim_product.csv]
outcomes:
  - Describe the Fabric workspace items: lakehouse, warehouse, dataflow, notebook and semantic model
  - Choose between a lakehouse and a warehouse for a given workload
  - Load and shape data with a dataflow and with the SQL analytics endpoint
  - Publish a semantic model and connect a Power BI report to it
  - Explain OneLake, shortcuts and the refresh chain
---

## What Fabric is

**Microsoft Fabric** is a single platform for data work, built on one storage layer called **OneLake**. Instead of separate tools for storage, pipelines, warehousing and reporting, every item in Fabric reads from the same copy of the data. Power BI is one of the experiences inside Fabric.

For a Power BI analyst, the important items are:

| Item | What it is | Typical use |
|---|---|---|
| Lakehouse | Files and tables stored in OneLake, read with SQL or Spark | Large data, mixed files and tables |
| Warehouse | A SQL-first store for structured tables | Star schemas for reporting |
| Dataflow Gen2 | No-code Power Query data preparation | Cleaning and loading without code |
| Notebook | Python, PySpark or SQL code | Advanced transformations and data science |
| Semantic model | The model (tables, relationships, DAX measures) that reports use | Shared, governed measures |
| Report | The Power BI visuals | What people look at |

:::case One sales model, many reports
A retail company keeps sales data in OneLake. Finance, marketing and operations each want their own report, but they must all agree on what "revenue" means. The answer is one semantic model in a Fabric workspace that all three reports connect to, so the measure is written once and changed in one place.
:::

## OneLake and shortcuts

OneLake is the single logical data lake for the organisation. Each workspace has a lakehouse or warehouse, and the data is stored once. A **shortcut** points to data in another location (another lakehouse, or Azure storage, or Amazon S3) without copying it. Use shortcuts to avoid duplicating large tables across workspaces.

::::tip Shortcut, do not copy
A copy drifts out of date and doubles storage. A shortcut always reads the current data. Copy only when you need a snapshot, for example for an audit.
::::

## Lakehouse versus warehouse

Both store tables in OneLake. The choice depends on the workload:

- **Lakehouse**: keeps files (CSV, JSON, Parquet) alongside tables. Spark notebooks and SQL both work on it. Good for data engineering and mixed data.
- **Warehouse**: SQL-only tables with full T-SQL support, including stored procedures and fine-grained permissions. Good for structured reporting and teams that think in SQL.

A lakehouse also exposes a **SQL analytics endpoint**, which lets you query its tables with SQL. Many teams therefore land raw data in a lakehouse, then build reporting tables in a warehouse or view them through the endpoint.

## Loading data with a dataflow

A dataflow uses Power Query, the same tool as Power BI Desktop, to load and shape data in the service. It is the right choice when the transformation is ordinary cleaning and the team does not write code.

Steps:

1. In the workspace, select **New item > Dataflow Gen2**.
2. Add a source, for example a CSV file uploaded to the lakehouse.
3. Apply transformations: change types, remove blank rows, merge with a customer table.
4. Set the output destination to a lakehouse or warehouse table.
5. Publish, then run the dataflow once to check the output.

The output is a table in OneLake. Any report can read it, which is why dataflows suit shared, reusable cleaned data.

::::warn Keep logic in one place
If the same cleaning happens in a dataflow, in a notebook and again in Power BI Desktop, the three versions will disagree. Choose one place for each transformation and document it.
::::

## Building a star schema in the warehouse

Reporting works best on a star schema: one fact table of sales and several dimension tables of customers and products. Create the tables in the warehouse with a short script, then load them.

```sql
-- Dimension: customers (one row per customer)
CREATE TABLE dbo.dim_customer (
    customer_key   INT         NOT NULL,
    customer_name  VARCHAR(100),
    segment        VARCHAR(50),
    territory      VARCHAR(50)
);

-- Fact: sales (one row per order line, keys point to dimensions)
CREATE TABLE dbo.fact_sales (
    order_date     DATE,
    customer_key   INT,
    product_key    INT,
    quantity       INT,
    sales_amount   DECIMAL(12, 2),
    cost_amount    DECIMAL(12, 2)
);
```

The fact table holds numbers and keys. Descriptive text lives in dimensions. This shape keeps the semantic model small and fast, and it matches the star schema taught in the modelling lesson.

## Publishing a semantic model

A semantic model is the Power BI dataset in Fabric. You create it from the warehouse or lakehouse tables, add relationships and measures, and publish it to the workspace.

1. Open the warehouse and choose **New semantic model**.
2. Select the tables to include, for example `fact_sales`, `dim_customer` and `dim_product`.
3. Confirm the relationships. They should run from each dimension (one side) to the fact table (many side).
4. Write the DAX measures in the model, not in individual reports, so every report uses the same definition:

```dax
Total Sales = SUM ( fact_sales[sales_amount] )
Total Cost  = SUM ( fact_sales[cost_amount] )
Gross Margin % = DIVIDE ( [Total Sales] - [Total Cost], [Total Sales] )
```

5. Save the model. Reports now connect to it in Power BI and see the same measures.

## Connecting a report

From Power BI Desktop, choose **Get data > Power BI semantic models** and select the published model. The report is built on top of the shared model: visuals and measures come from the model, while layout and filters belong to the report.

This separation is the key idea. A change to the model's measure updates every report that uses it, without editing each one. The reverse also matters: a report should not define its own revenue measure, or the numbers will drift.

## Refresh and the chain of dependencies

Data flows through a chain: source, then dataflow or notebook, then lakehouse or warehouse, then semantic model, then report. A refresh must run in order. If the dataflow fails, the model shows yesterday's data, and the report shows yesterday's numbers without any visible error.

Practical rules:

- Schedule the upstream item first, and the semantic model refresh after it, with a short gap.
- Check the refresh history after each run, not only when a report looks wrong.
- Use a notification on failure so that the team hears about it first.

## Governance basics in Fabric

- **Workspace roles** (Admin, Member, Contributor, Viewer) control who can change items. Give analysts Contributor or Member only where they need to build.
- **Endorsement** marks a semantic model as Promoted or Certified, so people know which model to trust.
- **Lineage view** shows how a report depends on the model, the warehouse and the source, which speeds up impact checks before a change.
- **Sensitivity labels** can classify data, for example as Confidential, and follow it through the chain.

::::key What to remember
- Fabric keeps all data in one place, OneLake, and every item reads from it.
- Use shortcuts instead of copies, and lakehouses for files and mixed data, warehouses for structured reporting.
- Dataflows suit no-code cleaning; notebooks suit code; both write tables to OneLake.
- Define measures once in the semantic model, and let every report use them.
- Refresh in order, and check refresh history, because a silent failure shows old numbers.
::::

:::quiz
Q: What is OneLake?
- A single report in Power BI
* The single logical data lake that all Fabric items read from
- A type of DAX measure
- A gateway for on-premises data
> OneLake is the shared storage layer for Fabric.

Q: When is a shortcut better than a copy?
- When you need an audit snapshot
* When you want the other location to read current data without duplicating storage
- When the source is offline
- Never; copies are always better
> A shortcut points to the data, so it stays current.

Q: Which item suits a team that writes T-SQL and needs stored procedures?
- A dataflow
* A warehouse
- A report
- A shortcut
> Warehouses support full T-SQL, including stored procedures.

Q: Why define measures in the semantic model rather than in each report?
- Reports cannot store measures
* So every report uses one definition, and a change is made once
- Measures run faster there only
- It hides the measures
> One definition prevents numbers from drifting between reports.

Q: A dataflow fails overnight and nobody notices until a manager asks. What is the best fix?
- Remove the dataflow
* Schedule refreshes in order and set a failure notification
- Refresh the report manually every hour
- Turn off the semantic model
> Refresh order and failure alerts make silent failures visible.
:::

:::exercise Design the chain
A company has order data in CSV files, customer and product lists in a CRM export, and three reports for finance, sales and operations. Draw the Fabric chain: which items you would use (lakehouse, warehouse, dataflow, notebook, semantic model, report), in what order, and where you would define the revenue and margin measures. Name one refresh rule and one governance control.
???
One possible design: CSV files land in a lakehouse; a Dataflow Gen2 cleans and types them into tables; the tables are modelled as a star schema in a warehouse; one semantic model holds the relationships and the Total Sales and Gross Margin % measures; the three reports connect to that model. Refresh the dataflow first, then the model. Governance: endorse the model as Certified and limit edit rights to a named team.
:::
