"""Generates every practice dataset used in the course. All data is fictional and seeded, so results are reproducible."""
import os, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "datasets"); os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2026)
def save(df, name): df.to_csv(os.path.join(OUT, name), index=False); print(f"{name:32s} {df.shape}")

# ---------------------------------------------------------------- 1. Superstore-style retail sales (India)
regions = {"North": [("Delhi", "Delhi"), ("Chandigarh", "Punjab"), ("Jaipur", "Rajasthan"), ("Lucknow", "Uttar Pradesh")],
           "South": [("Bengaluru", "Karnataka"), ("Chennai", "Tamil Nadu"), ("Hyderabad", "Telangana"), ("Kochi", "Kerala")],
           "East": [("Kolkata", "West Bengal"), ("Bhubaneswar", "Odisha"), ("Patna", "Bihar"), ("Guwahati", "Assam")],
           "West": [("Mumbai", "Maharashtra"), ("Pune", "Maharashtra"), ("Ahmedabad", "Gujarat"), ("Indore", "Madhya Pradesh")]}
cat = {"Furniture": {"Chairs": (2500, 9000), "Tables": (6000, 22000), "Bookcases": (4000, 15000), "Furnishings": (300, 2500)},
       "Office Supplies": {"Binders": (80, 600), "Paper": (150, 700), "Storage": (500, 4000), "Art": (60, 500), "Appliances": (1500, 9000)},
       "Technology": {"Phones": (6000, 40000), "Accessories": (400, 5000), "Machines": (9000, 60000), "Copiers": (15000, 90000)}}
brands = ["Apex", "Nova", "Orbit", "Zenith", "Lumen", "Vertex", "Pioneer", "Crest"]
products = []
pid = 1
for c, subs in cat.items():
    for s, (lo, hi) in subs.items():
        for b in rng.choice(brands, 6, replace=False):
            products.append(dict(product_id=f"P{pid:04d}", category=c, sub_category=s, product_name=f"{b} {s[:-1] if s.endswith('s') else s} {rng.integers(100, 999)}",
                                 list_price=round(float(rng.uniform(lo, hi)), -1)))
            pid += 1
P = pd.DataFrame(products)
first = ["Aarav", "Vivaan", "Aditya", "Ishaan", "Arjun", "Sai", "Reyansh", "Krishna", "Ananya", "Diya", "Saanvi", "Aadhya", "Isha", "Kavya", "Meera", "Riya",
         "Rohan", "Kabir", "Nikhil", "Pooja", "Neha", "Sneha", "Rahul", "Priya", "Vikram", "Asha", "Farhan", "Zoya", "Imran", "Simran", "Harpreet", "Joseph"]
last = ["Sharma", "Verma", "Iyer", "Reddy", "Nair", "Das", "Patel", "Shah", "Gupta", "Khan", "Singh", "Mehta", "Rao", "Bose", "Joshi", "Menon", "Kulkarni", "Fernandes"]
custs = []
for i in range(1, 801):
    reg = rng.choice(list(regions)); city, state = regions[reg][rng.integers(0, 4)]
    custs.append(dict(customer_id=f"C{i:04d}", customer_name=f"{rng.choice(first)} {rng.choice(last)}", segment=rng.choice(["Consumer", "Corporate", "Home Office"], p=[.52, .30, .18]),
                      city=city, state=state, region=reg))
C = pd.DataFrame(custs)
rows = []
dates = pd.date_range("2023-01-01", "2025-12-31")
season = np.array([0.8, 0.8, 1.0, 0.9, 0.9, 0.85, 0.9, 1.0, 1.05, 1.25, 1.35, 1.3])  # festive Q4 lift
growth = {2023: 1.0, 2024: 1.12, 2025: 1.27}
w = np.array([season[d.month - 1] * growth[d.year] for d in dates]); w /= w.sum()
n_orders = 3200
od = np.sort(rng.choice(dates, n_orders, p=w))
for k, d in enumerate(od, 1):
    cu = C.iloc[rng.integers(0, len(C))]
    mode = rng.choice(["Standard Class", "Second Class", "First Class", "Same Day"], p=[.6, .2, .15, .05])
    ship = pd.Timestamp(d) + pd.Timedelta(days=int({"Standard Class": rng.integers(4, 8), "Second Class": rng.integers(2, 5), "First Class": rng.integers(1, 3), "Same Day": 0}[mode]))
    for _ in range(rng.choice([1, 1, 1, 2, 2, 3, 4])):
        p = P.iloc[rng.integers(0, len(P))]
        q = int(rng.choice([1, 1, 2, 2, 3, 4, 5, 6, 7], p=[.2, .1, .2, .1, .15, .1, .07, .05, .03]))
        disc = float(rng.choice([0, 0, 0, 0.1, 0.15, 0.2, 0.3, 0.4], p=[.35, .15, .1, .12, .1, .1, .05, .03]))
        if p.sub_category in ("Tables", "Bookcases") and rng.random() < .4: disc = max(disc, 0.3)
        sales = round(p.list_price * q * (1 - disc), 2)
        margin = {"Furniture": .12, "Office Supplies": .22, "Technology": .18}[p.category] - disc * 1.1 + rng.normal(0, .05)
        rows.append(dict(order_id=f"IN-{pd.Timestamp(d).year}-{k:05d}", order_date=pd.Timestamp(d).date(), ship_date=ship.date(), ship_mode=mode,
                         customer_id=cu.customer_id, customer_name=cu.customer_name, segment=cu.segment, city=cu.city, state=cu.state, region=cu.region,
                         product_id=p.product_id, category=p.category, sub_category=p.sub_category, product_name=p.product_name,
                         sales=sales, quantity=q, discount=disc, profit=round(sales * margin, 2)))
S = pd.DataFrame(rows); S.insert(0, "row_id", range(1, len(S) + 1))
save(S, "superstore_sales.csv"); save(P, "products.csv"); save(C, "customers.csv")

# ---------------------------------------------------------------- 2. Video game sales (fictional titles)
genres = ["Action", "Sports", "Shooter", "Role-Playing", "Platform", "Racing", "Simulation", "Puzzle", "Adventure", "Fighting", "Strategy", "Misc"]
plats = {"PS4": (2013, 2020), "PS5": (2020, 2025), "XOne": (2013, 2020), "XSX": (2020, 2025), "Switch": (2017, 2025), "PC": (2010, 2025), "PS3": (2010, 2016), "X360": (2010, 2015), "3DS": (2011, 2018), "Mobile": (2012, 2025)}
pubs = ["Starforge Interactive", "Blue Comet Games", "Pixel Harbor", "Red Lantern Studios", "Northwind Play", "Quantum Leaf", "Iron Owl Entertainment",
        "Monsoon Games", "Silverline Software", "Tiger Bay Studios", "Cloudpeak Games", "Lotus Arcade", "Saffron Works", "Delta Nine", "Orchid Interactive"]
adj = ["Shadow", "Galactic", "Eternal", "Crimson", "Neon", "Silent", "Wild", "Lost", "Iron", "Golden", "Hidden", "Final", "Rapid", "Frozen", "Mystic"]
noun = ["Legends", "Racers", "Kingdom", "Odyssey", "Arena", "Frontier", "Quest", "Strike", "Saga", "Tactics", "League", "Escape", "Horizon", "Empire", "Rally"]
G = []
for i in range(2400):
    pl = rng.choice(list(plats)); y0, y1 = plats[pl]; yr = int(rng.integers(y0, y1 + 1)); gen = rng.choice(genres)
    base = rng.lognormal(-1.2, 1.1)
    reg = {"Sports": (.45, .35, .05), "Shooter": (.5, .32, .04), "Role-Playing": (.3, .25, .35), "Puzzle": (.3, .3, .25), "Fighting": (.38, .3, .2)}.get(gen, (.42, .32, .12))
    if pl in ("3DS", "Switch"): reg = (reg[0] * .8, reg[1] * .9, reg[2] * 2.2)
    sh = np.array(reg + (1 - sum(reg),)); sh = np.clip(sh * rng.uniform(.7, 1.3, 4), .01, None); sh /= sh.sum()
    na, eu, jp, ot = [round(float(base * s), 2) for s in sh]
    G.append(dict(rank=0, name=f"{rng.choice(adj)} {rng.choice(noun)}" + ("" if rng.random() < .6 else f" {rng.integers(2, 6)}"), platform=pl, year=yr, genre=gen,
                  publisher=rng.choice(pubs, p=np.r_[np.full(5, .12), np.full(10, .04)]), na_sales=na, eu_sales=eu, jp_sales=jp, other_sales=ot))
G = pd.DataFrame(G); G["global_sales"] = G[["na_sales", "eu_sales", "jp_sales", "other_sales"]].sum(axis=1).round(2)
G = G.sort_values("global_sales", ascending=False).reset_index(drop=True); G["rank"] = range(1, len(G) + 1)
save(G, "video_game_sales.csv")

# ---------------------------------------------------------------- 3. HR employees
depts = {"Sales": ["Sales Executive", "Sales Manager", "Sales Representative"], "R&D": ["Research Scientist", "Lab Technician", "Research Director", "Data Scientist"],
         "HR": ["HR Executive", "HR Manager"], "Finance": ["Analyst", "Accountant", "Finance Manager"], "IT": ["Developer", "Tester", "Tech Lead", "Support Engineer"],
         "Operations": ["Operations Executive", "Operations Manager"]}
H = []
for i in range(1, 1501):
    d = rng.choice(list(depts), p=[.28, .26, .06, .1, .2, .1]); jt = rng.choice(depts[d]); age = int(np.clip(rng.normal(35, 8), 21, 60))
    yrs = int(np.clip(rng.exponential(5), 0, age - 20)); edu = rng.choice(["Bachelor's", "Master's", "Diploma", "PhD"], p=[.5, .33, .12, .05])
    lvl = 1 + ("Manager" in jt or "Lead" in jt or "Director" in jt) * 2 + (yrs > 8)
    sal = int(round((300000 + lvl * 250000 + yrs * 45000 + (edu == "Master's") * 120000 + (edu == "PhD") * 300000) * rng.uniform(.85, 1.2), -3))
    sat = int(rng.integers(1, 5)); ot = rng.random() < .28; dist = int(rng.integers(1, 30)); perf = int(rng.choice([1, 2, 3, 4, 5], p=[.05, .15, .45, .25, .1]))
    z = -1.6 + 0.9 * ot - 0.45 * (sat - 2.5) - 0.07 * yrs - 0.03 * (age - 35) + 0.03 * dist - sal / 4e6 + (d == "Sales") * .4
    H.append(dict(emp_id=f"E{i:05d}", gender=rng.choice(["Male", "Female"], p=[.58, .42]), age=age, department=d, job_title=jt, education=edu,
                  hire_date=(pd.Timestamp("2026-03-31") - pd.Timedelta(days=int(yrs * 365 + rng.integers(0, 365)))).date(), years_at_company=yrs,
                  monthly_income=round(sal / 12), job_satisfaction=sat, overtime="Yes" if ot else "No", distance_from_home_km=dist, performance_rating=perf,
                  city=rng.choice(["Bengaluru", "Pune", "Hyderabad", "Gurugram", "Chennai", "Mumbai"]), attrition="Yes" if rng.random() < 1 / (1 + np.exp(-z)) else "No"))
save(pd.DataFrame(H), "hr_employees.csv")

# ---------------------------------------------------------------- 4. Bank loans (default prediction)
n = 850
age = rng.integers(20, 56, n); ed = rng.choice([1, 2, 3, 4, 5], n, p=[.45, .3, .15, .08, .02]); employ = np.clip((age - 18) * rng.uniform(0, .7, n), 0, 33).astype(int)
address = np.clip((age - 18) * rng.uniform(0, .6, n), 0, 34).astype(int); income = np.round(np.clip(rng.lognormal(3.4 + .03 * employ + .1 * ed, .45, n), 12, 450), 1)
debtinc = np.round(np.clip(rng.gamma(2.2, 4.5, n), .1, 41), 1); creddebt = np.round(income * debtinc / 100 * rng.uniform(.15, .55, n), 2); othdebt = np.round(income * debtinc / 100 - creddebt, 2)
z = -1.1 + .12 * debtinc - .17 * employ - .07 * address + .45 * creddebt / 3 + .05 * (ed - 1) - .01 * (age - 35)
default = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
B = pd.DataFrame(dict(customer_id=[f"L{i:04d}" for i in range(1, n + 1)], age=age, ed=ed, employ=employ, address=address, income=income, debtinc=debtinc, creddebt=creddebt, othdebt=othdebt, default=default))
B.loc[700:, "default"] = np.nan  # last 150 are new applicants (no outcome yet)
save(B, "bank_loans.csv")

# ---------------------------------------------------------------- 5. House prices
n = 1200
city = rng.choice(["Bengaluru", "Pune", "Hyderabad", "Chennai"], n); area = np.round(rng.normal(1250, 420, n).clip(380, 3800), -1)
bed = np.clip(np.round(area / 520 + rng.normal(0, .6, n)), 1, 5).astype(int); bath = np.clip(bed - rng.integers(0, 2, n), 1, 5)
agey = rng.integers(0, 30, n); dist = np.round(rng.gamma(2.5, 4, n).clip(1, 45), 1); park = rng.choice([0, 1], n, p=[.3, .7])
cmult = pd.Series(city).map({"Bengaluru": 1.25, "Pune": 1.0, "Hyderabad": 1.05, "Chennai": .95}).values
price = (area * 6.5 * cmult - agey * 1.4 * 100 / 100 * 30 - dist * 2.1 * 10 + bed * 4 * 10 + park * 6 * 10) / 100 + rng.normal(0, 7, n)
H2 = pd.DataFrame(dict(house_id=range(1, n + 1), city=city, area_sqft=area, bedrooms=bed, bathrooms=bath, age_years=agey, distance_to_center_km=dist, parking=park, price_lakh=np.round(price.clip(15), 1)))
H2.loc[rng.choice(n, 25, replace=False), "area_sqft"] = np.nan; H2.loc[rng.choice(n, 4, replace=False), "price_lakh"] = [410.0, 395.5, 2.0, 520.0]
save(H2, "house_prices.csv")

# ---------------------------------------------------------------- 6. Online retail transactions (RFM)
T = []
inv = 100000
for c in range(1, 501):
    kind = rng.choice(["loyal", "regular", "occasional", "lapsed"], p=[.15, .35, .35, .15])
    nb = {"loyal": rng.integers(12, 40), "regular": rng.integers(5, 14), "occasional": rng.integers(1, 5), "lapsed": rng.integers(2, 8)}[kind]
    end = pd.Timestamp("2025-12-31") - pd.Timedelta(days=int({"lapsed": rng.integers(200, 600)}.get(kind, rng.integers(0, 120))))
    for d in pd.to_datetime(rng.integers(pd.Timestamp("2024-01-01").value // 10**9, end.value // 10**9, nb), unit="s"):
        inv += 1; T.append(dict(invoice_no=inv, customer_id=f"R{c:04d}", invoice_date=d.date(), amount=round(float(rng.lognormal(7.2 if kind == 'loyal' else 6.6, .6)), 2)))
save(pd.DataFrame(T).sort_values("invoice_date"), "retail_transactions.csv")

# ---------------------------------------------------------------- 7. Telecom churn
n = 3000
ten = rng.integers(0, 73, n); contract = rng.choice(["Month-to-month", "One year", "Two year"], n, p=[.55, .25, .2]); internet = rng.choice(["Fiber", "DSL", "No internet"], n, p=[.45, .35, .2])
mc = np.round(20 + (internet == "Fiber") * 55 + (internet == "DSL") * 30 + rng.normal(10, 12, n).clip(0), 2); calls = rng.poisson(1.3, n); pay = rng.choice(["UPI", "Card", "Net banking", "Auto-debit"], n)
senior = (rng.random(n) < .16).astype(int)
z = -1.2 - .045 * ten + 1.3 * (contract == "Month-to-month") - .8 * (contract == "Two year") + .5 * (internet == "Fiber") + .35 * calls + .012 * (mc - 60) + .3 * senior - .4 * (pay == "Auto-debit")
TC = pd.DataFrame(dict(customer_id=[f"T{i:05d}" for i in range(1, n + 1)], senior_citizen=senior, tenure_months=ten, contract=contract, internet_service=internet, payment_method=pay,
                       monthly_charges=mc, total_charges=np.round(mc * np.maximum(ten, 1) * rng.uniform(.95, 1.05, n), 2), support_calls=calls, churn=np.where(rng.random(n) < 1 / (1 + np.exp(-z)), "Yes", "No")))
save(TC, "telecom_churn.csv")

# ---------------------------------------------------------------- 8. Daily sales time series
d = pd.date_range("2022-01-01", "2025-12-31"); t = np.arange(len(d))
units = 200 + .12 * t + 25 * np.sin(2 * np.pi * d.dayofyear / 365.25 - 1.2) + np.where(d.dayofweek >= 5, 35, 0) + rng.normal(0, 14, len(d))
save(pd.DataFrame(dict(date=d.date, units_sold=np.round(units).astype(int))), "daily_sales.csv")

# ---------------------------------------------------------------- 9. Hypothesis-testing datasets
ab = pd.DataFrame(dict(user_id=range(1, 4001), group=np.repeat(["A_control", "B_new_checkout"], 2000)))
ab["converted"] = np.r_[(rng.random(2000) < .112), (rng.random(2000) < .134)].astype(int)
ab["order_value"] = np.where(ab.converted == 1, np.round(rng.normal(np.where(ab.group == "A_control", 1450, 1490), 380), 0), 0)
save(ab, "ab_test.csv")
dl = pd.DataFrame(dict(city=np.repeat(["Pune", "Hyderabad"], [60, 55]), delivery_minutes=np.r_[rng.normal(31.5, 6, 60), rng.normal(34.2, 7, 55)].round(1)))
save(dl, "delivery_times.csv")
sv = pd.DataFrame(dict(age_group=rng.choice(["18-25", "26-40", "41+"], 600, p=[.35, .4, .25])))
pref = {"18-25": [.5, .3, .2], "26-40": [.38, .37, .25], "41+": [.22, .38, .4]}
sv["preferred_channel"] = [rng.choice(["App", "Website", "Store"], p=pref[a]) for a in sv.age_group]
save(sv, "channel_survey.csv")
dt = pd.DataFrame(dict(diet=np.repeat(["Keto", "Mediterranean", "Low-fat"], 40), weight_loss_kg=np.r_[rng.normal(4.8, 1.6, 40), rng.normal(4.1, 1.5, 40), rng.normal(3.2, 1.7, 40)].round(2)))
save(dt, "diet_study.csv")

# ---------------------------------------------------------------- 10. Product reviews (NLP)
pos = ["Battery life is excellent and it charges fast", "Great value for money, totally worth it", "Delivery was quick and packaging was neat", "Camera quality is amazing in daylight",
       "Very comfortable to use all day", "Customer support solved my issue in minutes", "Sound is clear and the bass is rich", "Build quality feels premium", "Setup was simple and quick", "Love the display, colours are vivid"]
neg = ["Stopped working after two weeks", "Battery drains too fast", "Delivery was late and the box was damaged", "Poor build quality, feels cheap", "Customer care never replied",
       "Heats up a lot while charging", "The app keeps crashing", "Not worth the price at all", "Screen has dead pixels", "Refund process is very slow"]
neu = ["Product is okay, nothing special", "Average performance for daily use", "It works as described", "Delivered on the expected date", "Decent but could be better"]
R = []
for i in range(1, 1201):
    s = rng.choice(["positive", "negative", "neutral"], p=[.5, .35, .15]); src = {"positive": pos, "negative": neg, "neutral": neu}[s]
    txt = rng.choice(src) + ("" if rng.random() < .6 else (". " + rng.choice(src).lower()))
    R.append(dict(review_id=i, product=rng.choice(["Earbuds", "Smartphone", "Smartwatch", "Laptop", "Speaker"]), rating={"positive": rng.choice([4, 5]), "negative": rng.choice([1, 2]), "neutral": 3}[s], review_text=txt, sentiment=s))
save(pd.DataFrame(R), "product_reviews.csv")

# ---------------------------------------------------------------- 11. Adventure Cycles star schema (Power BI)
terr = pd.DataFrame(dict(territory_key=range(1, 7), territory=["North India", "South India", "East India", "West India", "UAE", "Singapore"], country=["India", "India", "India", "India", "UAE", "Singapore"]))
prods = []
for k, (c, sc, lo, hi) in enumerate([("Bikes", "Road Bikes", 45000, 180000), ("Bikes", "Mountain Bikes", 35000, 150000), ("Bikes", "Touring Bikes", 40000, 120000), ("Components", "Frames", 8000, 40000),
                                     ("Components", "Wheels", 3000, 18000), ("Accessories", "Helmets", 1500, 6000), ("Accessories", "Bottles", 200, 900), ("Clothing", "Jerseys", 900, 3500), ("Clothing", "Gloves", 400, 1800)]):
    for j in range(5):
        lp = round(float(rng.uniform(lo, hi)), -2); prods.append(dict(product_key=len(prods) + 1, product=f"{sc[:-1]} {chr(65 + j)}-{rng.integers(100, 999)}", subcategory=sc, category=c, list_price=lp, standard_cost=round(lp * rng.uniform(.55, .7), -1)))
prods = pd.DataFrame(prods)
cust = pd.DataFrame(dict(customer_key=range(1, 1201), customer_name=[f"{rng.choice(first)} {rng.choice(last)}" for _ in range(1200)], gender=rng.choice(["M", "F"], 1200),
                         age_band=rng.choice(["18-25", "26-35", "36-50", "51+"], 1200, p=[.2, .4, .3, .1]), territory_key=rng.integers(1, 7, 1200)))
fs = []
for i in range(9000):
    dte = pd.Timestamp("2023-01-01") + pd.Timedelta(days=int(rng.integers(0, 1095)) )
    pr = prods.iloc[int(rng.integers(0, len(prods)))]; cu = cust.iloc[int(rng.integers(0, len(cust)))]
    q = int(rng.choice([1, 1, 1, 2, 3])) if pr.category == "Bikes" else int(rng.integers(1, 6))
    fs.append(dict(order_number=f"SO{50000 + i}", order_date=dte.date(), product_key=pr.product_key, customer_key=cu.customer_key, territory_key=cu.territory_key, quantity=q,
                   unit_price=pr.list_price, sales_amount=round(q * pr.list_price * rng.choice([1, 1, .95, .9]), 2), total_cost=q * pr.standard_cost))
fs = pd.DataFrame(fs).sort_values("order_date")
dd = pd.DataFrame(dict(date=pd.date_range("2023-01-01", "2025-12-31"))); dd["year"] = dd.date.dt.year; dd["quarter"] = "Q" + dd.date.dt.quarter.astype(str); dd["month_no"] = dd.date.dt.month; dd["month"] = dd.date.dt.strftime("%b"); dd["weekday"] = dd.date.dt.strftime("%a"); dd["date"] = dd.date.dt.date
D = os.path.join(OUT, "adventure_cycles"); os.makedirs(D, exist_ok=True)
for nm, df in [("fact_sales", fs), ("dim_product", prods), ("dim_customer", cust), ("dim_territory", terr), ("dim_date", dd)]: df.to_csv(os.path.join(D, nm + ".csv"), index=False); print(f"adventure_cycles/{nm}.csv", df.shape)

# ---------------------------------------------------------------- 12. Small Excel practice table
emp = pd.DataFrame(dict(emp_id=[f"E{i:03d}" for i in range(101, 121)], name=[f"{a} {b}" for a, b in zip(rng.choice(first, 20, replace=False), rng.choice(last, 20))],
                        department=rng.choice(["Sales", "Finance", "IT", "HR", "Operations"], 20), city=rng.choice(["Delhi", "Mumbai", "Pune", "Bengaluru", "Chennai"], 20),
                        join_date=pd.to_datetime(rng.integers(pd.Timestamp("2016-01-01").value // 10**9, pd.Timestamp("2025-12-31").value // 10**9, 20), unit="s").date,
                        salary=np.round(rng.integers(35, 160, 20) * 1000, -3), rating=rng.integers(1, 6, 20)))
save(emp, "employees_small.csv")

# ---------------------------------------------------------------- 13. Reps table used in the Excel dynamic-array lesson
reps = pd.DataFrame({"Rep": ["Asha", "Ravi", "Meera", "Kabir", "Zoya", "Farhan", "Neha", "Rohan"], "Region": ["North", "West", "South", "North", "East", "West", "South", "North"],
                     "Product": ["Laptop", "Phone", "Laptop", "Tablet", "Phone", "Laptop", "Tablet", "Phone"], "Units": [5, 12, 3, 8, 15, 4, 10, 9],
                     "Price": [55000, 18000, 55000, 25000, 18000, 55000, 25000, 18000]})
reps["Revenue"] = reps.Units * reps.Price
save(reps, "reps_small.csv")

# ---------------------------------------------------------------- 14. Product lookup table used in the Excel lookup lesson
lk = pd.DataFrame({"Product ID": ["P101", "P102", "P103", "P104", "P105", "P106"], "Product": ["Office Chair", "Standing Desk", "Laser Printer", "Notebook Pack", "Smartphone", "Bookcase"],
                   "Category": ["Furniture", "Furniture", "Technology", "Office Supplies", "Technology", "Furniture"], "Price": [4500, 18500, 12900, 240, 21999, 7600], "Stock": [32, 8, 15, 540, 27, 0]})
save(lk, "lookup_products.csv")
