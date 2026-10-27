---
num: 12
title: "Files, Exceptions, JSON and CSV"
live: "Python class 10"
updated: "Python 3.13"
level: Intermediate
duration: 110 min
summary: Read and write text, CSV and JSON files safely with pathlib and with-blocks, handle errors with try/except/else/finally, raise your own exceptions, and log what happened, using a small "load a messy file" project.
datasets: [superstore_sales.csv]
outcomes:
  - Open, read and write text files with with-blocks and pathlib
  - Read and write CSV with the csv module and JSON with the json module
  - Handle errors with try, except, else and finally, and catch specific exceptions
  - Raise exceptions and define custom exception classes
  - Use logging instead of print for programs that run unattended
---

## Files and paths

Use `pathlib.Path` for paths (works on Windows, macOS and Linux) and a `with` block to open files: the file is closed automatically, even if an error happens.

```python run
from pathlib import Path
folder = Path("demo_files"); folder.mkdir(exist_ok=True)
notes = folder / "notes.txt"                              # / joins path parts
with open(notes, "w", encoding="utf-8") as f:              # "w" overwrites, "a" appends, "r" reads (default)
    f.write("Line one\n")
    f.writelines(["Line two\n", "Line three\n"])
with open(notes, "a", encoding="utf-8") as f: print("Line four", file=f)
print(notes.read_text(encoding="utf-8"))
print(notes.exists(), notes.name, notes.stem, notes.suffix, notes.stat().st_size, "bytes")
```

```python run
with open(notes, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):                    # iterate line by line: constant memory for huge files
        print(i, line.rstrip("\n"))
with open(notes, encoding="utf-8") as f: lines = f.read().splitlines()
print(lines, sorted(p.name for p in folder.glob("*.txt")))
```

| Mode | Meaning |
|---|---|
| `"r"` | Read (error if missing) |
| `"w"` | Write (creates or **overwrites**) |
| `"a"` | Append to the end |
| `"x"` | Create; error if it exists |
| `"b"` suffix | Binary (`"rb"`, `"wb"`) for images, Excel, Parquet |

:::tip Always give the encoding
`encoding="utf-8"` avoids garbled ₹, é or Hindi text and avoids differences between Windows and Linux defaults.
:::

## CSV files

The standard `csv` module handles quoting and commas inside values. (For analysis you will usually use `pandas.read_csv`, Lesson 16.)

```python run
import csv
rows = [{"id": 1, "city": "Pune", "note": "fast, friendly"}, {"id": 2, "city": "Delhi", "note": 'said "ok"'}]
with open(folder / "people.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["id", "city", "note"])
    w.writeheader(); w.writerows(rows)
print((folder / "people.csv").read_text(encoding="utf-8"))
with open(folder / "people.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f): print(r)                 # every value is a string
```

```python run
# Stream a real 6,000-line CSV without pandas: total sales per region
from collections import defaultdict
totals = defaultdict(float)
with open("superstore_sales.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f): totals[row["region"]] += float(row["sales"])
print({k: round(v / 1e6, 1) for k, v in sorted(totals.items())})
```

## JSON files

JSON maps to Python like this: object ↔ dict, array ↔ list, string ↔ str, number ↔ int/float, true/false ↔ True/False, null ↔ None.

```python run
import json
config = {"source": "superstore_sales.csv", "regions": ["North", "South"], "min_sales": 1000, "debug": False, "owner": None}
with open(folder / "config.json", "w", encoding="utf-8") as f: json.dump(config, f, indent=2)
with open(folder / "config.json", encoding="utf-8") as f: loaded = json.load(f)
print(loaded == config, loaded["regions"], json.dumps({"price": 4500.5, "ok": True, "x": None}))
print(json.dumps({"city": "Pune", "₹": 1}, ensure_ascii=False))
```

`json.dump`/`json.load` work with files; `json.dumps`/`json.loads` work with strings (the "s" is for string). Dates and sets are not JSON types: convert them first (`d.isoformat()`, `list(s)`).

## Exceptions

An **exception** is Python's way of reporting an error. Unhandled, it stops the program and prints a traceback. Handled, your program can recover.

```python run
def safe_ratio(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("  cannot divide by zero")
        return None
    except TypeError as e:
        print("  wrong types:", e)
        return None
    else:                        # runs only when no exception happened
        return round(result, 2)
    finally:                     # always runs: clean-up
        print("  checked", a, b)
print(safe_ratio(10, 4)); print(safe_ratio(1, 0)); print(safe_ratio("10", 2))
```

```python fig: try / except / else / finally: which blocks run.
dg.flow(["try:\nrisky code", "except X:\nhandle error", "else:\nonly if no error", "finally:\nalways"], title="Exception handling flow")
```

### Common built-in exceptions

| Exception | Typical cause |
|---|---|
| `ValueError` | Right type, wrong value: `int("abc")` |
| `TypeError` | Wrong type: `"a" + 1` |
| `KeyError` | Missing dict key |
| `IndexError` | List index out of range |
| `FileNotFoundError` | Missing file |
| `ZeroDivisionError` | Divide by zero |
| `AttributeError` | Object has no such attribute or method |
| `ImportError` / `ModuleNotFoundError` | Package not installed |

```python run
tests = [lambda: int("abc"), lambda: "a" + 1, lambda: {}["x"], lambda: [1][5], lambda: open("missing.csv"), lambda: None.upper()]
for t in tests:
    try: t()
    except Exception as e: print(f"{type(e).__name__:<18} {e}")
```

:::warning Do not swallow every error
`except: pass` or `except Exception: pass` hides bugs. Catch the **specific** exceptions you expect, and let unexpected ones surface (or log them and re-raise).
:::

### Raising your own exceptions

```python run
class DataQualityError(Exception):
    """Raised when an input file fails validation."""

def validate(df):
    missing = {"order_id", "sales"} - set(df.columns)
    if missing: raise DataQualityError(f"missing columns: {sorted(missing)}")
    if (df["sales"] < 0).any(): raise ValueError("negative sales found")
    return True

import pandas as pd
for d in (pd.DataFrame({"order_id": [1], "sales": [5]}), pd.DataFrame({"order_id": [1]}), pd.DataFrame({"order_id": [1], "sales": [-2]})):
    try: print("valid:", validate(d))
    except (DataQualityError, ValueError) as e: print(type(e).__name__, "->", e)
```

Use `raise ... from e` to wrap a low-level error in a clearer one while keeping the original cause.

## Logging

`print` is for interactive work. Programs that run on a schedule (ETL jobs, APIs) should use `logging`, which adds timestamps and levels and can write to files.

```python run
import logging, io
stream = io.StringIO()
log = logging.getLogger("etl"); log.handlers.clear(); log.setLevel(logging.INFO)
h = logging.StreamHandler(stream); h.setFormatter(logging.Formatter("%(levelname)s | %(name)s | %(message)s")); log.addHandler(h)
log.debug("not shown: below INFO"); log.info("loaded 6,323 rows"); log.warning("12 rows had blank city")
try: 1 / 0
except ZeroDivisionError: log.exception("step failed")       # logs the traceback too
print(stream.getvalue().splitlines()[:3])
```

Levels from low to high: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

## Project: load a messy file safely

```python run
messy = """order_id,amount,city
1,1200,Pune
2,abc,Delhi
3,,Kochi
4,950,
5,-40,Goa
"""
(folder / "messy.csv").write_text(messy, encoding="utf-8")

def load_orders(path):
    good, bad = [], []
    with open(path, newline="", encoding="utf-8") as f:
        for lineno, row in enumerate(csv.DictReader(f), start=2):
            try:
                amount = float(row["amount"])
                if amount < 0: raise ValueError("negative amount")
                if not row["city"]: raise ValueError("blank city")
                good.append({"order_id": int(row["order_id"]), "amount": amount, "city": row["city"]})
            except ValueError as e:
                bad.append((lineno, str(e)))
    return good, bad

good, bad = load_orders(folder / "messy.csv")
print("good:", good); print("rejected:", bad)
with open(folder / "rejected.json", "w", encoding="utf-8") as f: json.dump(bad, f)
import shutil; shutil.rmtree(folder)                       # tidy up the demo folder
```

Real pipelines do exactly this: keep the good rows, quarantine and report the bad ones, never crash on one bad line.

## Summary

:::key
- Use `pathlib.Path` and `with open(path, mode, encoding="utf-8")`; iterate a file line by line for big files.
- `csv.DictReader`/`DictWriter` handle quoting (values are strings); `json.load`/`dump` convert JSON ↔ Python.
- `try` / `except SpecificError` / `else` / `finally`; never use a bare `except: pass`.
- `raise` your own exceptions (subclass `Exception`) to signal bad data clearly.
- Use `logging` with levels for unattended programs.
:::

:::quiz
Q: Why use `with open(...) as f:`?
- It is faster
* The file is closed automatically, even if an error occurs
- It reads the whole file
- It is required for CSV
> The context manager handles clean-up.

Q: What does mode `"w"` do to an existing file?
- Appends
* Overwrites it
- Raises an error
- Reads it
> Use `"a"` to append and `"x"` to refuse overwriting.

Q: When does the `else` block of a `try` statement run?
- Always
* Only if no exception was raised in `try`
- Only after an exception
- Never
> `finally` is the block that always runs.

Q: What does `json.loads` take?
- A file
* A string
- A dictionary
- A path
> `load` takes a file object; `loads` takes a string.

Q: What exception does `int("abc")` raise?
- TypeError
* ValueError
- KeyError
- SyntaxError
> The type (str) is acceptable, the value is not.

Q: Why prefer `logging` over `print` for scheduled jobs?
- It is shorter
* It adds levels and timestamps and can write to files and monitoring tools
- print is deprecated
- logging is faster
> You can filter by level and keep a history.
:::

:::exercise File and error problems
(1) Write a function that counts lines, words and characters in a text file. (2) Read `superstore_sales.csv` with `csv.DictReader` and count rows per `category`. (3) Save that result as JSON and load it back. (4) Write `to_int(text, default=0)` that returns the default on `ValueError`. (5) Raise a custom `EmptyFileError` when a file has no data rows.
???
```python
def wc(path):
    text = Path(path).read_text(encoding="utf-8")
    return len(text.splitlines()), len(text.split()), len(text)
from collections import Counter
with open("superstore_sales.csv", newline="", encoding="utf-8") as f:
    counts = Counter(r["category"] for r in csv.DictReader(f))
Path("cat.json").write_text(json.dumps(counts), encoding="utf-8")
print(json.loads(Path("cat.json").read_text(encoding="utf-8")))
def to_int(text, default=0):
    try: return int(text)
    except ValueError: return default
class EmptyFileError(Exception): pass
def check(path):
    with open(path, encoding="utf-8") as f:
        if len(f.read().splitlines()) < 2: raise EmptyFileError(path)
```
:::

:::interview Questions you may be asked
**Q: How do you read a 10 GB file in Python?**
Iterate it line by line (`for line in f`), or read in chunks (`pd.read_csv(..., chunksize=...)`), so memory stays constant.

**Q: Difference between `except Exception` and a bare `except`?**
A bare `except` also catches `KeyboardInterrupt` and `SystemExit`; catch specific exceptions where possible.

**Q: What is `finally` used for?**
Clean-up that must always happen, such as closing connections or releasing locks.

**Q: How do you handle bad rows in an ETL job?**
Validate each row, keep good rows, write rejects with the reason to a quarantine file or table, log counts, and alert if the reject rate is too high.
:::
