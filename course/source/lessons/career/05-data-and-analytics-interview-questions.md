---
num: 5
title: Data Engineering and Analytics Interview Questions with Model Answers
live: "Gap-fill lesson"
updated: "2026"
level: Intermediate
duration: 120 min
summary: Practise twelve core questions on ETL versus ELT, idempotency, batch and streaming, schemas, surrogate keys, late data, dbt tests, Airflow, Spark shuffles, warehouses versus lakehouses, pipeline testing and change data capture, each with a model answer and the reasoning an interviewer listens for.
datasets: []
outcomes:
  - Answer core data engineering and analytics questions clearly and briefly
  - Give the trade-off behind each answer, not only the definition
  - Recognise follow-up questions that test depth
---

## How interviewers use these questions

Interviewers rarely want a textbook definition. They listen for four things: whether you know the term, whether you can explain it simply, whether you know when it applies, and whether you know its trade-off. A good answer covers all four in under two minutes. The model answers below are written at that length.

## The twelve questions

**1. What is the difference between ETL and ELT?**
*Model answer.* ETL transforms data before loading it into the target; ELT loads raw data first and transforms it inside the warehouse. ELT suits cloud warehouses that have cheap, powerful compute, and it keeps raw data so models can be rebuilt. ETL is chosen when data must be masked or validated before it lands, for example personal data that must never reach the warehouse in raw form.

**2. What is idempotency?**
*Model answer.* An operation is idempotent when running it twice has the same effect as running it once. Pipelines need this because retries and reruns are normal. A load that appends rows is not idempotent; a load that merges on a key, or overwrites a partition, is.

**3. Batch versus streaming?**
*Model answer.* Batch processes accumulated data at intervals, such as nightly. Streaming processes each event as it arrives. Batch is simpler, cheaper and easier to test; streaming gives low latency at higher operational cost. Choose by how fresh the data must be and what it costs to be late.

**4. Star versus snowflake schema?**
*Model answer.* Both have a central fact table and dimension tables. A star schema keeps each dimension flat, which makes queries simple and fast. A snowflake normalises dimensions into sub-tables, which saves a little storage and adds joins. Star schemas are usually preferred for reporting; snowflakes appear where dimensions are very large or shared.

**5. What is a surrogate key and why use it?**
*Model answer.* A surrogate key is a system-generated identifier, such as an integer, that has no business meaning. It keeps the warehouse stable when source keys change, reduces join size, and is essential for slowly changing dimensions where one customer has several versions over time.

**6. How do you handle late-arriving data?**
*Model answer.* First, decide the tolerance: how late can a record arrive and still count? Then reprocess the affected partitions or window rather than only appending new rows, use the event time rather than arrival time for aggregates, and report the restated numbers with a note. Monitor how often late data arrives so the window can be tuned.

**7. What does a dbt test check?**
*Model answer.* dbt tests check assumptions about a model's data: that a column is unique, not null, that values belong to an accepted list, or that a relationship between tables holds. They run on every build, and a failing test stops the pipeline from publishing wrong data. Custom tests can check business rules, such as "revenue is never negative".

**8. What is Airflow used for?**
*Model answer.* Airflow schedules and orchestrates workflows defined as directed acyclic graphs (DAGs). It runs tasks in dependency order, retries failures, records run history and alerts on errors. It does not process the data itself; it calls the tools that do.

**9. Spark shuffles and partitions?**
*Model answer.* A shuffle is the redistribution of data across the cluster, typically for a join or a group-by, and it is expensive because data moves over the network. Partitions are the units of parallel work. Too few partitions leave machines idle; too many add overhead. Reducing shuffles, filtering early and choosing sensible partition counts are the usual fixes for slow jobs.

**10. Warehouse versus lakehouse?**
*Model answer.* A warehouse stores structured tables with strong SQL performance and governance. A lakehouse keeps data in open file formats on cheap storage and adds table features such as transactions and schema management, so it can serve both analytics and machine learning. Many organisations use both: a lakehouse for raw and mixed data, and a warehouse or serving layer for reporting.

**11. How do you test a data pipeline?**
*Model answer.* Test at four levels: unit tests for transformation functions on small inputs; schema tests on each table; data-quality tests such as row counts, nulls and reconciliation totals against the source; and an end-to-end run on sample data. Add a failure drill, where you break an input on purpose and confirm the alert fires.

**12. What is CDC?**
*Model answer.* Change data capture reads a database's change log to capture inserts, updates and deletes as they happen, instead of re-reading whole tables. It keeps the warehouse close to real time at low load on the source. It needs database access for the log and careful handling of schema changes.

## Follow-up questions to expect

| If you say... | Expect a follow-up like... |
|---|---|
| "I would use an upsert" | "What is the key, and what happens with duplicates in the source?" |
| "Streaming for everything" | "What does it cost to run, and who is paged at night?" |
| "dbt tests cover quality" | "Which failures would a dbt test miss?" |
| "Partition the data" | "What partition key would you choose, and why not the most detailed one?" |

:::interview A reliable way to answer
Give the definition in one sentence, the reason it matters in one sentence, one example, and the trade-off. Then stop and let the interviewer ask for more. A short answer with a clear trade-off impresses more than a long lecture.
:::

::::key What to remember
- Every answer needs a trade-off, not only a definition.
- Idempotency, late data and testing are the topics that separate candidates.
- Use a concrete example from your own work when you can.
- Expect follow-ups; have the next layer of detail ready.
::::

:::quiz
Q: Which approach is idempotent?
- Appending the same file every night
* Merging rows on a key so a rerun does not duplicate them
- Inserting without checks
- Sending every event twice
> Merges on a key keep a rerun from creating duplicates.

Q: When is ETL the better choice than ELT?
- When the warehouse is very cheap
* When data must be masked or validated before it reaches the warehouse
- When there is no transformation
- When data is never stored
> ETL transforms before loading, which suits strict masking requirements.

Q: What is a surrogate key?
- The customer's email address
* A system-generated identifier with no business meaning
- A password
- The date of the record
> Surrogate keys keep the warehouse stable when source keys change.

Q: What does a dbt `unique` test check?
- That the model runs quickly
* That a column has no duplicate values
- That the file is in CSV format
- That the model is documented
> The test fails when duplicates appear in the column.

Q: Which tool is responsible for scheduling and retrying the steps of a pipeline?
- Spark
* Airflow
- A dashboard
- A spreadsheet
> Airflow orchestrates tasks; the processing tools do the data work.
:::

:::exercise Practise aloud
Choose five of the twelve questions and answer each aloud in under two minutes, with one example from a project you have done. Record yourself, listen back, and rewrite any answer that has no trade-off in it.
???
Hints: time each answer. Replace vague words such as "stuff" or "some tools" with a named tool or a number. If you cannot give an example, use a realistic example from a public dataset and say so.
:::
