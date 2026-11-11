---
num: 1
title: What Data Engineering Is, Its Roles and the Data Formats It Uses
live: "Gap-fill lesson"
updated: "2026"
level: Beginner
duration: 120 min
summary: Understand what data engineers build, the path data takes from source to report, and the file formats used to store and move it (CSV, JSON, XML, Parquet, Avro and ORC), with the trade-offs in size, speed and schema that decide which to use.
datasets: [daily_sales.csv, superstore_sales.csv]
outcomes:
  - Describe the data engineering role and how it differs from analytics and data science
  - Trace data from a source system to a trusted reporting table
  - Compare CSV, JSON, XML, Parquet, Avro and ORC on size, speed, schema and readability
  - Choose a file format for a given job, with reasons
---

## What data engineering is

Data engineering builds and runs the systems that move, store and prepare data, so that analysts, data scientists and AI applications can use it reliably. Without reliable pipelines, a dashboard shows wrong numbers and a model trains on stale data. The data engineer is responsible for that reliability.

:::case The order that never reached the dashboard
A sales app writes orders to a database. A nightly job should copy them to a warehouse, so that the Monday revenue dashboard is correct. One Sunday the job silently skipped a file. The dashboard showed a 9% drop that nobody could explain for two days. Data engineering exists to make that failure impossible to hide and fast to fix.
:::

## The path data takes

```
Sources (apps, databases, APIs, files)
   └─► Ingestion: copy raw data into a landing zone
         └─► Storage: keep raw copies, cleaned data and reporting tables
               └─► Transformation: clean, join, model, aggregate
                     └─► Serving: trusted tables for analysts, models and apps
                           └─► Consumers: Power BI, notebooks, AI features
```

Every arrow is a point where data can be lost, duplicated or delayed. Most of data engineering is making those arrows reliable and visible.

## Roles around the data

| Role | Main work | Typical tools |
|---|---|---|
| Data engineer | Pipelines, storage, reliability, performance | SQL, Python, Spark, Airflow, dbt, cloud services |
| Analytics engineer | Modelled tables and tested transformations for analysts | SQL, dbt, a warehouse |
| Data analyst | Questions, dashboards, reports | SQL, Excel, Power BI |
| Data scientist | Models and experiments | Python, statistics, ML libraries |
| Platform engineer | The infrastructure the others run on | Cloud, containers, infrastructure as code |

In a small team one person may do several roles. The distinction matters because each role needs different guarantees: an engineer must make loads correct and repeatable; an analyst must trust the meaning of each column.

## File formats

A **file format** decides how data is laid out on disk. It affects size, how fast it can be read, whether a schema is stored with it, and whether people can open it in a text editor.

| Format | Type | Schema stored? | Strength | Weakness | Typical use |
|---|---|---|---|---|---|
| CSV | Text, rows | No | Universal, readable | No types, slow, large | Exports and small files |
| JSON | Text, nested | No (implicit) | Nested and flexible | Verbose, slow for big data | APIs and event payloads |
| XML | Text, nested tags | Optional | Standard in some industries | Very verbose | Legacy and exchange formats |
| Parquet | Binary, columnar | Yes | Small, fast for analysis | Not human-readable | Analytics storage |
| Avro | Binary, row-based | Yes (in the file) | Schema evolution, streaming | Less efficient for analytics | Event streams and messages |
| ORC | Binary, columnar | Yes | Compact, fast for analytics | Mainly used in the Hadoop world | Big-data warehouses |

**Columnar** formats (Parquet, ORC) store each column together. An analytics query that needs two columns from a hundred reads only those two. **Row-based** formats (CSV, Avro) store each record together, which suits writing and streaming one record at a time.

Compression (such as Snappy or gzip) makes files smaller at the cost of some processing time. Columnar files compress very well because similar values sit next to each other.

## See the difference in the data

The block below uses the sales file from the course. It writes the same rows as CSV and as JSON in memory and compares their sizes. The lesson on storage and modelling returns to columnar formats in detail.

```python run
import io
import pandas as pd

sales = pd.read_csv("daily_sales.csv", parse_dates=["date"]).head(365)

csv_text = sales.to_csv(index=False)
json_text = sales.to_json(orient="records", date_format="iso")

print("rows:", len(sales))
print("CSV characters:", len(csv_text))
print("JSON characters:", len(json_text))
print("CSV first line:", csv_text.splitlines()[0])
print("JSON first record:", json_text[:70])
```

JSON is larger here because every record repeats the field names. Columnar binary formats remove that repetition and store types, which is why they dominate analytics storage.

## Choosing a format

1. **Who reads it?** If people open it in Excel, CSV is the practical choice.
2. **How is it queried?** Analytics on large data favours Parquet or ORC.
3. **Does it change over time?** Avro handles schema evolution well for event streams.
4. **Does it cross systems?** Check that each consumer supports the format and its types.

::::warn CSV loses types
A CSV has no record of whether `001` is a number or a code. Leading zeros disappear, dates become text, and a comma inside a field breaks the row. Store analytical data in typed formats, and keep CSV for exchange and inspection.
::::

## Roles in practice: a pipeline's owner

Every pipeline needs a named owner who is paged when it fails, who reviews its changes and who answers questions about its tables. Without an owner, a pipeline becomes a silent dependency that nobody maintains.

:::interview What is the difference between a data engineer and a data analyst?
The analyst answers questions with data that already exists in trusted tables. The engineer makes sure those tables exist, are correct, are refreshed on time and are recoverable when something breaks. The analyst asks what happened; the engineer makes sure the answer is right.
:::

::::key What to remember
- Data engineering builds the reliable path from source to trusted tables.
- Know the roles: engineer, analytics engineer, analyst, scientist and platform engineer.
- Choose formats by reader, query pattern, schema needs and cross-system support.
- Columnar formats suit analytics; row formats suit streams; CSV suits inspection.
- Every pipeline needs an owner.
::::

:::quiz
Q: Which format stores data column by column and suits analytics queries?
- CSV
- JSON
* Parquet
- XML
> Columnar storage reads only the columns a query needs.

Q: What is a key weakness of CSV for analytical data?
- It is too small
* It stores no types, so leading zeros and dates can be lost
- It cannot be opened in Excel
- It cannot store numbers
> Typed formats keep the meaning of each column.

Q: Which format is well suited to streams of events where the schema may change?
* Avro
- Plain text
- A PDF
- An image
> Avro stores its schema with the data and handles evolution.

Q: What does a data engineer primarily guarantee?
- That every chart looks good
* That pipelines load correct, repeatable and recoverable data on time
- That analysts never ask questions
- That models are accurate
> Reliability of the data path is the core responsibility.

Q: Why does JSON use more space than Parquet for the same rows?
- JSON cannot be compressed
* JSON repeats field names in every record, while Parquet stores each column once with its type
- JSON stores images
- Parquet does not store numbers
> Repeated keys and text values inflate JSON.
:::

:::exercise Choose formats for three jobs
For each job, choose a file format and give two reasons: (a) an export that a finance team opens in Excel each Monday; (b) clickstream events arriving continuously from a website, with new fields added every few months; (c) five years of daily sales queried for monthly totals by region.
???
Expected choices: (a) CSV, for readability and universal support, with a note that types must be checked on import. (b) Avro, for streaming and schema evolution. (c) Parquet, columnar and compressed, for analytical queries that read few columns.
:::
