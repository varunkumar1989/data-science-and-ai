---
num: 8
title: "Dictionaries: Key-Value Data, Counting and Grouping"
live: "Python class 6"
updated: "Python 3.13"
level: Beginner
duration: 100 min
summary: Store and look up data by key. Create and update dictionaries, use get, setdefault, items, Counter and defaultdict, nest dictionaries, and convert between dictionaries, JSON-like records and DataFrames using the Superstore data.
datasets: [superstore_sales.csv]
outcomes:
  - Create dictionaries and read, add, update and delete keys safely
  - Loop over keys, values and items and merge dictionaries
  - Count and group with get, setdefault, Counter and defaultdict
  - Work with nested dictionaries and lists of dictionaries (JSON-like records)
  - Convert between dictionaries and pandas DataFrames
---

## What is a dictionary?

A **dictionary** (`dict`) maps **keys** to **values**: look up by name instead of by position. It keeps insertion order (Python 3.7+), and lookups are O(1) on average.

```python fig: A dictionary is a set of key → value pairs. The key is hashed, so the lookup does not scan the data.
dg.cards([("'name'  →  'Kavya Iyer'", "key 'name' is hashed to find its value"), ("'dept'  →  'HR'", "key 'dept' maps to a string"), ("'salary'  →  97000", "values can be any type")], title="emp = {'name': 'Kavya Iyer', 'dept': 'HR', 'salary': 97000}")
```

```python run
emp = {"name": "Kavya Iyer", "dept": "HR", "salary": 97000}
print(emp["name"], emp.get("dept"), emp.get("city"), emp.get("city", "unknown"), len(emp), "salary" in emp)
try: emp["city"]
except KeyError as e: print("KeyError:", e)
```

`d[key]` raises `KeyError` when missing; `d.get(key, default)` never does.

## Changing a dictionary

```python run
emp["city"] = "Pune"                 # add
emp["salary"] += 3000                 # update
emp.update({"dept": "Finance", "grade": "M2"})
removed = emp.pop("grade")           # remove and return
del emp["city"]
print(emp, removed)
print(emp.setdefault("level", "L3"), emp.setdefault("dept", "X"), emp)    # set only if missing
```

| Method | Effect |
|---|---|
| `d[k] = v` | Add or overwrite |
| `d.get(k, default)` | Safe read |
| `d.setdefault(k, default)` | Read; insert default if missing |
| `d.update(other)` or `d \| other` | Merge (right side wins) |
| `d.pop(k[, default])` | Remove and return |
| `d.popitem()` | Remove the last pair |
| `del d[k]` | Delete (KeyError if missing) |
| `d.keys()`, `d.values()`, `d.items()` | Views |
| `d.copy()` | Shallow copy |
| `dict.fromkeys(keys, value)` | Create with the same value |

## Looping

```python run
prices = {"Pen": 10, "Notebook": 45, "Stapler": 180}
for k in prices: print(k, end=" ")
print()
for k, v in prices.items(): print(f"{k:<10}{v:>5}")
print(list(prices.values()), sum(prices.values()), max(prices, key=prices.get), sorted(prices.items(), key=lambda kv: -kv[1]))
merged = prices | {"Pen": 12, "Folder": 30}               # Python 3.9+
print(merged)
print({v: k for k, v in prices.items()})                   # invert (values must be unique and hashable)
```

## Counting and grouping

The most common dictionary jobs are **count** and **group**:

```python run
from collections import Counter, defaultdict
words = "the cat and the hat and the bat".split()
manual = {}
for w in words: manual[w] = manual.get(w, 0) + 1            # classic pattern
print(manual)
c = Counter(words)
print(c, c.most_common(2), c["the"], c["dog"])
groups = defaultdict(list)                                    # missing key starts as an empty list
for w in words: groups[len(w)].append(w)
print(dict(groups))
```

```python run
import pandas as pd
s = pd.read_csv("superstore_sales.csv")
by_region = Counter(s["region"])                              # count rows
revenue = defaultdict(float)
for r, amount in zip(s["region"], s["sales"]): revenue[r] += amount
print(by_region.most_common())
print({k: round(v / 1e6, 1) for k, v in sorted(revenue.items(), key=lambda kv: -kv[1])}, "(sales in millions)")
print(s.groupby("region")["sales"].sum().div(1e6).round(1).sort_values(ascending=False).to_dict())   # same in pandas
```

## Nested dictionaries and JSON-like records

Real data (API responses, configs, documents) nests dictionaries and lists. Python's `json` module reads and writes exactly this structure.

```python run
import json
order = {"order_id": "O-1001", "customer": {"id": "C7", "name": "Asha", "city": "Pune"},
         "items": [{"sku": "P1", "qty": 2, "price": 450.0}, {"sku": "P2", "qty": 1, "price": 1200.0}]}
total = sum(i["qty"] * i["price"] for i in order["items"])
print(order["customer"]["city"], len(order["items"]), total, order.get("shipping", {}).get("city", "n/a"))
text = json.dumps(order, indent=2)
print(text[:90].replace("\n", " "), "...", json.loads(text) == order)
```

A **list of dictionaries** is the standard row format, and it converts straight to a DataFrame:

```python run
rows = [{"sku": "P1", "qty": 2, "price": 450.0}, {"sku": "P2", "qty": 1, "price": 1200.0}, {"sku": "P3", "qty": 5, "price": 80.0}]
df = pd.DataFrame(rows)
df["value"] = df.qty * df.price
print(df)
print(df.set_index("sku")["value"].to_dict(), df.to_dict("records")[0])
```

## Lookup tables and dispatch

```python run
tier = {"North": "A", "South": "A", "East": "B", "West": "C"}                # mapping/lookup
print(s["region"].map(tier).value_counts().to_dict())
ops = {"add": lambda a, b: a + b, "mul": lambda a, b: a * b}                  # dictionary of functions
print(ops["add"](3, 4), ops["mul"](3, 4))
```

:::note Keys must be hashable
Strings, numbers and tuples work as keys; lists, sets and dicts do not. Use a tuple `("North", 2025)` for composite keys. Copying: `d.copy()` is shallow; use `copy.deepcopy` for nested data (Lesson 6).
:::

## Common mistakes

| Mistake | Fix |
|---|---|
| `d["missing"]` raises KeyError | `d.get(k, default)` or `if k in d` |
| Changing a dictionary's size while looping over it | Loop over `list(d)` or build a new dict |
| `{}` for an empty set | `set()`; `{}` is an empty dict |
| Duplicate keys in a literal | The last one silently wins |
| Assuming a shallow copy protects nested data | `copy.deepcopy` |

## Summary

:::key
- A dict maps hashable keys to values with O(1) average lookup and keeps insertion order.
- Use `get` for safe reads, `setdefault`/`defaultdict` for grouping, `Counter` for counting, `d | other` to merge.
- Loop with `items()`; build with dict comprehensions `{k: f(v) for k, v in ...}`.
- Nested dict/list structures are JSON; a list of dicts converts to a DataFrame with `pd.DataFrame(rows)`.
- Dictionaries are lookup tables: `series.map(dict)` is a fast way to recode a column.
:::

:::quiz
Q: What does `d.get("x", 0)` do when "x" is missing?
- Raises KeyError
* Returns 0
- Adds the key
- Returns None
> `get` never raises; it returns the default.

Q: Which is a valid dictionary key?
- `[1, 2]`
* `(1, 2)`
- `{1, 2}`
- `{"a": 1}`
> Keys must be hashable (immutable).

Q: Which tool counts occurrences most directly?
- `defaultdict(list)`
* `collections.Counter`
- `set`
- `zip`
> `Counter(items).most_common()`.

Q: What does `{"a": 1} | {"a": 2, "b": 3}` give?
- {"a": 1, "b": 3}
* {"a": 2, "b": 3}
- Error
- {"a": 3}
> The right-hand dictionary wins on conflicts.

Q: How do you loop over keys and values together?
- `for k in d.values()`
* `for k, v in d.items()`
- `for k, v in d`
- `for v in d.keys()`
> `items()` yields (key, value) pairs.

Q: What does `pd.DataFrame(list_of_dicts)` produce?
- A Series
* A table with one row per dictionary and columns from the keys
- A list
- An error
> This is the standard way to turn JSON-like records into a table.
:::

:::exercise Dictionary problems
(1) Count the frequency of each character in `"banana"`. (2) Group Superstore product `category` into a dictionary of sets of `sub_category`. (3) Invert `{"a": 1, "b": 2}`. (4) Given a list of orders, compute the total per customer using `defaultdict`. (5) Merge two dictionaries where the second overrides the first.
???
```python
from collections import Counter, defaultdict
print(Counter("banana"))
g = defaultdict(set)
for c, sc in zip(s["category"], s["sub_category"]): g[c].add(sc)
print({k: sorted(v) for k, v in g.items()})
print({v: k for k, v in {"a": 1, "b": 2}.items()})
orders = [("C1", 100), ("C2", 50), ("C1", 25)]
t = defaultdict(int)
for cid, amt in orders: t[cid] += amt
print(dict(t), {"x": 1} | {"x": 9, "y": 2})
```
:::

:::interview Questions you may be asked
**Q: How does a dictionary achieve O(1) lookup?**
It hashes the key to find a slot in a hash table; collisions are resolved by probing, so the average cost is constant.

**Q: `d[k]` vs `d.get(k)`?**
`d[k]` raises KeyError for a missing key; `get` returns None (or a default).

**Q: Are dictionaries ordered?**
Yes, they preserve insertion order from Python 3.7 onwards.

**Q: Count word frequencies in a text.**
`Counter(text.lower().split()).most_common(10)`.
:::
