# Evaluating Model Fit with R-squared (R²) — A Practical Tutorial for Beginners

> **Audience:** beginners in machine learning with basic Python.
> **Goal:** understand what R² tells you, how to compute it, how to _read_ it, and — just as
> importantly — how it can mislead you.

---

## 1. What is R-squared?

R-squared (written R², the **coefficient of determination**) is a number between
(roughly) 0 and 1 that tells you **how much of the variation in your target
variable `y` your model explains**.

**The core idea in one sentence:**

> R² compares your model's errors against a trivial "model" that always predicts
> the average of `y`.

The formula:

```javascript
          SS_res        sum of squared errors of YOUR model
R² = 1 - --------  =  1 - --------------------------------------
          SS_tot        total variation of y around its own mean
```

- **SS_res** (residual sum of squares) = Σ(y_actual − y_predicted)² → everything your model got wrong.
- **SS_tot** (total sum of squares) = Σ(y_actual − ȳ)² → how much `y` varies at all.

**Analogy — the variance budget.** Think of all the variation in `y` as a pie.
SS*res is the slice your model \_failed* to explain. R² is the share of the pie
your model _did_ explain:

- R² = 0 → your model explains **nothing** (no better than predicting the mean).
- R² = 1 → your model explains **everything** (perfect predictions).
- R² = 0.85 → your model explains **85%** of the variation; 15% is still unexplained.

**Important:** R² is a metric for **regression** problems (predicting a number),
_not_ classification (predicting a category).

---

## 2. How to read the number

| R² value (test data) | Rough interpretation                                                   |
| -------------------- | ---------------------------------------------------------------------- |
| 0.95 – 1.00          | Excellent fit (suspiciously perfect? check for overfitting or leakage) |
| 0.80 – 0.95          | Good fit for many real-world problems                                  |
| 0.50 – 0.80          | Moderate; depends heavily on the domain                                |
| 0.00 – 0.50          | Weak; most variation is unexplained                                    |
| **negative**         | **Worse than predicting the mean!** (See Example 5)                    |

Two golden rules:

1. **Judge R² on TEST data** (data the model has never seen), not training data.
2. **Never compare R² across different datasets** — a "good" R² in one domain
   (e.g. physics) may be impossible in another (e.g. human behaviour).

---

## 3. Setup

Install the libraries once, then you are ready:

```bash
pip install numpy matplotlib scikit-learn
```

Every example below is also collected in the runnable script
`evaluating_r_squared.py` — comments on every line explain what it does.

---

## 4. Example 1 — Your first R²: simple linear regression

We create fake data where we _know_ the truth (`y = 5 + 3x + noise`), train a
linear regression, and look at its R² on training and test data.

```python
# ======================================================================
# EXAMPLE 1 - Your first R^2: simple linear regression
# ======================================================================
print("=" * 60)
print("EXAMPLE 1: Simple linear regression")
print("=" * 60)

# Create fake data with a KNOWN true relationship:  y = 5 + 3x + noise
X = np.random.rand(100, 1) * 10                    # 100 samples, 1 feature, values 0-10
y = 5 + 3 * X.ravel() + np.random.randn(100) * 3   # true line + random noise (std 3)

# Split the data: 80% to LEARN from, 20% to TEST on (kept hidden from training)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=1)

model = LinearRegression()     # create a linear regression model
model.fit(X_train, y_train)      # "fit" = find the best line through the train points

print("True slope was 3.0,     model learned:", round(model.coef_[0], 3))
print("True intercept was 5.0,   model learned:", round(model.intercept_, 3))

r2_train = model.score(X_train, y_train)                 # R^2 on data the model has seen
r2_test = r2_score(y_test, model.predict(X_test))          # R^2 on UNSEEN data

print(f"R^2 on training data: {r2_train:.3f}")
print(f"R^2 on test data:     {r2_test:.3f}")
print("-> Interpretation: about "
      f"{r2_test:.0%} of the variation in y is explained by our model on new data.")
print("   The remaining {0:.0%} is still 'unexplained' (mostly noise).".format(1 - r2_test))
```

**What to notice:**

- The learned slope (≈2.8) and intercept (≈5.9) are close to the true values
  (3 and 5) — the model recovered the real relationship despite the noise.
- `model.score(X, y)` for regression models in scikit-learn **returns exactly R²**.
  `r2_score(y_true, y_pred)` is the explicit, equivalent way to compute it.
- Test R² ≈ 0.93 means: on new data, about **93% of the variation in y is
  explained** by our model; the remaining 7% is mostly noise we cannot predict.

---

## 5. Example 2 — Computing R² by hand

To truly understand a metric, compute it yourself once:

```python
# ======================================================================
# EXAMPLE 2 - Computing R^2 BY HAND (understand what it really is)
# ======================================================================
print("=" * 60)
print("EXAMPLE 2: Computing R^2 by hand")
print("=" * 60)

y_pred = model.predict(X_test)                          # model guesses for the test set

ss_res = np.sum((y_test - y_pred) ** 2)                   # SS_res: sum of squared ERRORS
                                                          #         (what the model got wrong)
ss_tot = np.sum((y_test - y_test.mean()) ** 2)            # SS_tot: TOTAL variation of y
                                                          #         around its own mean

r2_by_hand = 1 - ss_res / ss_tot          # the definition of R^2:
                                          # 1 - (unexplained variation / total variation)

print(f"SS_res (unexplained) = {ss_res:.2f}")
print(f"SS_tot (total)       = {ss_tot:.2f}")
print(f"R^2 by hand          = {r2_by_hand:.3f}")
print(f"R^2 from sklearn     = {r2_score(y_test, y_pred):.3f}   (same thing!)")
```

You should see that the by-hand value matches scikit-learn exactly. From now on
you know _exactly_ what `r2_score` is doing: **1 − (unexplained variation ÷ total variation)**.

---

## 6. Example 3 — Multiple regression and Adjusted R²

Plain R² has a flaw: **it never decreases when you add more features**, even
useless ones. The fix is **adjusted R²**, which charges a small penalty for
every extra predictor:

```javascript
                    (1 − R²)(n − 1)
adjusted R² = 1 − ---------------------
                    n − p − 1

n = number of samples,  p = number of features
```

```python
# ======================================================================
# EXAMPLE 3 - Multiple regression + ADJUSTED R^2
# ======================================================================
print("=" * 60)
print("EXAMPLE 3: Multiple regression + adjusted R^2")
print("=" * 60)

n = 200                                       # number of samples (rows)
X_multi = np.random.rand(n, 5) * 10         # 5 features; only the first 3 truly matter
y_multi = (4
           + 2.0 * X_multi[:, 0]             # feature 0 pushes y up
           - 1.5 * X_multi[:, 1]             # feature 1 pushes y down
           + 0.5 * X_multi[:, 2]             # feature 2 pushes y up a little
           + np.random.randn(n) * 5)         # random noise + features 3,4 are USELESS

Xm_train, Xm_test, ym_train, ym_test = train_test_split(
    X_multi, y_multi, test_size=0.25, random_state=1)

def adjusted_r2(r2, n_samples, n_features):
    """Penalise R^2 for every extra predictor the model uses."""
    return 1 - (1 - r2) * (n_samples - 1) / (n_samples - n_features - 1)

# FULL model: throws in all 5 features (2 of them are useless junk)
full = LinearRegression().fit(Xm_train, ym_train)          # fit on train...
r2_full = full.score(Xm_test, ym_test)                     # ...evaluate on test

# SMALL model: keeps only the 3 features that really matter
small = LinearRegression().fit(Xm_train[:, :3], ym_train)   # [:, :3] = first 3 columns
r2_small = small.score(Xm_test[:, :3], ym_test)

n_test = len(ym_test)   # number of test samples (needed by the formula)
print(f"5-feature model: R^2 = {r2_full:.3f} "
      f"-> adjusted R^2 = {adjusted_r2(r2_full, n_test, 5):.3f}")
print(f"3-feature model: R^2 = {r2_small:.3f} "
      f"-> adjusted R^2 = {adjusted_r2(r2_small, n_test, 3):.3f}")
print("-> Plain R^2 barely changed, but adjusted R^2 REWARDS the simpler model.")
print("   Use adjusted R^2 when comparing models with different numbers of features.")
```

**What to notice:** both models achieve almost the same plain R² (the two junk
features added nothing), but adjusted R² is **higher for the simpler model**.
**Use adjusted R² whenever you compare models with different numbers of features.**

---

## 7. Example 4 — Where R² misleads you: overfitting

Here is the single most important practical lesson. We fit polynomials of
increasing flexibility (degree = how wiggly the curve may be):

```python
# ======================================================================
# EXAMPLE 4 - Where R^2 MISLEADS you: overfitting
# ======================================================================
print("=" * 60)
print("EXAMPLE 4: Where R^2 misleads - overfitting")
print("=" * 60)

# Fresh dataset: only 30 samples, so a very flexible curve has enough
# freedom to "hug" the training points instead of finding the true line
np.random.seed(10)                                    # seed chosen so this demo is dramatic
Xof = np.random.rand(30, 1) * 10                      # 30 samples, feature 0-10
yof = 5 + 3 * Xof.ravel() + np.random.randn(30) * 2.0 # true line y = 5 + 3x + noise
Xof_train, Xof_test, yof_train, yof_test = train_test_split(
    Xof, yof, test_size=0.25, random_state=1)

print(f"{'degree':>8} {'R^2 train':>10} {'R^2 test':>10}")
for degree in [1, 2, 5, 15]:
    poly = PolynomialFeatures(degree=degree, include_bias=False)
    Xtr_p = poly.fit_transform(Xof_train)   # expand x into x, x^2, ..., x^degree
    Xte_p = poly.transform(Xof_test)          # apply the SAME expansion to test data
    m = LinearRegression().fit(Xtr_p, yof_train)
    # model.score() for regression models returns exactly R^2
    print(f"{degree:>8} {m.score(Xtr_p, yof_train):>10.3f} {m.score(Xte_p, yof_test):>10.3f}")
print("-> Training R^2 rises (0.98 -> 0.985) while test R^2 COLLAPSES to ~0.5.")
print("   A high R^2 on TRAINING data alone proves nothing!")

# Draw the degree-15 curve so you can SEE the overfitting
poly15 = PolynomialFeatures(degree=15, include_bias=False)
m15 = LinearRegression().fit(poly15.fit_transform(Xof_train), yof_train)
x_grid = np.linspace(0, 10, 300).reshape(-1, 1)      # dense x-grid for a smooth curve
y_grid = m15.predict(poly15.transform(x_grid))        # curve predictions on that grid

r2_tr15 = m15.score(poly15.transform(Xof_train), yof_train)  # R^2 on train
r2_te15 = m15.score(poly15.transform(Xof_test), yof_test)    # R^2 on test

plt.figure(figsize=(7, 5))
plt.scatter(Xof_train, yof_train, color="steelblue", alpha=0.6, label="train data")
plt.scatter(Xof_test,  yof_test,  color="orange",   alpha=0.8, label="test data")
plt.plot(x_grid, 5 + 3 * x_grid.ravel(), "g--", linewidth=2, label="true line")
plt.plot(x_grid, y_grid, "r-", linewidth=1.5,
         label=f"degree-15 fit (R^2 train={r2_tr15:.3f}, test={r2_te15:.3f})")
plt.title("Training R^2 improved, yet the model got WORSE on new data")
plt.ylim(yof.min() - 3, yof.max() + 3)
plt.legend()
plt.tight_layout()
plt.savefig("example4_overfitting.png", dpi=120)     # save figure next to this script
plt.close()
print("Figure saved: example4_overfitting.png")
```

**What to notice:**

- Training R² _improves_ as the curve gets more flexible (0.980 → 0.985).
- Test R² _collapses_ (0.96 → 0.48) — the wiggly curve memorised the training
  points instead of learning the true line.
- R² on **training data alone would have told you the degree-15 model was best.**
  Only test R² reveals the truth.

The saved figure `example4_overfitting.png` shows the red degree-15 curve
snaking through the training points while missing the green true line — and
missing the orange test points even worse.

---

## 8. Example 5 — What a negative R² means

R² can be negative, and beginners often panic. It simply means:

> The model performs **worse** than a "model" that always predicts the average of `y`.

```python
# ======================================================================
# EXAMPLE 5 - What a NEGATIVE R^2 means
# ======================================================================
print("=" * 60)
print("EXAMPLE 5: What a NEGATIVE R^2 means")
print("=" * 60)

y_pred = model.predict(X_test)

# Baseline 1: ignore the model, just predict the average of the training targets
mean_pred = np.full_like(y_test, y_train.mean())
print(f"R^2 of 'always predict the mean': "
      f"{r2_score(y_test, mean_pred):.3f}  (roughly 0, as expected)")

# Baseline 2: a deliberately terrible prediction (always 10 units too high)
bad_pred = np.full_like(y_test, y_test.mean() + 10)
print(f"R^2 of a deliberately bad model:  "
      f"{r2_score(y_test, bad_pred):.3f}")

print("-> Negative R^2 means: the model performs WORSE than simply")
print("   predicting the average value of y. Seen often on test data")
print("   when a model overfits or the data shifts.")
```

Always predicting the mean scores ≈ 0 (it is exactly the baseline R² compares
against). Predicting 10 units too high scores ≈ −1. In practice you see negative
test R² when a model overfits badly or when test data comes from a shifted
distribution.

---

## 9. Example 6 — R² is not enough: pair it with MAE and RMSE

R² is unit-less and relative — it says nothing about **how big the errors are
in real units**. Complement it with:

- **MAE** (mean absolute error) = average |actual − predicted|, in `y`'s units.
- **RMSE** (root mean squared error) = like MAE, but large errors are punished harder.

```python
# ======================================================================
# EXAMPLE 6 - R^2 alongside MAE and RMSE
# ======================================================================
print("=" * 60)
print("EXAMPLE 6: R^2 alongside MAE and RMSE")
print("=" * 60)

mae  = mean_absolute_error(y_test, y_pred)          # average |error|, in y's units
rmse = np.sqrt(mean_squared_error(y_test, y_pred))  # like MAE but big errors hurt more

print(f"R^2  = {r2_score(y_test, y_pred):.3f}   (unit-less: share of variance explained)")
print(f"MAE  = {mae:.3f}   (average error, in the same units as y)")
print(f"RMSE = {rmse:.3f}   (typical 'big' error, same units as y)")
print("-> R^2 tells you 'how well overall', MAE/RMSE tell you 'how wrong, on average'.")

# A quick predicted-vs-actual plot: points near the dashed line = good fit
plt.figure(figsize=(5, 5))
plt.scatter(y_test, y_pred, color="steelblue", alpha=0.7)
lims = [y_test.min() - 2, y_test.max() + 2]          # range for the diagonal
plt.plot(lims, lims, "r--", label="perfect predictions")
plt.xlabel("actual y")
plt.ylabel("predicted y")
plt.title("Predicted vs actual")
plt.legend()
plt.tight_layout()
plt.savefig("example6_predicted_vs_actual.png", dpi=120)
plt.close()
print("Figure saved: example6_predicted_vs_actual.png")
```

**Rule of thumb:** report R² _and_ MAE/RMSE together. R² answers "does the
model capture the overall pattern?", MAE/RMSE answer "how wrong is a typical
prediction?". The saved figure `example6_predicted_vs_actual.png` plots
predicted vs actual values — points hugging the dashed diagonal = good fit.

---

## 10. Pitfalls cheat-sheet

| Pitfall                           | Why it matters                                     | Defence                                           |
| --------------------------------- | -------------------------------------------------- | ------------------------------------------------- |
| **Trusting training R²**          | Flexible models can reach R² ≈ 1 by memorising     | Always evaluate on held-out test data (Example 4) |
| **Adding features to "boost" R²** | Plain R² never decreases when you add predictors   | Use adjusted R² for model comparison (Example 3)  |
| **Comparing R² across datasets**  | Variance in `y` differs; R² is relative            | Compare models within the same dataset & split    |
| **Ignoring error size**           | R² = 0.99 can still mean errors of millions of €   | Report MAE/RMSE alongside (Example 6)             |
| **Using R² for classification**   | It measures variance explained, not class accuracy | Use accuracy, F1, ROC-AUC, etc.                   |
| **Assuming high R² ⇒ causation**  | Correlation ≠ causation                            | Domain knowledge / experiments needed             |

---

## 11. Takeaway checklist

- [ ] R² = share of variance in `y` explained by the model (1 − SS_res/SS_tot).
- [ ] Judge R² on **test data**, never training data alone.
- [ ] Use **adjusted R²** when comparing models with different feature counts.
- [ ] A **negative R²** = worse than predicting the mean.
- [ ] **Pair R² with MAE/RMSE** to know the practical error size.
- [ ] There is no universal "good" R² — context decides.

---

_Companion script: `evaluating_r_squared.py` — run it with `python evaluating_r_squared.py`
to reproduce every example and generate the figures._
