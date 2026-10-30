---
num: 5
title: SELECT, WHERE, ORDER BY & Filtering Operators
live: "SQL class 3"
updated: "SQL Server 2022, 2026"
level: Beginner
duration: 120 min
summary: Retrieve exactly the rows and columns you need. Master SELECT, aliases with AS, DISTINCT, TOP, WHERE with comparison and logical operators, IN, BETWEEN, LIKE wildcards, IS NULL, ORDER BY, and the logical order in which SQL processes a query.
datasets: [superstore_sales.csv, customers.csv]
outcomes:
  - Select columns, calculated expressions and aliases, and remove duplicates with DISTINCT
  - Filter rows with comparison, logical, IN, NOT IN, BETWEEN, LIKE, NOT LIKE, IS NULL and IS NOT NULL
  - Sort results by one or more columns, expressions and positions; limit rows with TOP
  - Explain the logical processing order of a query and why it matters for aliases
  - Translate business questions into correct SELECT statements
---

## The shape of a SELECT statement

```sql
SELECT   column_list            -- what to show
FROM     table_name             -- where it comes from
WHERE    row_conditions         -- which rows to keep
GROUP BY grouping_columns       -- (Lesson 7)
HAVING   group_conditions       -- (Lesson 7)
ORDER BY sort_columns;          -- how to sort the result
```

Only `SELECT` is required (`SELECT 1 + 1;` works). Everything else is optional but must appear in this order.

## SELECT: columns, expressions and aliases

```sql run rows=5
SELECT TOP 5
       order_id,
       order_date,
       customer_name,
       sales,
       profit,
       sales - profit                     AS cost,
       ROUND(100.0 * profit / sales, 1)   AS margin_pct,
       'INR'                              AS currency
FROM superstore;
```

- `SELECT *` returns every column. Use it to explore, never in production code (it breaks when columns change and reads more data than needed).
- An **alias** renames a column or table in the result: `AS margin_pct`. `AS` is optional (`sales - profit cost`) but makes code clearer. Aliases with spaces need brackets or quotes: `AS [Margin %]`.
- Expressions can use operators, functions and literals.

### Table aliases

```sql
SELECT s.order_id, s.sales
FROM superstore AS s;          -- 's' is a short name for the table
```

Table aliases become essential with joins (Lesson 8).

## DISTINCT: unique values

```sql run
SELECT DISTINCT region
FROM superstore
ORDER BY region;
```

```sql run
SELECT DISTINCT category, sub_category
FROM superstore
ORDER BY category, sub_category;
```

`DISTINCT` applies to the **whole row** of selected columns: the second query returns each category–sub-category combination once. To count unique values: `COUNT(DISTINCT customer_id)`.

## TOP: limit the rows

```sql run
SELECT TOP 5 order_id, customer_name, city, sales
FROM superstore
ORDER BY sales DESC;
```

| Dialect | Syntax for "first 5 rows" |
|---|---|
| SQL Server | `SELECT TOP 5 … ORDER BY …` (also `TOP 10 PERCENT`, `TOP 5 WITH TIES`) |
| SQL Server 2012+, ANSI | `ORDER BY … OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY` (Lesson 11) |
| PostgreSQL, MySQL, SQLite, DuckDB | `… ORDER BY … LIMIT 5` |
| Oracle | `FETCH FIRST 5 ROWS ONLY` |

:::warn TOP without ORDER BY
Without `ORDER BY`, the database returns rows in no guaranteed order, so "top 5" may differ between runs. Always sort when you use TOP.
:::

## WHERE: filtering rows

### Comparison operators

```sql run
SELECT COUNT(*) AS lines_over_50k
FROM superstore
WHERE sales > 50000;
```

```sql run rows=6
SELECT order_id, city, category, sales, discount
FROM superstore
WHERE region = 'West'
  AND category = 'Furniture'
  AND discount >= 0.3
ORDER BY sales DESC;
```

Text values go in **single quotes** (`'West'`). Double quotes are for identifiers in standard SQL. Dates are written as text in ISO format: `order_date >= '2025-01-01'`.

### IN and NOT IN

`IN` is shorthand for several `OR` conditions on the same column.

```sql run
SELECT city, COUNT(*) AS order_lines
FROM superstore
WHERE city IN ('Pune', 'Mumbai', 'Ahmedabad')
GROUP BY city
ORDER BY city;
```

```sql run
SELECT COUNT(*) AS non_metro_lines
FROM superstore
WHERE city NOT IN ('Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad');
```

:::mistake NOT IN with a NULL
If the list (or subquery) inside `NOT IN` contains a NULL, `NOT IN` returns **no rows at all**, because `x <> NULL` is UNKNOWN. Use `NOT EXISTS` (Lesson 10) or filter NULLs out of the subquery.
:::

### BETWEEN

`BETWEEN a AND b` is **inclusive** of both ends.

```sql run
SELECT COUNT(*) AS lines_between_10k_and_20k
FROM superstore
WHERE sales BETWEEN 10000 AND 20000;
```

For dates, prefer a **half-open range**: `order_date >= '2025-01-01' AND order_date < '2026-01-01'`. It works whether the column is `DATE` or `DATETIME2`; `BETWEEN '2025-01-01' AND '2025-12-31'` silently misses orders placed after midnight on 31-Dec when the column has times.

```sql run
SELECT COUNT(DISTINCT order_id) AS orders_in_2025
FROM superstore
WHERE order_date >= '2025-01-01' AND order_date < '2026-01-01';
```

### LIKE: pattern matching

| Wildcard | Meaning | Example | Matches |
|---|---|---|---|
| `%` | Any sequence of characters (including none) | `'Apex%'` | Apex Chair 412, Apex Phone 118 |
| `_` | Exactly one character | `'C00_1'` | C0011, C0021 … |
| `[ ]` (SQL Server) | One character from a set or range | `'[A-C]%'` | starts with A, B or C |
| `[^ ]` (SQL Server) | One character not in the set | `'[^A-M]%'` | starts with N–Z |

```sql run
SELECT DISTINCT product_name
FROM superstore
WHERE product_name LIKE 'Apex Ch%'
ORDER BY product_name;
```

```sql run
SELECT COUNT(DISTINCT customer_id) AS customers_named_with_khan
FROM superstore
WHERE customer_name LIKE '%Khan%';
```

```sql run
SELECT DISTINCT city
FROM superstore
WHERE city NOT LIKE '%a%'          -- city names without a lowercase 'a'
ORDER BY city;
```

:::note Case sensitivity
SQL Server's default collation is **case-insensitive**, so `LIKE 'apex%'` also matches "Apex…". PostgreSQL is case-sensitive (use `ILIKE`), and so is the practice engine used for the outputs in this handbook. Write patterns in the same case as the data to be safe everywhere.
:::

Leading wildcards (`'%Khan'`) cannot use an index and scan the whole table; fine for analysis, slow for apps on big tables.

### IS NULL and IS NOT NULL

```sql run
SELECT COUNT(*) AS homes_missing_area
FROM houses
WHERE area_sqft IS NULL;
```

(The `houses` table is loaded from `house_prices.csv`; 25 houses have a missing area, which you will clean in the Python track.)

### Combining conditions

```sql run rows=8
SELECT order_id, region, category, ship_mode, sales, profit
FROM superstore
WHERE (region = 'North' OR region = 'East')
  AND category <> 'Office Supplies'
  AND ship_mode IN ('First Class', 'Same Day')
  AND profit < 0
ORDER BY profit;
```

## ORDER BY: sorting

```sql run rows=8
SELECT region, city, COUNT(*) AS lines, ROUND(SUM(sales), 0) AS sales
FROM superstore
GROUP BY region, city
ORDER BY region ASC, sales DESC;
```

- `ASC` (default) or `DESC` for each column separately.
- Sort by an expression or alias: `ORDER BY sales - profit DESC`, `ORDER BY margin_pct`.
- Sort by column position (`ORDER BY 2 DESC`) works but is fragile; avoid it in saved code.
- NULLs sort **first** in ascending order in SQL Server (last in PostgreSQL/Oracle by default).
- Custom order with CASE: `ORDER BY CASE ship_mode WHEN 'Same Day' THEN 1 WHEN 'First Class' THEN 2 ELSE 3 END`.

## The logical processing order

You *write* `SELECT` first, but SQL *processes* the clauses in a different order. This explains several common errors.

```python fig: Logical processing order of a SELECT statement. Each step works on the output of the previous one.
dg.vflow(["1. FROM / JOIN: build the source rows", "2. WHERE: keep matching rows", "3. GROUP BY: form groups", "4. HAVING: keep matching groups",
          "5. SELECT: compute columns and aliases", "6. DISTINCT: remove duplicates", "7. ORDER BY: sort (aliases allowed)", "8. TOP / OFFSET-FETCH: limit"], title="How SQL processes a query", width=6.4)
```

Consequences:

- You **cannot** use a column alias in `WHERE`, because WHERE runs before SELECT: `WHERE margin_pct > 10` fails. Repeat the expression, or use a subquery/CTE.
- You **can** use an alias in `ORDER BY`, because it runs after SELECT.
- `WHERE` cannot contain aggregate functions (`WHERE SUM(sales) > 100`); use `HAVING` (Lesson 7).

```sql
-- Fails: Invalid column name 'margin_pct'
SELECT order_id, 100.0 * profit / sales AS margin_pct
FROM superstore
WHERE margin_pct > 10;

-- Works: repeat the expression in WHERE, use the alias in ORDER BY
SELECT order_id, 100.0 * profit / sales AS margin_pct
FROM superstore
WHERE 100.0 * profit / sales > 10
ORDER BY margin_pct DESC;
```

## From business question to query

:::steps Translate a question
Question: *"Which Technology orders in the South had a discount but still made more than ₹10,000 profit in 2025? Show the biggest first."*
1. **Table**: superstore.
2. **Rows** (WHERE): category = Technology, region = South, discount > 0, profit > 10000, order date in 2025.
3. **Columns** (SELECT): order_id, order_date, city, sub_category, discount, profit.
4. **Order**: profit descending.
:::

```sql run rows=8
SELECT order_id, order_date, city, sub_category, discount, profit
FROM superstore
WHERE category = 'Technology'
  AND region = 'South'
  AND discount > 0
  AND profit > 10000
  AND order_date >= '2025-01-01' AND order_date < '2026-01-01'
ORDER BY profit DESC;
```

:::ai Do it with AI
Give an assistant your table's column list and a question, and ask for SQL Server syntax: *"Table superstore(order_id, order_date, region, city, category, sub_category, sales, discount, profit). Write a T-SQL query for: Furniture orders in Kolkata or Patna in 2024 with negative profit, sorted by profit."* Read the query before running it: check the date range, the brackets around OR, and that it uses the column names you gave.
:::

## Summary

:::key
- `SELECT` columns and expressions; name them with `AS`; avoid `SELECT *` in saved queries.
- `DISTINCT` removes duplicate rows of the selected columns; `TOP n` with `ORDER BY` limits results.
- Filter with `=, <>, >, <, >=, <=`, `AND/OR/NOT` (use brackets), `IN`, `BETWEEN` (inclusive), `LIKE` with `%` and `_`, and `IS NULL`.
- For dates use half-open ranges: `>= start AND < next_start`.
- `ORDER BY` sorts ascending by default; can use aliases.
- Logical order: FROM → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → TOP. That is why aliases fail in WHERE.
:::

:::quiz
Q: Which query returns each distinct region exactly once?
- `SELECT region FROM superstore`
* `SELECT DISTINCT region FROM superstore`
- `SELECT UNIQUE(region) FROM superstore`
- `SELECT TOP 1 region FROM superstore`
> DISTINCT removes duplicate rows from the result.

Q: `WHERE sales BETWEEN 100 AND 200` includes which values?
- 101 to 199
* 100 to 200, both included
- 100 to 199
- 101 to 200
> BETWEEN is inclusive of both boundaries.

Q: Which pattern finds product names that contain "Desk" anywhere?
- `LIKE 'Desk%'`
- `LIKE '%Desk'`
* `LIKE '%Desk%'`
- `LIKE '_Desk_'`
> % on both sides matches any characters before and after.

Q: Why does `WHERE margin_pct > 10` fail when margin_pct is an alias defined in SELECT?
* WHERE is processed before SELECT, so the alias does not exist yet
- Aliases can only be used with GROUP BY
- margin_pct must be in brackets
- You must use HAVING for all aliases
> Logical order: WHERE comes before SELECT.

Q: What is wrong with `WHERE order_date BETWEEN '2025-01-01' AND '2025-12-31'` on a DATETIME2 column?
- Nothing
* It misses rows on 31-Dec after 00:00:00
- It includes 2026 dates
- BETWEEN does not work with dates
> '2025-12-31' means midnight; later times that day are excluded. Use < '2026-01-01'.

Q: `SELECT TOP 3 * FROM orders` without ORDER BY returns:
- The 3 newest orders
- The 3 largest orders
* Any 3 rows, in no guaranteed order
- An error
> Without ORDER BY, row order is not defined.
:::

:::exercise Superstore filters
Write queries for: (1) all Same Day orders in the West with sales over ₹50,000; (2) customers whose names start with A, B or C (distinct, sorted); (3) order lines with a 40% discount in the Furniture category, showing the 10 biggest losses; (4) the number of order lines in 2024 for the Corporate segment in Pune or Indore.
???
```sql
-- (1)
SELECT order_id, order_date, city, sales FROM superstore
WHERE ship_mode = 'Same Day' AND region = 'West' AND sales > 50000 ORDER BY sales DESC;
-- (2) SQL Server
SELECT DISTINCT customer_name FROM superstore WHERE customer_name LIKE '[A-C]%' ORDER BY customer_name;
-- (3)
SELECT TOP 10 order_id, product_name, sales, profit FROM superstore
WHERE discount = 0.4 AND category = 'Furniture' ORDER BY profit ASC;
-- (4)
SELECT COUNT(*) AS lines FROM superstore
WHERE segment = 'Corporate' AND city IN ('Pune', 'Indore')
  AND order_date >= '2024-01-01' AND order_date < '2025-01-01';
```
:::

:::interview Questions you may be asked
**Q: What is the order of execution of a SQL query?**
FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, then TOP/OFFSET-FETCH.

**Q: Difference between WHERE and HAVING?**
WHERE filters rows before grouping and cannot use aggregates; HAVING filters groups after aggregation.

**Q: How do you find employees whose name's second letter is "a"?**
`WHERE name LIKE '_a%'`.

**Q: IN vs EXISTS?**
IN compares a value with a list or subquery result; EXISTS checks whether a correlated subquery returns any row. EXISTS is safer with NULLs and often efficient for large subqueries (Lesson 10).
:::
