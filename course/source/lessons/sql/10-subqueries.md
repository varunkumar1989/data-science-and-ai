---
num: 10
title: Subqueries, Derived Tables & EXISTS
live: "SQL classes 4–5"
updated: "SQL Server 2022, 2026"
level: Intermediate
duration: 120 min
summary: Put queries inside queries. Use scalar subqueries, multi-row subqueries with IN, ANY and ALL, correlated subqueries, EXISTS and NOT EXISTS, and derived tables (inline views) to answer questions that one level of SELECT cannot, and learn when a join, CTE or window function is better.
datasets: [superstore_sales.csv, hr_employees.csv]
outcomes:
  - Identify scalar, multi-row, multi-column and table subqueries and where each can be used
  - Filter with subqueries using comparison operators, IN, NOT IN, ANY and ALL
  - Write correlated subqueries and explain how they are evaluated
  - Use EXISTS and NOT EXISTS safely, and know why NOT IN fails with NULLs
  - Build derived tables (inline views) to aggregate before joining
---

## What is a subquery?

A **subquery** (inner query, nested query) is a `SELECT` written inside another statement, in brackets. The outer query uses its result.

```python fig: Where subqueries can appear and what they return.
dg.cards([("In WHERE", "Filter with a value or list: WHERE sales > (SELECT AVG(sales) …)"), ("In FROM (derived table / inline view)", "Treat a query result as a table: FROM (SELECT …) AS t"),
          ("In SELECT", "Add a calculated value per row: (SELECT COUNT(*) … ) AS n"), ("In HAVING", "Compare groups with a value: HAVING SUM(x) > (SELECT …)"),
          ("Correlated", "Refers to the outer row; runs once per outer row (logically)"), ("EXISTS / NOT EXISTS", "Tests whether any matching row exists")], cols=3, title="Subquery types and places")
```

| By what it returns | Example | Used with |
|---|---|---|
| **Scalar** (one value) | `(SELECT AVG(sales) FROM superstore)` | `=, >, <` … or as a column |
| **Multi-row** (one column, many rows) | `(SELECT customer_id FROM orders WHERE …)` | `IN`, `NOT IN`, `ANY`, `ALL`, `EXISTS` |
| **Table** (many columns and rows) | `(SELECT region, SUM(sales) … GROUP BY region)` | `FROM` as a derived table |

## Scalar subqueries

"Which order lines are above the average line value?"

```sql run
SELECT COUNT(*) AS lines_above_average,
       (SELECT ROUND(AVG(sales), 0) FROM superstore) AS average_line_sales
FROM superstore
WHERE sales > (SELECT AVG(sales) FROM superstore);
```

The inner query runs first and returns one number; the outer query compares each row with it. You cannot write `WHERE sales > AVG(sales)` directly, because aggregates are not allowed in WHERE (Lesson 5's processing order).

"Show each region's sales and its share of the grand total":

```sql run
SELECT region,
       ROUND(SUM(sales), 0)                                                    AS sales,
       ROUND(100.0 * SUM(sales) / (SELECT SUM(sales) FROM superstore), 1)       AS pct_of_total
FROM superstore
GROUP BY region
ORDER BY sales DESC;
```

## Multi-row subqueries: IN, NOT IN, ANY, ALL

"Orders from customers in the Corporate segment" (without a join):

```sql run
SELECT COUNT(*) AS corporate_orders
FROM orders
WHERE customer_id IN (SELECT customer_id FROM customers WHERE segment = 'Corporate');
```

"Employees earning more than **every** employee in HR" and "more than **at least one** Sales manager":

```sql run
SELECT COUNT(*) AS earn_more_than_all_hr
FROM employees
WHERE monthly_income > ALL (SELECT monthly_income FROM employees WHERE department = 'HR');
```

```sql run
SELECT COUNT(*) AS earn_more_than_some_sales_manager
FROM employees
WHERE monthly_income > ANY (SELECT monthly_income FROM employees WHERE job_title = 'Sales Manager');
```

| Operator | Meaning | Equivalent |
|---|---|---|
| `> ALL (…)` | Greater than every value | `> (SELECT MAX(…))` |
| `> ANY (…)` / `> SOME (…)` | Greater than at least one value | `> (SELECT MIN(…))` |
| `= ANY (…)` | Equal to one of the values | `IN (…)` |
| `<> ALL (…)` | Different from every value | `NOT IN (…)` |

## Correlated subqueries

A **correlated** subquery refers to a column of the outer query, so its result changes for every outer row.

"Which employees earn more than the average of **their own** department?"

```sql run rows=8
SELECT e.emp_id, e.department, e.job_title, e.monthly_income
FROM employees AS e
WHERE e.monthly_income > (SELECT AVG(e2.monthly_income)
                          FROM employees AS e2
                          WHERE e2.department = e.department)     -- refers to the outer row
ORDER BY e.monthly_income DESC;
```

Conceptually, for each employee `e`, SQL computes the average of e's department and compares. Optimisers usually rewrite this efficiently, but on large tables a window function (Lesson 12: `AVG(…) OVER (PARTITION BY department)`) or a join to a derived table is often clearer and faster.

"Latest order of each customer" (a classic):

```sql run rows=6
SELECT o.customer_id, o.order_id, o.order_date
FROM orders AS o
WHERE o.order_date = (SELECT MAX(o2.order_date)
                      FROM orders AS o2
                      WHERE o2.customer_id = o.customer_id)
ORDER BY o.customer_id;
```

## EXISTS and NOT EXISTS

`EXISTS (subquery)` is TRUE if the subquery returns **at least one row**. It stops at the first match, and the columns it selects do not matter (`SELECT 1` is conventional).

"Customers who bought at least one Copier":

```sql run
SELECT COUNT(*) AS customers_who_bought_copiers
FROM customers AS c
WHERE EXISTS (SELECT 1
              FROM orders AS o
              JOIN order_items AS oi ON oi.order_id = o.order_id
              JOIN products AS p     ON p.product_id = oi.product_id
              WHERE o.customer_id = c.customer_id
                AND p.sub_category = 'Copiers');
```

"Customers who have never ordered" (anti-join, compare with Lesson 8):

```sql run
SELECT COUNT(*) AS customers_without_orders
FROM customers AS c
WHERE NOT EXISTS (SELECT 1 FROM orders AS o WHERE o.customer_id = c.customer_id);
```

### Why NOT EXISTS is safer than NOT IN

```sql run
WITH a AS (SELECT 1 AS id UNION ALL SELECT 2 UNION ALL SELECT 3),
     b AS (SELECT 2 AS id UNION ALL SELECT NULL)
SELECT
    (SELECT COUNT(*) FROM a WHERE id NOT IN (SELECT id FROM b))                         AS not_in_rows,
    (SELECT COUNT(*) FROM a WHERE NOT EXISTS (SELECT 1 FROM b WHERE b.id = a.id))       AS not_exists_rows;
```

`NOT IN` returns **0 rows** because `b` contains a NULL: `3 NOT IN (2, NULL)` means `3 <> 2 AND 3 <> NULL`, which is UNKNOWN. `NOT EXISTS` correctly returns 2 rows (1 and 3). Prefer `NOT EXISTS`, or add `WHERE id IS NOT NULL` inside the `NOT IN` subquery.

## Derived tables (inline views)

A subquery in `FROM` acts as a temporary table for the rest of the query. It **must have an alias**. Derived tables are the standard way to **aggregate first, then filter, join or aggregate again**.

"Average order value by segment" requires two levels: first total each order, then average the orders.

```sql run
SELECT segment,
       COUNT(*)                   AS orders,
       ROUND(AVG(order_total), 0) AS avg_order_value
FROM (
    SELECT o.order_id, c.segment, SUM(oi.sales) AS order_total     -- level 1: one row per order
    FROM orders AS o
    JOIN customers AS c    ON c.customer_id = o.customer_id
    JOIN order_items AS oi ON oi.order_id   = o.order_id
    GROUP BY o.order_id, c.segment
) AS order_totals                                                    -- level 2: average of orders
GROUP BY segment
ORDER BY avg_order_value DESC;
```

If you averaged `oi.sales` directly, you would get the average **line** value, not the average **order** value: a frequent interview trap.

"Cities whose 2025 sales beat their 2024 sales", using two derived tables joined together:

```sql run
SELECT a.city, ROUND(a.sales, 0) AS sales_2024, ROUND(b.sales, 0) AS sales_2025,
       ROUND(100.0 * (b.sales - a.sales) / a.sales, 1) AS growth_pct
FROM (SELECT city, SUM(sales) AS sales FROM superstore WHERE YEAR(order_date) = 2024 GROUP BY city) AS a
JOIN (SELECT city, SUM(sales) AS sales FROM superstore WHERE YEAR(order_date) = 2025 GROUP BY city) AS b
  ON b.city = a.city
WHERE b.sales > a.sales
ORDER BY growth_pct DESC;
```

:::note Nested (ordinary) subqueries vs inline views
A subquery in `WHERE` that does not refer to the outer query is an **ordinary (nested) subquery**: it runs once. A subquery in `FROM` is an **inline view** (derived table). One that refers to the outer row is **correlated**. In class these were introduced as inline views and ordinary subqueries; the next step is the **CTE** (Lesson 13), which is a named, more readable inline view.
:::

## Subqueries in SELECT

A scalar subquery in the column list adds a per-row value:

```sql run rows=6
SELECT c.customer_id, c.customer_name,
       (SELECT COUNT(*) FROM orders AS o WHERE o.customer_id = c.customer_id)     AS order_count,
       (SELECT MAX(o.order_date) FROM orders AS o WHERE o.customer_id = c.customer_id) AS last_order
FROM customers AS c
ORDER BY order_count DESC, c.customer_id;
```

Each correlated scalar subquery runs per customer. For many such columns, a single `LEFT JOIN` to an aggregated derived table is usually faster.

## Choosing the right tool

| Need | Good options |
|---|---|
| Compare with an overall aggregate | Scalar subquery, or window function |
| Filter by membership in another table | `IN`, `EXISTS`, or `JOIN` |
| Rows with no match | `NOT EXISTS` (safest), `LEFT JOIN … IS NULL`, `EXCEPT` |
| Compare with the row's own group | Correlated subquery, or `AVG() OVER (PARTITION BY …)` |
| Aggregate in two steps | Derived table or CTE |
| Reuse the same subquery several times | CTE (Lesson 13) |

## Summary

:::key
- Subqueries are queries in brackets inside another query; they can return a value, a list or a table.
- Scalar subqueries compare with or display a single value (e.g. the overall average).
- `IN`, `ANY`, `ALL` work with multi-row subqueries; `> ALL` = greater than the max.
- Correlated subqueries reference the outer row (e.g. above the employee's department average).
- `EXISTS` / `NOT EXISTS` test for matching rows; prefer `NOT EXISTS` over `NOT IN` when NULLs are possible.
- Derived tables (inline views) aggregate first, then filter/join; they need an alias.
:::

:::quiz
Q: Why does `WHERE sales > AVG(sales)` fail?
- AVG needs GROUP BY
* Aggregate functions are not allowed in WHERE; use a subquery
- sales must be in brackets
- The comparison must use ALL
> WHERE runs before aggregation, so compute the average in a subquery.

Q: A subquery in FROM must have:
- An ORDER BY
* An alias
- A WHERE clause
- A GROUP BY
> Derived tables must be named.

Q: `WHERE x NOT IN (SELECT y FROM t)` returns no rows even though some x values are missing from t. Most likely cause?
- t is empty
* t.y contains a NULL
- x has duplicates
- NOT IN cannot be used with subqueries
> One NULL in the list makes every NOT IN comparison UNKNOWN.

Q: What is a correlated subquery?
- A subquery in FROM
* A subquery that references a column from the outer query
- A subquery with a JOIN
- A subquery that returns one value
> It is evaluated in the context of each outer row.

Q: `salary > ALL (SELECT salary FROM emp WHERE dept = 'HR')` is equivalent to:
* salary > the maximum HR salary
- salary > the minimum HR salary
- salary > the average HR salary
- salary IN the HR salaries
> Greater than all values means greater than the largest one.

Q: To compute average order value from order lines, you should:
- AVG(sales) on order_items
* Sum sales per order in a derived table, then average those totals
- Divide total sales by the number of lines
- Use COUNT(DISTINCT sales)
> Average order value is the mean of order totals, which needs two aggregation levels.
:::

:::exercise Subquery practice
(1) List products whose total sales are above the average product's total sales. (2) For each department, show employees whose income is the highest in that department. (3) Find cities where every order line in 2025 had a discount of at most 20%. (4) Show customers whose first order was in 2025.
???
```sql
-- (1)
SELECT product_id, SUM(sales) AS sales FROM order_items GROUP BY product_id
HAVING SUM(sales) > (SELECT AVG(t.s) FROM (SELECT SUM(sales) AS s FROM order_items GROUP BY product_id) AS t);
-- (2)
SELECT e.department, e.emp_id, e.monthly_income FROM employees e
WHERE e.monthly_income = (SELECT MAX(e2.monthly_income) FROM employees e2 WHERE e2.department = e.department);
-- (3)
SELECT DISTINCT city FROM superstore s
WHERE YEAR(order_date) = 2025
  AND NOT EXISTS (SELECT 1 FROM superstore s2 WHERE s2.city = s.city AND YEAR(s2.order_date) = 2025 AND s2.discount > 0.2);
-- (4)
SELECT customer_id FROM orders GROUP BY customer_id HAVING MIN(order_date) >= '2025-01-01';
```
:::

:::interview Questions you may be asked
**Q: Difference between a correlated and a non-correlated subquery?**
A non-correlated subquery runs independently once; a correlated subquery references the outer query and is evaluated per outer row.

**Q: EXISTS vs IN?**
IN compares a value with a list; EXISTS checks for the existence of matching rows and stops at the first one. EXISTS handles NULLs safely in the negative form (NOT EXISTS).

**Q: Find employees who earn more than their department's average.**
Correlated subquery on department, or `AVG(income) OVER (PARTITION BY department)` in a CTE and filter.

**Q: Subquery vs JOIN: which is faster?**
It depends; modern optimisers often produce the same plan. Joins are usually clearer for combining columns; EXISTS for existence tests; derived tables/CTEs for multi-step aggregation. Check the execution plan.
:::
