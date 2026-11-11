---
num: 11
title: Cloud Fundamentals for Data: IaaS, PaaS, SaaS, Regions, Identity and Cost
live: "Gap-fill lesson"
updated: "2026"
level: Intermediate
duration: 120 min
summary: Learn the cloud concepts a data team relies on, from service models and regions to identity and access, then map the equivalent data services across AWS, Azure and Google Cloud, and control cost with tagging, storage tiers, right-sized compute and budgets.
datasets: []
outcomes:
  - Explain IaaS, PaaS and SaaS with data-platform examples
  - Choose regions, identities and access rules for a data platform
  - Map a data service to its AWS, Azure and Google Cloud equivalent
  - Find and reduce data platform costs with tagging, tiers and budgets
---

## The cloud service models

The cloud rents computing as services. The three main models differ in how much the provider manages for you.

| Model | You manage | Provider manages | Data example |
|---|---|---|---|
| IaaS (infrastructure) | Operating system, runtime, data, applications | Physical machines, network, storage hardware | A virtual machine you install Airflow on |
| PaaS (platform) | Data, code and configuration | Servers, scaling, patching, runtime | A managed warehouse or a managed Spark service |
| SaaS (software) | Data and users | The whole application | A BI tool in the browser, a CRM |

The more managed the service, the less you operate and the more you pay per unit of work. A team with few engineers usually chooses managed platforms for data, and keeps custom infrastructure for the parts that are truly special.

:::case Build or buy the warehouse
A five-person team considers installing a database on virtual machines. It would need patching, backups, scaling and on-call cover. A managed warehouse removes that work at a higher price per query. The decision is about where the team's time is best spent, not which option is technically superior.
:::

## Regions, availability and residency

A **region** is a geographic location with one or more data centres. An **availability zone** is an isolated data centre within a region. Choose regions for three reasons: latency to users, data residency law (for personal data, some countries require storage within their borders), and the availability of the services you need, because not every service exists in every region.

Keep the data platform in one region where possible, and replicate deliberately for disaster recovery. Cross-region copies cost money and add latency.

## Identity and access

Cloud accounts use **identities** (users, groups, service accounts) and **roles or policies** that grant permissions. Four principles keep a data platform safe:

1. **Least privilege.** Grant the smallest set of permissions a job needs.
2. **Service accounts for pipelines.** A pipeline runs under its own identity, not a person's login.
3. **No long-lived keys in code.** Use the platform's identity mechanism or a secrets manager.
4. **Audit.** Every access and change to sensitive data is logged and reviewed.

## A service map across the three clouds

The names differ, but the building blocks are similar. Check each provider's current documentation before you commit to a name.

| Need | AWS | Azure | Google Cloud |
|---|---|---|---|
| Object storage (files, lake) | Amazon S3 | Azure Data Lake Storage Gen2 | Cloud Storage |
| Managed warehouse | Amazon Redshift | Azure Synapse Analytics | BigQuery |
| Managed Spark | Amazon EMR, AWS Glue | Azure Databricks, Synapse Spark | Dataproc |
| Streaming | Amazon Kinesis, MSK (Kafka) | Event Hubs, Event Hubs for Kafka | Pub/Sub, Managed Kafka |
| Orchestration | Amazon MWAA (managed Airflow) | Azure Data Factory, Managed Airflow | Cloud Composer (managed Airflow) |
| Serverless functions | AWS Lambda | Azure Functions | Cloud Functions |
| Identity | IAM | Microsoft Entra ID, RBAC | Cloud IAM |

Many organisations also use **Databricks** and **Snowflake**, which run on all three clouds, and **Microsoft Fabric** in the Microsoft ecosystem (covered in the Power BI lessons).

## Cost: where the money goes

Data platform costs usually come from four places:

| Cost driver | Why it grows | Control |
|---|---|---|
| Compute | Clusters left running; oversized machines | Auto-suspend, auto-scale, right-size |
| Storage | Raw copies kept forever; duplicate tables | Lifecycle rules, storage tiers, delete unused copies |
| Data transfer | Moving data between regions or to the internet | Keep compute near storage; avoid unnecessary copies |
| Queries | Scanning full tables; repeated identical queries | Partition and cluster tables; cache results; select only needed columns |

## Cost controls that work

1. **Tag everything** with team, product and environment, so that each cost can be assigned to an owner.
2. **Set budgets and alerts** at 50%, 80% and 100% of the monthly budget.
3. **Use storage tiers.** Move files that are rarely read to cheaper cold tiers, and delete temporary data on a schedule.
4. **Auto-suspend compute** when idle, and size clusters for the workload rather than the peak.
5. **Review monthly.** Find the top five costs, and ask who owns each and whether it is still needed.

```python run
# A simple monthly cost model: compare two storage choices for the same data
data_tb = 5
hot_price_per_tb = 23.0          # illustrative monthly price per TB; check the provider's price list
cold_price_per_tb = 4.0          # illustrative
share_read_monthly = 0.10        # 10% of the data is read each month

hot_all = data_tb * hot_price_per_tb
tiered = data_tb * (share_read_monthly * hot_price_per_tb + (1 - share_read_monthly) * cold_price_per_tb)
print(f"all hot: {hot_all:.2f}   tiered: {tiered:.2f}   saving: {hot_all - tiered:.2f} per month")
```

The prices are placeholders that show the method. Replace them with the current figures from the provider's pricing page, and note the date you checked.

::::warn Free tiers and surprise bills
Cloud free tiers are real but limited. A query that scans a large table, a cluster left running over a weekend, or a copy sent across regions can cost more in one day than a month of storage. Set budgets before you start building.
::::

## Security basics for data in the cloud

- Encrypt data at rest and in transit by default.
- Keep storage buckets private; never make a data bucket public for convenience.
- Restrict network access so that databases accept connections only from known services.
- Monitor for unusual access, and rotate credentials.

:::interview How would you reduce a data platform's cloud cost by a third?
Start with measurement: tag costs by owner and find the largest drivers. Then right-size and auto-suspend compute, move cold data to cheaper tiers, remove unused copies, partition tables so queries scan less, and set budgets with alerts. Measure after each change, and report the saving with the date.
:::

::::key What to remember
- IaaS, PaaS and SaaS differ in what you manage; managed services trade price for operational effort.
- Choose regions for latency, residency and service availability.
- Use service identities with least privilege and no long-lived keys in code.
- The service names differ across AWS, Azure and Google Cloud; the building blocks are similar.
- Control cost through tagging, budgets, tiers, auto-suspend and query design.
::::

:::quiz
Q: In PaaS, what does the provider typically manage that you do not?
- Your data
* Servers, scaling and patching of the platform
- Your code
- Your users
> PaaS removes the infrastructure work from you.

Q: Why use a service account for a pipeline?
- It is faster
* It gives the pipeline its own least-privilege identity instead of a person's login
- It avoids billing
- It removes the need for permissions
> Service identities are auditable and limited.

Q: Which cost driver is most often caused by a cluster left running at the weekend?
- Storage
- Data transfer
* Compute
- Documentation
> Compute is billed while it is running.

Q: What is a sensible first step in cost reduction?
- Delete all data
* Tag costs by owner and find the largest drivers
- Buy a bigger machine
- Turn off monitoring
> Measurement shows where the money goes.

Q: Which AWS service is the managed equivalent of a data warehouse?
- Amazon S3
* Amazon Redshift
- AWS Lambda
- Amazon Kinesis
> Redshift is the managed warehouse; S3 is storage.
:::

:::exercise Map and cost one pipeline
Choose a simple pipeline (files land daily, a warehouse table is built, a dashboard reads it). Map each component to a service on one cloud, list the identity each needs, and estimate the monthly cost of storage and compute using the provider's current price list. State the date you checked the prices and one cost control you would apply.
???
Hints: count storage as the total size times the price per unit, and compute as the hours the cluster runs times its hourly price. Put placeholder prices in your working and replace them with the official figures before reporting.
:::
