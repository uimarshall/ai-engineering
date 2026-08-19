# Day 49: Adding & Dropping Columns in Pandas (+ Feature Engineering & Feature Selection)

> **Prerequisite:** Day 49 (Accessing Columns) and Day 48 (Understanding Our Data). Companion practice file: `204_Adding_And_Dropping_Columns.py` — run it, then compare with the blocks below.
>
> Same real data as before: `grocery_database.xlsx` → `transactions` sheet (**38,506 × 6**: `customer_id`, `transaction_date`, `transaction_id`, `product_area_id`, `num_items`, `sales_cost`).

Accessing columns (prev note) was **reading** the table. Today we **write** to it: we add brand-new columns that don't exist yet, and we drop the ones we don't want. Together these two skills are the hands-on form of **feature engineering** and **feature selection** — the two steps that decide whether a machine-learning model is good or mediocre.

---

## 1. The Big Idea: Why Add & Drop Columns at All?

Raw data is a *gift wrapped in the wrong shape*. The columns a company exports are the columns their **database** found convenient — not the columns a **manager** or a **model** needs. Your job:

- **Add columns** that capture the thing you actually care about (profit, a category, a ratio, a flag).
- **Drop columns** that are noise, redundant, or *leak the answer* (IDs, the label itself, things that only exist after the event).

```
raw 6 columns   --add 4 new-->   10 useful columns   --drop 3-->   7-column model-ready table
```

That transformation — *raw → engineered → trimmed* — is what turns "a spreadsheet" into "**the inputs to a decision or a model**."

---

## 2. The Script, Line by Line (Beginner-Friendly)

### 2.1 Imports & load

```python
import pandas as pd
import numpy as np                      # NumPy — pandas is built on it; we need it for np.where / np.select

transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")
```

Note the **`import numpy as np`**. Several "add a column" recipes (`np.where`, `np.select`) are NumPy functions, not plain pandas — so you reach for `np` here. (From Day 40/42 you know NumPy as the fast array engine under pandas.)

### 2.2 Add a **constant** column: `store_id = 1`

```python
transactions["store_id"] = 1
```

This creates a new column `store_id` and sets **every single row** to `1`.

> **What this is really for:** a **constant / flag / placeholder** column. Real uses:
> - "Everything in this file is from **store #1**" — so that when you later `concat` a second store's file (`store_id = 2`), you can tell them apart.
> - A **flag** column you'll fill in conditionally later.
> - A column you need to *exist* before a model/dashboard that expects a fixed schema.

**The mechanics to understand (this one line is the foundation of every "add" below):**

1. `transactions["store_id"]` on the *left* of `=` **creates the column** if it doesn't exist (or overwrites it if it does).
2. The value on the *right* (`1`) is a **scalar**. pandas **broadcasts** that single value to **all 38,506 rows**.
3. Because the new column is all integers, pandas stores it as `int64`.

> **Rule:** `df["new"] = <any value that is either one number OR one value-per-row>` → adds/overwrites a column. That's the whole rule. Everything else in this note is a variation of it.

### 2.3 Add a **computed** column: 20% of `sales_cost`

```python
transactions["profit"] = transactions["sales_cost"] * 0.2
```

The new `profit` column is **`sales_cost` × 0.2**, row by row.

> **SQL equivalent:** `SELECT customer_id, sales_cost, sales_cost * 0.2 AS profit FROM transactions`

**The crucial idea — this is *vectorized*, not a loop.** You did **not** write:

```python
# DOWNGRADE (slow, never do this for whole columns):
for i in range(len(transactions)):
    transactions.loc[i, "profit"] = transactions.loc[i, "sales_cost"] * 0.2
```

Instead one line did the math on **all 38,506 rows at once**. Because `sales_cost` is a whole column (a Series), multiplying it by `0.2` multiplies *each element* and returns a new Series — assigning that Series as `transactions["profit"]` fills the new column. This is pandas' core superpower and the reason pandas is **~100× faster** than a Python `for` loop for this. *(You saw the warning about loops in Day 48's pitfalls — this is the fix.)*

> **Pattern:** *any two aligned columns can be combined.* `df["a"] + df["b"]`, `df["a"] / df["b"]`, `df["a"] ** 2`, `df["a"] - df["b"]` … all create new columns. E.g. an average order value: `transactions["avg_per_item"] = transactions["sales_cost"] / transactions["num_items"]`.

### 2.4 Add a **conditional** column (if/else) with `np.where`

```python
# If sales_cost > 20 -> "Large", else -> "Small", into a new column "sales_type"
transactions["sales_type"] = np.where(transactions["sales_cost"] > 20, "Large", "Small")
```

Read `np.where` **as an English if-else over the whole column**:

```
np.where( CONDITION ,  VALUE_IF_TRUE ,  VALUE_IF_FALSE )
            (per-row     (put this when  (put this when
             True/False)   True)            False)
```

- `transactions["sales_cost"] > 20` → a **list of True/False for every row** (a *boolean mask* — you built these in Day 48).
- `np.where(mask, "Large", "Small")` → a new column: `"Large"` where the mask is `True`, `"Small"` where it's `False`.

**Why not use a normal Python `if`?** A normal `if` tests **one value**. Here we need a *separate* decision for each of the 38,506 rows — `np.where` does all of them at once. This is **categorization / binning** — turning a continuous number (a cost) into a category (a label), which is one of the most common analyst tasks ("tag orders as big/small," "grade scores as pass/fail," "flag customers as high/low risk").

> On *this* data, the median `sales_cost` was **23.18** (Day 48), so a threshold of 20 puts most rows on the "Large" side with a smaller "Small" tail — the 20/80 split you'll see when you `value_counts()` it.

### 2.5 Add a **multi-condition** column with `np.select`

`np.where` only does **one** branch (two outcomes). Real logic often needs **several** tiers. That's `np.select`:

```python
condition_rules = [ transactions["sales_cost"] > 50,
                    transactions["sales_cost"] > 20,
                    transactions["sales_cost"] > 10 ]
outcomes = ["X-Large", "Large", "Medium"]

# Anything not caught by the conditions above gets the default:
transactions["sales_type"] = np.select(condition_rules, outcomes, default="Small")
```

`np.select` is **"a ladder of ifs"** applied to the whole column:

```
np.select( [cond_1, cond_2, cond_3],   # list of conditions (per-row True/False)
           [out_1,  out_2,  out_3],    # matching outcomes
           default = "Small" )         # fallback if NOTHING matched
```

**The one rule that trips people up: order matters — the FIRST True condition wins.** For a row with `sales_cost = 60`:

- `> 50`? **True** → assigned `X-Large` and **stops checking** (it never looks at `> 20`).
For `sales_cost = 30`:
- `> 50`? No. `> 20`? **Yes** → `Large`, stops.
For `sales_cost = 15`:
- `> 50`? No. `> 20`? No. `> 10`? **Yes** → `Medium`.
For `sales_cost = 5`:
- none true → **default** `Small`.

> ⚠️ **Order matters.** If you wrote `[>10, >20, >50]` you'd label *everything above 10* as just `Medium` — the `>20` and `>50` tiers would never fire. Always list conditions from **most specific / most restrictive to least**.

**`np.where` vs `np.select` at a glance:**

| | `np.where` | `np.select` |
| --- | --- | --- |
| Branches | **2** (True / False) | **N** (many) + a default |
| Shape | `np.where(cond, a, b)` | `np.select([cond1, cond2, …], [out1, out2, …], default=…)` |
| Order matters? | No (only one condition) | **Yes — first True wins** |
| Use for | one split (big/small) | a tiered ladder (XL/L/M/S) |

> **SQL equivalent** (if you're coming from Days 1–19): this is exactly a **`CASE WHEN`** ladder:
> ```sql
> CASE WHEN sales_cost > 50 THEN 'X-Large'
>      WHEN sales_cost > 20 THEN 'Large'
>      WHEN sales_cost > 10 THEN 'Medium'
>      ELSE 'Small' END
> ```
> You built these in SQL (Day 7 `CASE_WHEN`). `np.where`/`np.select` are the **pandas/NumPy versions acting on a whole column at once** instead of row-by-row in the DB.

### 2.6 **Drop** a column

```python
# axis = 1  ->  drop a COLUMN
# axis = 0  ->  drop a ROW
new_df_drop_col = transactions.drop(["sales_cost"], axis=1)
```

`drop` **removes** the named column(s) from a *copy* of the frame.

**The `axis` argument — the part that confuses everyone:**

| `axis` | Means | Drop it… |
| --- | --- | --- |
| **`0`** | the **rows** | by row label/index |
| **`1`** | the **columns** | by column name |

You're dropping `sales_cost`, which is a **column**, so **`axis=1`**. (The `0/1` numbering comes from "rows are the 0th axis, columns are the 1st axis.")

> **⚠️ It returns a NEW DataFrame — the original is untouched.** Note the code assigns the result to `new_df_drop_col`. If you just write `transactions.drop(...)` on its own line, **nothing is dropped** (the returned copy is thrown away). This is the same "returns a new object" habit as Day 46's pitfall.

**Three equivalent ways to drop a column (pick one, be consistent):**

```python
transactions.drop(["sales_cost"], axis=1)   # the script's way
transactions.drop(columns="sales_cost")     # the clearest — "columns=" spells it out
del transactions["sales_cost"]              # in-place, removes from the original (no new df)
```

`del` is the only one that **modifies the original in place** and returns `None` — use it when you definitely want to lose the column for good and aren't chaining.

**Drop multiple columns at once:** just put them all in the list → `transactions.drop(["sales_cost", "store_id"], axis=1)`.

---

## 3. The Full Toolkit

### 3.1 Adding columns — every way you'll need

| Goal | Code | Notes |
| --- | --- | --- |
| Constant / flag | `df["c"] = 1` | broadcasts one value to all rows |
| Arithmetic from other cols | `df["a*b"] = df["a"] * df["b"]` | vectorized, the workhorse |
| Return a **new** df (chainable) | `df.assign(a_b=df["a"]*df["b"])` | doesn't touch the original; great in pipelines |
| One row's worth / single cell | `df.loc[0, "c"] = 5` | precise, avoids copy surprises |
| if/else (2 branches) | `df["c"] = np.where(df["a"]>x, "Hi", "Lo")` | one split |
| tiered ladder (N branches) | `df["c"] = np.select([c1,c2,…],[o1,o2,…], default="…")` | first True wins |
| **bin** a number into ranges | `df["c"] = pd.cut(df["a"], bins=[0,10,20,50,999], labels=["S","M","L","XL"])` | cleaner than hand-writing `np.select` for fixed ranges |
| equal-frequency bins | `df["c"] = pd.qcut(df["a"], q=4, labels=["Q1","Q2","Q3","Q4"])` | splits into quartiles |
| run a **function** per row | `df["c"] = df["a"].apply(lambda v: v.upper())` | when no vectorized form exists (slower) |
| combine several cols into one | `df["full"] = df["first"] + " " + df["last"]` | string concat too |
| add a column from **another** df | `df["c"] = other_df["c2"]` | indices must align |

`pd.cut` / `pd.qcut` are worth memorizing: they do the "tiered ladder" of Section 2.5 **with named bins**, and they handle the edge of the last bin automatically (you don't hand-write `> 50`, `> 20`…).

```python
# same sales_type tiers, but with named bins (note: cut bins are ranges [lo, hi])
transactions["sales_type"] = pd.cut(transactions["sales_cost"],
                                    bins=[-1, 10, 20, 50, 1e6],
                                    labels=["Small","Medium","Large","X-Large"],
                                    right=True)
```

### 3.2 Dropping columns — every way you'll need

| Goal | Code |
| --- | --- |
| Drop one column (non-destructive) | `df.drop("col", axis=1)` |
| Drop several | `df.drop(["a","b","c"], axis=1)` |
| Drop by position | `df.drop(df.columns[0], axis=1)` |
| Drop in place | `del df["col"]` / `df.drop("col", axis=1, inplace=True)` (avoid `inplace`) |
| Keep only what I named (inverse) | `df[["a","b","c"]]` — *select* instead of drop |
| Drop all cols with NaN in them | `df.dropna(axis=1)` |
| Drop cols above a missing-rate threshold | `df.dropna(axis=1, thresh=len(df))` |

> **Pro trick:** often you don't *drop* — you **keep a chosen subset** (`df[["a","b","c"]]` from the Accessing Columns note). Both get you to a smaller table; "keep a whitelist" is safer than "drop a blacklist" because you can't accidentally keep something you forgot to drop.

### 3.3 The `inplace` question (set it once, stop thinking about it)

Most of the methods above **return a new DataFrame** rather than editing the original. You have two consistent choices:

```python
# A) reassignment (RECOMMENDED — explicit, no surprises)
transactions = transactions.drop(columns=["sales_cost"])

# B) inplace=True (modifies the original; discouraged in modern pandas)
transactions.drop(columns=["sales_cost"], inplace=True)
```

**Pick (A) and always reassign.** It keeps your data flow obvious ("the old frame is gone, this is the new one") and avoids the `SettingWithCopyWarning` copy bugs (Day 46 pitfall).

---

## 4. Typical Use Cases (where this shows up in companies)

| What you add / drop | The real company question it answers | Who cares |
| --- | --- | --- |
| `df["profit"] = sales_cost * margin` | "What's our **take** on each sale?" (margin analysis) | **Finance / P&L** |
| `df["avg_per_item"] = sales_cost / num_items` | "Do bulk buyers get a **cheaper per-unit price**?" (pricing) | **Pricing / Merchandising** |
| `np.select(...)` → customer **tiers** (Bronze/Silver/Gold) | "Who gets the **loyalty program** and at what level?" | **CRM / Marketing** |
| `pd.cut` / `pd.qcut` → **segments** by spend | "Split customers into quartiles so we can **target the top 25%**." | **Marketing / Segmentation** |
| `df["month"] = df["date"].dt.to_period("M")` | "Reveal **seasonality** — which months spike?" | **Demand planning** |
| drop `customer_id`, `transaction_id` | "Remove **IDs** (no predictive signal) before modeling." | **ML / DS** |
| drop the **label** from X | "The answer must not be one of the **inputs** (leakage)!" | **ML / DS** |
| `df.dropna(axis=1)` / drop high-missing cols | "Kill **unreliable columns** before they poison a model." | **Data quality / DS** |

On *this* grocery data, the script's `profit` and `sales_type` columns are prototypes of two of the most-asked-for derived fields in retail: **per-line margin** and **order-size segmentation**.

---

## 5. Common Pitfalls (the ones that actually bite)

1. **Forgetting to reassign a non-destructive method.** `transactions.drop(...)` with no `=` does nothing. Always `transactions = transactions.drop(...)` (or use `del`).
2. **`axis` confusion.** Dropping a column needs `axis=1`; `axis=0` drops *rows*. When in doubt, use the keyword form `drop(columns=[...])` — it's self-explaining.
3. **`np.select` in the wrong order.** Conditions are checked **top-down, first-True-wins**. Put the **most restrictive first**, or your upper tiers never fire.
4. **Using a Python `if` / looping for a whole column.** `if df["x"]: ...` on a Series raises *"truth value of a Series is ambiguous."* For per-row decisions, use `np.where` / `np.select` / `pd.cut` (vectorized) or `.apply` (slow) — never a `for` loop.
5. **Adding to a *filtered copy*, mutating the original.** `big = df[df.x>20]; big["flag"]=1` may not update `df` (the copy warning). Assign via the original: `df.loc[df.x>20, "flag"] = 1`.
6. **A constant column becomes the wrong type quietly.** `df["flag"] = 1` is `int64`; if you later `concat` a file where that column is text, pandas will upcast the whole thing to `object`. Decide the type *up front*.
7. **Leaking the answer into a feature you add.** If you compute a column using information from the *outcome* (or the future), the model "cheats" on training and **fails** in production. (Section 6.4.)

---

## 6. Beyond This Script — Feature Engineering & Feature Selection (the DS/ML heart of it)

Adding = **feature engineering**. Dropping = **feature selection**. These two are the most *impactful* steps in building a model — more than the choice of algorithm in most tabular problems. Here's the map, tied to this data.

### 6.1 Feature engineering (adding the right columns)

A model can only learn from the columns you **give** it. The raw export almost never contains the *right* raw ingredients, so you build them. The main families you've now used:

| Family (what you're adding) | Example on this data | Why it helps |
| --- | --- | --- |
| **Arithmetic / ratios** | `profit = sales_cost*0.2`, `avg_per_item = sales_cost/num_items` | captures *rate* info a raw total hides |
| **Binning / segmentation** | `sales_type` via `np.select` / `pd.cut` (S/M/L/XL) | turns a continuous number model & humans both understand |
| **Interactions** | `df["items_x_area"] = num_items * product_area_id` | lets a model see "this area × this volume" combos |
| **Time features** | `month = date.dt.to_period("M")`, `weekday = date.dt.day_name()` | exposes seasonality / weekly rhythm |
| **Aggregations as features** | per-customer `total_spend` (via `groupby(...).transform("sum")`) | brings a history summary onto each row |
| **Encodings** | `pd.get_dummies(df, columns=["product_area_id"])` | turns a category into model-readable numbers |
| **Flags / indicators** | `is_big = (sales_cost>50).astype(int)` | one-hot-ish shortcuts for rules |

> The professional habit: start from the **business/question** ("what drives churn?"), then ask *"what column would I need to compute that?"* — and add it. You rarely use every raw column as-is.

### 6.2 Feature selection (dropping the irrelevant / harmful columns)

Just because a column *exists* doesn't mean it should go into a model. Reasons to drop:

| Reason | Example here |
| --- | --- |
| **No signal / ID-like** | `customer_id`, `transaction_id` — big numbers that mean nothing to a model |
| **Redundant (multicollinearity)** | `profit` derived from `sales_cost` is 100% correlated with it — keep one, or the model double-counts |
| **The label / leakage** | never include the outcome you're predicting as an input |
| **Too much missing** | a column 60% empty (Day 48: `isna().sum()`) is usually dropped |
| **Curse of dimensionality** | too many noise columns hurts accuracy & slows training |

> **The irony that bites:** the more columns you *add*, the more you must *select* carefully. Feature engineering and feature selection are two hands on the same steering wheel.

### 6.3 The #1 trap when adding columns: **data leakage**

A **leak** is when a "feature" actually contains information about the *answer*. The model looks brilliant on training data (it's reading the answer key) and **collapses** on new data. Classic leaks:

- Using a column computed *after* the prediction point (e.g. "customer's *total* lifetime spend" to predict a single *future* purchase).
- Including the label directly, or a near-duplicate of it.
- Scaling/bining using statistics from the **test** set.

**The rule:** every added column must be computable **at the moment you're making the prediction**, using only information available *then*. If you can't answer that, it's a leak.

### 6.4 Do it in a **pipeline** that only the *model* sees

The professional version of everything above:

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

# X = the features you kept, y = the label
pipe = Pipeline([
    ("prep", ColumnTransformer([
        ("num", StandardScaler(), ["num_items", "sales_cost"])])),   # scale numeric
    ("model", LogisticRegression()),
])
pipe.fit(X, y)        # the scaler learns on TRAIN only -> no leak into test
pipe.score(X_test, y_test)   # report TEST performance, never training
```

A pipeline guarantees your add/scale/drop steps are applied **identically** to training and new data — which is what makes a model **reproducible** and **shippable**. That connective tissue (scaling + encoding + modeling in one object) is the standard scikit-learn pattern; the pandas work of *building the columns* (this note) is what feeds it.

### 6.5 The whole preprocessing loop (where this note sits)

```
 1. Question     "predict each customer's next-month churn"
 2. EDA (Day 48) inspect types, missing, outliers
 3. SELECT cols (Accessing Columns note)
 4. ENGINEER cols (THIS note — add profit, tiers, bins, flags)   <-- you are here
 5. SELECT/DROP (feature selection — remove IDs, leaks, junk)
 6. SPLIT train/test  (never leak across the split)
 7. MODEL + EVALUATE  (scikit-learn / XGBoost)
 8. TUNE + SHIP (pipelines, monitoring)
```

Steps 3–5 are **all pandas column work** — reading (accessing), writing (adding/dropping), and choosing (selecting). Master these three and you control the entire *pre-model* half of every data project.

---

## 7. Cheat Sheet (one screen)

### Adding columns

| Goal | Code |
| --- | --- |
| Constant / flag | `df["c"] = 1` |
| Arithmetic combo | `df["p"] = df["a"] * 0.2` (or `+ / - / ** / /`) |
| Non-mutating, chainable | `df.assign(p=df["a"]*0.2)` |
| Single cell | `df.loc[0, "c"] = 5` |
| if/else (2) | `df["c"] = np.where(df["a"]>20, "Large", "Small")` |
| tiered (N) | `df["c"] = np.select([c1,c2],[o1,o2], default="Small")` — **first True wins** |
| named range bins | `df["c"] = pd.cut(df["a"], bins=[0,10,20,1e6], labels=["S","M","L"])` |
| quantile bins | `df["c"] = pd.qcut(df["a"], q=4)` |
| per-row function | `df["c"] = df["a"].apply(fn)` (slow — last resort) |
| concat two text cols | `df["full"] = df["f"] + " " + df["l"]` |

### Dropping columns

| Goal | Code |
| --- | --- |
| Drop one (new frame) | `df.drop("col", axis=1)` or `df.drop(columns="col")` |
| Drop several | `df.drop(["a","b"], axis=1)` |
| Drop in place | `del df["col"]` |
| Keep a whitelist | `df[["a","b","c"]]` (often better than dropping) |
| Drop whole-column NaNs | `df.dropna(axis=1)` |

### axis + in-place

```text
axis=0 -> rows      axis=1 -> columns
df = df.drop(...)  ✅ reassign      del df["c"]  ✅ in-place      df.drop(...) alone  ❌ discarded
```

### Preprocessing loop

```text
SELECT -> ENGINEER(add) -> SELECT/DROP -> SPLIT -> MODEL -> EVALUATE -> SHIP
 (read)     (this note)     (select)    (never leak)  (scikit-learn)
```

| Need | Tool |
| --- | --- |
| Encode a category | `pd.get_dummies(df, columns=[...])` |
| Scale numbers | `StandardScaler()` (fit on train only) |
| Split | `train_test_split(X, y, test_size=0.2, random_state=42)` |
| Keep steps repeatable | `Pipeline( ColumnTransformer(...) , estimator )` |

---

## 8. Recap

- **Adding a column is one rule:** `df["new"] = <one value, or one value-per-row>`. Vary the right-hand side — a constant (`1`), a **vectorized** arithmetic combo (`sales_cost*0.2`), a **categorical** via `np.where` (2-way) or `np.select` (N-way) or `pd.cut` (named bins) — and you've engineered features.
- **`np.where` = one if/else over every row; `np.select` = a ladder of ifs, first-True-wins, with a default.** (They are the pandas twin of SQL's `CASE WHEN`.) **Order your conditions most-restrictive-first.**
- **Dropping a column = `drop(..., axis=1)`**, and remember it returns a **new frame** — reassign it (or `del`). `axis=0` is rows, `axis=1` is columns.
- **Adding = feature engineering, dropping = feature selection.** These two decide model quality more than the algorithm does — and they carry the top trap: **data leakage** (a feature that secretly contains the answer). A column is a valid feature only if it's computable *at prediction time*.
- **Wrap it in a pipeline** (scale + encode + model in one object) so the same steps apply to training, testing, and future data — that's what makes a model *shippable* instead of just a notebook toy.

You've gone from *reading* a column (previous note) to *writing* the table a model needs: **build the right columns, cut the rest, keep the answer out of the inputs.** That is the entire pre-model half of data science, and it runs on exactly the pandas you're practicing right now.
