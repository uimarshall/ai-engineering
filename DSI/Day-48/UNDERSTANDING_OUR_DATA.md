# Day 48: Understanding & Exploring Our Data (Python / Pandas)

> **Prerequisite:** Day 47 (Creating & Importing DataFrames). Companion practice file: `Understanding_Our_Data.py` — run it, then compare its output with the blocks below.

Day 47 showed you *how to get data in*. Today we answer the first question every analyst asks the moment a dataset lands in their lap:

> **"What is actually in here — and what is it trying to tell me?"**

That first pass is called **Exploratory Data Analysis (EDA)**. It is the single highest-leverage habit in the whole data job. You never model, chart, or trust a dataset you have not *met* first.

Everything below uses the real `grocery_database.xlsx` file that ships next to the script. All numbers are the actual output of running the code — not made up.

---

## 1. What We Are Looking At (The Business Story)

`grocery_database.xlsx` is the kind of file a grocery chain (think Walmart, Carrefour, Loblaws) exports from its point-of-sale system. It has **two related sheets**:

| Sheet | Shape (rows × cols) | What it holds | Real-world equivalent |
| --- | --- | --- | --- |
| `transactions` | **38,506 × 6** | One **line-item per purchase** (a "basket item" per transaction) | The **sales receipts** — the "what did people buy & pay" log |
| `customer_details` | **870 × 4** | One **row per customer** (distance, gender, credit score) | The **CRM / loyalty-card** profile of each shopper |

These two tables share `customer_id`, which is the **key** that lets you join them later (a customer's *purchases* + their *profile*). That join is what turns raw receipts into answers like "do people who live far from the store buy less?"

### The columns, translated

**`transactions`** — what was bought and paid:

| Column | Type | Meaning |
| --- | --- | --- |
| `customer_id` | int | Which loyalty member (1 – 870) |
| `transaction_date` | datetime | When the purchase happened (2020-04-01 → 2020-09-30) |
| `transaction_id` | int | The unique receipt/checkout (18,160 distinct receipts) |
| `product_area_id` | int | Dept/aisle: 1 – 5 (e.g. Dairy, Fruits, Household…) |
| `num_items` | int | How many units in that line |
| `sales_cost` | float | How much that line cost (the **money column**) |

**`customer_details`** — who the shopper is:

| Column | Type | Meaning |
| --- | --- | --- |
| `customer_id` | int | The link back to transactions (1 – 870) |
| `distance_from_store` | float | km (or miles) from the store |
| `gender` | text | `F` / `M` |
| `credit_score` | float | A 0–1 risk score (higher = safer credit) |

**Why you should care:** every "decision" a company makes — stocking, discounts, where to build the next store, who to extend credit to — traces back to *some* transformation of these two tables. The script you're reading is the **first 10 minutes** of that pipeline.

---

## 2. The Code, Line by Line (Beginner-Friendly)

### 2.0 Import & Load

```python
import pandas as pd
transactions = pd.read_excel("grocery_database.xlsx", sheet_name="transactions")
```

- `import pandas as pd` — we agree `pd` is our short name for the whole pandas library.
- `pd.read_excel(...)` — **builds a DataFrame from an Excel file.** (You met its cousin `pd.read_csv` in Day 47.)
- `sheet_name="transactions"` — an Excel file can hold **many sheets** (tabs). This picks the *transactions* tab specifically, otherwise pandas would grab the first one it finds.

After this one line, `transactions` is a **DataFrame**: an in-memory, spreadsheet-like grid of 38,506 rows and 6 columns that Python can now do math on.

### 2.1 `shape` — the size of the grid

```python
transactions.shape   # (38506, 6)
```

A **tuple**: `(rows, columns)`. Think of it like "this sheet is 38,506 long and 6 wide." You check this *first* because it tells you whether the file loaded correctly (an empty import returns `(0, 0)`).

### 2.2 `head()` / `tail()` — peek at the edges

```python
transactions.head()    # first 5 rows
transactions.head(20)  # first 20 rows
transactions.tail()    # last 5 rows
transactions.tail(10)  # last 10 rows
```

You **never** print 38,506 rows — your screen (and your sanity) cannot handle it. Instead you peek at the **top and bottom** to learn:

- **`head()`** → what a *typical* record looks like + the column names + data types.
- **`tail()`** → often reveals the **end of the timeline**. Ours jumps to late `2020-09`, confirming the data is ordered by date and spans 6 months.

> **Tip:** `head(n)` and `tail(n)` where `n` is optional — default is **5**.

### 2.3 `sample()` — grab random rows

```python
transactions.sample()        # 1 random row
transactions.sample(10)      # 10 random rows
sample = transactions.sample(frac=0.1)   # 10% of all rows  -> ~3851 rows
```

Two flavors:

- `sample(n)` → pick **n** random rows (a count).
- `sample(frac=p)` → pick a **fraction** of all rows. `0.1` = 10% of 38,506 ≈ **3,851 rows**.

**Why:** you want a *random* glance, not just the first 5 (which may be unrepresentative). It is how you quickly eyeball whether data looks sane before trusting it, and how you build a small **test subset** of a huge table.

#### 📡 Real output (what `sample()` actually gave)

```
   customer_id transaction_date  transaction_id  product_area_id  num_items  sales_cost
5271          549       2020-08-14    ...                  3          5        31.20
...
```

A random line from mid-summer — one of thousands like it.

### 2.4 `describe()` — the heart of the script ✅

This is the **most important function** in the file, so it gets its own deep-dive in **[Section 3](#3-the-describe--function-broken-down-cell-by-cell)** below. Short version: it computes the **summary statistics** of every *numeric* column at once.

### 2.5 `nlargest()` / `nsmallest()` — the extremes

```python
transactions.nlargest(5, "sales_cost")   # 5 MOST expensive lines
transactions.nlargest(25, "sales_cost")
transactions.nsmallest(25, "sales_cost") # 25 CHEAPEST lines
```

> **Read it literally:** "**n** **largest** *5* rows, ordered by the **`sales_cost`** column." Same for `nsmallest`.

This is the fastest way to **spot outliers** — you're literally pulling the top and bottom values to stare at them.

#### Real output — top 5 by `sales_cost`

```
       customer_id transaction_date  transaction_id  product_area_id  num_items  sales_cost
10443          224       2020-07-22    436683121376                1         27       669.34
 1367           27       2020-08-31    437085904531                1         27       639.22
  491           10       2020-09-29    437372244148                1         26       630.88
26319          593       2020-09-04    437126622541                1         24       611.83
32232          731       2020-04-29    435847289476                1         27       600.48
```

Notice a **pattern that matters**: the 5 most expensive lines all come from **`product_area_id = 1`** with **24–27 items**. That's not noise — it's a *signal* (a whole-cart purchase from one department, e.g. a big household stock-up). You would never have found that by reading 38,506 rows.

And the cheapest lines are the `0.00` and `0.01` values (promotional/free items, rounding to a cent).

### 2.6 `nunique()` — how many *distinct* values

```python
transactions.nunique()
```

Counts **unique** values per column:

```
customer_id           870     # 870 different customers
transaction_date      183     # purchases landed on 183 different days
transaction_id      18160     # 18,160 different receipts
product_area_id         5     # only 5 departments
num_items              59     # 59 possible item-quantities (1..310)
sales_cost          10986     # 10,986 different price totals
```

**Why it's gold:** `nunique()` tells you the **"category-ness"** of a column. Low unique count (`product_area_id` = 5, `gender` = 2) → it's a **categorical** column (use colors / labels in a chart). Very high (`sales_cost` ≈ 11k) → it's a **continuous/measure** column (use a number line / average it). This one call tells you *how to treat each column* downstream.

**The real decision read — each number here answers a business question:**

| `nunique()` value | Column | What it tells the business |
| --- | --- | --- |
| **870** | `customer_id` | Exactly how many **loyalty members** we have — and it matches the 870 rows in `customer_details`, so the two sheets **agree** (a mismatch would mean orphaned records). |
| **183** | `transaction_date` | Purchases landed on only **183 days** out of 183 calendar days in Apr–Sep → the store traded **every single day** (no gaps) — a good coverage/quality check. |
| **18,160** | `transaction_id` | There are **18,160 real receipts**, but **38,506 rows** → on average each receipt has **~2.1 line-items**. That's a *data-shape* fact (we're at item level, not receipt level) that tells you to `groupby` before summing revenue. |
| **5** | `product_area_id` | Confirms the claim of **"exactly 5 departments."** More than 5 would reveal an unmapped/legacy department code to fix in the source system. |
| **59** | `num_items` | 59 possible quantities (1→310). The **spread up to 310** already hints at the bulk/wholesale outliers you will confirm with `nlargest`. |
| **10,986** | `sales_cost` | Nearly **as many distinct prices as rows** → confirms it's a fine-grained *measure*, and that price values do **not** repeat in big chunks (no single "default price" dominating the data). |

It also **duplicates-checks** for you: if `customer_id` were supposed to have 870 but reported 8,700, something (a bad join, a duplicated export) was wrong *before* you ever built a chart.

### 2.7 Loading the second sheet & `isna()` — hunting for missing data

```python
customer_details = pd.read_excel("grocery_database.xlsx", sheet_name="customer_details")

customer_details.isna()        # a whole grid of True/False: True = "this cell is empty"
customer_details.isna().sum()  # count the empties in each column
```

- `isna()` (aka `isnull()`) → a **mask of the same shape** where every cell is `True` if that cell is **missing (NaN)**, else `False`.
- `.sum()` on it → since `True` counts as 1, this **totals the missing cells per column**.

#### Real output — where the holes are

```
customer_id            0     # the key is complete (good — you need it to join!)
distance_from_store    5     # 0.57% missing
gender                 5     # 0.57% missing
credit_score           8     # 0.92% missing
```

**Reading it like a professional — each hole number becomes a specific action:**

| Column | Missing | How a company **decides** what to do with it |
| --- | --- | --- |
| `customer_id` | **0** | ✅ Nothing to do — the **join key is 100% complete**, so `transactions` and `customer_details` can be merged cleanly (a missing key would *silently orphan* whole customer histories). |
| `credit_score` | **8 (0.92%)** | The **biggest hole**. Before any credit/churn model: either **drop those 8**, or **impute** them with the median (0.59) / mean (0.597), or **create an "unknown" flag** — then *document* which you chose. You must decide; you cannot ignore it. |
| `gender` | **5 (0.57%)** | Trivially low → either **drop the 5** or **fill with a neutral "U" (unknown)** category. Never force them all to "F" or "M" — that would *invent* data. |
| `distance_from_store` | **5 (0.57%)** | Fill with the **median (1.66)** (robust) rather than the mean (2.615) — the mean is already inflated by the 400.97 outlier, so it would mis-fill. |

**The rule of thumb a team uses:** missing **< ~5%** → *fix cheaply* (drop / median-fill) and move on. **5–20%** → investigate *why* it's missing (a broken form field?) and consider a "missing = its own category" flag. **> 20%** → **stop** — the column is too unreliable to model on; escalate to the data owner. All four columns here score **< 1%**, so this dataset is *clean enough* to trust for analysis.

> **Key idea:** `isna()` turns "how dirty is my data?" from a *vague worry* into a *concrete number with a concrete action attached.*

---

## 3. The `describe()` Function — Broken Down Cell by Cell

`describe()` on the `transactions` sheet produced **this** (numbers are real):

| **stat** | `customer_id` | `transaction_date` | `transaction_id` | `product_area_id` | `num_items` | **`sales_cost`** |
| --- | --- | --- | --- | --- | --- | --- |
| **count** | 38,506 | 38,506 | 38,506 | 38,506 | 38,506 | **38,506** |
| **mean** | 429.88 | 2020-06-30 19:37 | 4.36e+11 | 2.888 | 6.191 | **40.25** |
| **min** | 1.00 | 2020-04-01 | 4.355e+11 | 1.00 | 1.00 | **0.00** |
| **25%** | 209.00 | 2020-05-16 | 4.360e+11 | 2.00 | 2.00 | **11.42** |
| **50%** | 422.00 | 2020-07-01 | 4.364e+11 | 3.00 | 4.00 | **23.18** |
| **75%** | 656.00 | 2020-08-16 | 4.369e+11 | 4.00 | 8.00 | **45.98** |
| **max** | 870.00 | 2020-09-30 | 4.373e+11 | 5.00 | **310.00** | **669.34** |
| **std** | 255.22 | NaN | 5.29e+08 | 1.360 | 5.962 | **54.60** |

Let's decode **each row** — this is the mental model that "gets" `describe()`:

| Stat | Plain-English meaning | What it warns you about |
| --- | --- | --- |
| **count** | How many **non-missing** values pandas measured | If `count` < row count, the column **has nulls** (here 38,506 = full, so clean) |
| **mean** | The **average** (sum ÷ count) | Sensitive to big values — a few huge orders pull it up |
| **min / max** | The **floor and ceiling** | Instant range + first glimpse of **outliers** |
| **25%** (Q1) | Value below which **25%** of data falls | The "lower middle" |
| **50%** (median) | The **middle** value (below it = exactly half) | Robust "typical" — ignores outliers, great when data is skewed |
| **75%** (Q3) | Value below which **75%** of data falls | The "upper middle" |
| **std** (std dev) | **How spread out** values are around the mean | Big std = very varied; tiny std = all similar |

The three percentiles (25 / 50 / 75) are called **quartiles** — they slice the data into four equal pieces. The full set is also called the **five-number summary** (min, Q1, median, Q3, max) — the basis of a **box plot**.

### 🏢 From numbers to decisions — what *each* `describe()` stat is **for**

Meaning is only half the value. A manager does not buy a number; they buy a **decision**. Here is how **each row** in `describe()` (using our real `sales_cost` values) turns into an actual business action:

| Stat | Our number | What a company **decides** with it |
| --- | --- | --- |
| **count** | 38,506 (= all rows → no missing) | **Data-quality gate**: if next week's count suddenly dropped to 30,000, a pipeline broke. It is also the **denominator** — total revenue over the 6 months ≈ `mean × count` = 40.25 × 38,506 ≈ **$1.55M**. |
| **mean** | 40.25 | The headline **"average order value (AOV)".** But because whales drag it up, use the mean for **totals/forecasts**, **not** for describing "a typical customer." |
| **median (50%)** | 23.18 | The **robust "typical" basket**. *This* is the number you price a "back-to-average-shopper" promotion around — it is not fooled by the giant outlier orders the mean is. |
| **25% (Q1)** | 11.42 | Marks the **low end of "normal."** Baskets below this are your *low-value / at-risk* segment. |
| **75% (Q3)** | 45.98 | Marks the **high end of "normal."** Combined with Q1 it builds the **IQR fence** (45.98 + 1.5×IQR = 97.82) that flags the **3,342 outlier** high-value orders for separate analysis. |
| **std** | 54.60 | **Consistency / risk signal.** std (54.6) > mean (40.25) means revenue is **lumpy & hard to forecast** → budget for more safety stock and treat forecasts conservatively. A *small* std would mean steady, predictable sales. |
| **min** | 0.00 | A **$0 line inside a paid checkout = red flag** → audit for pricing bugs, unapplied discounts, or fraud. |
| **max** | 669.34 | Your **single biggest order → a whale/VIP** → a loyalty-reward or bulk-buy-program target (and the top candidate to verify as a genuine outlier vs. a typo). |

> **The pattern:** `count` and `max` → **QA / integrity** · `mean` → **revenue & forecasting** · `median` → **the real "typical" customer** · `Q1/Q3 + std` → **segmentation, risk & anomaly fences** · `min` → **fraud/bug checks**. One function, six different decisions.

### 💰 The column that tells the business story: `sales_cost`

Focus on the **last column** (`sales_cost`) — it's the money, and it's a textbook case study:

- **mean = 40.25** but **median = 23.18** → the average is *nearly double* the typical value. **That gap is the tell-tale sign of a right-skewed distribution**: most transactions are cheap, a few are very expensive, and the few expensive ones drag the mean upward.
- **min = 0.00** → free/zero-price lines exist (promotions, returns, gifts).
- **max = 669.34** → the single priciest line is **~16× the median**. That's your **outlier** (more in Section 5).
- **Q1 = 11.42, Q3 = 45.98** → a "normal" transaction lands roughly **between 11 and 46**. Anything far beyond 46 on the high end deserves a look.
- **std = 54.60** → spread is *larger than the mean itself*. Another way of saying **"this data is wildly varied / has a fat tail."**

> **One-sentence read of `describe()` on `sales_cost`:** *"Most baskets cost ~$23, a typical one is $11–$46, but a handful run to $669 — and those heavy tails are what we must understand (or clean) before trusting any average."*

### ⚠️ Two things `describe()` quietly does

1. **It only summarizes *numeric* columns by default.** A text column like `gender` would be skipped. To see everything, use `describe(include="all")` (the script's second call).
2. **The `transaction_id` column is misleading "statistically."** Its mean (4.36e+11), min, max are just huge receipt numbers — mathematically valid but **meaningless**. `describe()` doesn't know a column is just an *ID*; **you** have to. (Same goes for `customer_id` and `product_area_id` — their "mean 429" means nothing.) *Lesson: `describe()` gives you numbers; reading it well is your job.*

---

## 4. Real-Life Applications (Where This Shows Up in Companies)

Every line in this script is a **micro-version of a real analyst task**. Here's the mapping:

| Script function | The real company question it answers | Job / team that cares |
| --- | --- | --- |
| `shape` | "Did the export actually load? Is this week's file bigger than last week's?" (a sudden drop = broken pipeline) | Data Engineering / Ops |
| `head` / `tail` | "When did sales start and end? Is the newest day's data arriving?" | Analyst, 30-sec health check |
| `sample` | "Give me a random 10 receipts for a manual quality audit" | QA / Data Validation |
| `describe` | "What's our **typical** basket value, and how variable is it, per month? Did average order value drop last month?" | **Revenue / Finance / Sales** |
| `nlargest` / `nsmallest` | "Who are our top-spending customers? (so we can give them a VIP deal)" + "are we leaking money in 0.01-cent refunds?" | **Marketing / CRM** |
| `nunique` | "We claim 5 product departments — the data agrees (5). And we really have 870 active members." | Data quality / Reporting |
| `isna().sum()` | "Our loyalty CRM has 8 customers missing a credit score — we can't approve those before we impute or flag them." | **Risk / Credit / CRM** |

### Concrete "use case" you could actually build from *this exact data*

1. **Customer value tiers (80/20 rule).** Group `transactions` by `customer_id`, sum `sales_cost`, rank. You'd find a small handful of "whales" (top customer spends **$10,422**) who drive disproportionate revenue → target them with loyalty perks.
2. **Store location decision.** Join `transactions` + `customer_details` on `customer_id`, then plot `distance_from_store` vs. total spend. *Do far customers buy less?* That's the input to "should we open/demolish a store?"
3. **Credit & churn risk.** `credit_score` (low = risky) + purchase frequency → **predict which customers will churn or default**. This is literally a classic machine-learning dataset.
4. **Pricing / promo sanity check.** The `0.00` and `0.01` lines → audit for **pricing bugs, unapplied discounts, or fraud** (a $0 line in a paid checkout is usually a mistake worth catching).
5. **Seasonality.** `transaction_date` → bucket by month (`2020-04 … 2020-09`) and chart. (Our counts are ~6,300–6,500 per month — a flat season. A spikier retail item would reveal peaks you'd stock for.)

> **The "superpower" frame:** a company does not *have* "insights." It has raw rows like yours. Pandas is the tool that turns **38,000 receipts** into the one or two numbers a manager actually makes decisions on. That transformation — *meet the data → summarize → spot the odd bits → answer the money question* — is the entire Day-48 skill.

---

## 5. Outliers — What, Why, and Where They Live in *This* Data

### What is an outlier?

An **outlier** is a data point that is **far from the majority** of the data — a value so high or so low that it looks like it "doesn't belong" with its neighbors. Two reasons a value can be an outlier:

1. **It's a real, legitimate extreme** (a genuine bulk buyer, a one-off mega-order).
2. **It's an error** — a typo, a wrong unit, a system glitch (someone typed 310 instead of 30; a distance recorded in a different unit).

**The crucial point:** you usually **can't tell which until you investigate**, which is exactly why finding them is a *goal*, not a nuisance.

### The standard tool: the IQR (Interquartile Range) rule

```
IQR   = Q3 − Q1
Lower fence = Q1 − 1.5 × IQR
Upper fence = Q3 + 1.5 × IQR
Anything below the lower fence OR above the upper fence → OUTLIER
```

The **1.5 × IQR** is the industry-standard "fence." (Box plots literally draw a "whisker" at this boundary.)

### Applying it to **this** data

**A) `sales_cost` (money)**
- Q1 = 11.42, Q3 = 45.98 → **IQR = 34.56**
- Upper fence = 45.98 + (1.5 × 34.56) = **97.82**
- Lower fence = 11.42 − (1.5 × 34.56) = **−40.42** → a negative "floor," which is **impossible** for a price. So there are **no low-side outliers** (the min is $0, a legitimate free item).
- **Rows above $97.82 → 3,342 rows (≈8.7%)** flag as high-side outliers. The absolute peak is the **$669.34** line (27 items, `product_area_id = 1`).
- **Why it's classed as an outlier:** a "typical" basket costs $11–$46. A $669 line is **7× the upper quartile** — statistically extreme. *Interpretation:* probably a **bulk/household stock-up** (real) — worth a VIP look, not a delete.

**B) `num_items` (quantity)**
- Q1 = 2, Q3 = 8 → IQR = 6 → **upper fence = 8 + 9 = 17**
- **max = 310** items in one line — a **textbook outlier** (39× the fence). The top few: 310, 79, 79, 62, 61, 61…
- **Why an outlier:** the *median* order is **4** items. 310 in a single line is almost certainly **legitimate bulk (business/wholesale) OR a data entry error** — exactly the ambiguity I warned about. 1,998 rows sit above the fence.
- (Also note: a 310-item order produced `sales_cost = 557.73` — that's a cheap-per-item bulk buy, consistent with wholesale.)

**C) `distance_from_store` — the surprise outlier**
- Q1 = 0.74, Q3 = 2.94, median = 1.66 → IQR = 2.20 → **upper fence ≈ 6.24**
- **max = 400.97** — **64× the fence!** This is the most dramatic outlier in the whole file.
- **Why an outlier / what it likely means:** everyone else is within a few km. A **400.97** is almost certainly **a data-entry error or a wrong unit** (e.g. recorded in a different scale, or a far-away customer's address). This is precisely the kind of thing that, if left alone, would **silently wreck** any distance-based model — which is why `describe()`/`nlargest()` flagging it matters *before* you build anything.

### A second "smoke test" for outliers: the mean vs. median gap

A **quick-and-dirty** outlier detector you can eyeball from `describe()` alone:

> If **mean ≫ median** (or mean ≪ median) for a column that *shouldn't* be skewed, **something is pulling the mean** → likely high-side outliers.

`sales_cost` is the perfect example: **mean 40.25 vs median 23.18** → big gap → right tail is heavy → outliers live at the top. `num_items`: **mean 6.19 vs median 4** → same story. This two-number check is how you decide *which column is worth* running the full IQR test on.

### What do you *do* with an outlier? (Never just "delete")

1. **Investigate** — is it real or an error? (`400.97` distance → fix the source.)
2. **If it's a real, meaningful extreme** → keep it, but report the **median** (robust) instead of the mean, or analyze the tail separately (VIP/bulk segment).
3. **If it's an error** → correct it, or if uncorrectable, remove / cap it.
4. **Cap it (winsorize)** → e.g., "treat anything above the fence as the fence value" so one monster row can't distort an average.

---

## 6. The Superpowers of Pandas (Concepts This Script Hints At)

The script only shows the surface. Here are the **"superpowers" layered directly on top of what you just learned** — the move from *understanding* data to *manipulating* it. Each is a one-liner you'll reach for constantly.

### 6.1 The `.dt` accessor — do *real date math*

The `transaction_date` column is a **true datetime** (see the `datetime64[us]` type in `dtypes`), not a string. That unlocks:

```python
transactions.dt.month          # 4 5 6 7 8 9 ...
transactions.groupby(transactions.transaction_date.dt.to_period("M")).sales_cost.sum()
# -> total revenue PER MONTH, the #1 "sales trend" question.
```

You can slice by **Year / Month / Quarter / Day / Weekday** and instantly build a sales-trend report. *(We used this: revenue is ~6,300 receipts/month, pretty flat across Apr–Sep 2020.)*

### 6.2 `groupby` — the "pivot-table" superpower

> "Group rows by X, then do Y to each group."

```python
transactions.groupby("product_area_id").sales_cost.sum()      # revenue by department
transactions.groupby("customer_id").sales_cost.nlargest(5)    # top 5 spenders
transactions.groupby("customer_id").num_items.sum()            # total items per customer
```

This one method is responsible for **~half of all business analysis** (revenue by category, by region, by month, by customer…). It's the programmatic version of Excel Pivot Tables.

### 6.3 Boolean masking — filter with *questions*, not just values

Every column can answer **True/False** questions, and stacking them filters rows:

```python
high_value   = transactions[transactions.sales_cost > 97.82]        # the outliers!
big_baskets  = transactions[transactions.num_items > 17]            # the quantity outliers
april_only   = transactions[transactions.transaction_date.dt.month == 4]
```

**This is how you turn `describe()`'s findings into action:** the IQR fence we computed (97.82) plugs straight into a mask to *extract* the 3,342 outlier rows for a report.

### 6.4 `merge` / `join` — combine the two sheets on their key

Recall the shared `customer_id`? That's the **join key**. Merging turns two small tables into one rich table ("every purchase, tagged with the customer's credit score & distance"):

```python
full = pd.merge(transactions, customer_details, on="customer_id")
```

Now `full` has 10 columns and you can ask: *"do low-credit customers buy more on credit?"* — a question impossible without merging. This is the bridge from "exploring" to **modeling**.

### 6.5 `.value_counts()` — frequency of categories (the "mode")

```python
transactions.product_area_id.value_counts()   # which department is hottest?
customer_details.gender.value_counts()        # F / M / NaN mix
```

We used it: departments 3 (8,699) and 2 (8,473) dominate; customer base is slightly more female (485 F vs 380 M, with 5 unknown). **`value_counts` is `describe` for *non-numeric* columns.**

### 6.6 `dtypes` — read the "type" of each column

```python
transactions.dtypes
```

Gave us: `int64`, `datetime64[us]`, `float64`. Your **first** call on any dataset — the type tells you what operations are legal (you can average `sales_cost` (a number) but a `mean` on `gender` (text) is nonsense — remember how `describe` silently skipped it).

### 6.7 The full EDA toolkit, in order

If a dataset lands on your desk tomorrow, this is the **repeatable checklist** (all of it one-liners in Pandas):

1. `df.shape` — how big?
2. `df.dtypes` — what's each column's type? (spot text vs number vs date)
3. `df.head()` — eyeball a few rows.
4. `df.describe(include="all")` — the five-number summary for every column.
5. `df.isna().sum()` — how many holes per column?
6. `df.nunique()` — categorical or continuous?
7. `df.<col>.value_counts()` (for low-unique cols) / `.describe()` (for numeric)
8. `nlargest` / `nsmallest` + IQR fences → **find outliers**.
9. *Then* ask the business question with `groupby` / masks / `merge`.

Run those nine on *any* table and you go from "what is this file?" to "here's what it's telling us" in minutes. That's the Day-48 skill in one paragraph.

---

## 7. Cheat Sheet (one screen)

| I want to… | Code |
| --- | --- |
| Size of the table | `df.shape` |
| First / last rows | `df.head(n)` / `df.tail(n)` |
| Random sample | `df.sample(n)` or `df.sample(frac=0.1)` |
| Column types | `df.dtypes` |
| **Numeric summary** | `df.describe()` |
| Summary for *everything* | `df.describe(include="all")` |
| Top / bottom n rows by a column | `df.nlargest(n, "col")` / `df.nsmallest(n, "col")` |
| Distinct values per column | `df.nunique()` |
| Missing values | `df.isna().sum()` |
| "Is it missing?" full grid | `df.isna()` |
| Frequency of categories | `df["col"].value_counts()` |
| Revenue by group | `df.groupby("col").other.sum()` |
| Date parts (month, quarter…) | `df["date"].dt.month`, `.dt.to_period("M")` |
| Filter with a condition | `df[df.col > 97.82]` |
| Join two tables on a key | `pd.merge(dfA, dfB, on="customer_id")` |
| **Outlier fence (IQR)** | `q3 + 1.5*(q3-q1)` then `df[df.col > fence]` |

---

## 8. Recap

- **`shape, head/tail, sample, dtypes`** → *meet* the data.
- **`describe()`** → *summarize* it (mean, median, quartiles, std, min, max). Learn to read the **mean-vs-median gap** as an outlier/skew alarm.
- **`nunique(), value_counts()`** → learn the *shape* (categorical vs continuous) of each column.
- **`isna().sum()`** → quantify *dirtiness* (missingness) before trusting anything.
- **`nlargest/nsmallest` + IQR** → *find* the odd values, then **investigate** whether each is real or an error — don't auto-delete.
- **`groupby, masks, dt, merge`** → the *superpowers* that turn a summary into **business decisions**: revenue by month/customer/department, outlier reports, and joined customer+purchase tables.

You have now gone from **38,506 raw receipts** to a set of concrete, decision-ready facts (typical basket ≈ $23; 870 customers; a few whale spenders; a suspicious 400 km "distance" to fix; ~8.7% high-value orders to study). *That* is the entire loop a data professional runs every single day.
