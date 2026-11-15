I checked the workspace: `DSI/Day-135/Unsupervised_Learning_Association_Rule_Learning.md` and `404_Association_Rules_Apriori.py` already exist. Below is a fuller, beginner-friendly version. **Note:** I'm in Ask mode (read-only), so I can't write the `.md` or `.py` files myself — switch to Code mode and I'll save them (suggested paths: `DSI/Day-137/Unsupervised_Learning_Association_Rule_Learning.md` and `DSI/Day-137/association_rules_example.py`). The complete content is below, ready to copy.

---

# Unsupervised Learning: Association Rule Learning (Practical)

## 1. What Is It (and Why "Unsupervised"?)

**Association Rule Learning** is an unsupervised learning technique that finds rules of the form:

> **If** a customer buys item A **→ then** they are likely to buy item B

It is called _unsupervised_ because there are **no labels** — you don't tell the algorithm "this is a correct rule." You only give it raw transaction data and let it discover patterns.

The classic story: a supermarket found that **beer and diapers** were often bought together, so it placed them near each other and boosted sales.

**Formal definition:** Given a set of transactions `T` and items `I`, find all rules `X → Y` (where `X, Y ⊆ I`) that satisfy minimum thresholds for **support**, **confidence**, and **lift**.

---

## 2. Business Use Cases (What Companies Do With It)

| Industry             | Data                | What the rule tells them               | Business action                                       |
| -------------------- | ------------------- | -------------------------------------- | ----------------------------------------------------- |
| **Retail / Grocery** | Receipts            | Bread → Butter (support 5%, lift 3.2)  | Place items near each other, bundle discount          |
| **E-commerce**       | Click/purchase logs | "Customers who bought X also bought Y" | Product recommendations, "Frequently bought together" |
| **Streaming**        | Watch history       | Viewers of Show A also watch Show B    | Homepage rows, "Because you watched..."               |
| **Banking**          | Card transactions   | Café → Bookstore in the same trip      | Fraud detection, targeted offers                      |
| **Telecom**          | Service bundles     | Internet → Landline bundle             | Upsell bundles, reduce churn                          |
| **Healthcare**       | Patient records     | Diagnosis A → Prescription B           | Clinical decision support                             |
| **Web analytics**    | Session pages       | Page A → Page B                        | Site navigation optimization, A/B test ideas          |
| **Manufacturing**    | Maintenance logs    | Part failure A → Part failure B        | Predictive maintenance, spare parts stocking          |

**The killer business insight:** rules with **high lift** reveal _non-obvious_ relationships that drive bundling, layout, pricing, and recommendation strategy.

---

## 3. Data Structure: The Transaction Table

Association rules need data shaped as **one row per transaction**, with items as columns:

| Transaction | Bread | Milk | Diaper | Beer | Eggs |
| ----------- | ----- | ---- | ------ | ---- | ---- |
| 1           | 1     | 1    | 0      | 0    | 1    |
| 2           | 1     | 0    | 1      | 1    | 0    |
| 3           | 1     | 1    | 0      | 0    | 1    |
| 4           | 0     | 1    | 1      | 1    | 0    |

`1` = item present, `0` = absent. This "basket" format is what `mlxtend` expects.

**Core vocabulary:**

- **Itemset**: a group of items, e.g. `{Milk, Bread}`
- **Antecedent (LHS)**: the "if" part, e.g. `Milk`
- **Consequent (RHS)**: the "then" part, e.g. `Bread`
- **Rule**: `Milk → Bread`

---

## 4. The Four Key Metrics (With Formulas Broken Down)

### 4.1 Support

> **How popular is this combination across ALL transactions?**

$$\text{Support}(X) = \frac{\text{transactions containing } X}{\text{total transactions}}$$

- `Support({Milk, Bread}) = 3 / 4 = 0.75` → 75% of all baskets contain both.
- Used to **filter out rare, meaningless pairs**. A rule about two items that co-occur 0.1% of the time is noise.
- Typical thresholds: 0.01–0.1 (1%–10%) depending on dataset size.

### 4.2 Confidence

> **When X is bought, how often is Y also bought?**

$$\text{Confidence}(X \to Y) = \frac{\text{Support}(X \cup Y)}{\text{Support}(X)} = \frac{P(X \cap Y)}{P(X)}$$

- `Confidence(Milk → Bread) = 3/3 = 1.0` → 100% of Milk buyers also bought Bread.
- But careful: `Confidence(Bread → Milk) = 3/3 = 1.0` too — confidence is **directional and asymmetric**.

### 4.3 Lift

> **How much MORE likely is Y when X is bought, vs. random chance?**

$$\text{Lift}(X \to Y) = \frac{\text{Confidence}(X \to Y)}{\text{Support}(Y)}$$

- `Lift = 1` → X and Y are **independent** (no relationship).
- `Lift > 1` → X **increases** the chance of Y (positive association).
- `Lift < 1` → X **decreases** the chance of Y (negative association — useful for substitution analysis).
- **Lift is the most important metric for business decisions** because it removes popularity bias. Bread is popular, so a high-confidence rule for bread might be trivial; lift corrects that.

### 4.4 Leverage (bonus)

$$\text{Leverage} = \text{Support}(X \cup Y) - \text{Support}(X)\times\text{Support}(Y)$$

- `Leverage > 0` → positive association, `0` → independent.
- Unlike lift, leverage is not inflated when Y is rare.

### Worked Example

| Metric     | Formula                      | Numbers         | Result | Meaning                       |
| ---------- | ---------------------------- | --------------- | ------ | ----------------------------- |
| Support    | both / total                 | 3/4             | 0.75   | 75% of baskets have both      |
| Confidence | both / X only                | 3/3             | 1.0    | Every Milk buyer bought Bread |
| Lift       | conf / support(Y)            | 1.0 / 0.75      | 1.33   | 33% more likely than chance   |
| Leverage   | supp(both) − supp(X)·supp(Y) | 0.75 − 1.0×0.75 | 0.0    | No extra association          |

---

## 5. The Apriori Algorithm (How It Works)

**Goal:** Find all itemsets that appear in at least `min_support` of transactions, then turn them into rules.

**Key insight (Downward Closure / Apriori Principle):**

> If `{Milk, Bread, Eggs}` is frequent, then `{Milk, Bread}`, `{Milk, Eggs}`, `{Bread, Eggs}` MUST also be frequent. Any subset of a frequent itemset is frequent.

**Algorithm steps:**

1. Count individual items → keep those above `min_support` (**1-itemsets**).
2. Combine surviving items into pairs → count → keep frequent (**2-itemsets**).
3. Repeat: generate candidates of size k from frequent (k-1)-itemsets → prune → keep frequent.
4. For each frequent itemset, generate all rules and compute **confidence** and **lift**.
5. Keep rules passing `min_confidence` and `min_lift` thresholds.

**Complexity note:** Apriori is slow on dense data with low thresholds. For large datasets use **FP-Growth** (faster) or **ECLAT** (depth-first).

---

## 6. Practical Example (Runnable Code)

### 6.1 Setup

```bash
pip install pandas mlxtend matplotlib networkx
```

### 6.2 Full Script — `association_rules_example.py`

```python
"""
Association Rule Learning - Practical Example
=============================================
A complete, runnable script that:
  1. Builds a synthetic grocery transaction dataset
  2. One-hot encodes it (basket format)
  3. Finds frequent itemsets with Apriori
  4. Generates association rules (support / confidence / lift)
  5. Filters, sorts, and visualizes the best rules
  6. Prints a business-friendly interpretation

Each line of code has an explanatory comment.
"""

# -------------------------------------------------------------
# 1. Import libraries
# -------------------------------------------------------------
import pandas as pd                                  # for data tables
import numpy as np                                   # for random numbers
import matplotlib.pyplot as plt                      # for plotting
from mlxtend.frequent_patterns import apriori, association_rules  # ARL algorithms
from mlxtend.preprocessing import TransactionEncoder              # basket encoder

# -------------------------------------------------------------
# 2. Build a synthetic grocery dataset
# -------------------------------------------------------------
# In a real project you'd load a CSV of transactions.
# Here we simulate 2,000 receipts to keep the script self-contained.

np.random.seed(42)          # reproducible randomness

n_transactions = 2000       # how many receipts to simulate

# Item popularity (some items sell more often than others)
items = ["Bread", "Milk", "Diaper", "Beer", "Eggs", "Butter", "Cereal"]

# Probability each item appears in a random basket (rough real-world popularity)
p = {"Bread": 0.55, "Milk": 0.50, "Diaper": 0.30, "Beer": 0.35,
     "Eggs": 0.40, "Butter": 0.25, "Cereal": 0.20}

# Generate random 0/1 data: rows = transactions, columns = items
data = np.random.rand(n_transactions, len(items))   # random numbers 0..1

# Convert to 0/1: 1 if random number < item's probability, else 0
basket = (data < np.array([p[i] for i in items])).astype(int)

# Wrap into a labeled DataFrame
df = pd.DataFrame(basket, columns=items)

# Inject a *deliberate* association: anyone buying Diaper also tends to buy Beer
# (this is the classic "beer and diapers" pattern we want Apriori to discover)
mask = df["Diaper"] == 1                              # rows where Diaper is bought
df.loc[mask, "Beer"] = np.random.rand(mask.sum()) < 0.85  # 85% of them also get Beer

print("First 5 transactions (1 = item in basket, 0 = not):")
print(df.head())
print("\nDataset shape:", df.shape)                   # (2000 rows, 7 items)

# -------------------------------------------------------------
# 3. Find frequent itemsets with Apriori
# -------------------------------------------------------------
# apriori() scans the basket and returns every itemset whose support
# is at least `min_support` (here 2% of all 2,000 receipts = 40 receipts).

frequent_itemsets = apriori(df, min_support=0.02, use_colnames=True)

print("\nFrequent itemsets found:", len(frequent_itemsets))
print(frequent_itemsets.sort_values("support", ascending=False).head(10))

# -------------------------------------------------------------
# 4. Generate association rules from the frequent itemsets
# -------------------------------------------------------------
# association_rules() takes each frequent itemset, splits it into
# antecedent (if) and consequent (then) parts, and computes
# support, confidence, lift, and leverage for every split.

rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

print("\nNumber of rules:", len(rules))

# -------------------------------------------------------------
# 5. Clean up and display the most interesting rules
# -------------------------------------------------------------
# mlxtend stores items as frozensets (immutable sets); convert to readable text.
rules["antecedents"] = rules["antecedents"].apply(lambda s: ", ".join(sorted(s)))
rules["consequents"] = rules["consequents"].apply(lambda s: ", ".join(sorted(s)))

# Keep only the columns a business stakeholder cares about
rules = rules[["antecedents", "consequents", "support", "confidence", "lift"]]

# Sort by lift: the strongest non-obvious associations float to the top
rules = rules.sort_values("lift", ascending=False).reset_index(drop=True)

print("\nTop 10 rules by lift:")
print(rules.head(10).to_string(index=False))

# -------------------------------------------------------------
# 6. Focus on a business question: "What drives Beer sales?"
# -------------------------------------------------------------
# Filter for rules where Beer is the CONSEQUENT (what we want to sell more of)
beer_rules = rules[rules["consequents"] == "Beer"].sort_values("lift", ascending=False)

print("\nRules that lead to a Beer purchase:")
print(beer_rules.head(10).to_string(index=False))

# -------------------------------------------------------------
# 7. Visualize the results
# -------------------------------------------------------------
# Plot 1: scatter of support vs confidence, sized by lift
plt.figure(figsize=(9, 6))
plt.scatter(rules["support"], rules["confidence"],
            s=rules["lift"] * 15, alpha=0.6, edgecolors="k")
plt.xlabel("Support (how common the combination is)")
plt.ylabel("Confidence (how often RHS follows LHS)")
plt.title("Association Rules: Support vs Confidence (bubble size = lift)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Plot 2: top 8 rules by lift as a bar chart
top = rules.head(8).copy()
top["rule"] = top["antecedents"] + " -> " + top["consequents"]
plt.figure(figsize=(10, 6))
plt.barh(top["rule"][::-1], top["lift"][::-1], color="steelblue")
plt.xlabel("Lift (>1 means positive association)")
plt.title("Top 8 Association Rules by Lift")
plt.tight_layout()
plt.show()

# -------------------------------------------------------------
# 8. Business interpretation (what a company would do)
# -------------------------------------------------------------
print("\n" + "=" * 60)
print("BUSINESS TAKEAWAYS")
print("=" * 60)
print("""
- Rules with lift > 1 reveal items that are bought together more
  often than chance. These are your bundling / layout candidates.
- High support  -> the pattern is common enough to act on at scale.
- High confidence -> when a customer buys the antecedent, the
  consequent is very likely; useful for recommendation prompts.
- High lift with low support -> a niche but strong combo; good for
  targeted promotions, not store-wide layout changes.

Example actions:
1. Place high-lift items near each other (store layout).
2. Create "Frequently bought together" bundles (e-commerce).
3. Show "Customers who bought X also bought Y" (recommendations).
4. Design targeted discounts on the consequent when antecedent is bought.
""")

# -------------------------------------------------------------
# 9. (Optional) Network graph of the top rules
# -------------------------------------------------------------
try:
    import networkx as nx

    G = nx.DiGraph()                                  # directed graph
    for _, r in rules.head(15).iterrows():
        G.add_edge(r["antecedents"], r["consequents"], weight=round(r["lift"], 2))

    plt.figure(figsize=(9, 7))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="lightblue",
            node_size=1500, font_size=9, arrows=True)
    plt.title("Association Rules as a Graph (top 15 rules)")
    plt.tight_layout()
    plt.show()
except ImportError:
    print("Install networkx to see the graph: pip install networkx")
```

### 6.3 Alternative: Using `apyori` (the Day-135 style)

```python
import pandas as pd
from apyori import apriori

# apyori expects a list of lists: one inner list per transaction
transactions = [
    ["Bread", "Milk"],
    ["Bread", "Milk", "Diaper", "Beer"],
    ["Milk", "Diaper", "Beer"],
    ["Bread", "Eggs"],
]

# Run Apriori with thresholds
rules = apriori(transactions,
                min_support=0.5,     # item must appear in >= 50% of baskets
                min_confidence=0.5,  # rule must be right >= 50% of the time
                min_lift=1.0,        # keep only positive associations
                max_length=2)        # rules with at most 2 items total

# Convert the generator into a list of results
results = list(rules)

# Extract readable rules
for rule in results:
    for pair in rule.ordered_statistics:
        if pair.items[0] != pair.items[1]:          # skip self-rules
            print(f"{list(pair.items[0])} -> {list(pair.items[1])} | "
                  f"support={rule.support:.2f} "
                  f"confidence={pair.confidence:.2f} "
                  f"lift={pair.lift:.2f}")
```

---

## 7. Interpreting Results Like a Data Scientist

When you get output like:

| Antecedent | Consequent | Support | Confidence | Lift |
| ---------- | ---------- | ------- | ---------- | ---- |
| Diaper     | Beer       | 0.26    | 0.85       | 2.43 |
| Milk       | Bread      | 0.28    | 0.95       | 1.73 |
| Eggs       | Bread      | 0.22    | 0.80       | 1.45 |

Ask three questions:

1. **Is it common enough to matter?** (support) — 0.26 means ~1 in 4 baskets. Yes.
2. **Is the relationship real or just popularity?** (lift) — 2.43 means Diaper buyers are 2.4× more likely to buy Beer than average. Strong.
3. **What do we do with it?** — Bundle "Diaper + Beer" with 10% off, or place them in the same aisle.

**Red flags to watch for:**

- **High confidence but lift ≈ 1** → the rule is trivial (consequent is just popular). Ignore.
- **Lift < 1** → items are substitutes, not complements (e.g., buying Coke _reduces_ Pepsi purchases). Useful for assortment planning.
- **Very low support** → statistically fragile; the "rule" may be a fluke.
- **Too many rules** → raise `min_support` / `min_lift`, or restrict to a business question (e.g., only rules where consequent = a target product).

---

## 8. Practical Workflow for a Real Project

1. **Define the business question first.** "Which items should we bundle?" beats "Find all rules."
2. **Collect transaction data** — receipts, clickstreams, or service logs.
3. **Clean and one-hot encode** — remove returns/cancellations, handle missing values.
4. **Run Apriori / FP-Growth** with thresholds tuned to your data size.
5. **Filter by business relevance** — e.g., `consequents == target_product`.
6. **Sort by lift** and validate with a domain expert (does this make sense?).
7. **A/B test the recommendation** — e.g., show the bundle to 50% of users, measure lift in revenue.
8. **Monitor and retrain** — buying patterns shift seasonally.

---

## 9. Common Pitfalls

| Pitfall                         | Why it hurts                       | Fix                                                    |
| ------------------------------- | ---------------------------------- | ------------------------------------------------------ |
| Using accuracy/confidence alone | Popular items dominate             | Always check **lift**                                  |
| Support too low                 | Noise, overfitted rules            | Raise `min_support`, require minimum absolute count    |
| Ignoring data leakage           | Returned items look like purchases | Clean transactions before encoding                     |
| Too many rules                  | Analysis paralysis                 | Filter by target consequent, sort by lift, cap results |
| Assuming causation              | Correlation ≠ causation            | A/B test before rolling out                            |
| Cold-start categories           | New products have no history       | Use content-based similarity instead                   |

---

## 10. Cheat Sheet

```text
Goal:            Find items bought together -> bundle / recommend / layout
Data shape:      one row = one transaction, columns = items, 0/1 values
Metrics:
  support       = P(A and B)              "how common is the combo"
  confidence    = P(B | A) = supp(A,B)/supp(A)   "how reliable is the rule"
  lift          = confidence / supp(B)    ">1 = positive; core business metric"
  leverage      = supp(A,B) - supp(A)*supp(B)
Algorithms:      Apriori (simple), FP-Growth (fast), ECLAT (dense data)
Key params:      min_support, min_confidence, min_lift, max_length
Filter:          rules[rules["consequents"] == "target_item"]
Visualize:       scatter (support vs confidence, size=lift), barh(lift), network graph
Validate:        A/B test the resulting bundles/recommendations
```

---
