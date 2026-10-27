---
num: 19
title: "pandas IV: Dates, Time Series, Resampling and Rolling Windows"
live: "Python class 15"
updated: "pandas 2.3 / 3.0"
level: Intermediate
duration: 110 min
summary: Work with time. Parse dates, extract parts with .dt, do date arithmetic, set a DatetimeIndex, resample to weeks, months and quarters, compute rolling and expanding windows, shifts and growth rates, and build a cohort-style monthly report with the daily sales data.
datasets: [daily_sales.csv, superstore_sales.csv]
outcomes:
  - Parse and format dates and extract year, month, weekday and quarter
  - Do date arithmetic with Timedelta and DateOffset, including business days
  - Resample time series and use rolling, expanding and exponentially weighted windows
  - Compute period-over-period change, year-over-year growth and cumulative totals with shift, pct_change and cumsum
  - Handle time zones and missing dates
---

## Parsing dates

```python run
import pandas as pd, numpy as np
pd.set_option("display.max_columns", 20); pd.set_option("display.width", 160)
d = pd.to_datetime(pd.Series(["2025-01-15", "2025-03-01", "2025-12-31"]))
print(d.dt.year.tolist(), d.dt.month_name().tolist(), d.dt.day_name().tolist(), d.dt.quarter.tolist(), d.dt.isocalendar().week.tolist())
print(pd.to_datetime("05/01/2025", dayfirst=True).date(), pd.to_datetime("05/01/2025").date())     # 5 Jan vs 1 May!
print(pd.to_datetime("2025-01-15 14:30").strftime("%d %b %Y, %I:%M %p"), pd.Timestamp("2025-02-28").is_month_end)
```

:::warning Day-first dates
Indian and European data often write 05/01/2025 for 5 January. Pass `dayfirst=True` or, better, an explicit `format="%d/%m/%Y"`. Check a few parsed values every time.
:::

| `.dt` accessor | Gives |
|---|---|
| `.year`, `.month`, `.day`, `.hour` | Parts |
| `.day_name()`, `.month_name()` | Text names |
| `.dayofweek` (Mon = 0), `.quarter`, `.isocalendar().week` | Calendar positions |
| `.to_period("M")`, `.to_period("Q")` | Month / quarter periods |
| `.floor("D")`, `.normalize()` | Truncate time |
| `.is_month_end`, `.days_in_month` | Calendar flags |

## Date arithmetic

```python run
s = pd.read_csv("superstore_sales.csv", parse_dates=["order_date", "ship_date"])
s["ship_days"] = (s["ship_date"] - s["order_date"]).dt.days
print(s.groupby("ship_mode")["ship_days"].agg(["mean", "max"]).round(1))
t = pd.Timestamp("2025-01-31")
print(t + pd.Timedelta(days=30), t + pd.DateOffset(months=1), t + pd.offsets.MonthEnd(1), t + pd.offsets.BDay(3))
print(np.busday_count("2025-10-01", "2025-11-01"), "working days in October 2025 (Mon–Fri)")
print(pd.date_range("2025-01-01", periods=4, freq="W-MON").date.tolist(), pd.date_range("2025-01-01", "2025-06-30", freq="QE").date.tolist())
```

`Timedelta` adds exact durations; `DateOffset` and offsets follow the calendar (month ends, business days).

## A time series with a DatetimeIndex

```python run
daily = pd.read_csv("daily_sales.csv", parse_dates=["date"]).set_index("date").sort_index()
print(daily.shape, daily.index.min().date(), "to", daily.index.max().date())
print(daily.loc["2023-03"].head(3))                     # partial-string indexing: all of March 2023
print(daily.loc["2023-12-24":"2023-12-27"])
full = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
print("missing days:", len(full.difference(daily.index)))
```

## Resampling

`resample` is `groupby` for time: change the frequency and aggregate.

```python run
monthly = daily["units_sold"].resample("ME").sum()
print(monthly.head(4))
q = daily["units_sold"].resample("QE").agg(["sum", "mean", "max"]).round(1)
print(q.tail(4))
wk = daily["units_sold"].resample("W-SUN").sum()
print(wk.describe().round(0))
print(daily.groupby(daily.index.day_name())["units_sold"].mean().round(1).sort_values(ascending=False))
```

Frequencies: `D` day, `W` week, `ME` month end, `MS` month start, `QE` quarter, `YE` year, `h` hour, `min` minute.

## Rolling and expanding windows

```python run
ts = daily["units_sold"]
df = pd.DataFrame({"units": ts, "ma_7": ts.rolling(7).mean(), "ma_30": ts.rolling(30).mean(), "ewm_14": ts.ewm(span=14).mean(),
                   "max_so_far": ts.expanding().max(), "cum_units": ts.cumsum()})
print(df.iloc[[0, 6, 29, 400, -1]].round(1))
```

```python fig: Daily units with 7-day and 30-day moving averages: averages smooth out daily noise and reveal trend and seasonality.
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 3.4))
ax.plot(df.index, df["units"], color="#C9C3E6", lw=.6, label="daily")
ax.plot(df.index, df["ma_7"], color="#7C3AED", lw=1.1, label="7-day average")
ax.plot(df.index, df["ma_30"], color="#DB2777", lw=2, label="30-day average")
ax.set_ylabel("units sold"); ax.legend(frameon=False, ncol=3, loc="upper left"); ax.spines[["top", "right"]].set_visible(False)
```

## Shifts and growth

```python run
m = monthly.to_frame("units")
m["prev_month"] = m["units"].shift(1)
m["mom_%"] = (100 * m["units"].pct_change()).round(1)
m["yoy_%"] = (100 * m["units"].pct_change(12)).round(1)          # same month last year
m["ytd"] = m.groupby(m.index.year)["units"].cumsum()
print(m.tail(4))
yr = daily["units_sold"].resample("YE").sum()
print(yr, (100 * yr.pct_change()).round(1).tolist())
```

`shift(1)` is SQL's `LAG`; `shift(-1)` is `LEAD`; `pct_change(12)` on monthly data is year-over-year growth.

## Time zones

```python run
ts_utc = pd.Timestamp("2025-03-10 09:00", tz="UTC")
print(ts_utc.tz_convert("Asia/Kolkata"), ts_utc.tz_convert("America/New_York"))
naive = pd.Series(pd.to_datetime(["2025-03-10 09:00"]))
print(naive.dt.tz_localize("Asia/Kolkata").dt.tz_convert("UTC").tolist())
```

Store timestamps in UTC; convert to local time only for reporting.

## Mini case: monthly KPI report

```python run
s["month"] = s["order_date"].dt.to_period("M")
kpi = s.groupby("month").agg(sales=("sales", "sum"), orders=("order_id", "nunique"), customers=("customer_id", "nunique"))
kpi["aov"] = (kpi.sales / kpi.orders).round(0)
kpi["sales_3m_avg"] = kpi.sales.rolling(3).mean().round(0)
kpi["yoy_%"] = (100 * kpi.sales.pct_change(12)).round(1)
print((kpi.tail(6).assign(sales=lambda d: (d.sales / 1e6).round(2), sales_3m_avg=lambda d: (d.sales_3m_avg / 1e6).round(2))))
first = s.groupby("customer_id")["order_date"].min().dt.to_period("M").rename("first_month")
s2 = s.join(first, on="customer_id")
new_vs_repeat = s2.assign(kind=np.where(s2.month == s2.first_month, "new", "repeat")).groupby(["month", "kind"])["customer_id"].nunique().unstack().tail(3)
print(new_vs_repeat)
```

## Summary

:::key
- Parse with `pd.to_datetime` (give `format` or `dayfirst`); use `.dt` for parts and `to_period` for months/quarters.
- `Timedelta` = exact duration; `DateOffset`/`MonthEnd`/`BDay` = calendar-aware moves; `date_range` builds calendars.
- A sorted `DatetimeIndex` allows partial-string slicing (`df.loc["2025-03"]`) and `resample`.
- Rolling, expanding and EWM windows smooth series; `shift` = lag/lead, `pct_change(n)` = growth, `cumsum` = running totals.
- Keep timestamps in UTC, check for missing dates, and convert for display.
:::

:::quiz
Q: What does `daily.resample("ME").sum()` produce?
- Daily totals
* Monthly totals (labelled at month end)
- A 7-day average
- An error
> ME = month end frequency.

Q: Which gives year-over-year growth on monthly data?
- `pct_change(1)`
* `pct_change(12)`
- `shift(-12)`
- `rolling(12).mean()`
> Compare each month with the same month a year earlier.

Q: `shift(1)` is equivalent to which SQL function?
* LAG
- LEAD
- ROW_NUMBER
- NTILE
> `shift(-1)` is LEAD.

Q: How do you parse "05/01/2025" as 5 January?
- `pd.to_datetime(x)`
* `pd.to_datetime(x, dayfirst=True)` or `format="%d/%m/%Y"`
- `.dt.day`
- `astype(str)`
> The default assumes month first.

Q: What does `ts.rolling(7).mean()` give for the first 6 rows?
- 0
* NaN (not enough values yet)
- The value itself
- An error
> Use `min_periods=1` to allow partial windows.

Q: What is the difference between `Timedelta(days=30)` and `DateOffset(months=1)` from 31 Jan?
* Timedelta adds exactly 30 days (2 Mar); DateOffset moves to the same day next month, clipped to 28 Feb
- They are identical
- Timedelta is calendar-aware
- DateOffset adds 30 days
> Use calendar offsets for month logic.
:::

:::exercise Time-series practice (daily_sales.csv)
(1) Which month had the highest total units? (2) Compute the 28-day rolling sum and its maximum. (3) Average units by weekday and month (a heatmap-ready pivot). (4) Year-over-year growth by quarter. (5) Flag days where units exceed the 30-day average by 50%.
???
```python
print(monthly.idxmax(), monthly.max())
print(ts.rolling(28).sum().max())
pv = daily.assign(wd=daily.index.day_name(), m=daily.index.month).pivot_table(index="wd", columns="m", values="units_sold", aggfunc="mean").round(0)
qq = ts.resample("QE").sum(); print((100 * qq.pct_change(4)).round(1).dropna())
spikes = daily[ts > 1.5 * ts.rolling(30).mean()]; print(len(spikes))
```
:::

:::interview Questions you may be asked
**Q: resample vs groupby?**
`resample` is a time-based groupby on a DatetimeIndex that also creates empty periods; `groupby` with `dt.to_period` is similar but only returns periods present in the data.

**Q: How do you compute a 7-day moving average in pandas and in SQL?**
`s.rolling(7).mean()`; in SQL `AVG(x) OVER (ORDER BY d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`.

**Q: How do you handle missing dates in a daily series?**
Reindex to a full `date_range`, then decide: fill with 0 (no sales), forward-fill (stock levels), or interpolate (sensor readings).
:::
