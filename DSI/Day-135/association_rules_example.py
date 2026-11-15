# cspell:ignore mlxtend apriori apyori frequent_patterns itemsets
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

The script works in two modes:
  * If `mlxtend` is installed  -> uses the real `apriori` / `association_rules`.
  * If `mlxtend` is missing    -> uses the pure-pandas fallback defined below,
                                 so the lesson still runs anywhere.
"""

# -------------------------------------------------------------
# 1. Import libraries
# -------------------------------------------------------------
import itertools  # used by the fallback rule generator (combinations)

import matplotlib.pyplot as plt  # for plotting
import numpy as np  # for random numbers
import pandas as pd  # for data tables

# ARL algorithms (Apriori + rule generation).
# `pyright: ignore` silences the "import could not be resolved" warning when
# mlxtend is not installed in the environment, because the import below is
# already guarded by a try/except at runtime.
try:
    # pyright: ignore[reportMissingImports]
    from mlxtend.frequent_patterns import apriori, association_rules

    HAS_MLXTEND = True
except ModuleNotFoundError as exc:
    if exc.name != "mlxtend":
        raise
    HAS_MLXTEND = False
    print("mlxtend not installed -> using the built-in pandas fallback.\n")


# -------------------------------------------------------------
# 2. Fallback implementation (only used when mlxtend is absent)
# -------------------------------------------------------------
def _subsets(items, size):
    """Return every subset of `items` that has exactly `size` elements."""
    return (frozenset(c) for c in itertools.combinations(items, size))


def apriori_fallback(df, min_support=0.02, max_len=3):
    """Minimal Apriori: returns frequent itemsets with their support.

    Mirrors the output of `mlxtend.frequent_patterns.apriori`:
    a DataFrame with columns ["itemsets", "support"].
    """
    n_rows = len(df)  # total number of transactions
    mat = {col: df[col].to_numpy(dtype=bool) for col in df.columns}

    # Level 1: count each single item, keep the frequent ones
    level = {frozenset([c]): int(mat[c].sum()) for c in df.columns}
    level = {k: v for k, v in level.items() if v / n_rows >= min_support}
    all_itemsets = dict(level)  # accumulate every frequent itemset found

    k = 2
    while level and k <= max_len:
        keys = list(level)
        # Join step: union pairs of frequent (k-1)-itemsets into k-itemsets
        candidates = {
            a | b
            for a, b in itertools.combinations(keys, 2)
            if len(a | b) == k
        }
        # Prune step: every (k-1)-subset of a candidate must itself be frequent
        candidates = {
            c
            for c in candidates
            if all(s in all_itemsets for s in _subsets(c, k - 1))
        }

        # Count how many transactions contain all items of each candidate
        next_level = {}
        for c in candidates:
            mask = np.ones(n_rows, dtype=bool)
            for item in c:
                mask &= mat[item]
            count = int(mask.sum())
            if count / n_rows >= min_support:
                next_level[c] = count

        all_itemsets.update(next_level)  # keep them for rule generation
        level = next_level
        k += 1

    # Convert to the same shape mlxtend returns
    return pd.DataFrame(
        [
            {"itemsets": itemset, "support": count / n_rows}
            for itemset, count in all_itemsets.items()
        ]
    )


def association_rules_fallback(frequent_itemsets, min_threshold=1.0):
    """Turn frequent itemsets into rules and compute support/confidence/lift.

    Mirrors `mlxtend.frequent_patterns.association_rules` columns:
    antecedents, consequents, support, confidence, lift, leverage.
    """
    support_map = {
        frozenset(row["itemsets"]): row["support"]
        for _, row in frequent_itemsets.iterrows()
    }

    records = []
    for itemset, supp_both in support_map.items():
        if len(itemset) < 2:  # a single item can never form a rule
            continue
        # Try every way of splitting the itemset into "if" and "then" parts
        for size in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, size):
                ant = frozenset(antecedent)
                con = itemset - ant
                if not con:
                    continue
                supp_a = support_map.get(ant, 0)  # P(A)
                supp_c = support_map.get(con, 0)  # P(C)
                if supp_a == 0 or supp_c == 0:
                    continue
                confidence = supp_both / supp_a  # P(A and C) / P(A)
                lift = confidence / supp_c  # confidence / P(C)
                if lift >= min_threshold:
                    records.append(
                        {
                            "antecedents": ant,
                            "consequents": con,
                            "support": supp_both,
                            "confidence": confidence,
                            "lift": lift,
                            "leverage": supp_both - supp_a * supp_c,
                        }
                    )

    columns = [
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "lift",
        "leverage",
    ]
    if not records:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(records, columns=columns)


def find_rules(df, min_support=0.02, max_len=3, min_lift=1.0):
    """Run Apriori + rule generation, using mlxtend when available."""
    if HAS_MLXTEND:
        frequent_itemsets = apriori(
            df, min_support=min_support, use_colnames=True, max_len=max_len
        )
        return association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    frequent_itemsets = apriori_fallback(df, min_support=min_support, max_len=max_len)
    return association_rules_fallback(frequent_itemsets, min_threshold=min_lift)


# -------------------------------------------------------------
# 3. Build a synthetic grocery dataset
# -------------------------------------------------------------
# In a real project you'd load a CSV of transactions.
# Here we simulate 2,000 receipts to keep the script self-contained.

np.random.seed(42)  # reproducible randomness

n_transactions = 2000  # how many receipts to simulate

# Item popularity (some items sell more often than others)
items = ["Bread", "Milk", "Diaper", "Beer", "Eggs", "Butter", "Cereal"]

# Probability each item appears in a random basket (rough real-world popularity)
p = {
    "Bread": 0.55,
    "Milk": 0.50,
    "Diaper": 0.30,
    "Beer": 0.35,
    "Eggs": 0.40,
    "Butter": 0.25,
    "Cereal": 0.20,
}

# Generate random 0/1 data: rows = transactions, columns = items
data = np.random.rand(n_transactions, len(items))  # random numbers 0..1

# Convert to 0/1: 1 if random number < item's probability, else 0
basket = (data < np.array([p[i] for i in items])).astype(int)

# Wrap into a labeled DataFrame
df = pd.DataFrame(basket, columns=items)

# Inject a *deliberate* association: anyone buying Diaper also tends to buy Beer
# (this is the classic "beer and diapers" pattern we want Apriori to discover)
mask = df["Diaper"] == 1  # rows where Diaper is bought
# `.astype(int)` keeps the column numeric so Apriori counts it correctly
df.loc[mask, "Beer"] = (np.random.rand(mask.sum()) < 0.85).astype(int)

print("First 5 transactions (1 = item in basket, 0 = not):")
print(df.head())
print("\nDataset shape:", df.shape)  # (2000 rows, 7 items)

# -------------------------------------------------------------
# 4. Find frequent itemsets with Apriori
# -------------------------------------------------------------
# apriori() scans the basket and returns every itemset whose support
# is at least `min_support` (here 2% of all 2,000 receipts = 40 receipts).

rules = find_rules(df, min_support=0.02, max_len=3, min_lift=1.0)

print("\nNumber of rules:", len(rules))

# -------------------------------------------------------------
# 5. Clean up and display the most interesting rules
# -------------------------------------------------------------
if rules.empty:
    print("No rules found - try lowering min_support or min_lift.")
else:
    # mlxtend stores items as frozensets (immutable sets); convert to readable text.
    rules["antecedents"] = rules["antecedents"].apply(lambda s: ", ".join(sorted(s)))
    rules["consequents"] = rules["consequents"].apply(lambda s: ", ".join(sorted(s)))

    # Keep only the columns a business stakeholder cares about
    rules = rules[["antecedents", "consequents", "support", "confidence", "lift"]]

    # Sort by lift: the strongest non-obvious associations float to the top
    rules = rules.sort_values("lift", ascending=False).reset_index(drop=True)

    print("\nTop 10 rules by lift:")
    print(rules.head(10).to_string(index=False))

    # ---------------------------------------------------------
    # 6. Focus on a business question: "What drives Beer sales?"
    # ---------------------------------------------------------
    # Filter for rules where Beer is the CONSEQUENT (what we want to sell more of)
    beer_rules = rules[rules["consequents"] == "Beer"].sort_values("lift", ascending=False)

    print("\nRules that lead to a Beer purchase:")
    print(beer_rules.head(10).to_string(index=False))

    # ---------------------------------------------------------
    # 7. Visualize the results
    # ---------------------------------------------------------
    # Plot 1: scatter of support vs confidence, sized by lift
    plt.figure(figsize=(9, 6))
    plt.scatter(
        rules["support"],
        rules["confidence"],
        s=rules["lift"] * 15,
        alpha=0.6,
        edgecolors="k",
    )
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

    # ---------------------------------------------------------
    # 8. Business interpretation (what a company would do)
    # ---------------------------------------------------------
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

    # ---------------------------------------------------------
    # 9. (Optional) Network graph of the top rules
    # ---------------------------------------------------------
    try:
        import networkx as nx

        G = nx.DiGraph()  # directed graph
        for _, r in rules.head(15).iterrows():
            G.add_edge(r["antecedents"], r["consequents"], weight=round(r["lift"], 2))

        plt.figure(figsize=(9, 7))
        pos = nx.spring_layout(G, seed=42)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=1500,
            font_size=9,
        )
        plt.title("Association Rules as a Graph (top 15 rules)")
        plt.tight_layout()
        plt.show()
    except ImportError:
        print("Install networkx to see the graph: python -m pip install networkx")