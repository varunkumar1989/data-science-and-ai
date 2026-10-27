"""Render all Mermaid diagrams to PNG (white background) for the site and PDFs."""
import os, subprocess, json, concurrent.futures as cf
DS = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DS, "site", "img", "dg"); SRC = os.path.join(DS, "mmd")
os.makedirs(OUT, exist_ok=True); os.makedirs(SRC, exist_ok=True)
CFG = {"theme": "base", "themeVariables": {"primaryColor": "#E8EEF9", "primaryBorderColor": "#1F3864", "primaryTextColor": "#18213A",
       "lineColor": "#2C4C86", "secondaryColor": "#FDF3E1", "tertiaryColor": "#E5F3F3", "fontFamily": "Inter, Arial, sans-serif", "fontSize": "15px"},
       "flowchart": {"curve": "basis", "padding": 14}}
D = {}

D["ds_lifecycle"] = """flowchart LR
  A([Business question]) --> B[Collect data<br/>Excel · SQL · APIs]
  B --> C[Clean & prepare<br/>Power Query · pandas]
  C --> D[Explore & visualise<br/>pivots · charts · EDA]
  D --> E[Model & predict<br/>statistics · ML]
  E --> F[Communicate<br/>Power BI · Tableau · story]
  F --> G([Decision & action])
  G -. new questions .-> A
  classDef s fill:#1F3864,color:#fff,stroke:#1F3864
  class A,G s"""

D["excel_terms"] = """flowchart TB
  WB[Workbook .xlsx<br/>the file] --> WS1[Worksheet: Sales]
  WB --> WS2[Worksheet: Targets]
  WS1 --> R[Rows 1..1,048,576]
  WS1 --> C[Columns A..XFD 16,384]
  R --> CELL[Cell B7<br/>column B + row 7]
  C --> CELL
  CELL --> V[Value: 1250]
  CELL --> F[Formula: =C7*D7]
  CELL --> FMT[Format: ₹#,##0]
  WS1 --> RNG[Range A1:D20<br/>block of cells]
  RNG --> TBL[Table: Ctrl+T<br/>auto-expanding, named]"""

D["excel_formula_anatomy"] = """flowchart LR
  EQ["="] --> FN["Function name<br/>VLOOKUP"]
  FN --> P["( arguments )"]
  P --> A1["lookup value<br/>A2"]
  P --> A2["table<br/>$F$2:$H$50"]
  P --> A3["column no.<br/>3"]
  P --> A4["exact match<br/>FALSE"]
  classDef k fill:#E9A23B,color:#1A1406,stroke:#C9831B
  class EQ k"""

D["rdbms_stack"] = """flowchart TB
  U1[Analyst in SSMS] --> SRV
  U2[Power BI report] --> SRV
  U3[Python script] --> SRV
  subgraph SRV[Database SERVER  e.g. SQL Server instance]
    direction TB
    DBMS[RDBMS software<br/>query engine · security · storage]
    DBMS --> DB1[(Database: RetailDB)]
    DBMS --> DB2[(Database: HRDB)]
    DB1 --> T1[Table: Customer]
    DB1 --> T2[Table: Orders]
    DB1 --> T3[Table: Product]
  end"""

D["er_retail"] = """erDiagram
  CUSTOMER ||--o{ ORDERS : places
  ORDERS ||--|{ ORDER_ITEM : contains
  PRODUCT ||--o{ ORDER_ITEM : "appears in"
  CATEGORY ||--o{ PRODUCT : groups
  CUSTOMER {
    int customer_id PK
    varchar name
    char gender
    varchar city
    date dob
  }
  ORDERS {
    int order_id PK
    int customer_id FK
    date order_date
    varchar store_type
  }
  ORDER_ITEM {
    int order_id PK,FK
    int line_no PK
    int product_id FK
    int qty
    decimal price
  }
  PRODUCT {
    int product_id PK
    varchar product_name
    int category_id FK
  }
  CATEGORY {
    int category_id PK
    varchar category_name
  }"""

D["sql_families"] = """flowchart LR
  SQL((SQL)) --> DDL[DDL<br/>CREATE · ALTER<br/>DROP · TRUNCATE]
  SQL --> DML[DML<br/>INSERT · UPDATE<br/>DELETE · MERGE]
  SQL --> DQL[DQL<br/>SELECT]
  SQL --> DCL[DCL<br/>GRANT · REVOKE]
  SQL --> TCL[TCL<br/>COMMIT · ROLLBACK<br/>SAVEPOINT]"""

D["sql_order"] = """flowchart LR
  F[1 FROM / JOIN] --> W[2 WHERE] --> G[3 GROUP BY] --> H[4 HAVING] --> S[5 SELECT] --> D[6 DISTINCT] --> O[7 ORDER BY] --> T[8 TOP / OFFSET]
  classDef a fill:#FDF3E1,stroke:#E9A23B
  class S a"""

D["joins"] = """flowchart TB
  subgraph J[Which join?]
    direction LR
    I[INNER JOIN<br/>only matching rows]
    L[LEFT JOIN<br/>all left + matches<br/>NULL when no match]
    R[RIGHT JOIN<br/>all right + matches]
    FO[FULL OUTER JOIN<br/>everything from both]
    C[CROSS JOIN<br/>every combination<br/>rows A × rows B]
    S[SELF JOIN<br/>table joined to itself<br/>employee → manager]
  end"""

D["set_ops"] = """flowchart LR
  A[(2023 customers)] --> U[UNION<br/>both, no duplicates]
  B[(2024 customers)] --> U
  A --> UA[UNION ALL<br/>both, keeps duplicates]
  B --> UA
  A --> IN[INTERSECT<br/>in both years]
  B --> IN
  A --> EX[EXCEPT<br/>2023 but not 2024 = churned]
  B --> EX"""

D["ssms_import"] = """flowchart LR
  A[Install SQL Server<br/>Developer / Express] --> B[Install SSMS]
  B --> C[Connect: server name,<br/>Windows authentication]
  C --> D[New Query → CREATE DATABASE]
  D --> E[Right-click DB → Tasks →<br/>Import Flat File]
  E --> F[Preview → Modify columns<br/>types, keys, nulls]
  F --> G[Finish → SELECT TOP 100 *]"""

D["compiler_interpreter"] = """flowchart TB
  subgraph CO[Compiler: C, C++, Java→bytecode]
    direction LR
    S1[Whole source code] --> CC[Compiler] --> EXE[Machine-code program] --> RUN1[Runs fast, many times]
  end
  subgraph IN[Interpreter: Python, R, JavaScript]
    direction LR
    S2[Source line 1, 2, 3...] --> II[Interpreter<br/>translates + runs<br/>line by line] --> RUN2[Results immediately<br/>stops at first error]
  end"""

D["lang_levels"] = """flowchart TB
  H[High-level languages<br/>Python · SQL · R · Java<br/>English-like, portable] --> M[Assembly language<br/>MOV, ADD<br/>CPU-specific mnemonics]
  M --> L[Machine code<br/>0101 1100<br/>what the CPU executes]
  H -. translated by compiler / interpreter .-> L"""

D["control_flow"] = """flowchart TD
  S([Start: read order]) --> Q{Amount > 5,000?}
  Q -- Yes --> D1[Discount = 10%]
  Q -- No --> Q2{Prime member?}
  Q2 -- Yes --> D2[Discount = 5%]
  Q2 -- No --> D3[Discount = 0]
  D1 --> P["Final = Amount × (1 − Discount)"]
  D2 --> P
  D3 --> P
  P --> M{More orders?}
  M -- Yes --> S
  M -- No --> E([End: print total])"""

D["stats_map"] = """flowchart TB
  ST((Statistics)) --> DE[Descriptive<br/>summarise what happened]
  ST --> INF[Inferential<br/>generalise from a sample]
  DE --> CT[Central tendency<br/>mean · median · mode]
  DE --> SP[Spread<br/>range · IQR · variance · SD]
  DE --> SH[Shape<br/>skewness · kurtosis]
  DE --> VIS[Visuals<br/>histogram · box plot]
  INF --> PR[Probability &<br/>distributions]
  INF --> SA[Sampling &<br/>CLT]
  INF --> CI[Confidence<br/>intervals]
  INF --> HT[Hypothesis<br/>tests]
  INF --> RE[Correlation &<br/>regression]"""

D["sampling"] = """flowchart LR
  P[(Population<br/>all customers)] --> SRS[Simple random<br/>every member equal chance]
  P --> STR[Stratified<br/>sample within each city]
  P --> CL[Cluster<br/>pick whole stores at random]
  P --> SYS[Systematic<br/>every 10th invoice]
  P --> CON[Convenience<br/>whoever is easy: biased!]"""

D["maths_ml"] = """flowchart LR
  LA[Linear algebra<br/>vectors · matrices] --> DATA[Represent data<br/>X = rows × features]
  CA[Calculus<br/>derivatives · gradients] --> OPT[Optimise<br/>gradient descent]
  PR[Probability<br/>Bayes · distributions] --> UNC[Quantify uncertainty<br/>probabilities, p-values]
  DATA --> ML[[Machine learning model]]
  OPT --> ML
  UNC --> ML"""

D["automation_ladder"] = """flowchart LR
  L0[Manual<br/>copy-paste] --> L1[Formulas &<br/>Tables]
  L1 --> L2[Power Query<br/>refreshable ETL]
  L2 --> L3[Macros / Office Scripts<br/>+ Power Automate]
  L3 --> L4[SQL jobs, views,<br/>stored procedures]
  L4 --> L5[Python pipelines<br/>scheduled]
  L5 --> L6[BI refresh + alerts<br/>Power BI · Tableau]
  L6 --> L7[ML / AI agents<br/>predict & act]"""

D["automation_pipeline"] = """flowchart LR
  SRC[(Sources<br/>ERP · CRM · CSV · API)] --> ING[Ingest<br/>Python / Power Query]
  ING --> DB[(SQL warehouse<br/>staging → clean tables)]
  DB --> TR[Transform<br/>views · stored procs]
  TR --> BI[Power BI / Tableau<br/>scheduled refresh]
  TR --> MLM[ML model<br/>daily scoring]
  MLM --> DB
  BI --> AL[Alerts & subscriptions<br/>email · Teams]
  SCH{{Scheduler<br/>SQL Agent · Task Scheduler<br/>Airflow · Power Automate}} -.-> ING
  SCH -.-> TR
  SCH -.-> MLM"""

D["ai_family"] = """flowchart TB
  AI[Artificial Intelligence<br/>machines doing tasks that need intelligence] --> ML[Machine Learning<br/>learns patterns from data]
  ML --> DL[Deep Learning<br/>multi-layer neural networks]
  DL --> GEN[Generative AI<br/>creates text, images, code]
  GEN --> LLM[Large Language Models<br/>ChatGPT · Claude · Gemini]
  LLM --> AG[Agentic AI<br/>plans + uses tools + acts]"""

D["llm_flow"] = """flowchart LR
  P[Prompt] --> T[Tokenise<br/>text → tokens]
  T --> TF[Transformer<br/>attention over context]
  TF --> PR[Probabilities for<br/>next token]
  PR --> S[Sample one token<br/>temperature]
  S --> A[Append to answer]
  A -->|repeat until done| TF"""

D["rag"] = """flowchart LR
  Q[User question] --> E[Embed question]
  DOCS[(Company documents)] --> CH[Chunk + embed] --> VDB[(Vector database)]
  E --> SR[Similarity search]
  VDB --> SR
  SR --> CTX[Top-k relevant chunks]
  CTX --> LLM[LLM: answer using<br/>ONLY these chunks]
  Q --> LLM
  LLM --> ANS[Grounded answer<br/>+ citations]"""

D["agent_loop"] = """flowchart TD
  G([Goal: 'Prepare weekly sales report']) --> PL[Plan steps]
  PL --> ACT[Act with a tool<br/>SQL · Python · Excel · email]
  ACT --> OBS[Observe result]
  OBS --> RF{Goal met?}
  RF -- No: adjust plan --> PL
  RF -- Yes --> OUT([Deliver report + summary])
  MEM[(Memory / context)] -.-> PL
  HUM[Human approval<br/>for risky actions] -.-> ACT"""

D["ml_types"] = """flowchart TB
  ML((Machine learning)) --> SUP[Supervised<br/>has the answer column]
  ML --> UNS[Unsupervised<br/>no answer column]
  ML --> RL[Reinforcement<br/>learns by reward]
  SUP --> REG[Regression<br/>predict a number<br/>sales next month]
  SUP --> CLS[Classification<br/>predict a category<br/>will customer churn?]
  UNS --> CLU[Clustering<br/>customer segments]
  UNS --> DR[Dimension reduction<br/>PCA]
  UNS --> AS[Association<br/>bread → butter]"""

D["ml_workflow"] = """flowchart LR
  A[Define problem<br/>+ target y] --> B[Get data] --> C[Clean & EDA] --> D[Feature<br/>engineering]
  D --> E[Split<br/>train / test] --> F[Train models] --> G[Tune<br/>cross-validation] --> H[Evaluate on test]
  H --> I[Deploy] --> J[Monitor & retrain]
  J -.-> B"""

D["powerbi_arch"] = """flowchart LR
  S[(Excel · SQL · SharePoint<br/>APIs · Fabric)] --> PQ[Power Query<br/>clean & shape]
  PQ --> MOD[Data model<br/>star schema + DAX]
  MOD --> REP[Report<br/>visuals · slicers]
  REP --> PUB[Publish to<br/>Power BI Service]
  PUB --> DSH[Dashboards · Apps<br/>refresh · RLS · alerts]
  PUB --> CP[Copilot<br/>summaries · Q&A]"""

D["tableau_flow"] = """flowchart LR
  C[Connect<br/>file · DB · cloud] --> DS[Data source<br/>relationships · extract]
  DS --> WS[Worksheet<br/>shelves · Marks card]
  WS --> CALC[Calculations<br/>row · aggregate · table calc · LOD]
  CALC --> DB[Dashboard<br/>actions · filters]
  DB --> ST[Story]
  DB --> PUB[Publish<br/>Tableau Cloud / Server / Public]
  PUB --> PUL[Pulse & Agent<br/>AI metrics · Q&A]"""

D["python_ecosystem"] = """flowchart TB
  PY((Python)) --> CORE[Core language<br/>variables · loops · functions]
  PY --> NP[NumPy<br/>fast arrays & maths]
  NP --> PD[pandas<br/>tables: clean · join · group]
  PD --> VIZ[matplotlib · seaborn · plotly<br/>charts]
  PD --> SK[scikit-learn<br/>machine learning]
  PD --> ST[scipy · statsmodels<br/>statistics]
  SK --> DLB[TensorFlow · PyTorch<br/>deep learning]
  PY --> AUT[openpyxl · requests · schedule<br/>automation]
  PY --> APP[Flask · Streamlit<br/>apps & APIs]"""

D["reverse_eng"] = """flowchart LR
  O[Finished output<br/>dashboard · report · model · formula] --> OBS[1 Observe<br/>what does it show?]
  OBS --> DEC[2 Decompose<br/>into parts]
  DEC --> TR[3 Trace each part<br/>back to data + logic]
  TR --> RB[4 Rebuild<br/>small version yourself]
  RB --> CMP[5 Compare<br/>numbers match?]
  CMP --> DOC[6 Document &<br/>improve]"""

D["interview_flow"] = """flowchart LR
  R[Resume + portfolio<br/>3 projects] --> SC[Screening call] --> T[Technical test<br/>SQL · Excel · Python]
  T --> CS[Case study /<br/>take-home]
  CS --> HM[Hiring manager<br/>business + stats]
  HM --> HR[HR & offer]"""

D["tools_map"] = """flowchart TB
  T((AI tools for<br/>data work)) --> CH[Chat assistants<br/>ChatGPT · Claude · Gemini · Grok · Copilot]
  T --> RS[Research & search<br/>Perplexity · NotebookLM · Gemini Deep Research]
  T --> CO[Coding<br/>GitHub Copilot · Cursor · Claude Code · Colab AI]
  T --> AN[Analysis<br/>ChatGPT data analysis · Julius · Copilot in Excel]
  T --> BI[BI copilots<br/>Power BI Copilot · Tableau Agent · Gemini in Sheets]
  T --> BU[Build apps<br/>Lovable · Bolt · v0 · Replit]
  T --> AU[Automate<br/>Power Automate · Zapier · Make · n8n]"""

def render(name):
    src = os.path.join(SRC, name + ".mmd"); open(src, "w").write(D[name])
    cfg = os.path.join(SRC, "cfg.json")
    r = subprocess.run(["mmdc", "-i", src, "-o", os.path.join(OUT, name + ".png"), "-b", "white", "-s", "2", "-c", cfg, "-w", "1200"],
                       capture_output=True, text=True, timeout=180)
    return name, r.returncode, (r.stderr or "")[-300:]

if __name__ == "__main__":
    json.dump(CFG, open(os.path.join(SRC, "cfg.json"), "w"))
    with cf.ThreadPoolExecutor(4) as ex:
        for name, rc, err in ex.map(render, list(D)):
            print(name, "OK" if rc == 0 else "FAIL " + err)
