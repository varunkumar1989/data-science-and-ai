---
num: 10
title: "Comprehensions, Lambda, map/filter and Generators"
live: "Python class 8"
updated: "Python 3.13"
level: Beginner
duration: 100 min
summary: Write compact, readable Python. Learn list, set and dict comprehensions, lambda with sorted/min/max, map and filter, any and all, generators and itertools, and when plain loops or pandas are the better choice.
datasets: [superstore_sales.csv]
outcomes:
  - Write list, set and dictionary comprehensions with conditions and nesting
  - Use lambda functions with sorted, min, max, map and filter
  - Use any, all, zip, enumerate and sum with generator expressions
  - Explain lazy evaluation and write generator functions with yield
  - Use itertools and functools for common patterns and know when not to be clever
---

## List comprehensions

A **comprehension** builds a collection from another in one expression: `[expression for item in iterable if condition]`.

```python fig: A comprehension reads like the sentence "give me X for each item, if the condition holds".
dg.flow(["for item in iterable", "if condition", "expression", "new list"], title="[ expression  for item in iterable  if condition ]")
```

```python run
nums = [1, 2, 3, 4, 5, 6]
squares = [n * n for n in nums]
evens = [n for n in nums if n % 2 == 0]
labels = ["even" if n % 2 == 0 else "odd" for n in nums]          # if/else goes BEFORE the for
loop_version = []
for n in nums:
    if n % 2 == 0: loop_version.append(n * n)
print(squares, evens, labels, [n * n for n in nums if n % 2 == 0] == loop_version)
```

```python run
words = ["  Pune ", "delhi", " KOCHI", "goa  "]
print([w.strip().title() for w in words])
print([(x, y) for x in (1, 2) for y in ("a", "b")])             # two loops
matrix = [[1, 2, 3], [4, 5, 6]]
print([v for row in matrix for v in row], [list(col) for col in zip(*matrix)])    # flatten, transpose
```

### Set and dictionary comprehensions

```python run
print({len(w) for w in ["tea", "cup", "mug", "plate"]})                         # set
prices = {"Pen": 10, "Notebook": 45, "Stapler": 180}
print({k: round(v * 1.18, 2) for k, v in prices.items()})                                  # dict
print({k: v for k, v in prices.items() if v > 20}, {c: ord(c) for c in "abc"})
```

:::tip Keep it readable
If a comprehension needs more than one condition or nested level, or does not fit comfortably on one or two lines, use a normal loop or a helper function. Clever is not the goal; clear is.
:::

## Lambda functions

A **lambda** is a small anonymous function: `lambda args: expression`.

```python run
sq = lambda x: x * x                          # fine to learn with, but def is better for named functions
print(sq(5), (lambda a, b: a + b)(2, 3))
people = [("Asha", 29, 62000), ("Ravi", 35, 88000), ("Meera", 31, 75000)]
print(sorted(people, key=lambda p: p[2], reverse=True))        # sort by salary
print(min(people, key=lambda p: p[1]), max(people, key=lambda p: p[2])[0])
print(sorted(["banana", "kiwi", "apple", "fig"], key=lambda w: (len(w), w)))    # sort by length, then alphabet
```

Lambdas shine as the `key=` for `sorted`, `min`, `max`, and in `df.apply`.

## map, filter, any, all

```python run
nums = [3, 8, 12, 5, 20]
print(list(map(lambda x: x * 2, nums)), list(map(str, nums)), list(filter(lambda x: x > 6, nums)))
print([x * 2 for x in nums], [x for x in nums if x > 6])         # comprehensions say the same thing
print(any(n > 15 for n in nums), all(n > 0 for n in nums), sum(1 for n in nums if n % 2 == 0))
print(list(zip(["a", "b", "c"], [1, 2, 3])), dict(zip("abc", range(3))), list(enumerate("xyz", 1)))
```

`map` and `filter` return lazy iterators; wrap with `list(...)`. Most Python programmers prefer comprehensions, but you will see both.

## Generators: lazy sequences

A **generator expression** uses parentheses and produces items one at a time, without building the whole list in memory.

```python run
import sys
big_list = [n * n for n in range(1_000_000)]
big_gen = (n * n for n in range(1_000_000))
print(sys.getsizeof(big_list) // 1000, "KB list vs", sys.getsizeof(big_gen), "bytes generator")
print(sum(n * n for n in range(1_000_000)), next(iter(big_gen)), next(big_gen))
```

A **generator function** uses `yield`. It pauses at each `yield` and resumes on the next request:

```python run
def countdown(n):
    while n > 0:
        yield n
        n -= 1
print(list(countdown(5)))
def read_in_batches(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]
for batch in read_in_batches(list(range(10)), 4): print(batch)
def fib():
    a, b = 0, 1
    while True:                    # infinite sequence, safe because it is lazy
        yield a
        a, b = b, a + b
import itertools
print(list(itertools.islice(fib(), 12)))
```

Generators are how Python reads large files line by line, streams API pages and chains pipeline steps with constant memory. Once consumed, a generator is empty:

```python run
g = (x for x in range(3))
print(list(g), list(g))
```

## itertools and functools highlights

```python run
import itertools, functools, operator
from collections import Counter
print(list(itertools.chain([1, 2], [3], [4, 5])), list(itertools.combinations("ABC", 2)), list(itertools.product("AB", [0, 1])))
print(list(itertools.accumulate([10, 20, 5, 15])), functools.reduce(operator.mul, [1, 2, 3, 4, 5]))
for key, grp in itertools.groupby(sorted(["ant", "bee", "ape", "bat"]), key=lambda w: w[0]): print(key, list(grp))
@functools.lru_cache(maxsize=None)               # memoise a function: remember results of earlier calls
def slow_square(n): return n * n
print([slow_square(n) for n in (4, 4, 5, 4)], slow_square.cache_info())
```

## Real data examples

```python run
import pandas as pd
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date"])
regions = sorted(s["region"].unique())
print({r: round(float(s.loc[s.region == r, "sales"].sum()) / 1e6, 1) for r in regions})                  # dict comprehension
top_customers = [c for c, n in s["customer_id"].value_counts().items() if n >= 18][:5]
print(top_customers, len([c for c, n in s["customer_id"].value_counts().items() if n >= 18]))
rows = s.head(4)[["order_id", "sales", "profit"]].to_dict("records")
print([{**r, "margin": round(100 * r["profit"] / r["sales"], 1)} for r in rows])                  # enrich records
print(sorted(s["category"].unique(), key=lambda c: -s.loc[s.category == c, "sales"].sum()))        # sort by a computed key
```

## Which tool when?

| Situation | Prefer |
|---|---|
| Transform or filter a small list | List comprehension |
| Sort by a rule | `sorted(..., key=lambda ...)` |
| Huge or streaming data | Generator (expression or function) |
| Table columns | Vectorised pandas (`df["a"] * 2`, `np.where`), not comprehensions |
| Multi-step logic with side effects | Plain `for` loop |
| Reuse the same transformation | Named `def` function |

## Summary

:::key
- `[expr for x in it if cond]` builds a list; `{…}` builds sets and dicts; the conditional expression (`a if c else b`) comes before `for`.
- `lambda` is an anonymous one-expression function, mostly used as `key=` and in `apply`.
- `map`/`filter` are lazy; comprehensions are usually clearer. `any`, `all`, `sum` work well with generator expressions.
- Generators (`( … )` or `yield`) produce values lazily, use almost no memory and can be infinite; they can be consumed only once.
- `itertools` and `functools` (`chain`, `combinations`, `groupby`, `lru_cache`, `reduce`) cover many patterns; keep code readable and vectorise table work.
:::

:::quiz
Q: What does `[x * 2 for x in range(4) if x != 2]` give?
- [0, 2, 4, 6]
* [0, 2, 6]
- [0, 4, 6]
- [2, 6]
> Item 2 is filtered out before doubling.

Q: Where does an `if ... else` go in a comprehension?
- After the for
* Before the for, as part of the expression
- It is not allowed
- At the end
> `[a if cond else b for x in it]`.

Q: What is the main advantage of a generator expression over a list comprehension?
- It is faster to type
* It is lazy and uses very little memory
- It supports indexing
- It can be reused
> Values are produced one at a time.

Q: What does `sorted(people, key=lambda p: p[2])` do?
- Sorts by the first item
* Sorts by the third item of each tuple
- Reverses the list
- Raises an error
> `key` supplies the sort value.

Q: What happens when you iterate a generator twice?
- It restarts
* The second pass is empty because it was consumed
- It raises an error
- It doubles the values
> Create a new generator or use a list.

Q: Which is usually best for adding a column to a DataFrame?
- A for loop over rows
* A vectorised column operation
- A generator
- A lambda inside a nested loop
> Vectorised code is shorter and much faster.
:::

:::exercise Comprehension problems
(1) List the squares of odd numbers from 1 to 20. (2) Build a dictionary from words to their lengths for words longer than 3 letters. (3) Flatten `[[1,2],[3],[4,5,6]]`. (4) Sort `["pune","Delhi","goa","Kochi"]` case-insensitively. (5) Write a generator that yields only the primes below 50. (6) From the Superstore data, list sub-categories with total profit below zero.
???
```python
print([n * n for n in range(1, 21) if n % 2])
print({w: len(w) for w in ["tea", "plate", "mug", "bottle"] if len(w) > 3})
print([v for part in [[1, 2], [3], [4, 5, 6]] for v in part])
print(sorted(["pune", "Delhi", "goa", "Kochi"], key=str.lower))
def primes(limit):
    for n in range(2, limit):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)): yield n
print(list(primes(50)))
loss = s.groupby("sub_category")["profit"].sum()
print(list(loss[loss < 0].index))
```
:::

:::interview Questions you may be asked
**Q: List comprehension vs generator expression?**
Both iterate with the same syntax; the list builds everything now in memory, the generator yields lazily and is single-use.

**Q: When should you avoid a comprehension?**
When logic needs several statements, side effects, or deep nesting; readability matters more than brevity.

**Q: What does `yield` do?**
It turns a function into a generator: the function pauses, hands back a value, and resumes where it left off on the next call.

**Q: How do you flatten a list of lists?**
`[x for sub in lists for x in sub]` or `itertools.chain.from_iterable(lists)`.
:::
