# Causal Impact Analysis — A Beginner's Guide

> Companion code: `causal_impact_analysis.py` (run it while reading this note)

---

## 1. The Question Causal Impact Answers

Your company launches something — a new checkout flow, a marketing campaign, a price change. A week later the metrics moved.

**The question every stakeholder asks:**

> "Did our change _cause_ that, or would it have happened anyway?"

That is exactly what **Causal Impact Analysis** answers. It estimates the effect of an **intervention** on an **outcome** when you cannot run a clean randomized A/B test.

### Why not just compare before vs after?

Because businesses are not static. Orders grow over time, seasons change, competitors act, ad spend fluctuates. If orders were already trending up, comparing "before vs after" credits your change with growth you would have gotten anyway.

Causal Impact fixes this by building a **counterfactual**: a prediction of what _would_ have happened without the intervention, then subtracting it.

---

## 2. The Core Idea (One Sentence)

> **Impact = What actually happened − What would have happened anyway**

The second term is called the **counterfactual**, and it is estimated from a model trained on the **pre-intervention period** using **control variables** — metrics that affect your outcome but were _not_ touched by the intervention.

### A picture is worth 1000 formulas

```
orders
  |                              ┌──── Observed (solid) ────┐
  |                     ┌────────┤                          │
  |            ┌────────┘        │                          │
  |   ┌────────┘                 ╰──── Counterfactual (dashed)
  |___│______________________________________________|________
      |            PRE period       |  POST period
      |       (train the model)     | (compare)
                                 ▲
                        INTERVENTION DATE
```

- **Solid line** = what actually happened.
- **Dashed line** = the model's guess of what would have happened.
- **Gap between them after the intervention** = the causal impact.

---

## 3. The Five Building Blocks

| Concept               | Plain-English meaning                   | In the code                                   |
| --------------------- | --------------------------------------- | --------------------------------------------- |
| **Intervention**      | The change you made                     | `INTERVENTION_DATE = 2024-06-28`              |
| **Outcome (target)**  | The metric you care about               | `orders`                                      |
| **Control variables** | Predictors _not_ affected by the change | `ad_spend`, `web_traffic`, `competitor_price` |
| **Pre-period**        | Clean history used to _train_           | days 0–179                                    |
| **Post-period**       | Window where you _measure_ the effect   | days 180–239                                  |

**Golden rule for controls:** a control must be something the intervention did **not** change. If your price change also affected ad spend, ad spend is contaminated and must be dropped.

---

## 4. Step-by-Step Method

### Step 1 — Collect data with timestamps

One row per time unit (day/week/month), with the outcome plus candidate controls.

### Step 2 — Pick the intervention date

The exact moment the change took effect. Everything before = train, everything after = measure.

### Step 3 — Train the counterfactual model on PRE data only

This is the critical discipline: **never let post-intervention data leak into training**, or the model learns the effect instead of the baseline.

```python
model = sm.OLS(y_pre, X_pre).fit()
```

### Step 4 — Predict the POST period

Feed the post-period controls into the trained model. The output is the counterfactual.

```python
post["counterfactual"] = model.predict(X_post)
```

### Step 5 — Compute the impact

```python
post["impact"] = post["orders"] - post["counterfactual"]
total_impact = post["impact"].sum()
```

### Step 6 — Test significance

Ask whether the average daily impact is statistically different from zero.

```python
t_stat, p_value = stats.ttest_1samp(post["impact"].dropna(), popmean=0)
```

`p < 0.05` → the effect is unlikely to be chance.

### Step 7 — Run a placebo test

Pretend the intervention happened on a **fake date** in the pre-period. A trustworthy method finds **no meaningful effect** there. (More on this in §7 — it's the most valuable step.)

### Step 8 — Visualize and report

Three panels: observed vs counterfactual, point-wise impact, cumulative impact.

---

## 5. The Formula, Broken Down

The counterfactual model is ordinary **linear regression**:

$$
\hat{y}_t = \beta_0 + \beta_1 x_{1t} + \beta_2 x_{2t} + \dots + \beta_k x_{kt}
$$

| Symbol      | Name          | Meaning                                                  |
| ----------- | ------------- | -------------------------------------------------------- |
| $\hat{y}_t$ | Prediction    | Estimated orders on day $t$                              |
| $\beta_0$   | Intercept     | Baseline level when all controls are 0                   |
| $\beta_j$   | Coefficient   | Effect of a **one-unit** change in control $j$ on orders |
| $x_{jt}$    | Control value | Observed value of control $j$ on day $t$                 |
| $t$         | Time index    | Which day we are predicting                              |

**Then the impact itself:**

$$
\text{Impact}_t = y_t - \hat{y}_t
$$

$$
\text{Total Impact} = \sum_{t \in \text{post}} (y_t - \hat{y}_t)
$$

$$
\text{Lift \%} = \left(\frac{\sum y_t}{\sum \hat{y}_t} - 1\right) \times 100
$$

**Reading the coefficients** (from the actual run):

```
const              -83.36   <- baseline intercept
ad_spend             0.081  <- each extra $1 of ads -> +0.08 orders
web_traffic          0.010  <- each extra visitor  -> +0.01 orders
competitor_price     2.354  <- each $1 competitor increase -> +2.35 orders
day_index            0.048  <- organic growth per day (trend)
```

That last row matters enormously, and it is the single most common beginner mistake — see §8.

---

## 6. Business Use Cases

| Industry         | Intervention                 | Outcome             | Control variables                       |
| ---------------- | ---------------------------- | ------------------- | --------------------------------------- |
| **E-commerce**   | New checkout flow            | Orders / conversion | Ad spend, traffic, seasonality          |
| **Marketing**    | Brand campaign in one region | Sales               | Sales in untouched regions              |
| **Retail**       | Price change on one product  | Units sold          | Same product in other regions           |
| **SaaS**         | New pricing tier launched    | MRR / signups       | Traffic, trial volume, seasonality      |
| **Policy / Gov** | New tax or subsidy           | Consumer spending   | Neighbouring regions without the policy |
| **Operations**   | New logistics provider       | Delivery time       | Other warehouses / routes               |
| **Product**      | Feature rollout to 10%       | Engagement          | Holdout users                           |

**When to use it:** you have a clear intervention date, good controls, and _no possibility_ of a randomized test.

**When NOT to use it:** you can run a real A/B test (do that instead — it's stronger); you have no control data; or the intervention affected everyone simultaneously (no comparison left).

---

## 7. The Placebo Test — Your Best Friend

This is the step beginners skip and senior analysts never do.

**The idea:** run the entire analysis again with a **fake intervention date** placed where nothing changed. If your method is sound, it should report roughly zero effect.

**In the companion script:**

| Check                    | Result          | Reading                       |
| ------------------------ | --------------- | ----------------------------- |
| Real intervention lift   | **13.8%**       | The effect we care about      |
| Placebo lift (fake date) | **0.66%**       | Noise floor of the method     |
| Ratio                    | **~21× larger** | Real effect clearly dominates |

### ⚠️ An important nuance you must understand

In the script, the placebo p-value was **0.042**, which is technically "significant." A beginner reads that as "the method is broken." It is not.

**Why this happens:** with 60+ observations, a statistical test has enormous power. A trivial, meaningless 0.66% deviation can clear the p < 0.05 bar. This is the difference between:

- **Statistical significance** — "the deviation is probably not pure luck"
- **Practical significance** — "the deviation is big enough to matter"

**Always report effect size, not just the p-value.** That is why the script compares the placebo lift (0.66%) against the real lift (13.8%) instead of relying on the p-value alone. A 0.66% swing will never change a business decision; a 13.8% swing will.

---

## 8. Common Pitfalls

### Pitfall 1 — Forgetting the time trend (the #1 beginner error)

Your business grows organically. If the model has no trend term, it interprets steady growth as a post-intervention effect and **overstates** the impact. Always include a time index (`day_index`) unless you have strong reason not to.

### Pitfall 2 — Contaminated controls

If your intervention also changed a control variable, the model "explains away" your real effect and you understate impact. Choose controls that are provably untouched.

### Pitfall 3 — Data leakage

Including post-intervention data in training teaches the model the effect. Fit on pre-period data **only**.

### Pitfall 4 — Too little pre-period data

Below ~20–30 time points the model is unstable. Aim for at least 2–3× the length of your post-period.

### Pitfall 5 — Ignoring seasonality

Weekly/monthly cycles swamp the signal. Either add seasonal dummies, use a seasonal model, or compare like-for-like periods.

### Pitfall 6 — Over-reading a single p-value

See §7. Report magnitude, confidence intervals, and a placebo result together.

### Pitfall 7 — Assuming causation from correlation

The method _estimates_ causal impact under assumptions (controls unaffected, stable relationship). If those break, so does the conclusion. Sensitivity-test your results.

---

## 9. Reading the Three-Panel Plot

**Panel 1 — Observed vs Counterfactual.** Solid vs dashed line, with a shaded 95% interval. After the intervention, if the solid line sits consistently **above the band**, the effect is real.

**Panel 2 — Point-wise Impact.** Daily `observed − counterfactual`. Above zero = positive effect. Watch for a **sustained shift**, not one spike — a single spike may be noise.

**Panel 3 — Cumulative Impact.** The running total. A straight upward slope means a consistent effect. The final value is your headline number ("+2,530 extra orders").

---

## 10. Results From the Companion Script

```
Intervention   : New checkout flow launched 2024-06-28
Analysis window: 2024-06-28 to 2024-08-27 (61 days)

Observed orders      :     20,833
Expected (no change) :     18,303
Net extra orders     :      2,530
Estimated lift       :      13.8%
Statistically valid  : YES (p < 0.05)

Recovered lift     : 13.8%
True baked-in lift : 15.0%   <- we injected +15%, model recovered 13.8%
```

**Why is 13.8% not 15%?** Because the counterfactual uses only control variables and never sees the intervention — some real lift leaks into the noise term, plus sampling variation. Landing within ~1.2 percentage points of a known truth is a good result. If you injected +15% and recovered 40%, something is wrong with your model.

---

## 11. Production Tools

The companion script implements the method from first principles with `statsmodels` so every line is visible. In production, common choices:

| Tool                        | Notes                                                       |
| --------------------------- | ----------------------------------------------------------- |
| **`causalimpact`** (Python) | Port of Google's R package; Bayesian structural time series |
| **`CausalImpact`** (R)      | The original Google implementation                          |
| **`statsmodels`**           | Build your own regression/ARIMA counterfactual (used here)  |
| **`scikit-learn`**          | Any regressor can serve as the counterfactual model         |
| **`pymc` / `bambi`**        | Full Bayesian treatment with credible intervals             |

> ⚠️ **Windows note:** `causalimpact` may need a C++ compiler (`g++`) and can silently return `inferences = None` if unavailable. The `statsmodels` approach in the companion script has no such dependency.

---

## 12. Quick Reference

```
Goal:        Did our change cause the metric move?
Core idea:   Impact = Observed - Counterfactual
Counterfactual: model trained on PRE period using untouched controls
Formula:     y_hat = b0 + b1*x1 + ... + bk*xk
             impact = sum(y - y_hat)
             lift % = (sum(y) / sum(y_hat) - 1) * 100
Steps:       split -> train on pre -> predict post -> impact -> test -> placebo
Must-have:   time trend, clean controls, enough pre-period data
Sanity:      placebo test on a fake date must show ~0% lift
Report:      effect size + CI + p-value + placebo (never p-value alone)
```

---

## 13. One-Line Takeaway

**Causal Impact Analysis compares what actually happened against a model's forecast of what would have happened without your change — and the gap between them, validated against a fake-date placebo test, is your best estimate of whether the change truly worked.**
