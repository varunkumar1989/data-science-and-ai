---
num: 2
title: "Variables, Data Types, Type Conversion, print(), f-strings & input()"
live: "Python class 2"
updated: "Python 3.13"
level: Beginner
duration: 110 min
summary: Store and name values with variables, meet Python's core data types (int, float, str, bool, None, complex), convert between types, format output with print(), f-strings and .format(), and read user input with input() and sys.argv.
datasets: []
outcomes:
  - Create variables and follow Python naming rules and conventions
  - Identify and check types with type() and isinstance(); explain mutable vs immutable
  - Convert between int, float, str and bool, and predict what int(), float(), bool() and str() do
  - Format output with print() options, f-strings (including number formats) and str.format()
  - Read and validate input with input(), and avoid float rounding surprises
---

## Variables

A **variable** is a name that refers to a value stored in memory. You create it by assigning with `=`: no declaration, no type needed.

```python run
price = 1250          # an int
tax_rate = 0.18       # a float
product = "Laptop"    # a str
in_stock = True       # a bool
total = price * (1 + tax_rate)
print(product, "costs", total)
```

```python fig: A variable is a label attached to an object. Re-assigning moves the label; it does not change the old object.
dg.flow(["price  ──►  1250 (int object)", "price = 1500", "price  ──►  1500 (new int object)", "1250 is garbage-collected if nothing else refers to it"], colors=[dg.VIO, dg.CORAL, dg.TEAL, dg.GOLD], title="Names point to objects")
```

### Naming rules and conventions

| Rule | Example |
|---|---|
| Letters, digits and `_` only; cannot start with a digit | `sales_2025` ✓, `2025_sales` ✗ |
| Case-sensitive | `Total` and `total` are different |
| Cannot be a keyword (`if`, `for`, `class`, `None`, `True`…) | `class` ✗, `class_name` ✓ |
| **Convention**: `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_CASE` for constants | `monthly_income`, `CustomerOrder`, `GST_RATE` |
| Use meaningful names | `avg_order_value` not `aov2` or `x` |
| Avoid shadowing built-ins | Do not name variables `list`, `sum`, `max`, `str`, `id`, `input` |

```python run
a = b = c = 0                 # chained assignment
x, y, z = 1, 2.5, "three"     # multiple assignment (tuple unpacking)
x, y = y, x                   # swap without a temp variable
print(a, b, c, x, y, z)
```

## Data types

Everything in Python is an **object** with a **type**. Check it with `type()`.

| Type | Name | Example | Notes |
|---|---|---|---|
| `int` | Integer | `42`, `-7`, `1_000_000` | Unlimited size |
| `float` | Decimal number | `3.14`, `2e-3` | 64-bit binary floating point |
| `str` | Text | `"Pune"`, `'Pune'` | Immutable sequence of characters |
| `bool` | Boolean | `True`, `False` | Subclass of int (`True == 1`) |
| `NoneType` | "nothing" | `None` | Used for missing/absent values |
| `complex` | Complex number | `3 + 4j` | Rare in data work |
| `list`, `tuple`, `dict`, `set` | Collections | Lessons 8–10 | |

```python run
values = [42, 3.14, "Pune", True, None, 3 + 4j, [1, 2], (1, 2), {"a": 1}, {1, 2}]
for v in values:
    print(f"{str(v):10s} -> {type(v).__name__}")
```

```python run
print(isinstance(42, int), isinstance(True, int), isinstance(3.0, (int, float)))   # True True True
print(type(10 / 2), type(10 // 2))      # / always returns float; // with ints returns int
```

### Mutable vs immutable

- **Immutable**: cannot be changed after creation: `int`, `float`, `str`, `bool`, `tuple`, `frozenset`. "Changing" creates a new object.
- **Mutable**: can be changed in place: `list`, `dict`, `set`.

```python run
s = "data"
try:
    s[0] = "D"                     # strings are immutable
except TypeError as e:
    print("Error:", e)
s2 = "D" + s[1:]                    # build a new string instead
print(s2, "| id changed:", id(s) != id(s2))
```

### Numbers: int and float

```python run
big = 12_345_678_901_234_567_890 * 10      # ints never overflow
print(big)
print(0.1 + 0.2)                            # floats are approximate!
print(0.1 + 0.2 == 0.3, abs((0.1 + 0.2) - 0.3) < 1e-9)
print(round(2.675, 2), round(0.5), round(1.5), round(2.5))   # banker's rounding: halves go to even
```

:::warn Floating-point surprises
Computers store decimals in binary, so `0.1 + 0.2` is `0.30000000000000004`. For **money** use `decimal.Decimal` (or integers of paise); for comparisons use `math.isclose(a, b)` or `abs(a - b) < tolerance`. Python's `round()` rounds halves to the nearest even number (`round(2.5) = 2`), unlike Excel's `ROUND`.
:::

```python run
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))                    # exact decimal arithmetic
import math; print(math.isclose(0.1 + 0.2, 0.3))
```

### Booleans and None

```python run
print(True + True, 5 > 3, 5 == 5.0, "a" < "b", not False)
print(bool(0), bool(0.0), bool(""), bool([]), bool(None))      # all False: "falsy" values
print(bool(1), bool(-3), bool("0"), bool([0]))                  # all True: anything else is "truthy"
print(None is None, type(None))
```

**Falsy** values: `0`, `0.0`, `""`, `[]`, `{}`, `()`, `set()`, `None`, `False`. Everything else is truthy. `None` represents "no value" (like SQL NULL); test with `is None`, never `== None`.

## Type conversion

Convert with the type's name: `int()`, `float()`, `str()`, `bool()`, `list()`…

```python run
print(int("42"), int(3.99), int(-3.99), int(True))          # int() truncates towards zero
print(float("3.5"), float(7), float("1e3"))
print(str(123), str(3.0), str([1, 2]))
print(int("1010", 2), int("ff", 16), bin(10), hex(255))     # other bases
print(round(3.7), round(3.14159, 2), int(round(3.7)))
```

```python run error
print("5" + 3)                      # TypeError: can only concatenate str to str
```

```python run
print("5" + str(3), int("5") + 3, "5" * 3)      # explicit conversion; repetition for strings
```

```python run error
int("abc")                          # ValueError: invalid literal for int()
```

| Conversion | Result | Note |
|---|---|---|
| `int("42")` | 42 | String must look like an integer |
| `int("3.7")` | ValueError | Convert to float first: `int(float("3.7"))` |
| `int(3.99)` | 3 | Truncates (not rounds) |
| `float("abc")` | ValueError | |
| `str(None)` | `'None'` | |
| `bool("False")` | True | Any non-empty string is True! |
| `list("abc")` | `['a','b','c']` | |

**Implicit conversion** happens in mixed arithmetic: `int + float → float`, `bool + int → int`.

```python run
print(1 + 2.0, True + 1, type(1 + 2.0).__name__)
```

## print(): showing output

```python run
print("Order", 1001, "shipped")                    # items separated by a space
print("Order", 1001, "shipped", sep=" | ")          # change the separator
print("Loading", end="...")                          # change the line ending (no newline)
print("done")
print("Line one\nLine two\tTabbed")                  # escape sequences: \n newline, \t tab
print('He said "hi"', "It's fine", 'It\'s fine')     # quotes inside strings
print(r"C:\new\table")                                # raw string: backslashes kept
print("""A multi-line
string with triple quotes""")
```

### f-strings: the modern way to format

Put `f` before the quotes and `{expression:format}` inside:

```python run
name, qty, price, share = "Asha", 3, 1234.5678, 0.2345
print(f"{name} bought {qty} items")
print(f"Price: {price:.2f}")                 # 2 decimals
print(f"Price: {price:,.2f}")                # thousands separator
print(f"Share: {share:.1%}")                 # percentage
print(f"ID: {qty:03d}")                       # zero-padded to 3 digits
print(f"[{name:<10}] [{name:>10}] [{name:^10}]")        # left, right, centre in width 10
print(f"{price:>12,.1f}|")                    # right-aligned width 12
print(f"{qty * price:,.2f}  {qty = }")        # expressions work; {x = } prints name and value
print(f"{1234567:,}  {255:#x}  {255:b}  {0.000123:.2e}")
```

| Format spec | Meaning |
|---|---|
| `.2f` | 2 decimal places (fixed) |
| `,` | Thousands separator |
| `.1%` | Percentage with 1 decimal |
| `05d` | Integer padded with zeros to width 5 |
| `<10`, `>10`, `^10` | Left / right / centre in width 10 |
| `e` | Scientific notation |
| `x`, `b`, `o` | Hex, binary, octal |

### .format() and % (older styles)

```python run
print("{} bought {} items at {:.1f}".format("Asha", 3, 12.345))
print("{1} before {0}".format("B", "A"))
print("{name} paid {amt:,.0f}".format(name="Ravi", amt=1234567))
print("%s bought %d items at %.1f" % ("Asha", 3, 12.345))        # legacy, still seen in old code
```

Prefer **f-strings** in new code; you will meet `.format()` and `%` in older code and logs.

## Reading input

`input()` reads **text** from the keyboard and always returns a `str`:

```python
name = input("Your name: ")                    # waits for the user
age = int(input("Your age: "))                 # convert to a number
height = float(input("Height in metres: "))
print(f"Hello {name}, you are {age} and {height:.2f} m tall.")
```

Because this handbook runs without a keyboard, here is the same logic with the typed values supplied in code:

```python run
typed = ["Asha", "29", "1.62"]           # imagine the user typed these three answers
name = typed[0]; age = int(typed[1]); height = float(typed[2])
print(f"Hello {name}, you are {age} and {height:.2f} m tall.  In ten years: {age + 10}.")
```

### Validate input

```python
while True:
    text = input("Enter quantity (1-100): ")
    if text.isdigit() and 1 <= int(text) <= 100:
        quantity = int(text); break
    print("Please type a whole number between 1 and 100.")
```

Other ways to get values into a program: **command-line arguments** (`sys.argv`, `argparse`), **files** (Lesson 13), **databases and APIs** (later lessons), and **environment variables** (`os.environ["API_KEY"]`) for secrets.

## Useful built-in functions

```python run
nums = [4, 8, 15, 16, 23, 42]
print(len(nums), sum(nums), min(nums), max(nums), sorted(nums, reverse=True))
print(abs(-7), pow(2, 5), divmod(17, 5), round(sum(nums) / len(nums), 2))
print(type(nums).__name__, id(nums) > 0, dir(3)[:3])          # introspection helpers
help(len) if False else None                                   # help(len) prints documentation
```

## Mini project: a bill calculator

```python run
items = {"Notebook": (45.0, 10), "Pen pack": (60.0, 25), "Stapler": (180.0, 4)}     # name: (price, quantity)
GST = 0.18
subtotal = 0
print(f"{'Item':<12}{'Price':>8}{'Qty':>5}{'Amount':>10}")
for name, (price, qty) in items.items():
    amount = price * qty; subtotal += amount
    print(f"{name:<12}{price:>8.2f}{qty:>5}{amount:>10,.2f}")
print("-" * 35)
print(f"{'Subtotal':<25}{subtotal:>10,.2f}")
print(f"{'GST (18%)':<25}{subtotal * GST:>10,.2f}")
print(f"{'Total':<25}{subtotal * (1 + GST):>10,.2f}")
```

(The `for` loop and dictionary are explained in Lessons 6 and 9; notice how f-string alignment makes a tidy table.)

## Summary

:::key
- A **variable** is a name pointing to an object; names are `snake_case`, case-sensitive, and must not be keywords or shadow built-ins.
- Core types: `int`, `float`, `str`, `bool`, `NoneType`; `list/tuple/dict/set` come later. Check with `type()` and `isinstance()`.
- Strings, numbers and tuples are **immutable**; lists, dicts and sets are **mutable**.
- Floats are approximate (`0.1 + 0.2`): use `Decimal` for money and `math.isclose` for comparisons. `round()` uses banker's rounding.
- Convert with `int()`, `float()`, `str()`, `bool()`; `int("3.7")` fails, `int(3.99)` truncates, `bool("False")` is True.
- Format with **f-strings** (`{x:,.2f}`, `{p:.1%}`, `{n:05d}`, `{s:<10}`); `print` has `sep` and `end`.
- `input()` returns a string: convert and validate it.
:::

:::quiz
Q: What does `type(10 / 2)` return?
- `int`
* `float`
- `str`
- `bool`
> `/` always returns a float in Python 3 (5.0).

Q: What is `int(-3.9)`?
- −4
* −3
- 3
- −3.9
> int() truncates towards zero.

Q: Which is NOT falsy?
- `0`
- `""`
* `"0"`
- `None`
> A non-empty string, including "0", is truthy.

Q: What does `print(f"{0.2345:.1%}")` print?
- 0.2
* 23.4%
- 2.3%
- 0.23
> `.1%` multiplies by 100 and shows one decimal. 0.2345 displays as 23.4% because 0.2345 is stored as a binary value just below 0.2345.

Q: `x = input("Age: ")` and the user types 25. What is `type(x)`?
- `int`
* `str`
- `float`
- `bool`
> input() always returns text.

Q: Why is `0.1 + 0.2 == 0.3` False?
- Python is buggy
* Decimal fractions cannot be represented exactly in binary floating point
- Because of integer division
- Because of rounding to even
> Use math.isclose or Decimal.
:::

:::exercise Practice
(1) Ask for a price and quantity (simulate the input), compute the total with 18% GST and print it as `₹1,23,456.78`-style with thousands separators and 2 decimals. (2) Convert "1010" from binary to int and 255 to hex. (3) Explain the output of `print(round(2.5), round(3.5))`.
???
```python
price, qty = float("1250.5"), int("3")
total = price * qty * 1.18
print(f"Total: ₹{total:,.2f}")          # ₹4,426.77
print(int("1010", 2), hex(255))          # 10 0xff
print(round(2.5), round(3.5))            # 2 4 : halves round to the nearest even number
```
:::

:::interview Questions you may be asked
**Q: What is the difference between mutable and immutable types? Give examples.**
Immutable objects cannot change after creation (int, float, str, tuple); mutable ones can (list, dict, set). It matters for function arguments, dictionary keys (must be immutable/hashable) and copying.

**Q: What is the output of `bool("False")` and why?**
True: any non-empty string is truthy, regardless of its content.

**Q: How do you compare floats safely?**
`math.isclose(a, b)` or `abs(a - b) < tol`; use `Decimal` for exact decimal arithmetic such as money.

**Q: `is` vs `==`?**
`==` compares values; `is` compares identity (same object). Use `is None` for None.
:::
