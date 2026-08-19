# Day 49: Accessing Columns in Pandas (+ a Map of Data Science & ML)

> **Prerequisite:** Day 48 (Understanding & Exploring Our Data). Companion practice file: `203_Accessing_columns.py` — run it, then compare its output with the blocks below.
>
> Everything below uses the same real `grocery_database.xlsx` file from Day 48 (the `transactions` sheet: **38,506 rows × 6 columns**: `customer_id`, `transaction_date`, `transaction_id`, `product_area_id`, `num_items`, `sales_cost`).

Day 48 was about **understanding a whole table**. Day 49 answers the next question an analyst always asks:

> **"How do I pull out just the part I need — one column, a few columns, the columns *not* in a list — and in a form Python can actually use for math or a model?"**

That skill is called **column selection** (or **column subsetting**). It looks small, but it is one of the most-handled lines of code in the entire data job, and it contains the single most common beginner "gotcha" in pandas — the difference between a **Series** and a **DataFrame**.

---

## 1. The Big Idea: Two Objects, Easy to Confuse

Every column operation in pandas returns one of two things, and **which one** changes everything about what you can do next:

| Method | What it returns | Dimension | Analogy |
| --- | --- | --- | --- |
| `df["col"]` | a **Series** | 1D (one column) | a single column pulled out on its own |
| `df[["col"]]` | a **DataFrame** | 2D (one *or more* columns) | a smaller table made of chosen columns |

The **only visual difference** in the code is **one extra set of square brackets**. That one bracket is the most-missed detail in all of pandas, so let's nail it down before we go anywhere:

```python
single = transactions["sales_cost"]      # a Series (1D)
as_table = transactions[["sales_cost"]]  # a DataFrame (2D) — SAME column, wrapped
```

You can always **verify** which you have:

```python
type(single)    # <class 'pandas.core.series.Series'>
type(as_table)  # <class 'pandas.core.frame.DataFrame'>
single.ndim     # 1
as_table.ndim   # 2
```

**Why the distinction matters in practice:**

| Operation | On a **Series** (`df["x"]`) | On a **DataFrame** (`df[["x"]]`) |
| --- | --- | --- |
| `mean()` | average of that column ✓ | averages **every** column in it (returns a Series of means) |
| `.dropna()` | drops missing **values** within the column | drops any **row** that has a missing value in any selected column |
| `.sum()` | total of that column | one total **per selected column** |
| Feeding to a model | a single feature (a vector) | a **feature matrix** (X) — usually what you actually want |

> **Rule of thumb:** when you're doing *analysis* on one column, a **Series** is fine (it's lighter). When you're building *a set of columns to pass into something else* (a plot, a model, an export), use the **double-bracket DataFrame** form.

---

## 2. The Script, Line by Line (Beginner-Friendly)

Here is `203_Accessing_columns.py` walked through:

### 2.1 Load

```python
import pandas as pd
transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")
```

Same as Day 48: 38,506 rows × 6 columns in memory, ready for column operations.

### 2.2 `info()` — a quick glance at the cols

```python
transactions.info()
```

`info()` prints, for **every column at once**: its **name**, its **data type** (`int64`, `datetime64[us]`, `float64`, `object`…), and how many **non-null** values it has. It's the fastest single call to answer "what columns do I even have, and what type is each?" (You used `dtypes` in Day 48; `info()` is `dtypes` + missing counts + total memory in one printout.)

### 2.3 Method 1 — dot notation: `transactions.customer_id`

```python
new_df = transactions.customer_id        # selects ONE column -> a Series
```

This is **attribute access** — the same syntax as `transactions.shape` or `df.head()`. pandas looks for an attribute named `customer_id` and, because that is a column name, hands you that column **as a Series**.

> **SQL equivalent:** `SELECT customer_id FROM transactions`

**When dot notation works (and when it *doesn't*):**

| Column name | Dot notation `df.name`? | Why |
| --- | --- | --- |
| `customer_id` | ✅ works | valid Python identifier (underscores are fine) |
| `sales_cost` | ✅ works | valid identifier |
| `first name` | ❌ **fails** | contains a space → not a legal name |
| `2020_sales` | ❌ **fails** | starts with a digit → not a legal name |
| `index` | ❌ **dangerous** | collides with the built-in `df.index` method/property |
| `mean` / `sum` | ❌ **dangerous** | collides with built-in DataFrame methods |

So dot notation is **shorthand that only works for "clean" column names**. If your column has a space, a dash, a leading number, or a name that collides with a pandas method, you **must** use the bracket form in the next line.

### 2.4 Method 2 — single brackets: `transactions["customer_id"]`

```python
new_df = transactions["customer_id"]     # selects ONE column -> a Series
```

This is the **universal** way to select a **single** column. It works for **any** column name — spaces, dashes, leading numbers, even ones that collide with method names.

> **SQL equivalent:** `SELECT customer_id FROM transactions`

When in doubt, **use single brackets**: `df["customer_id"]`. It is the safest, most general, most "correct" habit. (Dot notation is just a shorter sugar for clean names.)

### 2.5 The single-bracket **vs** double-bracket gotcha

```python
new_df = transactions[["customer_id"]]   # SAME column, but now a 2D DataFrame
```

Notice the **double square brackets**: `[[ ... ]]`. The *inner* `[...]` is a **list** containing one column name. Because a list is being selected, pandas returns a **DataFrame** (a table) rather than a Series (a column).

| Code | Returns | `ndim` |
| --- | --- | --- |
| `transactions["customer_id"]` | Series | 1 |
| `transactions[["customer_id"]]` | DataFrame | 2 |

**Why would you ever *want* the DataFrame form for a single column?** Because some operations expect a *table*, not a bare column — e.g. `pd.concat` to stack tables, or passing a one-column feature **matrix** to a model. A Series is a *vector*; a one-column DataFrame is a *matrix with one feature*.

### 2.6 Selecting **multiple** columns

```python
new_df_2cols = transactions[["customer_id", "sales_cost"]]   # a 2-column DataFrame
```

This is the **workhorse** of column selection in real work: you pick exactly **the columns you care about** and drop the rest into a smaller, focused table.

> **SQL equivalent:** `SELECT customer_id, sales_cost FROM transactions`

On *this* data, this 2-column frame is already a mini-analysis table: *"for each line-item, who bought it and how much did it cost."*

---

## 3. The Full Toolkit for Accessing Columns

The script used three methods; here are **all** the tools you'll reach for, grouped by *what you're trying to pick*:

### 3.1 By **name**

```python
df["col"]                 # one column -> Series
df.col                    # one column -> Series  (clean names only)
df[["a", "b"]]            # several columns -> DataFrame
df[["a"]]                 # ONE column, but as a DataFrame
df.get("col")             # like df["col"], but returns None if the column is missing (no crash)
df.loc[:, "col"]          # label-based select; the `:` means "all rows"
```

### 3.2 By **position** (index number)

```python
df.iloc[:, 0]             # first column -> Series        (0-based)
df.iloc[:, [0, 1]]        # first two columns -> DataFrame
```

`iloc` is **position-based** (like a Python list). Use it when you don't know / don't care about the column *name*, only its **order**.

### 3.3 By **label range**

```python
df.loc[:, "customer_id":"product_area_id"]   # all columns FROM customer_id TO product_area_id (inclusive)
df.iloc[:, 1:4]                              # columns positions 1,2,3 (4 excluded — Python slicing)
```

### 3.4 By **pattern** (partial text or regex) or **type**

```python
df.filter(like="cost")            # columns whose name CONTAINS "cost"
df.filter(regex="^sales")         # columns whose name STARTS WITH "sales"
df.columns.to_series().str.contains("id").pipe(df.filter)   # any column containing "id"
df.select_dtypes(include=["int64"])   # all INTEGER columns
df.select_dtypes(include=["number"])  # all numeric (int + float)
df.select_dtypes(exclude=["object"])  # everything EXCEPT text
```

`select_dtypes` is a **superpower for feature engineering** — it lets you grab "all my numeric features" or "all my text columns to encode" in one line.

### 3.5 All columns **except** a few

A very common need: "I want everything *except* the IDs and the date."

```python
# the negative of "columns that are IN this list"
ids_to_skip = ["customer_id", "transaction_id", "transaction_date"]
features = transactions[~transactions.columns.isin(ids_to_skip)]
# -> product_area_id, num_items, sales_cost
```

`~` is the **NOT** operator applied to a boolean array of column names. (You'll meet `~` again for row filtering in Day 48/46: `df[~(df.x == 1)]`.)

### 3.6 Creating, renaming, and dropping columns

```python
# ADD a column (vectorized — no loop)
transactions["profit_estimate"] = transactions["sales_cost"] * 0.25
transactions.assign(discounted=transactions["sales_cost"] * 0.9)   # returns a NEW df

# RENAME
transactions = transactions.rename(columns={"sales_cost": "revenue"})

# REORDER (just pick columns in the new order)
transactions = transactions[["product_area_id", "num_items", "sales_cost"]]

# DROP
transactions = transactions.drop(columns=["transaction_id"])

# THE list of names, as a plain Python list
transactions.columns.to_list()
# ['customer_id','transaction_date','transaction_id','product_area_id','num_items','sales_cost']
```

### 3.7 Checking whether a column exists

```python
"sales_cost" in transactions.columns     # True
"total" in transactions.columns          # False
```

Useful in pipelines so you can do `if "x" in df.columns: ...` instead of crashing.

---

## 4. Typical Use Cases (Where This Actually Shows Up in Companies)

Column selection is not an academic exercise — it is how you go from "a raw 6-column export" to "the exact inputs a manager or a model needs." Mapping each to a real company question, on *this* grocery data:

| What you select | The real company question it answers | Who cares |
| --- | --- | --- |
| `transactions["sales_cost"]` (Series) | "What's the **average / total / median** line cost?" (`mean()`, `sum()`, `median()`) | **Revenue / Finance** |
| `transactions[["customer_id","sales_cost"]]` | "Build me the **customer → spend** table so we can rank spenders." | **Marketing / CRM (LTV)** |
| `transactions[["customer_id","sales_cost","num_items"]]` | "These are the **features + label** for a spend-prediction model." | **ML / Data Science** |
| `transactions[~transactions.columns.isin(["customer_id","transaction_id"])]` | "Give me **only the measurable fields** (drop the IDs) for analysis." | Analyst, always |
| `transactions.select_dtypes(include="number")` | "Hand me **every numeric column** to compute correlations at once." | Analyst (EDA) |
| `transactions[["product_area_id","sales_cost"]].groupby("product_area_id").sum()` | "**Revenue per department**." | **Ops / Merchandising** |
| `transactions.iloc[:, 5]` | "I don't remember the names — give me the **6th column** for a quick check." | Debugging / exploratory |
| `transactions.rename(columns={"sales_cost":"revenue"})` | "Rename to **match the dashboard's** required field names before export." | Reporting / ETL |

### The recurring professional pattern

Almost every analysis follows the same three beats, all built on column selection:

1. **Select the columns** you care about → a leaner, focused table (do it *first*; working on 6 cols instead of 60 makes everything faster and clearer).
2. **Filter the rows** (conditions) → the subset of *those* columns you care about.
3. **Aggregate** (`groupby`, `sum`, `mean`) → the one or two numbers a decision is made on.

```python
# The three beats, on this data: revenue per department in 2020-09
step1 = transactions[["product_area_id", "transaction_date", "sales_cost"]]   # select cols
step2 = step1[step1["transaction_date"].dt.month == 9]                         # filter rows
step3 = step2.groupby("product_area_id")["sales_cost"].sum()                   # aggregate
```

That whole block — *select → filter → aggregate* — is the professional's daily loop, and **column selection is beat one**.

---

## 5. Common Pitfalls (the ones that actually bite)

1. **The bracket trap (again, because it's the big one).** `df["col"]` = Series, `df[["col"]]` = DataFrame. If your code suddenly "does something different," check *this* first.
2. **Dot notation on a "bad" name.** `df.first name` (with a space) → `SyntaxError`. `df.index`, `df.mean`, `df.sum` → you get the **built-in attribute/method**, *not* your column. Use `df["index"]` etc. when the names collide.
3. **Passing a single-column DataFrame where a Series is expected** (or the reverse) to a function. `df[["x"]].mean()` returns a Series of means; `df["x"].mean()` returns a single number. When in doubt, call `.squeeze()` on a one-column DataFrame to turn it into a Series.
4. **Forgetting that selection can return a *copy*.** Modifying a selected column may not update the original (the `SettingWithCopyWarning` of Day 48). If you intend to mutate, assign into the original frame or use `.loc`.
5. **Assuming `df[0]` is the first column.** `df[0]` looks for a column *named* `0`. For position-based access use `df.iloc[:, 0]`.
6. **Silently dropping columns you still need** after a narrow `[["a","b"]]` select. Re-check `.columns` or `.shape` right after a selection when the table gets confusing.

---

## 6. Beyond Column Selection — A Map of Data Science & ML

Column selection sits at the start of a much bigger machine. Since Day 49 is where pandas stops being "spreadsheet tricks" and starts becoming **the front door to modeling**, here is a compact map of the whole field, tied back to *this* grocery dataset so it stays concrete.

### 6.1 The Data Science / ML lifecycle (the loop)

```
  1. Question      "Which customers are likely to stop buying (churn)?"
  2. Data          groceries: transactions + customer_details  (what we have)
  3. Cleaning      fix the 400 km distance outlier, impute 8 missing credit scores (Day 48)
  4. Feature eng.  build the right columns: days-since-last-visit, total-spend, avg-ticket
  5. Split         divide rows into TRAIN (learn) + TEST (examine, unseen)
  6. Model         fit an algorithm to the train rows
  7. Evaluate      compare predictions vs reality on the TEST set
  8. Tune & ship   fix problems, deploy, monitor in production
```

**Every step uses pandas.** Step 4 (feature engineering) is *mostly column selection + arithmetic* — the `df["new"] = df["a"] * 2` skill from Day 49.

### 6.2 Features vs. the label (the single most important idea in ML)

A model learns a relationship **from inputs to an output**:

- **Features (X)** — the *predictor* columns you *select*: `num_items`, `sales_cost`, `distance_from_store`, `credit_score`.
- **Label / target (y)** — the *outcome* you want to **predict**: e.g. `will_churn` (yes/no), or `next_month_spend` (a number).

```python
# The day-49 skill, applied to a model:
X = transactions[["num_items", "sales_cost", "product_area_id"]]   # FEATURES (a DataFrame)
y = transactions["some_outcome_column"]                            # LABEL   (a Series)
```

> Notice the pattern from Section 1: **X is a DataFrame (multiple feature columns), y is a Series (one label).** This is *exactly* the Series-vs-DataFrame distinction, showing up in *every* machine-learning codebase.

### 6.3 The three families of machine learning

| Family | Goal | Question it answers | Grocery example |
| --- | --- | --- | --- |
| **Supervised — Regression** | Predict a **number** | "How much will this customer spend next month?" | predict `next_month_spend` from past purchases |
| **Supervised — Classification** | Predict a **category** | "Will this customer churn? (yes/no)" | predict `will_churn` — the classic use of this dataset |
| **Unsupervised** | Find **hidden structure** (no label) | "Who are the natural customer groups?" | **clustering** (K-means) to segment shoppers into "bulk buyers," "one-off," "loyal regulars" |

*(A fourth family, **reinforcement learning**, learns *actions* by reward — think pricing/discount robots — and is outside this course's scope but good to know exists.)*

### 6.4 The #1 modeling mistake: overfitting

- **Underfitting** — the model is too simple to capture the pattern (bad at training *and* test).
- **Overfitting** — the model memorized the training data (great at training, **bad at new data**). This is the common one.

The only defense that always works is the **train/test split** (Section 6.1 step 5): you *never* let the model see the test data until the very end. Two related guardrails:

- **Cross-validation** — repeat the split several different ways so a lucky/bad split can't fool you.
- **Avoid data leakage** — never let information from the *future* (the label, or a feature that only exists after the event) sneak into your features. (E.g. don't use "customer's total spend *including* the month you're predicting" as a feature.)

### 6.5 How you *measure* a model (metrics)

| Problem type | Metrics (the "marks" for the model) |
| --- | --- |
| **Classification** | **Accuracy** (overall % right), **Precision** (of the ones it *flagged*, how many were right), **Recall** (of the *real* positives, how many did it catch), **F1** (balance of precision+recall), **ROC-AUC** (ranking quality) |
| **Regression** | **MAE** (avg absolute error), **RMSE** (avg error, punishes big misses harder), **R²** (fraction of variance explained, 0–1) |

> For a churn model, **recall** usually matters more than accuracy (missing a churner is costlier than a false alarm), and a model that's "90% accurate" can still be *useless* if churn is only a 5% event. Always match the metric to the **business cost**, not the prettiest number.

### 6.6 Feature engineering — where pandas shines (ties back to Day 49)

Models learn from **features**, and the best features are ones **you build** from the raw columns. This is where every pandas skill from Day 46–49 compounds:

```python
# Raw columns (Day 49: select them)
df = pd.merge(transactions, customer_details, on="customer_id")

# Engineered columns (Day 49: new columns via arithmetic + dates)
df["total_spend"]        = df.groupby("customer_id")["sales_cost"].transform("sum")
df["avg_ticket"]         = df["sales_cost"] / df.groupby("customer_id")["num_items"].transform("sum")
df["days_since_last"]    = (df["reference_date"] - df["transaction_date"]).dt.days

# Encode the category for a model (one-hot / dummy columns)
df = pd.get_dummies(df, columns=["product_area_id"])

# Scale/normalize the numbers so the model is fair (standardize to mean 0, std 1)
from sklearn.preprocessing import StandardScaler
X_scaled = StandardScaler().fit_transform(X)
```

- **Encoding categoricals:** a model can't read `F`/`M` or `product_area_id` text directly — turn them into numbers (`get_dummies` → one column per category, the "one-hot" trick).
- **Scaling/normalization:** distance features in km and credit scores in 0–1 are on wildly different scales; most algorithms (regression, k-means, SVM, neural nets) need them **balanced**.

### 6.7 The ecosystem (where each piece lives)

| Layer | Libraries / tools | What you use it for |
| --- | --- | --- |
| **Arrays / math** | **NumPy** | fast numeric arrays (pandas is built on it) |
| **Tables (this course)** | **Pandas** | selecting columns, cleaning, features |
| **Charts** | **Matplotlib**, **Seaborn**, **Plotly** | EDA plots — distributions, scatter, heatmaps |
| **Classic ML** | **scikit-learn** | train/test split, models, metrics, cross-val |
| **Gradient boosting** | **XGBoost**, **LightGBM**, **CatBoost** | top performers on tabular (exactly this kind of) data |
| **Deep learning** | **TensorFlow**, **PyTorch** | images, text, large-scale / sequence problems |
| **Dashboards / sharing** | **Tableau / Power BI**, **Streamlit** | presenting the answers (you did Tableau in Days 20–28) |

> **A useful fact:** for **tabular data like this grocery file, gradient-boosted trees (XGBoost/LightGBM) plus a good pandas feature pipeline routinely beat heavy deep learning.** Deep learning shines on *images, audio, and natural language* — not rows-and-columns.

### 6.8 Habits of a professional (the "adult" checklist)

- **Reproducible:** fix a random seed (`random_state=`) so runs are repeatable; document every cleaning step.
- **Versioned:** keep data + code + results together (a notebook or version-controlled scripts, like this `DSI/` series).
- **Honest:** report **test** performance, never training performance, to the business.
- **Data-aware:** a model is only as good as the columns fed to it. Garbage in, garbage out — *Day 48's* cleaning and outlier work is what makes Day 49's column selection meaningful.

---

## 7. Cheat Sheet (one screen)

### Accessing columns in pandas

| I want to… | Code | Returns |
| --- | --- | --- |
| One column | `df["col"]` (or `df.col`) | **Series** |
| One column, as a table | `df[["col"]]` | **DataFrame** |
| Several columns | `df[["a","b"]]` | DataFrame |
| Columns by position | `df.iloc[:, 0]` / `df.iloc[:, [0,1]]` | Series / DataFrame |
| All rows, one label-based col | `df.loc[:, "col"]` | Series |
| A range of columns | `df.loc[:, "a":"c"]` / `df.iloc[:, 1:4]` | DataFrame |
| Columns matching text | `df.filter(like="cost")` | DataFrame |
| Columns matching regex | `df.filter(regex="^s")` | DataFrame |
| Columns by data type | `df.select_dtypes(include="number")` | DataFrame |
| All columns except some | `df[~df.columns.isin([...])]` | DataFrame |
| Column name list | `df.columns.to_list()` | list |
| Does a column exist? | `"col" in df.columns` | bool |
| Safe get (no crash if absent) | `df.get("col")` | Series or None |
| Add a column | `df["new"] = ...` / `df.assign(new=...)` | DataFrame |
| Rename | `df.rename(columns={"old":"new"})` | DataFrame |
| Reorder | `df[["c","a","b"]]` | DataFrame |
| Drop | `df.drop(columns=["x"])` | DataFrame |

### The ML loop (one screen)

```text
Question -> Data -> Clean -> FEATURES(X) + LABEL(y) -> Split -> Model -> Evaluate -> Tune -> Ship
                          (Day-48)   (Day-49: select cols)    (scikit-learn) (metrics)
```

| Need | Tool |
| --- | --- |
| Split rows train/test | `train_test_split(X, y, test_size=0.2, random_state=42)` |
| Predict a number (regression) | Linear/Logistic-adjacent, Ridge, Random Forest Regressor |
| Predict a class (classification) | Logistic Regression, Random Forest, **XGBoost** |
| Find groups (no label) | K-Means, DBSCAN |
| Fit / evaluate | `model.fit(X_train, y_train)` / `model.score(X_test, y_test)` |
| Class metrics | accuracy, precision, recall, F1, ROC-AUC |
| Reg metrics | MAE, RMSE, R² |
| Encode categories | `pd.get_dummies(df, columns=[...])` |
| Scale numbers | `StandardScaler()` |

---

## 8. Recap

- **Accessing columns is the front door of every pandas task.** Three core methods cover 90% of daily work: `df["col"]` (one column → Series), `df[["a","b"]]` (several → DataFrame), and the pattern/type helpers for grabbing a *set* of columns at once.
- **The Series/DataFrame distinction is the #1 gotcha.** One extra set of brackets turns a column (1D) into a table (2D) — and that choice changes what `.mean()`, `.dropna()`, and *what you feed a model* all do.
- **Dot notation is sugar for clean names only.** Any column with a space, dash, leading digit, or a name colliding with a pandas method (`index`, `mean`, `sum`…) must use brackets.
- **Column selection is beat one of the analyst's loop:** select → filter → aggregate. You've now done it, on real company-shaped data.
- **And it's beat four of the *model's* loop:** features (X) and label (y) are just columns — selected for, engineered from, and scaled with the exact pandas skills of this course. From here, pandas doesn't just describe the data; it **feeds the machine learning that predicts from it.**

You have gone from *understanding a table* (Day 48) to *selecting the exact inputs a model needs and placing yourself on the full data-science map* — the line between "I can read a spreadsheet in Python" and "I can build a predictive model" is exactly this: **choose the right columns, pair them with a label, and let an algorithm learn the relationship.**
