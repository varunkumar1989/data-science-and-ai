"""Excel Basic-to-Advanced workbook: one sheet per topic with live formulas on a sample retail dataset."""
import os, random, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule, FormulaRule, ColorScaleRule, DataBarRule, IconSetRule
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.comments import Comment

DS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DS, "site", "files", "Excel_Basic_to_Advanced.xlsx"); os.makedirs(os.path.dirname(OUT), exist_ok=True)
F = "Arial"
NAVY, AMBER = "1F3864", "E9A23B"
H1 = Font(name=F, size=16, bold=True, color=NAVY); H2 = Font(name=F, size=12, bold=True, color=NAVY)
HDR = Font(name=F, bold=True, color="FFFFFF"); HFILL = PatternFill("solid", fgColor=NAVY)
BODY = Font(name=F, size=10); INPUT = Font(name=F, size=10, color="0000FF"); CODE = Font(name="Consolas", size=10, color="7A3E00")
NOTE = Font(name=F, size=9, italic=True, color="666666"); LINK = Font(name=F, size=10, color="0563C1", underline="single")
YEL = PatternFill("solid", fgColor="FFF2CC"); THIN = Side(style="thin", color="D0D5E0"); BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")

wb = Workbook()
def sheet(name, title, intro, widths):
    ws = wb.create_sheet(name)
    ws["A1"] = title; ws["A1"].font = H1
    ws["A2"] = intro; ws["A2"].font = NOTE; ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=len(widths)); ws.row_dimensions[2].height = 32
    for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws["A3"] = "← Index"; ws["A3"].hyperlink = "#'00 Index'!A1"; ws["A3"].font = LINK
    ws.sheet_view.showGridLines = False
    return ws
def header(ws, row, cols):
    for i, c in enumerate(cols, 1):
        x = ws.cell(row=row, column=i, value=c); x.font = HDR; x.fill = HFILL; x.alignment = WRAP; x.border = BOX
def text(ws, cell, value, font=BODY):
    c = ws[cell]; c.value = value; c.font = font; c.alignment = WRAP; c.border = BOX
    if isinstance(value, str) and value.startswith("="): c.data_type = "s"     # show formula as text
    return c
def live(ws, cell, formula, fmt=None):
    c = ws[cell]; c.value = formula; c.font = Font(name=F, size=10, bold=True); c.border = BOX; c.alignment = Alignment(vertical="top")
    if fmt: c.number_format = fmt
    return c
def rows_table(ws, start, cols, rows, live_col=None, fmts=None):
    """rows: list of tuples. Column index live_col (1-based) is written as a live formula."""
    header(ws, start, cols)
    for r, row in enumerate(rows, start + 1):
        for ci, v in enumerate(row, 1):
            ref = f"{get_column_letter(ci)}{r}"
            if ci == live_col and v is not None:
                live(ws, ref, v, (fmts or {}).get(r))
            else:
                text(ws, ref, v, CODE if (isinstance(v, str) and v.startswith("=")) else BODY)
    return start + len(rows) + 1

# ------------------------------------------------------------------ sample data
random.seed(26)
stores = [("S01", "Andheri", "Mumbai", "Maharashtra"), ("S02", "FC Road", "Pune", "Maharashtra"), ("S03", "Connaught Place", "Delhi", "Delhi"),
          ("S04", "Indiranagar", "Bengaluru", "Karnataka"), ("S05", "T Nagar", "Chennai", "Tamil Nadu"), ("S06", "Cyber Hub", "Gurugram", "Haryana")]
products = [("P101", "Smartphone A", "Mobiles", 18999, 15200), ("P102", "Smartphone B", "Mobiles", 32999, 27100), ("P201", "Laptop 14in", "Laptops", 54999, 47300),
            ("P202", "Laptop Pro 16", "Laptops", 94999, 81200), ("P301", "Wireless Earbuds", "Audio", 2999, 1650), ("P302", "Bluetooth Speaker", "Audio", 4499, 2900),
            ("P401", "Power Bank 20k", "Accessories", 1799, 980), ("P402", "Charger 65W", "Accessories", 1499, 760), ("P501", "Smart TV 43in", "TV", 32999, 28400),
            ("P502", "Smart TV 55in", "TV", 52999, 45100)]
ctypes = ["Walk-in", "Online", "Corporate"]
start = dt.date(2026, 4, 1)
orders = []
for i in range(1, 401):
    d = start + dt.timedelta(days=random.randint(0, 182))
    s = random.choices(stores, weights=[22, 15, 20, 18, 12, 13])[0]
    p = random.choices(products, weights=[16, 8, 7, 3, 18, 9, 14, 12, 7, 4])[0]
    q = random.choices([1, 2, 3, 4], weights=[70, 18, 8, 4])[0]
    disc = random.choice([0, 0, 0, 0.05, 0.1])
    orders.append((f"ORD-{i:04d}", d, s[0], s[2], p[0], p[2], q, p[3], disc, random.choice(ctypes), random.choice(["Yes", "No", "No"])))
orders.sort(key=lambda r: r[1])
N = len(orders); LAST = N + 1   # data rows 2..LAST on sheet Data

# ------------------------------------------------------------------ Data + Lookups
wsD = wb.active; wsD.title = "Data"
cols = ["OrderID", "OrderDate", "StoreID", "City", "ProductID", "Category", "Qty", "UnitPrice", "Discount", "CustomerType", "Warranty", "Amount", "Cost", "Profit"]
header(wsD, 1, cols)
for r, o in enumerate(orders, 2):
    for ci, v in enumerate(o, 1):
        c = wsD.cell(row=r, column=ci, value=v); c.font = BODY
    wsD.cell(row=r, column=2).number_format = "dd-mmm-yyyy"; wsD.cell(row=r, column=8).number_format = "#,##0"; wsD.cell(row=r, column=9).number_format = "0%"
    wsD.cell(row=r, column=12, value=f"=G{r}*H{r}*(1-I{r})").number_format = "#,##0"
    wsD.cell(row=r, column=13, value=f"=G{r}*INDEX(Lookups!$E$3:$E$12,MATCH(E{r},Lookups!$A$3:$A$12,0))").number_format = "#,##0"
    wsD.cell(row=r, column=14, value=f"=L{r}-M{r}").number_format = "#,##0"
    for ci in (12, 13, 14): wsD.cell(row=r, column=ci).font = BODY
for i, w in enumerate([11, 12, 8, 11, 9, 12, 5, 10, 9, 13, 9, 11, 11, 11], 1): wsD.column_dimensions[get_column_letter(i)].width = w
wsD.freeze_panes = "A2"; wsD.auto_filter.ref = f"A1:N{LAST}"
wsD["P1"] = "Sample data (generated for practice): 400 orders, Apr–Sep 2026, fictional electronics chain."; wsD["P1"].font = NOTE

wsL = wb.create_sheet("Lookups")
wsL["A1"] = "Lookup tables used by the formulas"; wsL["A1"].font = H2
header(wsL, 2, ["ProductID", "ProductName", "Category", "ListPrice", "UnitCost"])
for r, p in enumerate(products, 3):
    for ci, v in enumerate(p, 1): wsL.cell(row=r, column=ci, value=v).font = BODY
header(wsL, 2 + 0, ["ProductID", "ProductName", "Category", "ListPrice", "UnitCost"])
header_row = 2
for ci, h in enumerate(["StoreID", "StoreName", "City", "State"], 7): pass
for i, h in enumerate(["StoreID", "StoreName", "City", "State"]):
    c = wsL.cell(row=2, column=7 + i, value=h); c.font = HDR; c.fill = HFILL
for r, s in enumerate(stores, 3):
    for ci, v in enumerate(s, 7): wsL.cell(row=r, column=ci, value=v).font = BODY
for i, h in enumerate(["SalesFrom", "CommissionRate"]):
    c = wsL.cell(row=2, column=12 + i, value=h); c.font = HDR; c.fill = HFILL
for r, (a, b) in enumerate([(0, 0.02), (100000, 0.03), (500000, 0.05), (1000000, 0.07)], 3):
    wsL.cell(row=r, column=12, value=a).font = INPUT; wsL.cell(row=r, column=13, value=b).font = INPUT; wsL.cell(row=r, column=13).number_format = "0%"
c = wsL.cell(row=2, column=15, value="Holidays"); c.font = HDR; c.fill = HFILL
for r, h in enumerate([dt.date(2026, 8, 15), dt.date(2026, 10, 2), dt.date(2026, 10, 20), dt.date(2026, 11, 8)], 3):
    wsL.cell(row=r, column=15, value=h).number_format = "dd-mmm-yyyy"
for col, w in zip("ABCDEFGHIJKLMNO", [10, 18, 12, 10, 10, 2, 9, 16, 11, 12, 2, 11, 15, 2, 13]): wsL.column_dimensions[col].width = w

# ------------------------------------------------------------------ 00 Index (created first in order later)
idx = wb.create_sheet("00 Index", 0)
idx["A1"] = "Excel: Basic to Advanced – practice workbook"; idx["A1"].font = Font(name=F, size=18, bold=True, color=NAVY)
idx["A2"] = "Companion to the Data Science & AI Handbook (Advanced Excel session and Building Blocks · Class 1). Black bold cells are live formulas; blue cells are inputs you can change. Brown text shows the formula used."
idx["A2"].font = NOTE; idx.merge_cells("A2:D2"); idx["A2"].alignment = Alignment(wrap_text=True); idx.row_dimensions[2].height = 30
header(idx, 4, ["#", "Sheet", "Topic", "Level"])
idx.column_dimensions["A"].width = 5; idx.column_dimensions["B"].width = 26; idx.column_dimensions["C"].width = 70; idx.column_dimensions["D"].width = 16
idx.sheet_view.showGridLines = False

# ------------------------------------------------------------------ 01 Environment
ws = sheet("01 Environment", "01 · Excel environment, terminology & shortcuts", "Building Blocks · Class 1. Learn the vocabulary and the 30 shortcuts that save the most time.", [26, 60, 26, 40])
r = rows_table(ws, 5, ["Term", "Meaning", "Example", "Tip"], [
    ("Workbook", "The .xlsx file containing sheets", "Excel_Basic_to_Advanced.xlsx", ".xlsm if it contains macros"),
    ("Worksheet", "One grid of rows and columns", "Data, Lookups", "Double-click a tab to rename"),
    ("Cell / address", "Intersection of a column and row", "B7", "Name Box shows the active cell"),
    ("Range", "Block of cells", "A1:D20", "Ctrl+Shift+Arrow selects a range"),
    ("Formula", "Starts with = and calculates", "=G2*H2", "Ctrl+` shows all formulas"),
    ("Function", "Built-in named formula", "=SUM(L2:L401)", "Shift+F3 opens Insert Function"),
    ("Argument", "Input to a function", "SUM(number1, number2...)", "Separated by commas"),
    ("Table", "Formatted, auto-expanding range", "Ctrl+T", "Use names like Sales[Amount]"),
    ("Named range", "A friendly name for cells", "GST_Rate", "Formulas → Name Manager"),
    ("Ribbon / QAT", "Command tabs / quick-access toolbar", "Home, Insert, Data…", "Right-click a command → Add to QAT"),
])
ws.cell(row=r + 1, column=1, value="Shortcuts").font = H2
rows_table(ws, r + 2, ["Shortcut", "Action", "Shortcut", "Action"], [
    ("Ctrl+Arrow", "Jump to edge of data", "Ctrl+1", "Format Cells"),
    ("Ctrl+Shift+Arrow", "Select to edge of data", "Ctrl+T", "Create Table"),
    ("Ctrl+Space / Shift+Space", "Select column / row", "Ctrl+Shift+L", "Toggle filter"),
    ("Ctrl+Home / Ctrl+End", "First / last used cell", "Alt+=", "AutoSum"),
    ("Ctrl+PgUp / PgDn", "Previous / next sheet", "F4", "Toggle $ references; repeat action"),
    ("F2", "Edit cell", "Ctrl+;", "Insert today's date"),
    ("Ctrl+D / Ctrl+R", "Fill down / right", "Ctrl+Shift+;", "Insert current time"),
    ("Ctrl+E", "Flash Fill", "Alt+Enter", "New line inside a cell"),
    ("Ctrl+Alt+V", "Paste Special", "Ctrl+`", "Show formulas"),
    ("Alt+F1 / F11", "Quick chart / chart sheet", "Alt+F5 / Ctrl+Alt+F5", "Refresh pivot / Refresh All"),
    ("Ctrl+Z / Ctrl+Y", "Undo / Redo", "Alt+F11", "VBA editor"),
    ("Ctrl+F / Ctrl+H", "Find / Replace", "Ctrl+G or F5", "Go To (Special)"),
])

# ------------------------------------------------------------------ 02 References
ws = sheet("02 References", "02 · Cell references: relative, absolute, mixed", "Change the blue GST rate in C4 and watch every row update. The $ in $C$4 keeps the reference fixed when the formula is copied down.", [22, 14, 14, 16, 30, 18])
ws["B4"] = "GST rate"; ws["B4"].font = H2; ws["C4"] = 0.18; ws["C4"].font = INPUT; ws["C4"].number_format = "0%"; ws["C4"].fill = YEL
header(ws, 6, ["Product", "Price (₹)", "GST (₹)", "Price incl. GST", "Formula in C (copied down)", "Reference type"])
for i, (nm, pr) in enumerate([("Earbuds", 2999), ("Power Bank", 1799), ("Speaker", 4499), ("Charger", 1499)], 7):
    text(ws, f"A{i}", nm); ws[f"B{i}"] = pr; ws[f"B{i}"].font = INPUT; ws[f"B{i}"].number_format = "#,##0"
    live(ws, f"C{i}", f"=B{i}*$C$4", "#,##0.00"); live(ws, f"D{i}", f"=B{i}+C{i}", "#,##0.00")
    text(ws, f"E{i}", f"=B{i}*$C$4", CODE); text(ws, f"F{i}", "B relative, $C$4 absolute")
ws["A13"] = "Mixed references: multiplication grid"; ws["A13"].font = H2
ws["A14"] = "×"; ws["A14"].font = H2
for j in range(1, 6):
    ws.cell(row=14, column=1 + j, value=j).font = INPUT; ws.cell(row=14 + j, column=1, value=j).font = INPUT
    for k in range(1, 6):
        c = ws.cell(row=14 + j, column=1 + k, value=f"=$A{14 + j}*{get_column_letter(1 + k)}$14"); c.font = Font(name=F, bold=True); c.border = BOX
ws["A21"] = "Formula in B15, copied to the whole grid:  =$A15*B$14  ($A locks the column, $14 locks the row)"; ws["A21"].font = CODE

# ------------------------------------------------------------------ 03 Custom formats
ws = sheet("03 Custom Formats", "03 · Formatting & custom number formats", "The value in column B is the same in every row; only the number format in column C changes how it looks (Ctrl+1 → Custom).", [34, 14, 22, 52, 40])
header(ws, 5, ["Purpose", "Value", "Displayed as", "Custom format code", "Note"])
fmts = [("Thousands separator", 1250000, "#,##0", "Standard grouping"),
        ("Indian lakh/crore grouping", 1250000, "[>=10000000]##\\,##\\,##\\,##0;[>=100000]##\\,##\\,##0;##,##0", "12,50,000"),
        ("Millions", 1250000, '0.0,,"M"', "Each comma divides by 1,000"),
        ("Rupee currency", 99.5, '"₹"#,##0.00', "Currency with symbol"),
        ("Fixed-length ID", 7, "000", "Shows 007"),
        ("Readable date", dt.date(1986, 5, 9), "dd mmm' yyyy", "09 May' 1986"),
        ("Units while numeric", 80, '0 "kg"', "Still a number for maths"),
        ("Up/down arrows", 0.12, '[Color10]▲0%;[Red]▼0%;0%', "positive;negative;zero"),
        ("Negative in brackets", -45200, "#,##0;(#,##0);-", "Finance style; zero shows -"),
        ("Thousands with k", 87670, '[<100000]0.00,"k";0.0,"k"', "87.67k; ≥100000 one decimal"),
        ("Percentage", 0.0765, "0.0%", "Stored as a fraction"),
        ("Hide value", 12345, ";;;", "Value kept but invisible")]
for i, (p, v, f, nte) in enumerate(fmts, 6):
    text(ws, f"A{i}", p); ws[f"B{i}"] = v; ws[f"B{i}"].font = INPUT
    if isinstance(v, dt.date): ws[f"B{i}"].number_format = "yyyy-mm-dd"
    c = ws[f"C{i}"]; c.value = f"=B{i}"; c.number_format = f; c.font = Font(name=F, bold=True); c.border = BOX
    text(ws, f"D{i}", f, CODE); text(ws, f"E{i}", nte)
ws["A20"] = "Format has up to 4 sections:  positive ; negative ; zero ; text.  Conditions like [<100000] can replace them."; ws["A20"].font = NOTE

# ------------------------------------------------------------------ 04 Number
ws = sheet("04 Number", "04 · Number functions", "Real-world examples on a single order: change the blue inputs.", [26, 46, 16, 44])
ws["A5"] = "Order amount (₹)"; ws["B5"] = 12345.678; ws["B5"].font = INPUT; ws["A6"] = "Quantity"; ws["B6"] = 37; ws["B6"].font = INPUT
ws["A7"] = "Carton size"; ws["B7"] = 12; ws["B7"].font = INPUT
for a in ("A5", "A6", "A7"): ws[a].font = H2
rows_table(ws, 9, ["Function", "Formula", "Result", "Business use"], [
    ("ROUND", "=ROUND(B5*18%,2)", "=ROUND(B5*18%,2)", "GST at 18% to paise"),
    ("ROUNDUP", "=ROUNDUP(B6/B7,0)", "=ROUNDUP(B6/B7,0)", "Cartons needed (12 per carton)"),
    ("ROUNDDOWN", "=ROUNDDOWN(B5,-2)", "=ROUNDDOWN(B5,-2)", "Round down to hundreds"),
    ("INT", "=INT(B5/1000)", "=INT(B5/1000)", "Whole thousands"),
    ("MOD", "=MOD(B6,B7)", "=MOD(B6,B7)", "Loose units left over"),
    ("ABS", "=ABS(9500-B5)", "=ABS(9500-B5)", "Size of miss vs target 9,500"),
    ("CEILING.MATH", "=CEILING.MATH(B5,10)", "=_xlfn.CEILING.MATH(B5,10)", "Price rounded up to next ₹10"),
    ("POWER", "=POWER(1.12,5)", "=POWER(1.12,5)", "Growth factor at 12% for 5 years"),
    ("SQRT", "=SQRT(144)", "=SQRT(144)", "Square root"),
    ("SUMPRODUCT", "=SUMPRODUCT(Data!G2:G401,Data!H2:H401)", f"=SUMPRODUCT(Data!G2:G{LAST},Data!H2:H{LAST})", "Gross sales without a helper column"),
    ("RANDBETWEEN", "=RANDBETWEEN(1,100)", None, "Random sample IDs (recalculates every change, so no live value here)"),
], live_col=3)

# ------------------------------------------------------------------ 05 Text
ws = sheet("05 Text", "05 · Text functions", "Cleaning messy imported text. Inputs in blue.", [22, 44, 30, 40])
ws["A5"] = "Full name"; ws["B5"] = "  ravi   kumar  "; ws["A6"] = "Email"; ws["B6"] = "Asha.Verma@Example.com"
ws["A7"] = "Order code"; ws["B7"] = "NOR-1042-MUM"; ws["A8"] = "Phone"; ws["B8"] = "9876543210"; ws["A9"] = "Price text"; ws["B9"] = "₹1,250"
for a in ("A5", "A6", "A7", "A8", "A9"): ws[a].font = H2
for b in ("B5", "B6", "B7", "B8", "B9"): ws[b].font = INPUT
rows_table(ws, 11, ["Function", "Formula", "Result", "Use"], [
    ("TRIM + PROPER", "=PROPER(TRIM(B5))", "=PROPER(TRIM(B5))", "Tidy names"),
    ("LEFT", "=LEFT(B7,3)", "=LEFT(B7,3)", "Region prefix"),
    ("RIGHT", "=RIGHT(B7,3)", "=RIGHT(B7,3)", "City suffix"),
    ("MID + FIND", "=MID(B7,FIND(\"-\",B7)+1,4)", "=MID(B7,FIND(\"-\",B7)+1,4)", "Middle part"),
    ("LEN", "=LEN(B8)=10", "=LEN(B8)=10", "Valid 10-digit mobile?"),
    ("Domain", "=MID(B6,FIND(\"@\",B6)+1,50)", "=MID(B6,FIND(\"@\",B6)+1,50)", "Email domain"),
    ("LOWER", "=LOWER(B6)", "=LOWER(B6)", "Standardise emails"),
    ("UPPER", "=UPPER(B7)", "=UPPER(B7)", "Codes in capitals"),
    ("SUBSTITUTE + VALUE", "=VALUE(SUBSTITUTE(SUBSTITUTE(B9,\"₹\",\"\"),\",\",\"\"))", "=VALUE(SUBSTITUTE(SUBSTITUTE(B9,\"₹\",\"\"),\",\",\"\"))", "Text price → number"),
    ("Mask", "=\"XXXXXX\"&RIGHT(B8,4)", "=\"XXXXXX\"&RIGHT(B8,4)", "Hide phone digits"),
    ("CONCAT / &", "=PROPER(TRIM(B5))&\" (\"&RIGHT(B7,3)&\")\"", "=PROPER(TRIM(B5))&\" (\"&RIGHT(B7,3)&\")\"", "Build labels"),
    ("TEXTJOIN", "=TEXTJOIN(\", \",TRUE,Lookups!I3:I8)", "=_xlfn.TEXTJOIN(\", \",TRUE,Lookups!I3:I8)", "List of cities in one cell"),
    ("Word count", "=LEN(TRIM(B5))-LEN(SUBSTITUTE(TRIM(B5),\" \",\"\"))+1", "=LEN(TRIM(B5))-LEN(SUBSTITUTE(TRIM(B5),\" \",\"\"))+1", "Words in a cell"),
    ("TEXT", "=TEXT(1234.5,\"₹#,##0.00\")", "=TEXT(1234.5,\"₹#,##0.00\")", "Number as formatted text"),
], live_col=3)

# ------------------------------------------------------------------ 06 Date & Time
ws = sheet("06 Date & Time", "06 · Date & time functions", "Dates are serial numbers. Inputs in blue; Holidays list on the Lookups sheet.", [24, 52, 18, 40])
ws["A5"] = "Order date"; ws["B5"] = dt.date(2026, 10, 9); ws["A6"] = "Delivered"; ws["B6"] = dt.date(2026, 10, 21); ws["A7"] = "Date of birth"; ws["B7"] = dt.date(1990, 6, 15)
ws["A8"] = "Login"; ws["B8"] = dt.datetime(2026, 10, 9, 9, 15); ws["A9"] = "Logout"; ws["B9"] = dt.datetime(2026, 10, 9, 18, 40)
for a in ("A5", "A6", "A7", "A8", "A9"): ws[a].font = H2
for b in ("B5", "B6", "B7"): ws[b].font = INPUT; ws[b].number_format = "dd-mmm-yyyy"
for b in ("B8", "B9"): ws[b].font = INPUT; ws[b].number_format = "dd-mmm-yyyy hh:mm"
D = "dd-mmm-yyyy"
rows_table(ws, 11, ["Function", "Formula", "Result", "Use"], [
    ("YEAR / MONTH / DAY", "=YEAR(B5)", "=YEAR(B5)", "Group by year"),
    ("TEXT month", "=TEXT(B5,\"mmm-yy\")", "=TEXT(B5,\"mmm-yy\")", "Month label"),
    ("Weekday name", "=TEXT(B5,\"dddd\")", "=TEXT(B5,\"dddd\")", "Day of week"),
    ("DATE", "=DATE(2026,4,1)", "=DATE(2026,4,1)", "Start of FY 2026-27"),
    ("EOMONTH", "=EOMONTH(B5,0)", "=EOMONTH(B5,0)", "Month-end (billing cut-off)"),
    ("First of month", "=EOMONTH(B5,-1)+1", "=EOMONTH(B5,-1)+1", "Month start"),
    ("EDATE", "=EDATE(B5,3)", "=EDATE(B5,3)", "Warranty check after 3 months"),
    ("Days between", "=B6-B5", "=B6-B5", "Delivery days (calendar)"),
    ("NETWORKDAYS", "=NETWORKDAYS(B5,B6,Lookups!O3:O6)", "=NETWORKDAYS(B5,B6,Lookups!O3:O6)", "Working days excl. weekends & holidays"),
    ("WORKDAY", "=WORKDAY(B5,10,Lookups!O3:O6)", "=WORKDAY(B5,10,Lookups!O3:O6)", "SLA due date: 10 working days"),
    ("DATEDIF", "=DATEDIF(B7,B5,\"Y\")", "=DATEDIF(B7,B5,\"Y\")", "Age in completed years on order date"),
    ("WEEKNUM", "=WEEKNUM(B5,2)", "=WEEKNUM(B5,2)", "Week number (Mon start)"),
    ("Financial year", "=\"FY\"&IF(MONTH(B5)>=4,YEAR(B5)+1,YEAR(B5))", "=\"FY\"&IF(MONTH(B5)>=4,YEAR(B5)+1,YEAR(B5))", "Indian FY label"),
    ("FY quarter", "=\"Q\"&ROUNDUP((MOD(MONTH(B5)-4,12)+1)/3,0)", "=\"Q\"&ROUNDUP((MOD(MONTH(B5)-4,12)+1)/3,0)", "Apr–Jun = Q1"),
    ("Hours worked", "=(B9-B8)*24", "=(B9-B8)*24", "Shift length in hours"),
], live_col=3, fmts={15: D, 16: D, 17: D, 18: D, 21: D, 26: "0.00"})

# ------------------------------------------------------------------ 07 Aggregate
ws = sheet("07 Aggregate", "07 · Aggregate & conditional aggregate functions", "All formulas read the 400-order Data sheet. Change the blue city / dates to re-run.", [26, 70, 18, 34])
ws["A5"] = "City"; ws["B5"] = "Pune"; ws["A6"] = "From"; ws["B6"] = dt.date(2026, 7, 1); ws["A7"] = "To"; ws["B7"] = dt.date(2026, 9, 30)
for a in ("A5", "A6", "A7"): ws[a].font = H2
for b in ("B5", "B6", "B7"): ws[b].font = INPUT; ws[b].fill = YEL
ws["B6"].number_format = ws["B7"].number_format = "dd-mmm-yyyy"
L = LAST; A = f"Data!$L$2:$L${L}"; C = f"Data!$D$2:$D${L}"; Dt = f"Data!$B$2:$B${L}"; Cat = f"Data!$F$2:$F${L}"; Ty = f"Data!$J$2:$J${L}"; W = f"Data!$K$2:$K${L}"
rows_table(ws, 9, ["Function", "Formula", "Result", "Answer to"], [
    ("SUM", f"=SUM({A})", f"=SUM({A})", "Total revenue"),
    ("COUNT / COUNTA", f"=COUNTA(Data!$A$2:$A${L})", f"=COUNTA(Data!$A$2:$A${L})", "Number of orders"),
    ("AVERAGE", f"=AVERAGE({A})", f"=AVERAGE({A})", "Average order value"),
    ("MEDIAN", f"=MEDIAN({A})", f"=MEDIAN({A})", "Typical order (skew-proof)"),
    ("MAX / LARGE", f"=LARGE({A},3)", f"=LARGE({A},3)", "3rd largest order"),
    ("MIN / SMALL", f"=SMALL({A},1)", f"=SMALL({A},1)", "Smallest order"),
    ("COUNTBLANK", f"=COUNTBLANK(Data!$D$2:$D${L})", f"=COUNTBLANK(Data!$D$2:$D${L})", "Orders missing a city"),
    ("SUMIF", f"=SUMIF({C},B5,{A})", f"=SUMIF({C},B5,{A})", "Revenue for the chosen city"),
    ("SUMIFS (city + dates)", f"=SUMIFS({A},{C},B5,{Dt},\">=\"&B6,{Dt},\"<=\"&B7)", f"=SUMIFS({A},{C},B5,{Dt},\">=\"&B6,{Dt},\"<=\"&B7)", "City revenue between two dates"),
    ("COUNTIFS", f"=COUNTIFS({C},B5,{A},\">20000\")", f"=COUNTIFS({C},B5,{A},\">20000\")", "Big orders in the city"),
    ("AVERAGEIFS", f"=AVERAGEIFS({A},{Cat},\"Laptops\")", f"=AVERAGEIFS({A},{Cat},\"Laptops\")", "Average laptop order"),
    ("MAXIFS", f"=MAXIFS({A},{C},B5)", f"=_xlfn.MAXIFS({A},{C},B5)", "Biggest order in the city"),
    ("OR across cities", f"=SUM(SUMIFS({A},{C},{{\"Pune\",\"Mumbai\"}}))", f"=SUMPRODUCT(SUMIFS({A},{C},{{\"Pune\",\"Mumbai\"}}))", "Maharashtra revenue"),
    ("Conditional probability", f"=COUNTIFS({Ty},\"Walk-in\",{W},\"Yes\")/COUNTIF({Ty},\"Walk-in\")", f"=COUNTIFS({Ty},\"Walk-in\",{W},\"Yes\")/COUNTIF({Ty},\"Walk-in\")", "P(warranty | walk-in)"),
    ("RANK.EQ", "=RANK.EQ(C10,C10:C12)", None, "Rank a value in a list (see Dashboard sheet)"),
    ("STDEV.S", f"=STDEV.S({A})", f"=_xlfn.STDEV.S({A})", "Spread of order values"),
    ("SUBTOTAL (visible)", f"=SUBTOTAL(109,{A})", f"=SUBTOTAL(109,{A})", "Sum that ignores filtered-out rows"),
], live_col=3, fmts={**{r: "#,##0" for r in range(10, 26)}, 11: "0", 16: "0", 19: "0", 23: "0.0%"})

# ------------------------------------------------------------------ 08 Logical
ws = sheet("08 Logical", "08 · Logical functions & error handling", "Customer tiering and data checks on sample rows (blue inputs).", [14, 12, 10, 12, 30, 30, 22])
header(ws, 5, ["Customer", "Spend (₹)", "Prime?", "City", "Tier (nested IF)", "Tier (IFS)", "Zone (SWITCH)"])
cust = [("C01", 72000, "Yes", "Pune"), ("C02", 31000, "No", "Delhi"), ("C03", 8000, "Yes", "Mumbai"), ("C04", 0, "No", "Chennai")]
for i, (c_, s_, p_, ct) in enumerate(cust, 6):
    text(ws, f"A{i}", c_); ws[f"B{i}"] = s_; ws[f"B{i}"].font = INPUT; ws[f"B{i}"].number_format = "#,##0"; ws[f"C{i}"] = p_; ws[f"C{i}"].font = INPUT; ws[f"D{i}"] = ct; ws[f"D{i}"].font = INPUT
    live(ws, f"E{i}", f'=IF(B{i}>=50000,"Gold",IF(B{i}>=20000,"Silver","Bronze"))')
    live(ws, f"F{i}", f'=_xlfn.IFS(B{i}>=50000,"Gold",B{i}>=20000,"Silver",TRUE,"Bronze")')
    live(ws, f"G{i}", f'=_xlfn.SWITCH(D{i},"Pune","West","Mumbai","West","Delhi","North","South")')
rows_table(ws, 11, ["Function", "Formula (row 6)", "", "", "Result", "Use", ""], [
    ("AND", '=IF(AND(B6>50000,C6="Yes"),"VIP","-")', None, None, '=IF(AND(B6>50000,C6="Yes"),"VIP","-")', "Both conditions", None),
    ("OR", '=IF(OR(D7="Pune",D7="Mumbai"),"MH","Other")', None, None, '=IF(OR(D7="Pune",D7="Mumbai"),"MH","Other")', "Either condition", None),
    ("NOT", '=NOT(C8="Yes")', None, None, '=NOT(C8="Yes")', "Reverse a test", None),
    ("IFERROR", "=IFERROR(100000/B9,0)", None, None, "=IFERROR(100000/B9,0)", "Avoid divide-by-zero errors", None),
    ("IFNA", '=IFNA(MATCH("C09",A6:A9,0),"Not found")', None, None, '=_xlfn.IFNA(MATCH("C09",A6:A9,0),"Not found")', "Friendly lookup miss", None),
    ("ISNUMBER+SEARCH", '=ISNUMBER(SEARCH("pun",D6))', None, None, '=ISNUMBER(SEARCH("pun",D6))', "Text contains", None),
], live_col=5)

# ------------------------------------------------------------------ 09 Lookup
ws = sheet("09 Lookup", "09 · Lookup functions: VLOOKUP → INDEX/MATCH → XLOOKUP", "Find details for the product ID in B5. Lookup tables are on the Lookups sheet.", [26, 62, 20, 36])
ws["A5"] = "Product ID"; ws["B5"] = "P302"; ws["A5"].font = H2; ws["B5"].font = INPUT; ws["B5"].fill = YEL
ws["A6"] = "Rep sales (₹)"; ws["B6"] = 340000; ws["A6"].font = H2; ws["B6"].font = INPUT; ws["B6"].fill = YEL; ws["B6"].number_format = "#,##0"
P = "Lookups!$A$3:$E$12"
r = rows_table(ws, 8, ["Method", "Formula", "Result", "Note"], [
    ("VLOOKUP exact", f"=VLOOKUP(B5,{P},2,FALSE)", f"=VLOOKUP(B5,{P},2,FALSE)", "Name: column 2 of the table"),
    ("VLOOKUP price", f"=VLOOKUP(B5,{P},4,FALSE)", f"=VLOOKUP(B5,{P},4,FALSE)", "List price"),
    ("INDEX + MATCH", "=INDEX(Lookups!$C$3:$C$12,MATCH(B5,Lookups!$A$3:$A$12,0))", "=INDEX(Lookups!$C$3:$C$12,MATCH(B5,Lookups!$A$3:$A$12,0))", "Category; works in any direction"),
    ("Reverse lookup", '=INDEX(Lookups!$A$3:$A$12,MATCH("Charger 65W",Lookups!$B$3:$B$12,0))', '=INDEX(Lookups!$A$3:$A$12,MATCH("Charger 65W",Lookups!$B$3:$B$12,0))', "ID from name (left of the key)"),
    ("VLOOKUP + CHOOSE", '=VLOOKUP("Charger 65W",CHOOSE({1,2},Lookups!$B$3:$B$12,Lookups!$A$3:$A$12),2,FALSE)', '=VLOOKUP("Charger 65W",CHOOSE({1,2},Lookups!$B$3:$B$12,Lookups!$A$3:$A$12),2,FALSE)', "Classic left-lookup trick"),
    ("HLOOKUP", '=HLOOKUP("City",Lookups!$G$2:$J$8,3,FALSE)', '=HLOOKUP("City",Lookups!$G$2:$J$8,3,FALSE)', "Look across a header row"),
    ("Two-way INDEX/MATCH", '=INDEX(Lookups!$A$3:$E$12,MATCH(B5,Lookups!$A$3:$A$12,0),MATCH("UnitCost",Lookups!$A$2:$E$2,0))', '=INDEX(Lookups!$A$3:$E$12,MATCH(B5,Lookups!$A$3:$A$12,0),MATCH("UnitCost",Lookups!$A$2:$E$2,0))', "Row by ID, column by header"),
    ("Approximate (slabs)", "=VLOOKUP(B6,Lookups!$L$3:$M$6,2,TRUE)", "=VLOOKUP(B6,Lookups!$L$3:$M$6,2,TRUE)", "Commission rate for sales in B6"),
    ("Commission", "=B6*VLOOKUP(B6,Lookups!$L$3:$M$6,2,TRUE)", "=B6*VLOOKUP(B6,Lookups!$L$3:$M$6,2,TRUE)", "₹ commission"),
    ("Not-found handling", '=IFERROR(VLOOKUP("P999",Lookups!$A$3:$E$12,2,FALSE),"Missing")', '=IFERROR(VLOOKUP("P999",Lookups!$A$3:$E$12,2,FALSE),"Missing")', "Friendly message"),
], live_col=3, fmts={16: "0%", 17: "#,##0"})
ws.cell(row=r + 1, column=1, value="Excel 365 / 2021 only (type these in Excel 365; expected result shown)").font = H2
rows_table(ws, r + 2, ["Function", "Formula", "Expected result", "Why it's better"], [
    ("XLOOKUP", '=XLOOKUP(B5,Lookups!A3:A12,Lookups!B3:B12,"Missing")', "Bluetooth Speaker", "Any direction + built-in not-found"),
    ("XLOOKUP whole row", "=XLOOKUP(B5,Lookups!A3:A12,Lookups!B3:E12)", "Bluetooth Speaker | Audio | 4499 | 2900", "Returns several columns at once"),
    ("XLOOKUP slab", "=XLOOKUP(B6,Lookups!L3:L6,Lookups!M3:M6,,-1)", "3%", "-1 = exact or next smaller"),
    ("XMATCH", '=XMATCH("Laptop 14in",Lookups!B3:B12)', "3", "Position, with search modes"),
])

# ------------------------------------------------------------------ 10 Conditional formatting
ws = sheet("10 Conditional Formatting", "10 · Conditional formatting (rules already applied)", "Home → Conditional Formatting → Manage Rules to see each rule. Change the blue numbers to see formats move.", [12, 14, 12, 14, 12, 12, 40])
header(ws, 5, ["Invoice", "Due date", "Status", "Amount (₹)", "Margin %", "Score", "Rules applied"])
inv = [("INV-01", dt.date(2026, 9, 30), "Unpaid", 52000, 0.22, 88), ("INV-02", dt.date(2026, 11, 15), "Unpaid", 18000, -0.05, 45),
       ("INV-03", dt.date(2026, 10, 5), "Paid", 74000, 0.31, 92), ("INV-04", dt.date(2026, 8, 20), "Unpaid", 9000, 0.08, 61),
       ("INV-05", dt.date(2026, 12, 1), "Paid", 33000, 0.15, 73), ("INV-01", dt.date(2026, 10, 25), "Unpaid", 61000, 0.19, 80)]
for i, row in enumerate(inv, 6):
    for ci, v in enumerate(row, 1):
        c = ws.cell(row=i, column=ci, value=v); c.font = INPUT if ci > 1 else BODY; c.border = BOX
    ws.cell(row=i, column=2).number_format = "dd-mmm-yyyy"; ws.cell(row=i, column=4).number_format = "#,##0"; ws.cell(row=i, column=5).number_format = "0%"
red = PatternFill("solid", fgColor="F8CBAD"); amber = PatternFill("solid", fgColor="FFE699"); grey = PatternFill("solid", fgColor="E7E6E6")
ws.conditional_formatting.add("A6:F11", FormulaRule(formula=['AND($B6<DATE(2026,10,27),$C6="Unpaid")'], fill=red))
ws.conditional_formatting.add("A6:A11", FormulaRule(formula=["COUNTIF($A$6:$A$11,$A6)>1"], fill=amber, font=Font(bold=True)))
ws.conditional_formatting.add("D6:D11", DataBarRule(start_type="min", end_type="max", color="5B9BD5"))
ws.conditional_formatting.add("E6:E11", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C00000", bold=True)))
ws.conditional_formatting.add("F6:F11", ColorScaleRule(start_type="min", start_color="F8696B", mid_type="percentile", mid_value=50, mid_color="FFEB84", end_type="max", end_color="63BE7B"))
ws.conditional_formatting.add("C6:C11", IconSetRule("3Symbols", "num", [0, 0, 1], showValue=True))
ws["G6"] = 'Whole row red: =AND($B6<DATE(2026,10,27),$C6="Unpaid")  (overdue as of 27-Oct-2026)'; ws["G7"] = "Duplicate invoice IDs amber: =COUNTIF($A$6:$A$11,$A6)>1"
ws["G8"] = "Data bars on Amount"; ws["G9"] = "Negative margin red text: Cell Value < 0"; ws["G10"] = "3-colour scale on Score"
for a in ("G6", "G7", "G8", "G9", "G10"): ws[a].font = NOTE
ws["A14"] = "More custom rules to try:  zebra rows =MOD(ROW(),2)=0   ·   weekends =WEEKDAY($B6,2)>5   ·   top 10% → Top/Bottom rules"; ws["A14"].font = CODE
ws.freeze_panes = "A6"
ws["A16"] = "Freeze panes is set on this sheet (View → Freeze Panes): rows above row 6 stay visible while scrolling."; ws["A16"].font = NOTE

# ------------------------------------------------------------------ 11 Data validation
ws = sheet("11 Validation", "11 · Data validation (drop-downs and input rules)", "Click the yellow cells: each has a rule (Data → Data Validation).", [30, 22, 60])
rules = [("City (drop-down list)", "Pune", '"Mumbai,Pune,Delhi,Bengaluru,Chennai,Gurugram"', "list"),
         ("Product ID (list from a range)", "P101", "=Lookups!$A$3:$A$12", "list"),
         ("Quantity (whole number 1–50)", 2, None, "whole"), ("Order date (FY 2026-27 only)", dt.date(2026, 6, 1), None, "date"),
         ("Mobile (exactly 10 characters)", "9876543210", None, "len")]
for i, (lab, val, src, kind) in enumerate(rules, 5):
    ws[f"A{i}"] = lab; ws[f"A{i}"].font = H2; c = ws[f"B{i}"]; c.value = val; c.fill = YEL; c.font = INPUT; c.border = BOX
    if kind == "list":
        dv = DataValidation(type="list", formula1=src, allow_blank=False, showErrorMessage=True, errorTitle="Invalid", error="Pick a value from the list")
        ws[f"C{i}"] = f"List source: {src}"
    elif kind == "whole":
        dv = DataValidation(type="whole", operator="between", formula1="1", formula2="50", showErrorMessage=True, error="Enter 1 to 50"); ws[f"C{i}"] = "Whole number between 1 and 50"
    elif kind == "date":
        dv = DataValidation(type="date", operator="between", formula1="DATE(2026,4,1)", formula2="DATE(2027,3,31)", showErrorMessage=True, error="Date must be in FY 2026-27"); ws[f"C{i}"] = "Date between 01-Apr-2026 and 31-Mar-2027"; c.number_format = "dd-mmm-yyyy"
    else:
        dv = DataValidation(type="textLength", operator="equal", formula1="10", showErrorMessage=True, error="10 digits required"); ws[f"C{i}"] = "Text length = 10"
    dv.promptTitle = "Input rule"; dv.prompt = ws[f"C{i}"].value; dv.showInputMessage = True
    ws.add_data_validation(dv); dv.add(f"B{i}"); ws[f"C{i}"].font = NOTE
ws["A11"] = "Dependent drop-down idea: name each category's product list, then use =INDIRECT(B5) as the list source of the next cell."; ws["A11"].font = NOTE

# ------------------------------------------------------------------ 12 Sort & Filter
ws = sheet("12 Sort & Filter", "12 · Sorting, filters & freeze panes", "This copy of 40 orders has AutoFilter on (row 5) and frozen headers. Try: Data → Sort (City A–Z then Amount largest), filter Category = Laptops, then watch SUBTOTAL change.", [12, 13, 11, 13, 11])
header(ws, 5, ["OrderID", "OrderDate", "City", "Category", "Amount"])
for i, o in enumerate(orders[:40], 6):
    vals = [o[0], o[1], o[3], o[5], round(o[6] * o[7] * (1 - o[8]))]
    for ci, v in enumerate(vals, 1):
        c = ws.cell(row=i, column=ci, value=v); c.font = BODY
    ws.cell(row=i, column=2).number_format = "dd-mmm-yyyy"; ws.cell(row=i, column=5).number_format = "#,##0"
ws.auto_filter.ref = "A5:E45"; ws.freeze_panes = "A6"
ws["G5"] = "SUM (all rows)"; live(ws, "H5", "=SUM(E6:E45)", "#,##0"); ws["G6"] = "SUBTOTAL(109) (visible only)"; live(ws, "H6", "=SUBTOTAL(109,E6:E45)", "#,##0")
ws["G8"] = "Advanced Filter: Data → Advanced, criteria range G10:H11 (same row = AND)."; ws["G8"].font = NOTE
header(ws, 10, [None] * 6 + ["City", "Amount"]); ws["G10"] = "City"; ws["H10"] = "Amount"; ws["G11"] = "Pune"; ws["H11"] = ">20000"
ws.column_dimensions["G"].width = 28; ws.column_dimensions["H"].width = 14

# ------------------------------------------------------------------ 13 Pivot
ws = sheet("13 Pivot", "13 · Pivot tables (steps) + the same summary with formulas", "Build a real pivot from the Data sheet with the steps below. The grid on the right is a SUMIFS 'formula pivot' so you can check your numbers.", [44, 14, 14, 14, 14, 14, 14, 14])
steps = ["1. Click any cell in Data → Insert → PivotTable → New Worksheet.", "2. Rows: City. Columns: Category. Values: Sum of Amount.", "3. Value Field Settings → Number Format #,##0.",
         "4. Right-click OrderDate in Rows → Group → Months (and Years).", "5. Show Values As → % of Grand Total (or % of Row).", "6. Insert → Slicer: CustomerType; Insert → Timeline: OrderDate.",
         "7. Design → Report Layout → Tabular; Grand Totals on/off.", "8. Refresh after data changes: Alt+F5; Refresh All: Ctrl+Alt+F5.", "9. Calculated Field: Margin = Profit / Amount (PivotTable Analyze → Fields, Items & Sets)."]
for i, s in enumerate(steps, 5): ws[f"A{i}"] = s; ws[f"A{i}"].font = BODY; ws[f"A{i}"].alignment = WRAP
cats = ["Mobiles", "Laptops", "Audio", "Accessories", "TV"]; cities = [s[2] for s in stores]
header(ws, 16, ["Sum of Amount (₹)"] + cats + ["Total"])
for i, city in enumerate(cities, 17):
    text(ws, f"A{i}", city)
    for j, cat in enumerate(cats, 2):
        live(ws, f"{get_column_letter(j)}{i}", f'=SUMIFS(Data!$L$2:$L${L},Data!$D$2:$D${L},$A{i},Data!$F$2:$F${L},{get_column_letter(j)}$16)', "#,##0")
    live(ws, f"G{i}", f"=SUM(B{i}:F{i})", "#,##0")
text(ws, "A23", "Total")
for j in range(2, 8): live(ws, f"{get_column_letter(j)}23", f"=SUM({get_column_letter(j)}17:{get_column_letter(j)}22)", "#,##0")
ws["A25"] = "Excel 365 formula pivots:  =GROUPBY(Data!D2:D401, Data!L2:L401, SUM)   and   =PIVOTBY(Data!D2:D401, Data!F2:F401, Data!L2:L401, SUM)"; ws["A25"].font = CODE

# ------------------------------------------------------------------ 14 What-If
ws = sheet("14 What-If", "14 · What-if analysis: EMI, sensitivity grid, Goal Seek, break-even", "Change the blue inputs. The grid is built with formulas (a 2-variable Data Table gives the same result: Data → What-If → Data Table).", [30, 14, 14, 14, 14, 14, 14])
ws["A5"] = "Loan amount (₹)"; ws["B5"] = 1000000; ws["A6"] = "Annual rate"; ws["B6"] = 0.09; ws["A7"] = "Years"; ws["B7"] = 5
for a, b, f in (("A5", "B5", "#,##0"), ("A6", "B6", "0.00%"), ("A7", "B7", "0")):
    ws[a].font = H2; ws[b].font = INPUT; ws[b].fill = YEL; ws[b].number_format = f
ws["A8"] = "Monthly EMI"; ws["A8"].font = H2; live(ws, "B8", "=PMT(B6/12,B7*12,-B5)", "#,##0"); ws["C8"] = "=PMT(rate/12, months, -loan)"; ws["C8"].data_type = "s"; ws["C8"].font = CODE
ws["A9"] = "Total interest"; ws["A9"].font = H2; live(ws, "B9", "=B8*B7*12-B5", "#,##0")
ws["A11"] = "EMI sensitivity: rate × years"; ws["A11"].font = H2
header(ws, 12, ["Rate \\ Years", 3, 4, 5, 6, 7])
for i, rate in enumerate([0.08, 0.085, 0.09, 0.095, 0.10, 0.11], 13):
    c = ws.cell(row=i, column=1, value=rate); c.number_format = "0.0%"; c.font = INPUT; c.border = BOX
    for j in range(2, 7):
        live(ws, f"{get_column_letter(j)}{i}", f"=PMT($A{i}/12,{get_column_letter(j)}$12*12,-$B$5)", "#,##0")
ws["A20"] = "Break-even"; ws["A20"].font = H2
ws["A21"] = "Fixed cost per month (₹)"; ws["B21"] = 450000; ws["A22"] = "Price per unit (₹)"; ws["B22"] = 2999; ws["A23"] = "Variable cost per unit (₹)"; ws["B23"] = 1650
for b in ("B21", "B22", "B23"): ws[b].font = INPUT; ws[b].number_format = "#,##0"
ws["A24"] = "Break-even units"; ws["A24"].font = H2; live(ws, "B24", "=ROUNDUP(B21/(B22-B23),0)", "#,##0")
ws["A26"] = "Goal Seek: Data → What-If → Goal Seek → Set cell B8, To value 18000, By changing B7 (or B5) → finds the tenure/loan that gives ₹18,000 EMI."; ws["A26"].font = NOTE
ws["A27"] = "Scenario Manager: save Best/Base/Worst sets of B21:B23 and create a summary report. Solver (add-in): optimise with constraints."; ws["A27"].font = NOTE

# ------------------------------------------------------------------ 15 Dynamic arrays (365)
ws = sheet("15 Dynamic Arrays", "15 · Modern Excel 365 functions (type these in Excel 365)", "These functions spill results into many cells. They are shown as text with the expected result computed from the Data sheet, because they need Excel 365 / 2021+.", [22, 66, 46])
import collections
rev = collections.defaultdict(float)
for o in orders: rev[o[3]] += o[6] * o[7] * (1 - o[8])
top_city = sorted(rev.items(), key=lambda kv: -kv[1])
pune_big = sum(1 for o in orders if o[3] == "Pune" and o[6] * o[7] * (1 - o[8]) > 20000)
rows_table(ws, 5, ["Function", "Formula to type in Excel 365", "Expected result (from this data)"], [
    ("UNIQUE", "=UNIQUE(Data!D2:D401)", ", ".join(sorted(set(o[3] for o in orders)))),
    ("SORT", "=SORT(UNIQUE(Data!F2:F401))", ", ".join(sorted(set(o[5] for o in orders)))),
    ("FILTER", '=FILTER(Data!A2:L401,(Data!D2:D401="Pune")*(Data!L2:L401>20000),"None")', f"{pune_big} Pune orders above ₹20,000 (all columns)"),
    ("GROUPBY", "=GROUPBY(Data!D2:D401,Data!L2:L401,SUM,,,-2)", "; ".join(f"{c} {v:,.0f}" for c, v in top_city)),
    ("PIVOTBY", "=PIVOTBY(Data!D2:D401,Data!F2:F401,Data!L2:L401,SUM)", "City × Category revenue grid (same as sheet 13)"),
    ("TAKE + SORT", "=TAKE(SORT(Data!A2:L401,12,-1),5)", "Top 5 orders by amount"),
    ("SEQUENCE", "=SEQUENCE(12,1,DATE(2026,4,1),31)", "12 dates ~1 month apart from 01-Apr-2026"),
    ("TEXTSPLIT", '=TEXTSPLIT("NOR-1042-MUM","-")', "NOR | 1042 | MUM"),
    ("TEXTBEFORE / AFTER", '=TEXTAFTER("asha@example.com","@")', "example.com"),
    ("VSTACK", "=VSTACK(Jan!A2:E50,Feb!A2:E50)", "Two sheets appended into one list"),
    ("LET", "=LET(s,SUM(Data!L2:L401),c,SUM(Data!M2:M401),(s-c)/s)", "Overall margin % (see 18 Dashboard)"),
    ("LAMBDA (named GSTINCL)", "Name Manager: GSTINCL = LAMBDA(a,r,a*(1+r));  then =GSTINCL(2999,18%)", "3,538.82"),
    ("REGEXTEST", '=REGEXTEST("9876543210","^[6-9]\\d{9}$")', "TRUE (valid Indian mobile)"),
    ("PERCENTOF", "=PERCENTOF(SUMIFS(...),Data!L2:L401)", "Share of total"),
    ("COPILOT", '=COPILOT("Classify this review as Positive/Negative/Neutral",A2)', "AI label per row (needs Copilot licence)"),
    ("PY (Python in Excel)", '=PY(xl("Data!A1:N401",headers=True).groupby("City")["Amount"].sum())', "Python result inside a cell"),
])

# ------------------------------------------------------------------ 16 Power Query
ws = sheet("16 Power Query", "16 · Power Query: repeatable cleaning (steps)", "Do these steps on your own monthly files. Every click is recorded and replays on Refresh.", [6, 70, 50])
pq = [("Get Data → From File → From Folder → pick a folder of monthly CSVs → Combine & Transform", "One query combining every file"),
      ("Check column types (ABC/123/calendar icons); set OrderDate to Date using locale English (India) for dd-mm-yyyy", "Correct types"),
      ("Home → Remove Columns (keep only needed ones)", "Smaller, faster"),
      ("Transform → Format → Trim and Clean on text columns; Replace Values for typos", "Clean text"),
      ("Filter rows: remove blanks and test orders", "Valid rows only"),
      ("Add Column → Custom Column: [Qty] * [UnitPrice] * (1 - [Discount])", "Amount column"),
      ("Home → Merge Queries with a Products query on ProductID (Left Outer) → expand Category", "VLOOKUP replacement"),
      ("Select ID columns → Transform → Unpivot Other Columns (if months are across columns)", "Tidy long format"),
      ("Transform → Group By City: Sum of Amount", "Optional summary"),
      ("Close & Load To → Table (or Only Create Connection + Data Model)", "Output"),
      ("Next month: drop new file into the folder → Data → Refresh All", "Automation")]
header(ws, 5, ["#", "Step", "Result"])
for i, (s, rres) in enumerate(pq, 6):
    text(ws, f"A{i}", i - 5); text(ws, f"B{i}", s); text(ws, f"C{i}", rres)
ws["B18"] = 'M code example:  = Table.AddColumn(#"Changed Type", "Amount", each [Qty] * [UnitPrice] * (1 - [Discount]), type number)'; ws["B18"].font = CODE

# ------------------------------------------------------------------ 17 Charts
ws = sheet("17 Charts", "17 · Charts built from formulas (column, line, pie, combo-style)", "The tables below are live formulas on the Data sheet; the charts update when data changes.", [16, 14, 14, 14])
months = [dt.date(2026, m, 1) for m in range(4, 10)]
header(ws, 5, ["Month", "Revenue", "Profit", "Margin %"])
for i, m in enumerate(months, 6):
    c = ws.cell(row=i, column=1, value=m); c.number_format = "mmm-yy"; c.border = BOX
    live(ws, f"B{i}", f'=SUMIFS(Data!$L$2:$L${L},Data!$B$2:$B${L},">="&A{i},Data!$B$2:$B${L},"<="&EOMONTH(A{i},0))', "#,##0")
    live(ws, f"C{i}", f'=SUMIFS(Data!$N$2:$N${L},Data!$B$2:$B${L},">="&A{i},Data!$B$2:$B${L},"<="&EOMONTH(A{i},0))', "#,##0")
    live(ws, f"D{i}", f"=IF(B{i}=0,0,C{i}/B{i})", "0.0%")
header(ws, 14, ["Category", "Revenue"])
for i, cat in enumerate(cats, 15):
    text(ws, f"A{i}", cat); live(ws, f"B{i}", f'=SUMIFS(Data!$L$2:$L${L},Data!$F$2:$F${L},A{i})', "#,##0")
ch = LineChart(); ch.title = "Monthly revenue (₹)"; ch.height = 7; ch.width = 15
ch.add_data(Reference(ws, min_col=2, min_row=5, max_row=11), titles_from_data=True); ch.set_categories(Reference(ws, min_col=1, min_row=6, max_row=11)); ws.add_chart(ch, "F4")
bc = BarChart(); bc.type = "col"; bc.title = "Revenue vs profit by month"; bc.height = 7; bc.width = 15
bc.add_data(Reference(ws, min_col=2, max_col=3, min_row=5, max_row=11), titles_from_data=True); bc.set_categories(Reference(ws, min_col=1, min_row=6, max_row=11))
lc = LineChart(); lc.add_data(Reference(ws, min_col=4, min_row=5, max_row=11), titles_from_data=True); lc.y_axis.axId = 200; lc.y_axis.title = "Margin %"; lc.y_axis.crosses = "max"
bc += lc; ws.add_chart(bc, "F19")
pc = PieChart(); pc.title = "Revenue share by category"; pc.height = 7; pc.width = 12
pc.add_data(Reference(ws, min_col=2, min_row=14, max_row=19), titles_from_data=True); pc.set_categories(Reference(ws, min_col=1, min_row=15, max_row=19)); ws.add_chart(pc, "F34")

# ------------------------------------------------------------------ 18 Dashboard case study
ws = sheet("18 Dashboard Case Study", "18 · Case study: monthly sales dashboard for a 6-store electronics chain", "Scenario: the regional manager wants a one-page review. Pick the month in B5 (blue). Every number below is a live formula on the Data sheet (sample data).", [26, 16, 16, 16, 16, 16, 16])
ws["A5"] = "Month (first day)"; ws["A5"].font = H2; ws["B5"] = dt.date(2026, 9, 1); ws["B5"].font = INPUT; ws["B5"].fill = YEL; ws["B5"].number_format = "mmm-yyyy"
dvm = DataValidation(type="list", formula1="'17 Charts'!$A$6:$A$11", showErrorMessage=True); ws.add_data_validation(dvm); dvm.add("B5")
crit = f'Data!$B$2:$B${L},">="&$B$5,Data!$B$2:$B${L},"<="&EOMONTH($B$5,0)'
critp = f'Data!$B$2:$B${L},">="&EDATE($B$5,-1),Data!$B$2:$B${L},"<="&EOMONTH($B$5,-1)'
header(ws, 7, ["KPI", "This month", "Last month", "Change %"])
kpis = [("Revenue (₹)", f"=SUMIFS(Data!$L$2:$L${L},{crit})", f"=SUMIFS(Data!$L$2:$L${L},{critp})", "#,##0"),
        ("Orders", f"=COUNTIFS({crit})", f"=COUNTIFS({critp})", "#,##0"),
        ("Avg order value (₹)", "=IFERROR(B8/B9,0)", "=IFERROR(C8/C9,0)", "#,##0"),
        ("Profit (₹)", f"=SUMIFS(Data!$N$2:$N${L},{crit})", f"=SUMIFS(Data!$N$2:$N${L},{critp})", "#,##0"),
        ("Margin %", "=IFERROR(B11/B8,0)", "=IFERROR(C11/C8,0)", "0.0%"),
        ("Warranty attach rate", f'=IFERROR(COUNTIFS({crit},Data!$K$2:$K${L},"Yes")/B9,0)', f'=IFERROR(COUNTIFS({critp},Data!$K$2:$K${L},"Yes")/C9,0)', "0.0%")]
for i, (k, f1, f2, fm) in enumerate(kpis, 8):
    text(ws, f"A{i}", k); live(ws, f"B{i}", f1, fm); live(ws, f"C{i}", f2, fm); live(ws, f"D{i}", f"=IFERROR(B{i}/C{i}-1,0)", '[Color10]▲0.0%;[Red]▼0.0%;0.0%')
header(ws, 15, ["Store league", "Revenue", "Orders", "AOV", "Rank", "Share %"])
for i, s in enumerate(stores, 16):
    text(ws, f"A{i}", f"{s[0]} {s[1]}, {s[2]}")
    live(ws, f"B{i}", f'=SUMIFS(Data!$L$2:$L${L},Data!$C$2:$C${L},"{s[0]}",{crit})', "#,##0")
    live(ws, f"C{i}", f'=COUNTIFS(Data!$C$2:$C${L},"{s[0]}",{crit})', "#,##0")
    live(ws, f"D{i}", f"=IFERROR(B{i}/C{i},0)", "#,##0"); live(ws, f"E{i}", f"=_xlfn.RANK.EQ(B{i},$B$16:$B$21)", "0"); live(ws, f"F{i}", f"=IFERROR(B{i}/SUM($B$16:$B$21),0)", "0.0%")
ws.conditional_formatting.add("B16:B21", DataBarRule(start_type="num", start_value=0, end_type="max", color="5B9BD5"))
ws.conditional_formatting.add("E16:E21", CellIsRule(operator="equal", formula=["1"], fill=PatternFill("solid", fgColor="C6EFCE"), font=Font(bold=True)))
header(ws, 23, ["Category", "Revenue", "Profit", "Margin %"])
for i, cat in enumerate(cats, 24):
    text(ws, f"A{i}", cat)
    live(ws, f"B{i}", f'=SUMIFS(Data!$L$2:$L${L},Data!$F$2:$F${L},A{i},{crit})', "#,##0"); live(ws, f"C{i}", f'=SUMIFS(Data!$N$2:$N${L},Data!$F$2:$F${L},A{i},{crit})', "#,##0")
    live(ws, f"D{i}", f"=IFERROR(C{i}/B{i},0)", "0.0%")
ws.conditional_formatting.add("D24:D28", ColorScaleRule(start_type="min", start_color="F8696B", end_type="max", end_color="63BE7B"))
ws["A30"] = "Headline (auto):"; ws["A30"].font = H2
ws["B30"] = '="Revenue "&TEXT(B8,"₹#,##0")&" ("&TEXT(D8,"+0.0%;-0.0%")&" vs last month). Top store: "&INDEX(A16:A21,MATCH(1,E16:E21,0))&"."'
ws["B30"].font = Font(name=F, bold=True, color=NAVY); ws.merge_cells("B30:G30")
b2 = BarChart(); b2.type = "bar"; b2.title = "Store revenue this month"; b2.height = 7; b2.width = 13
b2.add_data(Reference(ws, min_col=2, min_row=15, max_row=21), titles_from_data=True); b2.set_categories(Reference(ws, min_col=1, min_row=16, max_row=21)); b2.legend = None; ws.add_chart(b2, "I7")
p2 = PieChart(); p2.title = "Category mix"; p2.height = 7; p2.width = 10
p2.add_data(Reference(ws, min_col=2, min_row=23, max_row=28), titles_from_data=True); p2.set_categories(Reference(ws, min_col=1, min_row=24, max_row=28)); ws.add_chart(p2, "I22")
ws["A33"] = "Questions this dashboard answers: Which store leads? Is revenue growing month on month? Which categories earn the best margin? Is warranty attachment improving?"; ws["A33"].font = NOTE

# ------------------------------------------------------------------ 19 Automation & AI
ws = sheet("19 Automation & AI", "19 · Automation & AI in Excel", "Copy these into Excel to try them. VBA needs the file saved as .xlsm; Copilot features need a Microsoft 365 Copilot licence.", [28, 90])
items = [("Record a macro", "View → Macros → Record Macro → do the steps → Stop. Edit with Alt+F11."),
         ("VBA: format every sheet", "Sub FormatAll()\n  Dim ws As Worksheet\n  For Each ws In ThisWorkbook.Worksheets\n    ws.Rows(1).Font.Bold = True\n    ws.Columns.AutoFit\n  Next ws\nEnd Sub"),
         ("VBA: export each sheet to PDF", "Sub ExportPDFs()\n  Dim ws As Worksheet\n  For Each ws In ThisWorkbook.Worksheets\n    ws.ExportAsFixedFormat xlTypePDF, ThisWorkbook.Path & \"\\\" & ws.Name & \".pdf\"\n  Next ws\nEnd Sub"),
         ("Office Script + Power Automate", "Excel for the web → Automate → Record Actions; then in Power Automate: Recurrence (Monday 9:00) → Run script → Send email with the file."),
         ("Copilot prompts", "• \"Add a column for profit margin and highlight negatives\"\n• \"Create a PivotTable of revenue by City and Category\"\n• \"Explain the formula in B30 of the dashboard\"\n• \"What are the top 3 insights in this data?\""),
         ("COPILOT function", "=COPILOT(\"Classify this customer review as Positive, Negative or Neutral\", C2)"),
         ("Python in Excel", "=PY(xl(\"Data!A1:N401\", headers=True).groupby(\"City\")[\"Amount\"].sum())"),
         ("External AI (ChatGPT / Claude / Gemini)", "\"My sheet has columns OrderDate (B), City (D), Amount (L). Write one Excel formula for revenue in Pune for the month in cell B5.\" → test on a few rows you can check by hand.")]
header(ws, 5, ["Technique", "How / code"])
for i, (a, b) in enumerate(items, 6):
    text(ws, f"A{i}", a); c = text(ws, f"B{i}", b, CODE if "\n" in b or b.startswith("=") else BODY)
    ws.row_dimensions[i].height = max(18, 15 * (b.count("\n") + 1))

# ------------------------------------------------------------------ index entries + order
order = ["00 Index", "01 Environment", "02 References", "03 Custom Formats", "04 Number", "05 Text", "06 Date & Time", "07 Aggregate", "08 Logical", "09 Lookup",
         "10 Conditional Formatting", "11 Validation", "12 Sort & Filter", "13 Pivot", "14 What-If", "15 Dynamic Arrays", "16 Power Query", "17 Charts",
         "18 Dashboard Case Study", "19 Automation & AI", "Data", "Lookups"]
desc = {"01 Environment": ("Workbook terms and 24 essential shortcuts", "Basic"), "02 References": ("Relative, absolute, mixed references; GST example; multiplication grid", "Basic"),
        "03 Custom Formats": ("12 custom number formats incl. Indian lakh, ▲▼, k/M", "Basic"), "04 Number": ("ROUND, ROUNDUP, INT, MOD, ABS, CEILING, SUMPRODUCT…", "Basic"),
        "05 Text": ("TRIM, PROPER, LEFT/RIGHT/MID, FIND, SUBSTITUTE, TEXTJOIN, masking", "Basic"), "06 Date & Time": ("EOMONTH, EDATE, NETWORKDAYS, WORKDAY, DATEDIF, FY & quarter", "Basic"),
        "07 Aggregate": ("SUM…STDEV, SUMIFS/COUNTIFS/AVERAGEIFS/MAXIFS, SUBTOTAL, conditional probability", "Intermediate"),
        "08 Logical": ("IF, nested IF, IFS, SWITCH, AND/OR/NOT, IFERROR, IFNA", "Intermediate"), "09 Lookup": ("VLOOKUP, INDEX/MATCH, CHOOSE, HLOOKUP, slabs, XLOOKUP", "Intermediate"),
        "10 Conditional Formatting": ("Overdue rows, duplicates, data bars, colour scales, icons; freeze panes", "Intermediate"),
        "11 Validation": ("Drop-down lists, number/date/length rules, input messages", "Intermediate"), "12 Sort & Filter": ("AutoFilter, multi-level sort, SUBTOTAL, advanced filter", "Intermediate"),
        "13 Pivot": ("Pivot steps + SUMIFS formula pivot to check results", "Advanced"), "14 What-If": ("PMT/EMI, sensitivity grid, break-even, Goal Seek, scenarios", "Advanced"),
        "15 Dynamic Arrays": ("UNIQUE, SORT, FILTER, GROUPBY, PIVOTBY, LET, LAMBDA, REGEX, COPILOT, PY", "Advanced (365)"),
        "16 Power Query": ("11-step repeatable cleaning recipe + M code", "Advanced"), "17 Charts": ("Line, combo (dual axis) and pie charts from live formulas", "Intermediate"),
        "18 Dashboard Case Study": ("Real-world monthly dashboard: KPIs vs last month, store league, category margins, auto headline", "Case study"),
        "19 Automation & AI": ("Macros/VBA, Office Scripts, Power Automate, Copilot, Python in Excel", "Advanced"), "Data": ("400 sample orders (generated)", "Data"),
        "Lookups": ("Products, stores, commission slabs, holidays", "Data")}
wb._sheets = [wb[n] for n in order]
for i, n in enumerate(order[1:], 5):
    idx.cell(row=i, column=1, value=i - 4).font = BODY
    c = idx.cell(row=i, column=2, value=n); c.hyperlink = f"#'{n}'!A1"; c.font = LINK
    idx.cell(row=i, column=3, value=desc[n][0]).font = BODY; idx.cell(row=i, column=4, value=desc[n][1]).font = BODY
idx["A28"] = "Sources for 2025–26 features: Microsoft Excel blog; Excel Campus '17 New Excel Updates from 2025'. Sample data is fictional."; idx["A28"].font = NOTE
wb.active = 0
for wsx in wb.worksheets:
    for row in wsx.iter_rows():
        for c in row:
            if c.font and c.font.name != F and c.font.name != "Consolas":
                c.font = Font(name=F, size=c.font.size, bold=c.font.bold, italic=c.font.italic, color=c.font.color, underline=c.font.underline)
from openpyxl.workbook.properties import CalcProperties
wb.calculation = CalcProperties(fullCalcOnLoad=True)
wb.save(OUT); print("saved", OUT)
