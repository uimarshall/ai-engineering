# The "Dummy Variable Trap" — A Beginner's Guide

_Covers: dummy variables, perfect multicollinearity, why your regression "goes crazy", and how to fix it in one line._

---

## 1. The 30-second version

You turn a categorical column (like `region = North/South/East/West`) into 4 "dummy" columns of 0s and 1s. You also keep the model's intercept. Now you have **5 columns that secretly contain only 4 columns' worth of information** — because the 4 dummies always add up to exactly 1, which is the intercept.

The maths breaks: the computer can't find _one_ unique answer, so it either errors out or silently hands you nonsense coefficients. That is the **dummy variable trap**.

**The fix:** with an intercept in the model, keep only **k − 1** dummies (e.g. 3 out of 4 regions). Or drop the intercept and keep all k.

---

## 2. What is a dummy variable?

A dummy variable is a 0/1 column that says "yes/no" to a category.

| region | price |
| ------ | ----- |
| North  | 120   |
| South  | 143   |
| North  | 108   |

becomes

| region_North | region_South |
| ------------ | ------------ |
| 1            | 0            |
| 0            | 1            |
| 1            | 0            |

Why do we need it? Because regression is arithmetic — it can multiply and add numbers, but it cannot multiply the word `"North"`. Dummies turn words into numbers.

---

## 3. The trap, in plain English

There are two ways to write the same model:

**Way A — drop one level (correct):**
$$\text{price} = \beta_0 + \beta_1 \cdot D_{South} + \beta_2 \cdot D_{East} + \beta_3 \cdot D_{West} + \varepsilon$$
Here `North` is the **baseline** — its effect is baked into $\beta_0$.

**Way B — keep all levels (the trap):**
$$\text{price} = \beta_0 + \beta_1 D_N + \beta_2 D_S + \beta_3 D_E + \beta_4 D_W + \varepsilon$$

Every row has exactly one region, so for **every single row**:

$$D_N + D_S + D_E + D_W = 1$$

And the intercept column is just a column of 1s. So:

$$\text{const} = D_N + D_S + D_E + D_W \quad \text{(exactly, row by row)}$$

The intercept column is a **perfect copy** of the sum of the dummies. You gave the model a column that adds zero new information. It's like hiring a 5th person to a 4-person job.

> **Analogy:** four light switches where the rule is "exactly one must be ON". If someone tells you switches 1–3, you already know switch 4. Switch 4 is redundant — and if you force the panel to "use all four to explain the light", there are infinitely many settings that work.

---

## 4. "Input variables perfectly predict each other" — what that means

It means: **given the other columns, you can compute one column with zero error.**

Not "they're correlated". Not "they move together roughly". _Exactly_. As an equation:

$$D_N = 1 - D_S - D_E - D_W$$

If I hand you the values of $D_S, D_E, D_W$ and the intercept, you can fill in $D_N$ for every row **without ever looking at the data**. The prediction is perfect — $R^2 = 1.0$, not 0.95, not 0.99. Perfect, to the last decimal.

Compare:

| Situation                        | Can you recover one column from the others? | Name                          | Consequence            |
| -------------------------------- | ------------------------------------------- | ----------------------------- | ---------------------- |
| Dummies + intercept (all levels) | Yes, exactly                                | **Perfect multicollinearity** | No unique solution     |
| `height_cm` and `height_inches`  | Yes, exactly ($\times 2.54$)                | **Perfect multicollinearity** | No unique solution     |
| `age` and `income` ($r = 0.7$)   | No, only approximately                      | **Multicollinearity**         | Unstable, but solvable |
| `age` and `shoe_size`            | Barely at all                               | —                             | Fine                   |

**"Multicollinearity"** = predictors that overlap in what they explain. **Perfect multicollinearity** = the overlap is 100%, and that's the trap.

---

## 5. Which assumption does it violate?

Ordinary Least Squares (OLS) is usually taught with ~5 assumptions. The relevant one is:

> **Assumption 5 (Full rank / no perfect multicollinearity):** the predictor matrix $X$ must have **full column rank** — no column may be an exact linear combination of the others.

Why does it matter? OLS's formula for the coefficients is:

$$\hat{\beta} = (X^\top X)^{-1} X^\top y$$

To compute this you must **invert** the matrix $X^\top X$. A matrix with a redundant column is **singular** — its determinant is 0, and _you cannot divide by zero_. Mathematically, $X^\top X$ has no inverse, so $\hat\beta$ isn't defined.

### The formula, piece by piece

For a 2-region toy example (rows: one North, one South), $X = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 0 & 1 \end{bmatrix}$ (const, $D_N$, $D_S$).

$$X^\top X = \begin{bmatrix} 2 & 1 & 1 \\ 1 & 1 & 0 \\ 1 & 0 & 1 \end{bmatrix}$$

Determinant, expanded along the first row:

$$\det = 2(1\cdot1 - 0\cdot0) \;-\; 1(1\cdot1 - 0\cdot1) \;+\; 1(1\cdot0 - 1\cdot1)$$
$$\det = 2(1) - 1(1) + 1(-1) = 2 - 1 - 1 = \mathbf{0}$$

$\det(X^\top X) = 0 \Rightarrow$ no inverse $\Rightarrow$ no unique $\hat\beta$. That's the whole trap in one line of arithmetic.

### The VIF version of the same idea

**Variance Inflation Factor** measures how much one predictor is explained by the others:

$$\text{VIF}_j = \frac{1}{1 - R_j^2}$$

where $R_j^2$ comes from regressing predictor $x_j$ on all the _other_ predictors.

- Balanced 4-level dummy with one dropped: $R_j^2 = 1/3 \Rightarrow \text{VIF} = \dfrac{1}{1 - 1/3} = 1.5$ ✅
- Trap case: $R_j^2 = 1 \Rightarrow \text{VIF} = \dfrac{1}{1-1} = \dfrac{1}{0} = \infty$ ❌

Standard errors scale with $\sqrt{\text{VIF}}$, so $\text{SE} \to \infty$: your coefficients become meaningless. Rules of thumb: VIF > 5 is concerning, VIF > 10 is serious, VIF = ∞ means you hit the trap.

---

## 6. Why it's dangerous (the "silent failure")

The nastiest part: **different tools behave differently.**

| Tool                             | What it does                                              | Danger                   |
| -------------------------------- | --------------------------------------------------------- | ------------------------ |
| `numpy.linalg.inv` on $X^\top X$ | Amplifies floating-point noise                            | Coefficients like `1e14` |
| `statsmodels` OLS                | Uses pseudo-inverse, prints a _warning_ about eigenvalues | Easy to ignore           |
| `sklearn.LinearRegression`       | Silently uses least-squares & returns **some** solution   | **No error at all**      |

`sklearn` won't complain. It will happily give you a model that **predicts perfectly well** while its coefficients are arbitrary. You'll ship it, then a stakeholder asks "so how much does the South region really add?" — and the honest answer is "the model doesn't know."

**Two completely different coefficient vectors can produce identical predictions.** If you add 100 to the intercept and subtract 100 from each of the 4 dummies, every prediction stays _exactly_ the same. So which one is "the" answer? Neither. The data simply cannot distinguish them.

---

## 7. The fixes

| Fix                                  | How                                   | When                                 |
| ------------------------------------ | ------------------------------------- | ------------------------------------ |
| **Drop one level**                   | `pd.get_dummies(df, drop_first=True)` | Classic OLS with intercept ✅        |
| **Drop the intercept**               | `sm.OLS(y, X, hasconst=False)`        | Rarely; dummies become group means   |
| **Use regularisation**               | Ridge / Lasso (`alpha > 0`)           | When you have many categories        |
| **Use a tree model**                 | Random Forest, XGBoost                | Trees don't invert matrices — immune |
| **Use a different parameterisation** | Sum-to-zero coding                    | ANOVA-style models                   |

⚠️ **Production tip:** `pd.get_dummies` doesn't remember which columns it made, so a new dataset may have different columns. In a real pipeline use `sklearn.preprocessing.OneHotEncoder(drop="first", handle_unknown="ignore")` inside a `Pipeline`/`ColumnTransformer`.

---

## 8. Business use cases

- **Marketing mix modelling** — channel dummies (`Email / Search / Social / Direct`). Keep all 4 with an intercept and every channel's ROI estimate becomes garbage; you can no longer answer "which channel works best?"
- **Retail seasonality** — `Q1–Q4` dummies. This is _the_ textbook trap. Always drop one quarter and interpret the rest _relative_ to it.
- **Real estate pricing** — neighbourhood dummies. With the trap you lose the ability to attribute price premiums per neighbourhood.
- **HR / people analytics** — department dummies when modelling attrition. The intercept becomes meaningless and coefficient signs can flip.
- **A/B/n testing** — 3+ treatment arms one-hot encoded. Report effects relative to the control arm by dropping the control dummy.
- **Credit scoring / insurance** — every protected-class variable encoded as dummies; regulators want interpretable, attributable coefficients, which the trap destroys.

**The business translation:** the trap converts "this channel is worth +£12k/month" into "we can't tell you." It doesn't hurt _prediction_, it destroys _explanation_ — which is usually the actual deliverable.

---

## 9. Cheat sheet

```
Categorical column with k levels  →  k dummy columns
+ intercept in the model          →  KEEP ONLY k-1  ✅
No intercept                      →  keep all k     ✅
Tree model / Ridge / Lasso        →  doesn't matter ✅
VIF = ∞  or  det(X'X) = 0         →  you hit the trap ❌
Ignore it and sklearn still "works" → the real danger ⚠️
```

**One sentence to remember:** _the dummies sum to the intercept, so one of them is a copy — drop it._

---

# Part 2 — Standalone runnable script

Save as `dummy_variable_trap.py`. It needs `numpy`, `pandas`, `matplotlib`, `statsmodels`, `scikit-learn`. It's fully offline (synthetic data) and writes every figure to `./plots/`. The numbered blocks below concatenate exactly into the file.

**Block 1 — imports, config, helpers**

```python
"""
dummy_variable_trap.py
----------------------
Demonstrates the "dummy variable trap" (perfect multicollinearity)
with a synthetic ice-cream-sales-by-region dataset.

All figures are saved to ./plots/ before being shown.
"""
import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

warnings.filterwarnings("ignore")  # statsmodels gets noisy on singular design matrices

PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)
RNG_SEED = 42
TRUE_MEANS = {"North": 100.0, "South": 130.0, "East": 115.0, "West": 90.0}


def savefig(name: str) -> None:
    """Save the current figure into ./plots/ then show it."""
    path = os.path.join(PLOTS_DIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"    [saved plot] {path}")
    plt.show()


def banner(title: str) -> None:
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def vif_table(X: pd.DataFrame) -> pd.Series:
    """VIF for each column = 1 / (1 - R^2 of that column on all the others)."""
    X = X.astype(float)
    out = {}
    for col in X.columns:
        y = X[col].to_numpy()
        others = sm.add_constant(X.drop(columns=col), has_constant="skip")
        r2 = sm.OLS(y, others).fit().rsquared
        out[col] = np.inf if r2 > 1 - 1e-10 else 1.0 / (1.0 - r2)
    return pd.Series(out, name="VIF")
```

**Block 2 — build the dataset**

```python
def make_dataset(n: int = 300, noise: float = 12.0, seed: int = RNG_SEED):
    """Synthetic sales data: region drives the mean, plus Gaussian noise."""
    rng = np.random.default_rng(seed)
    regions = rng.choice(list(TRUE_MEANS), size=n)
    sales = np.array([TRUE_MEANS[r] for r in regions]) + rng.normal(0, noise, n)
    df = pd.DataFrame({"region": regions, "sales": sales.round(2)})
    return df


def add_all_dummies(df: pd.DataFrame):
    """The TRAP: intercept + one dummy for EVERY level."""
    dummies = pd.get_dummies(df["region"], prefix="region").astype(float)
    X = sm.add_constant(dummies)          # 'const' lands in the first column
    return X, df["sales"].astype(float)


def add_dropped_dummies(df: pd.DataFrame, baseline: str = "North"):
    """The FIX: intercept + one dummy for every level EXCEPT the baseline."""
    dummies = pd.get_dummies(df["region"], prefix="region").astype(float)
    dummies = dummies.drop(columns=[f"region_{baseline}"])
    X = sm.add_constant(dummies)
    return X, df["sales"].astype(float)
```

**Block 3 — the hand-worked 2-row example**

```python
def demo_hand_example() -> None:
    banner("1. HAND EXAMPLE - det(X'X) = 0, so there is no inverse")
    X = np.array([[1.0, 1.0, 0.0],   # row 1: const, North, South
                  [1.0, 0.0, 1.0]])  # row 2: const, North, South
    XtX = X.T @ X
    print("X'X =\n", XtX)
    det = np.linalg.det(XtX)
    print(f"\ndet(X'X) = {det:.3e}   ->  effectively ZERO")
    print("No inverse exists -> beta-hat is not uniquely defined.")
    print("\nWhy? Check the identity row by row:")
    print("   const  =", X[:, 0])
    print("   D_N+D_S=", X[:, 1] + X[:, 2], " -> identical! Redundant column.")
```

**Block 4 — detect the trap in the real dataset**

```python
def demo_detect_trap(df: pd.DataFrame, X_full: pd.DataFrame) -> None:
    banner("2. SPOTTING THE TRAP IN OUR 4-REGION DATASET")
    Xv = X_full.to_numpy(dtype=float)

    dummies_sum = X_full.drop(columns="const").sum(axis=1)
    print("Are the dummies + intercept a perfect identity? ->",
          bool(np.allclose(dummies_sum, X_full["const"])))

    rank = np.linalg.matrix_rank(Xv)
    print(f"Matrix rank      : {rank}   (only {rank} independent columns)")
    print(f"Number of columns: {Xv.shape[1]}   (one too many!)")
    print(f"Condition number : {np.linalg.cond(Xv):.3e}   (huge = collinear)")

    corr = X_full.corr().round(2)
    print("\nFull-model VIF table (inf = perfect multicollinearity):")
    print(vif_table(X_full).to_string())
```

**Block 5 — three solvers, three answers**

```python
def solve_three_ways(X_full: pd.DataFrame, y: pd.Series,
                     X_red: pd.DataFrame) -> dict:
    """The same data, three numeric routes, wildly different coefficients."""
    banner("3. SAME DATA, THREE DIFFERENT ANSWERS")
    Xv, yv = X_full.to_numpy(float), y.to_numpy(float)
    answers = {}

    # (a) Textbook normal equations  -> divides by an (almost) zero determinant
    try:
        answers["normal equations"] = np.linalg.inv(Xv.T @ Xv) @ (Xv.T @ yv)
    except np.linalg.LinAlgError as err:
        print(f"normal equations failed: {err}")
        answers["normal equations"] = np.full(Xv.shape[1], np.nan)

    # (b) Least squares / pseudo-inverse -> silently returns *a* solution
    beta_lstsq, *_ = np.linalg.lstsq(Xv, yv, rcond=None)
    answers["lstsq (min-norm)"] = beta_lstsq

    # (c) The fix: drop one dummy
    beta_red = np.linalg.lstsq(X_red.to_numpy(float), yv, rcond=None)[0]
    answers["drop one level"] = beta_red

    for name, beta in answers.items():
        if name == "drop one level":
            cols = list(X_red.columns)
        else:
            cols = list(X_full.columns)
        fitted = (X_red if name == "drop one level" else X_full).to_numpy(float) @ beta
        r2 = 1 - ((yv - fitted) ** 2).sum() / ((yv - yv.mean()) ** 2).sum()
        print(f"\n{name}:")
        print("  " + ", ".join(f"{c}={v:,.2f}" for c, v in zip(cols, beta)))
        print(f"  R^2 on training data = {r2:.6f}")

    print("\n>>> Notice: R^2 is identical, but the coefficients are not.")
    print(">>> Prediction is fine; EXPLANATION is destroyed. That is the trap.")
    return answers
```

**Block 6 — identifiability: two 'truths', same predictions**

```python
def demo_identifiability(X_full: pd.DataFrame, y: pd.Series) -> None:
    banner("4. TWO DIFFERENT 'TRUTHS', IDENTICAL PREDICTIONS")
    Xv, yv = X_full.to_numpy(float), y.to_numpy(float)
    beta_a, *_ = np.linalg.lstsq(Xv, yv, rcond=None)

    # Add 100 to the intercept and subtract 100 from every dummy.
    shift = np.array([100.0, -100.0, -100.0, -100.0, -100.0])
    beta_b = beta_a + shift

    print("beta_a:", np.round(beta_a, 2))
    print("beta_b:", np.round(beta_b, 2))
    print("\nPredictions identical?", bool(np.allclose(Xv @ beta_a, Xv @ beta_b)))
    print("Residual sums of squares identical?",
          bool(np.allclose(((yv - Xv @ beta_a) ** 2).sum(),
                           ((yv - Xv @ beta_b) ** 2).sum())))
    print("\n>>> The data cannot choose between them. Neither can the software.")
```

**Block 7 — the fix in practice (statsmodels)**

```python
def demo_the_fix(X_red: pd.DataFrame, y: pd.Series) -> None:
    banner("5. THE FIX: DROP ONE LEVEL (North = baseline)")
    model = sm.OLS(y, X_red).fit()
    print(model.summary().tables[1])
    print("\nAll coefficients are now read RELATIVE TO NORTH (the baseline).")
    print("North's own mean lives inside the intercept.")
    print("\nVIF after dropping one dummy:")
    print(vif_table(X_red).to_string())
```

**Block 8 — plots**

```python
def make_plots(df, X_full, answers, X_red, y):
    banner("6. PLOTS")

    order = ["const", "North", "South", "East", "West"]

    def as_dict(X, beta, baseline="North"):
        d = {c.replace("region_", ""): v for c, v in zip(X.columns, beta)}
        d.setdefault(baseline, 0.0)      # baseline is forced to 0 by construction
        return {k: d.get(k, np.nan) for k in order}

    inv_d = as_dict(X_full, answers["normal equations"])
    lstsq_d = as_dict(X_full, answers["lstsq (min-norm)"])
    red_d = as_dict(X_red, answers["drop one level"])

    # --- Plot 1: coefficients from the three routes -----------------------
    x = np.arange(len(order))
    w = 0.26
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(x - w, [inv_d[k] for k in order], w, label="normal equations (inv)")
    ax.bar(x, [lstsq_d[k] for k in order], w, label="lstsq (min-norm)")
    ax.bar(x + w, [red_d[k] for k in order], w, label="drop one level (fixed)")
    ax.set_yscale("symlog", linthresh=1)
    ax.set_xticks(x, order)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("coefficient (symmetric log scale)")
    ax.set_title("Same data, three solvers: the trap produces meaningless coefficients")
    ax.legend()
    savefig("01_coefficient_chaos.png")

    # --- Plot 2: what the model actually learns (group means) -------------
    def group_means(X, beta):
        pred = pd.Series(X.to_numpy(float) @ beta, index=df.index)
        return pred.groupby(df["region"]).mean()

    means_lstsq = group_means(X_full, answers["lstsq (min-norm)"])
    means_red = group_means(X_red, answers["drop one level"])
    labels = list(TRUE_MEANS)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = np.arange(len(labels))
    ax.bar(x - 0.2, [means_lstsq[l] for l in labels], 0.4, label="all dummies (trap)")
    ax.bar(x + 0.2, [means_red[l] for l in labels], 0.4, label="drop one level (fixed)")
    ax.scatter(x, [TRUE_MEANS[l] for l in labels], color="black", zorder=5,
               marker="D", label="true mean used to generate data")
    ax.set_xticks(x, labels)
    ax.set_ylabel("mean sales")
    ax.set_title("Fitted group means agree — only the coefficients are arbitrary")
    ax.legend()
    savefig("02_group_means_agree.png")

    # --- Plot 3: VIF before vs after --------------------------------------
    vif_full = vif_table(X_full)
    vif_red = vif_table(X_red)
    fig, ax = plt.subplots(figsize=(11, 5.5))
    x = np.arange(len(order))
    plot_max = 1e4
    fv = [min(vif_full.get(k, np.nan), plot_max) for k in order]
    rv = [min(vif_red.get(k, np.nan), plot_max) for k in order]
    ax.bar(x - 0.2, fv, 0.4, label="all dummies (trap)")
    ax.bar(x + 0.2, rv, 0.4, label="drop one level (fixed)")
    ax.set_yscale("symlog", linthresh=1)
    ax.set_xticks(x, order)
    ax.set_ylabel("VIF (symmetric log scale)")
    ax.set_title("VIF explodes to infinity with all dummies in the model")
    for xi, v in zip(x, fv):
        if not np.isfinite(vif_full.get(order[xi], np.nan)) or v >= plot_max:
            ax.annotate("inf", (xi - 0.2, v), ha="center", va="bottom")
    ax.legend()
    savefig("03_vif_comparison.png")
```

**Block 9 — business notes + `main()`**

```python
def print_business_notes() -> None:
    banner("7. BUSINESS USE CASES & CHEAT SHEET")
    print("""
  * Marketing mix modelling : channel dummies (Email/Search/Social/Direct).
    Keep all four with an intercept and every channel ROI becomes unidentifiable.
  * Retail seasonality      : Q1-Q4 dummies -> always drop one quarter.
  * Real estate pricing     : neighbourhood dummies -> drop one to keep premiums.
  * HR / attrition models   : department dummies -> keep effects relative to a baseline.
  * A/B/n testing           : drop the control arm so effects are measured against it.
  * Credit & insurance      : regulators need attributable coefficients; the trap erases them.

  THE TRAP HURTS EXPLANATION, NOT PREDICTION.
  sklearn will not error out. That silent success is what makes it dangerous.

  CHEAT SHEET
    k categories + intercept        -> keep k-1 dummies   OK
    k categories, no intercept      -> keep k dummies     OK
    Tree model / Ridge / Lasso      -> immune             OK
    VIF = inf, det(X'X) = 0, huge cond number -> you hit the trap
    Production pipelines: OneHotEncoder(drop='first', handle_unknown='ignore')
""")


def main() -> None:
    print("=" * 72)
    print("THE DUMMY VARIABLE TRAP - a hands-on demo")
    print("=" * 72)

    df = make_dataset()
    print(f"\nDataset: {df.shape[0]} rows, {df['region'].nunique()} regions")
    print(df.groupby("region")["sales"].agg(["count", "mean"]).round(2))

    X_full, y = add_all_dummies(df)     # the trap
    X_red, _ = add_dropped_dummies(df)  # the fix

    demo_hand_example()
    demo_detect_trap(df, X_full)
    answers = solve_three_ways(X_full, y, X_red)
    demo_identifiability(X_full, y)
    demo_the_fix(X_red, y)
    make_plots(df, X_full, answers, X_red, y)
    print_business_notes()

    print("\nDone. Figures are in ./plots/")


if __name__ == "__main__":
    main()
```

### What you should see when you run it

1. `det(X'X) = 0` on the toy example, with a printed proof that `const == D_N + D_S`.
2. Rank 4 out of 5 columns, a condition number around `1e16`, and VIF = `inf`.
3. Three solvers producing **the same R²** but coefficient values differing by 10+ orders of magnitude.
4. A shift of `[+100, -100, -100, -100, -100]` leaving predictions bit-for-bit identical.
5. After `drop_first`, VIF drops to `1.5` and the intercept becomes the mean of North.
6. Three PNGs in `./plots/`.

---

If it's useful, I can follow this up with a companion piece on **regularisation as a cure for ordinary (non-perfect) multicollinearity** — ridge regression, the $L_2$ penalty, and how to read a VIF heatmap.
