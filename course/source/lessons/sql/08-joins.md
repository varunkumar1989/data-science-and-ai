---
num: 8
title: Joins and a Retail Case Study
live: "SQL class 4"
updated: "SQL Server 2022, 2026"
level: Intermediate
duration: 150 min
summary: Combine tables with INNER, LEFT, RIGHT, FULL OUTER, CROSS and SELF joins, find missing matches with anti-joins, avoid the classic join mistakes (row explosion, filters in ON vs WHERE), and answer a full set of business questions on the retail database.
datasets: [superstore_sales.csv, customers.csv, products.csv]
outcomes:
  - Explain each join type with a Venn picture and predict how many rows it returns
  - Write INNER, LEFT, RIGHT, FULL OUTER, CROSS and SELF joins with table aliases
  - Find unmatched rows with LEFT JOIN … IS NULL (anti-join)
  - Avoid row explosion, ambiguous columns, and the ON-vs-WHERE trap in outer joins
  - Join three or four tables to answer business questions
---

## Why joins?

In a normalised database (Lesson 2) customer details live in `customers`, products in `products`, and orders in `orders` and `order_items`. To answer "sales by customer segment and product category" you must **join** them back together on their keys. A join is SQL's version of XLOOKUP (Excel Lesson 7) and pandas `merge()`.

## A tiny example first

Two small tables make every join type easy to see:

```sql run
CREATE TABLE students (student_id INT PRIMARY KEY, name VARCHAR(20));
INSERT INTO students VALUES (1, 'Asha'), (2, 'Ravi'), (3, 'Meera'), (4, 'Kabir');

CREATE TABLE enrolments (student_id INT, course VARCHAR(20));
INSERT INTO enrolments VALUES (1, 'SQL'), (1, 'Python'), (2, 'Excel'), (5, 'Power BI');

SELECT 'students' AS t, COUNT(*) AS n FROM students UNION ALL SELECT 'enrolments', COUNT(*) FROM enrolments;
```

Asha (1) has two enrolments, Ravi (2) has one, Meera (3) and Kabir (4) have none, and enrolment for student 5 has no matching student (an "orphan" row).

```python fig: The join types as Venn diagrams. Shaded areas are the rows returned (A = left table, B = right table).
dg.joins_panel(("inner", "left", "right", "full", "left_anti"), labels=["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL OUTER JOIN", "LEFT ANTI JOIN"])
```

### INNER JOIN: only matches

```sql run
SELECT s.student_id, s.name, e.course
FROM students AS s
INNER JOIN enrolments AS e
        ON e.student_id = s.student_id
ORDER BY s.student_id, e.course;
```

Asha appears **twice** because she has two matching enrolments. Meera, Kabir and the orphan enrolment disappear.

### LEFT (OUTER) JOIN: everything from the left

```sql run
SELECT s.student_id, s.name, e.course
FROM students AS s
LEFT JOIN enrolments AS e
       ON e.student_id = s.student_id
ORDER BY s.student_id, e.course;
```

Every student is kept; where there is no match, the right-hand columns are **NULL**.

### RIGHT JOIN: everything from the right

```sql run
SELECT e.student_id, s.name, e.course
FROM students AS s
RIGHT JOIN enrolments AS e
        ON e.student_id = s.student_id
ORDER BY e.student_id;
```

Every enrolment is kept, including student 5 who has no name. A RIGHT JOIN is just a LEFT JOIN with the tables swapped; most people write LEFT JOINs for consistency.

### FULL OUTER JOIN: everything from both

```sql run
SELECT s.student_id AS s_id, s.name, e.student_id AS e_id, e.course
FROM students AS s
FULL OUTER JOIN enrolments AS e
             ON e.student_id = s.student_id
ORDER BY COALESCE(s.student_id, e.student_id), e.course;
```

Matched rows, plus unmatched students, plus unmatched enrolments. Useful for **reconciliation**: comparing two systems' lists to see what is missing on each side.

### Anti-join: rows with no match

```sql run
SELECT s.student_id, s.name
FROM students AS s
LEFT JOIN enrolments AS e ON e.student_id = s.student_id
WHERE e.student_id IS NULL;
```

"Students not enrolled in anything." The same result with `NOT EXISTS` is shown in Lesson 10.

### CROSS JOIN: every combination

```sql run
CREATE TABLE sizes (size VARCHAR(5));
INSERT INTO sizes VALUES ('S'), ('M'), ('L');
CREATE TABLE colours (colour VARCHAR(10));
INSERT INTO colours VALUES ('Black'), ('White');

SELECT c.colour, z.size
FROM colours AS c
CROSS JOIN sizes AS z
ORDER BY c.colour, z.size;
```

2 colours × 3 sizes = 6 rows: a **Cartesian product**. Use it on purpose (all product–month combinations for a report grid, a calendar × store table); never by accident.

### SELF JOIN: a table joined to itself

```sql run
CREATE TABLE team (emp_id INT, name VARCHAR(20), manager_id INT);
INSERT INTO team VALUES (1, 'Varun', NULL), (2, 'Asha', 1), (3, 'Ravi', 1), (4, 'Meera', 2), (5, 'Kabir', 2);

SELECT e.name AS employee, m.name AS manager
FROM team AS e
LEFT JOIN team AS m ON m.emp_id = e.manager_id
ORDER BY e.emp_id;
```

The same table appears twice with different aliases (`e` for employee, `m` for manager). LEFT JOIN keeps Varun, who has no manager.

### How many rows will a join return?

| Join | Rows returned |
|---|---|
| INNER | Sum over matches; a key matching m rows on the left and n on the right produces m × n rows |
| LEFT | Every left row at least once (more if it matches several right rows) |
| RIGHT | Every right row at least once |
| FULL | Matches + unmatched left + unmatched right |
| CROSS | Left rows × right rows |

## Joins on the retail database

```python fig: Join paths in RetailDB. Follow the keys: customers → orders → order_items → products.
dg.er({"customers": (0.3, 5.3, ["customer_id*", "customer_name", "segment", "city", "region"]),
       "orders": (3.4, 5.3, ["order_id*", "order_date", "ship_mode", "customer_id#"]),
       "order_items": (3.4, 2.75, ["item_id*", "order_id#", "product_id#", "quantity", "sales", "profit"]),
       "products": (6.5, 2.75, ["product_id*", "product_name", "category", "sub_category"])},
      [("customers", "orders", "customer_id"), ("orders", "order_items", "order_id"), ("products", "order_items", "product_id")], title="RetailDB join keys", width=9, height=5.6)
```

### Two tables

```sql run rows=8
SELECT o.order_id, o.order_date, c.customer_name, c.segment, c.city
FROM orders AS o
INNER JOIN customers AS c ON c.customer_id = o.customer_id
ORDER BY o.order_date DESC, o.order_id;
```

### Four tables

```sql run
SELECT c.segment,
       p.category,
       COUNT(DISTINCT o.order_id)  AS orders,
       ROUND(SUM(oi.sales), 0)     AS sales,
       ROUND(SUM(oi.profit), 0)    AS profit
FROM order_items AS oi
JOIN orders      AS o ON o.order_id    = oi.order_id
JOIN customers   AS c ON c.customer_id = o.customer_id
JOIN products    AS p ON p.product_id  = oi.product_id
GROUP BY c.segment, p.category
ORDER BY c.segment, sales DESC;
```

`JOIN` on its own means `INNER JOIN`. Start from the table at the most detailed level (the **grain**: here, one row per order item) and join outward to the lookup tables.

## Case study: questions for the Head of Sales

:::case Q1. Which customers have never placed an order?
Marketing wants to send them a welcome-back offer.
:::

```sql run
SELECT c.customer_id, c.customer_name, c.city, c.segment
FROM customers AS c
LEFT JOIN orders AS o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id;
```

:::case Q2. Which products have never been sold?
:::

```sql run
SELECT COUNT(*) AS products_never_sold
FROM products AS p
LEFT JOIN order_items AS oi ON oi.product_id = p.product_id
WHERE oi.item_id IS NULL;
```

:::case Q3. Top 10 customers by 2025 sales, with their city and segment
:::

```sql run
SELECT TOP 10
       c.customer_name, c.city, c.segment,
       COUNT(DISTINCT o.order_id) AS orders_2025,
       ROUND(SUM(oi.sales), 0)    AS sales_2025
FROM customers AS c
JOIN orders AS o       ON o.customer_id = c.customer_id
JOIN order_items AS oi ON oi.order_id   = o.order_id
WHERE o.order_date >= '2025-01-01' AND o.order_date < '2026-01-01'
GROUP BY c.customer_id, c.customer_name, c.city, c.segment
ORDER BY sales_2025 DESC;
```

:::case Q4. Which region × category combinations lose money on discounted Furniture?
:::

```sql run
SELECT c.region,
       p.sub_category,
       COUNT(*)                    AS lines,
       ROUND(AVG(oi.discount), 2)  AS avg_discount,
       ROUND(SUM(oi.profit), 0)    AS profit
FROM order_items AS oi
JOIN orders    AS o ON o.order_id    = oi.order_id
JOIN customers AS c ON c.customer_id = o.customer_id
JOIN products  AS p ON p.product_id  = oi.product_id
WHERE p.category = 'Furniture' AND oi.discount > 0
GROUP BY c.region, p.sub_category
HAVING SUM(oi.profit) < 0
ORDER BY profit;
```

:::case Q5. How does actual selling price compare with the list price?
:::

```sql run
SELECT p.category,
       ROUND(SUM(oi.sales), 0)                                   AS actual_sales,
       ROUND(SUM(oi.quantity * p.list_price), 0)                 AS list_value,
       ROUND(100.0 * (1 - SUM(oi.sales) / SUM(oi.quantity * p.list_price)), 1) AS avg_discount_given_pct
FROM order_items AS oi
JOIN products AS p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY avg_discount_given_pct DESC;
```

## Common join mistakes

### 1. Row explosion (fan-out)

Joining two "many" tables on a shared key multiplies rows. If you join `order_items` to another table with several rows per order (for example a `payments` table with instalments), each item is repeated for each payment and `SUM(sales)` is inflated. Always ask: *what is one row of each table, and is the key unique on one side?* Check with `COUNT(*)` before and after the join, or aggregate each table to the same grain first (Lesson 10).

### 2. Ambiguous column names

`SELECT order_id FROM orders JOIN order_items ON …` fails: "Ambiguous column name 'order_id'". Prefix columns with the table alias (`o.order_id`). Do it for every column in multi-table queries.

### 3. Filtering an outer join in WHERE

A condition on the **right** table placed in `WHERE` removes the NULL rows and silently turns a LEFT JOIN into an INNER JOIN:

```sql run
-- Intended: all students, with their SQL course if any
SELECT s.name, e.course
FROM students AS s
LEFT JOIN enrolments AS e ON e.student_id = s.student_id
WHERE e.course = 'SQL';            -- wrong: drops students without SQL
```

```sql run
SELECT s.name, e.course
FROM students AS s
LEFT JOIN enrolments AS e
       ON e.student_id = s.student_id
      AND e.course = 'SQL'         -- right: condition in ON keeps every student
ORDER BY s.student_id;
```

### 4. Joining on the wrong or non-unique key

Joining customers to orders on `city` instead of `customer_id` creates nonsense matches. Join on keys, and check the relationship (1:1, 1:N) you expect.

### 5. NULL keys never match

`NULL = NULL` is UNKNOWN, so rows with a NULL key never match in any join. Clean or default keys first if that matters.

:::tip Join check-list
1. What is the grain (one row = ?) of each table? 2. Which key connects them, and is it unique on one side? 3. Do I need unmatched rows (LEFT/FULL) or only matches (INNER)? 4. Did the row count change as expected? 5. Are filters on outer-joined tables in ON or WHERE on purpose?
:::

## Older join syntax you may see

```sql
-- Implicit join (comma join), pre-1992 style: works but avoid
SELECT o.order_id, c.customer_name
FROM orders o, customers c
WHERE o.customer_id = c.customer_id;
```

Forgetting the WHERE turns it into a CROSS JOIN. Use explicit `JOIN … ON`.

## Summary

:::key
- **INNER**: only matching rows. **LEFT**: all left rows + matches (NULLs where none). **RIGHT**: the mirror. **FULL**: everything. **CROSS**: every combination. **SELF**: a table with itself (aliases).
- **Anti-join**: `LEFT JOIN … WHERE right.key IS NULL` finds rows with no match.
- Join from the most detailed table outward, on keys, with aliases on every column.
- Watch for row explosion, ambiguous columns, and filters on the right table in WHERE (move them to ON).
- Joins = XLOOKUP / Power Query Merge / pandas merge / Power BI relationships.
:::

:::quiz
Q: Table A has 4 rows, B has 3. A CROSS JOIN returns:
- 3 rows
- 4 rows
- 7 rows
* 12 rows
> A Cartesian product returns 4 × 3 rows.

Q: Which join lists every customer, including those with no orders?
- `customers INNER JOIN orders`
* `customers LEFT JOIN orders`
- `customers RIGHT JOIN orders` with orders on the right
- `customers CROSS JOIN orders`
> LEFT JOIN keeps every row from the left table.

Q: How do you find products that were never ordered?
- `products INNER JOIN order_items WHERE item_id IS NULL`
* `products LEFT JOIN order_items … WHERE order_items.item_id IS NULL`
- `products FULL JOIN order_items`
- `SELECT DISTINCT product_id FROM order_items`
> A left anti-join returns left rows with no match.

Q: `FROM students s LEFT JOIN enrolments e ON … WHERE e.course = 'SQL'` behaves like:
- A LEFT JOIN
* An INNER JOIN, because rows with NULL course are removed
- A FULL JOIN
- A CROSS JOIN
> The WHERE condition on the right table discards the unmatched (NULL) rows.

Q: What is a self join used for?
* Relating rows of the same table, such as employees and their managers
- Joining a table to a copy in another database
- Removing duplicates
- Joining without a key
> The same table is used twice with different aliases.

Q: After joining order_items to a payments table with 2 instalments per order, SUM(sales) doubled. What happened?
- A NULL key
* Row explosion: each item was repeated once per payment row
- Integer division
- A wrong data type
> Joining two many-sided tables multiplies rows; aggregate to the same grain first.
:::

:::exercise Join practice
(1) List each order with customer name, city and the number of items in the order. (2) For each customer segment, show the share of sales from each category (%). (3) Find customers who bought Technology but never Furniture. (4) Using `team`, show each manager with the number of direct reports.
???
```sql
-- (1)
SELECT o.order_id, c.customer_name, c.city, COUNT(oi.item_id) AS items
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY o.order_id, c.customer_name, c.city;
-- (2)
SELECT c.segment, p.category,
       ROUND(100.0 * SUM(oi.sales) / SUM(SUM(oi.sales)) OVER (PARTITION BY c.segment), 1) AS pct_of_segment
FROM order_items oi JOIN orders o ON o.order_id = oi.order_id
JOIN customers c ON c.customer_id = o.customer_id JOIN products p ON p.product_id = oi.product_id
GROUP BY c.segment, p.category;            -- the window function is explained in Lesson 12
-- (3)
SELECT DISTINCT c.customer_id, c.customer_name
FROM customers c JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id JOIN products p ON p.product_id = oi.product_id
WHERE p.category = 'Technology'
  AND c.customer_id NOT IN (SELECT o2.customer_id FROM orders o2 JOIN order_items oi2 ON oi2.order_id = o2.order_id
                            JOIN products p2 ON p2.product_id = oi2.product_id WHERE p2.category = 'Furniture');
-- (4)
SELECT m.name AS manager, COUNT(e.emp_id) AS direct_reports
FROM team m LEFT JOIN team e ON e.manager_id = m.emp_id
GROUP BY m.emp_id, m.name HAVING COUNT(e.emp_id) > 0;
```
:::

:::interview Questions you may be asked
**Q: Explain the different types of joins.**
INNER returns matches; LEFT/RIGHT keep all rows from one side with NULLs where unmatched; FULL keeps all rows from both; CROSS returns every combination; SELF joins a table to itself.

**Q: Table A has 5 rows with id 1 repeated twice, B has 3 rows with id 1 repeated three times. How many rows does an inner join on id return (other ids unmatched)?**
2 × 3 = 6 rows.

**Q: How do you find records in one table but not another?**
LEFT JOIN … WHERE right.key IS NULL, NOT EXISTS, or EXCEPT (Lesson 9).

**Q: What is the difference between putting a condition in ON vs WHERE for a LEFT JOIN?**
In ON it only limits which right rows match (all left rows stay); in WHERE it filters the final result and removes unmatched left rows.
:::
