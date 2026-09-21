# Machine Learning for Absolute Beginners

### Supervised and Unsupervised Learning, Explained with Code, Graphs and a Real Business Case

**What you need**

```bash
pip install numpy pandas scikit-learn matplotlib
```

Python 3.9+, and about 45 minutes. No maths beyond high-school algebra — every formula below is broken down piece by piece.

---

## 1. What machine learning actually is

Traditional programming: **you write the rules**, the computer follows them.

```
rules + data  →  answers
```

Machine learning flips the direction. You show the computer many examples and it **works out the rules itself**:

```
data + answers  →  rules   (we call the rules a "model")
```

Then you use those learned rules on data the model has never seen. That's the entire idea: **learn patterns from data instead of being told the pattern.**

Why it matters: nobody can hand-write the rule "this email is spam." But a model can learn it from 100,000 labelled emails.

---

## 2. The vocabulary (read this once, it pays off)

| Term                       | Plain-English meaning                                                                                       |
| -------------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Feature**                | An input column. House size, customer's basket size. Usually written `x`.                                   |
| **Label / target**         | The thing you want to predict. Price, "spam/not spam". Written `y`.                                         |
| **Model**                  | The learned rule. A formula with tuned numbers inside.                                                      |
| **Training / fitting**     | The process of tuning those numbers using data. `.fit()` in scikit-learn.                                   |
| **Prediction / inference** | Using the trained model on new data. `.predict()`.                                                          |
| **Training set**           | Data used to learn.                                                                                         |
| **Test set**               | Data held back, used only to check how good the model really is.                                            |
| **Overfitting**            | Model memorised the training data instead of learning the pattern. Great on training data, bad on new data. |

**Golden rule:** never evaluate on the data you trained on. A student who has seen the exam answers isn't a good student — they're a good memoriser.

---

## 3. Supervised learning — "learning with an answer key"

You give the model **inputs _and_ the correct outputs**. It learns the mapping. Two flavours:

- **Regression** → the output is a _number_ (house price, next month's spend).
- **Classification** → the output is a _category_ (spam / not spam, churn / stay).

The mental model: **exam prep with a practice book that has all the answers.** Test day = new, unseen data.

### 3.1 Regression intuition

Plot house size against price and you'll see a rough upward band. A regression model looks for the straight line (or curve) that gets closest to every point at once. Learn the line's numbers, and you can predict the price of a house you've never seen.

### 3.2 The formula, broken down piece by piece

```
ŷ = w₀ + w₁x₁ + w₂x₂ + ... + w_dx_d
```

| Symbol       | Name                   | What it means                                                                    |
| ------------ | ---------------------- | -------------------------------------------------------------------------------- |
| `ŷ`          | "y-hat"                | The model's **prediction**. (The hat always means "estimated".)                  |
| `x₁ ... x_d` | Features               | The `d` input numbers for one example, e.g. `x₁ = size`, `x₂ = rooms`.           |
| `w₀`         | Intercept / bias       | The prediction when every feature is 0. Shifts the line up or down.              |
| `w₁ ... w_d` | Weights / coefficients | How much `ŷ` changes when that feature increases by 1, holding the others fixed. |
| `d`          | Number of features     | How many inputs you're feeding in.                                               |

Nothing here is exotic — it's the equation of a line, generalised to many dimensions. **Training = finding the `w` values that make the prediction errors as small as possible.**

### 3.3 Runnable code

```python
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

os.makedirs("plots", exist_ok=True)          # so savefig() never fails
rng = np.random.default_rng(42)

# ---------- 1. Make some fake "house" data ----------
n = 120
size  = rng.uniform(40, 180, n)                       # m²
price = 1.8 * size + 40 + rng.normal(0, 25, n)        # thousands, with noise

X = size.reshape(-1, 1)   # scikit-learn wants a 2-D array: (rows, features)
y = price

# ---------- 2. Fit and plot the line (picture only) ----------
model_plot = LinearRegression().fit(X, y)

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(X, y, s=22, alpha=0.6, label="actual houses")
ax.plot(np.sort(size), model_plot.predict(np.sort(size).reshape(-1, 1)),
        color="crimson", linewidth=2, label="model's line")
ax.set_xlabel("size (m²)")
ax.set_ylabel("price (thousands)")
ax.set_title("Supervised regression: the model learns a line")
ax.text(0.03, 0.93,
        f"price = {model_plot.intercept_:.1f} + {model_plot.coef_[0]:.2f} × size",
        transform=ax.transAxes, fontsize=10,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="gray"))
ax.legend()
ax.grid(alpha=0.3)
plt.savefig("plots/01_regression_line.png", dpi=150, bbox_inches="tight")
plt.show()

# ---------- 3. Now do it honestly: train/test split ----------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)

model = LinearRegression().fit(X_train, y_train)
pred  = model.predict(X_test)

rmse = mean_squared_error(y_test, pred) ** 0.5
print("intercept :", round(model.intercept_, 2))
print("weight    :", round(model.coef_[0], 3), "(thousand £ per m²)")
print("RMSE      :", round(rmse, 2), "thousand £")
print("R^2       :", round(r2_score(y_test, pred), 3))

# ---------- 4. Predicted vs actual ----------
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(y_test, pred, s=30, alpha=0.7)
lims = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
ax.plot(lims, lims, "k--", linewidth=1, label="perfect prediction")
ax.set_xlabel("actual price (thousands)")
ax.set_ylabel("predicted price (thousands)")
ax.set_title("Predicted vs actual on the held-out test set")
ax.legend()
ax.grid(alpha=0.3)
plt.savefig("plots/02_predicted_vs_actual.png", dpi=150, bbox_inches="tight")
plt.show()
```

### 3.4 Graph walkthrough

**`plots/01_regression_line.png`**

- **Each dot** = one house. X = size, Y = price.
- **The crimson line** is the model. It doesn't pass through every dot, and it shouldn't — the dots bounce around because of noise. It threads the middle of the band.
- **The text box** shows the learned rule. With my random seed it comes out around `price = 45 + 1.79 × size` (thousands), which is close to the `1.8` and `40` I secretly used to generate the data. That's the whole game: the model _recovered the hidden rule from examples_.
- **The dots' spread around the line** is the noise you can never explain. Real-world data has far more of it.
- **Read the weight like a sentence:** "1 extra m² is worth about 1.8 thousand." That interpretability is why linear models are still everywhere in business.

**`plots/02_predicted_vs_actual.png`**

- One dot per **test** house: actual price on X, predicted on Y.
- The **dashed diagonal** is perfection. Dots hugging it = accurate model.
- **Vertical distance to the diagonal = that prediction's error.** A dot far above the line means the model over-predicted.
- **A cloud shape** (rather than a tight cigar) means the model explains little. If the cloud is tilted horizontally around one value, the model has basically learned "always say the average."

### 3.5 How the model _learns_: the loss function

Training needs a way to score "how wrong am I?" so it can improve. For regression that's **Mean Squared Error**:

```
MSE = (1/n) · Σ (yᵢ − ŷᵢ)²
```

| Piece     | Meaning                                                                                                                               |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `n`       | Number of training examples.                                                                                                          |
| `yᵢ`      | The **actual** value for example `i`.                                                                                                 |
| `ŷᵢ`      | The **predicted** value for example `i`.                                                                                              |
| `yᵢ − ŷᵢ` | The **residual** — this example's error.                                                                                              |
| `( … )²`  | Squaring does two jobs: it makes negative and positive errors both count, and it **punishes big misses much harder** than small ones. |
| `Σ`       | Add up the squared errors over all examples.                                                                                          |
| `1/n`     | Divide by the count → an average.                                                                                                     |

Training is then a search: _find the weights `w` that make MSE as small as possible._ The algorithm (gradient descent) starts with random weights, checks which direction reduces MSE, and nudges them downhill, thousands of times. You rarely implement this — `.fit()` does it.

### 3.6 How you _judge_ the model

**RMSE** = `√MSE`. Same units as your target (thousand £ here), so it's readable: "typically off by about 26k."

**R² (R-squared)** — the share of the variation the model explains:

```
R² = 1 − SS_res / SS_tot

SS_res = Σ (yᵢ − ŷᵢ)²      ← your model's squared errors
SS_tot = Σ (yᵢ − ȳ)²       ← errors of the dumb baseline "always predict the mean"
```

| R² value | Meaning                                                        |
| -------- | -------------------------------------------------------------- |
| 1.0      | Perfect predictions. Suspicious in real life.                  |
| 0.7      | Explains 70% of the variation. Often a solid business model.   |
| 0.0      | No better than always guessing the average.                    |
| negative | **Worse** than guessing the average — you've broken something. |

### 3.7 Classification: when the answer is a category

The model computes a score `z` exactly like the regression formula, then squashes it into a probability with the **sigmoid**:

```
z = w₀ + w₁x₁ + ... + w_dx_d
p = 1 / (1 + e^(−z))
```

- `z` can be any number, from −∞ to +∞.
- `e^(−z)` explodes for very negative `z` and vanishes for very positive `z` — which forces `p` to land **between 0 and 1**, exactly like a probability should.
- **Decision rule:** predict class 1 if `p ≥ 0.5`, otherwise class 0.
- The set of points where `p = 0.5` (i.e. `z = 0`) is the **decision boundary** — a straight line in 2-D.

```python
import numpy as np, matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.linear_model import LogisticRegression

# Two clusters = two classes (0 and 1)
Xc, yc = make_blobs(n_samples=200, centers=[[2.5, 2.5], [5.5, 5.0]],
                    cluster_std=1.1, random_state=7)

clf = LogisticRegression(max_iter=1000).fit(Xc, yc)
print("accuracy on training data:", round(clf.score(Xc, yc), 3))

# Paint the whole plane with the model's opinion
xx, yy = np.meshgrid(np.linspace(0, 8, 400), np.linspace(0, 8, 400))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

fig, ax = plt.subplots(figsize=(7, 5))
ax.contourf(xx, yy, Z, alpha=0.18, cmap="coolwarm")
ax.scatter(Xc[:, 0], Xc[:, 1], c=yc, cmap="coolwarm", edgecolor="k", s=28)
ax.set_xlabel("feature 1")
ax.set_ylabel("feature 2")
ax.set_title("Classification: the model carves the plane into two regions")
plt.savefig("plots/03_classification_boundary.png", dpi=150, bbox_inches="tight")
plt.show()
```

**Graph walkthrough — `plots/03_classification_boundary.png`**

- Dots = examples, **colour = their true class**. Unlike regression, there's no line through them; the classes are clumps.
- The **shaded background** is the model's verdict for _every possible_ point, not just the ones it saw. Blue region = "I'd say class 0."
- The **seam between the two shades** is the decision boundary. A straight seam = logistic regression. Bendy seams = trees, SVM with a curved kernel, or neural nets.
- Points sitting on the wrong side of the seam are errors. A few are unavoidable when the clusters overlap — real data always overlaps.

---

## 4. Unsupervised learning — "no answer key, just structure"

You give the model **only inputs**. Nobody says what's right. It hunts for hidden structure.

- **Clustering** → group similar things together. _"Find customer segments."_ Nobody labelled those segments; the algorithm discovered them.
- **Dimensionality reduction** → squeeze many columns into a few meaningful ones (PCA, t-SNE, UMAP).

The mental model: **sorting a pile of loose photos into stacks** that seem to belong together, with nobody telling you the categories beforehand.

### 4.1 How clustering measures "similar"

Everything rests on **Euclidean distance** — the ordinary straight-line distance:

```
d(a, b) = √( (a₁−b₁)² + (a₂−b₂)² + ... + (a_d−b_d)² )
```

| Piece     | Meaning                                             |
| --------- | --------------------------------------------------- |
| `a`, `b`  | Two data points, each with `d` features.            |
| `a₁ − b₁` | The gap on the first feature.                       |
| `( … )²`  | Squared so gaps in any direction count positively.  |
| `√`       | Undo the squaring → distance in the original units. |

For 2 features this is literally Pythagoras. For 30 features it's the same idea in a space you can't draw.

**What K-Means minimises:** the total squared distance from each point to its own cluster centre (a.k.a. WCSS or _inertia_):

```
WCSS = Σ over clusters k  Σ over points x in cluster k  ‖x − μ_k‖²
```

- `μ_k` ("mu") = the **centroid**, the mean of all points in cluster `k`.
- `‖x − μ_k‖²` = squared distance from the point to its centroid.
- **Tight, compact clusters → small WCSS. That's what the algorithm is chasing.**

### 4.2 The algorithm, in four steps (Lloyd's algorithm)

1. Scatter `k` random centroids into the data.
2. **Assign** every point to its nearest centroid.
3. **Update** each centroid to the mean of the points now assigned to it.
4. Repeat 2–3 until the assignments stop changing.

At each round, WCSS can only go down or stay flat — which is why it always finishes.

### 4.3 Runnable code

```python
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

os.makedirs("plots", exist_ok=True)

# 300 unlabelled points in 4 natural groups
Xk, _ = make_blobs(n_samples=300, centers=4, cluster_std=0.9, random_state=3)

km = KMeans(n_clusters=4, n_init=10, random_state=0)
labels = km.fit_predict(Xk)          # note: we only pass X — there is no y

print("WCSS (inertia):", round(km.inertia_, 2))

fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(Xk[:, 0], Xk[:, 1], c=labels, cmap="viridis", s=28, alpha=0.8)
ax.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
           marker="X", s=220, c="red", edgecolor="black",
           label="centroids")
ax.set_title("Unsupervised K-Means: groups discovered without labels")
ax.legend()
ax.grid(alpha=0.3)
plt.savefig("plots/04_clusters.png", dpi=150, bbox_inches="tight")
plt.show()
```

**Graph walkthrough — `plots/04_clusters.png`**

- The generator secretly made 4 blobs, but the algorithm was **never told that**. It found them from geometry alone.
- **Colour = the discovered cluster.** Any consistent colour scheme is fine — cluster 2 isn't "better" than cluster 0.
- **Red X's = centroids.** Notice each sits at the visual centre of its colour cloud. That's the "mean of the members" rule from step 3.
- **Boundaries between colours are roughly halfway between centroids** — that's the nearest-centroid rule from step 2.
- What K-Means _cannot_ do: find odd shapes. It assumes clusters are roughly round and similar in size. Two interlocking crescents will confuse it badly.

### 4.4 How do you pick `k` when nobody tells you? The elbow method

Try several values of `k`, plot WCSS, and look for the bend:

```python
inertias = []
ks = range(1, 11)
for k in ks:
    m = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xk)
    inertias.append(m.inertia_)

fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(list(ks), inertias, marker="o")
ax.set_xlabel("number of clusters (k)")
ax.set_ylabel("WCSS / inertia (lower = tighter)")
ax.set_title("Elbow method: where does the curve stop dropping fast?")
ax.grid(alpha=0.3)
plt.savefig("plots/05_elbow.png", dpi=150, bbox_inches="tight")
plt.show()
```

**Graph walkthrough — `plots/05_elbow.png`**

- WCSS **always falls** as `k` grows — with `k` = number of points, WCSS = 0. So "lowest WCSS" is a trap.
- You're looking for the **elbow**: the point where extra clusters stop buying you much. Here it bends hard at **k = 4**, the true answer.
- The **"just one more cluster" test**: from k=1→2, 2→3, 3→4 the drops are huge; after 4 they're shallow. That's the signal.
- The elbow is often ambiguous. Combine it with domain knowledge — _"we can realistically run four marketing campaigns, not twenty."_

**One critical practical note:** K-Means uses distances, so a feature measured in thousands (income) will drown one measured in single digits (number of children). **Always scale first** — `StandardScaler()` in the business case below.

---

## 5. Side by side

|                         | Supervised                           | Unsupervised                                   |
| ----------------------- | ------------------------------------ | ---------------------------------------------- |
| Data needed             | Inputs **+** labels                  | Inputs only                                    |
| Question answered       | "Predict this known thing"           | "What structure is in here?"                   |
| Typical tasks           | Regression, classification           | Clustering, dimensionality reduction           |
| Output type             | Number, or category                  | Group IDs, or compressed features              |
| Example                 | Will this customer churn?            | What kinds of customers do we have?            |
| Cost of data            | Expensive — humans must label        | Cheap — labels not needed                      |
| How you measure success | RMSE, R², accuracy, precision/recall | Silhouette score, inertia, and human judgement |
| Main risk               | Overfitting, data leakage            | Finding groups that aren't meaningful          |

_(A third family — **reinforcement learning** — learns by trial, error and reward, like a dog earning treats. Another day.)_

**Rule of thumb:** labelled data and a specific thing to predict → supervised. Exploring, and you just want to see what's in the data → unsupervised.

---

## 6. Business use case: FreshCart, an online grocery

**The company.** FreshCart delivers groceries. Marketing has a budget and a CRM full of customers. Two questions:

1. **Supervised:** _"How much will each customer spend next month?"_ → so we can target the discount where it pays for itself.
2. **Unsupervised:** _"What kinds of customers do we actually have?"_ → so we can talk to each group differently.

This is the classic pairing: **unsupervised finds the audience, supervised finds the value.**

### 6.1 The data and the code

```python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

os.makedirs("plots", exist_ok=True)
rng = np.random.default_rng(7)

# --- 1. A CRM export: 600 customers, 3 behavioural features ---
def make_segment(n, orders, basket, visits, noise=0.10):
    return pd.DataFrame({
        "orders_per_month": rng.normal(orders, orders * noise + 0.1, n).clip(0),
        "avg_basket":       rng.normal(basket, basket * noise, n).clip(1),
        "app_visits":       rng.normal(visits, visits * noise + 0.1, n).clip(0),
    })

df = pd.concat([
    make_segment(150, 8.0, 45, 22),    # frequent, small baskets
    make_segment(180, 1.5, 30,  5),    # occasional
    make_segment(120, 6.5, 120, 12),   # frequent, huge baskets
    make_segment(150, 2.0, 25,  1),    # nearly gone quiet
], ignore_index=True).round(2)

# The supervised target: what they'll spend next month
df["next_month_spend"] = (
    0.55 * df["orders_per_month"] * df["avg_basket"]
    + 0.8 * df["app_visits"]
    + rng.normal(0, 12, len(df))
).round(2)

features = ["orders_per_month", "avg_basket", "app_visits"]
X  = df[features].to_numpy()
Xs = StandardScaler().fit_transform(X)     # ← always scale before clustering

# --- 2. Unsupervised: how many segments? elbow first ---
print("k   inertia")
for k in range(2, 8):
    m = KMeans(n_clusters=k, n_init=10, random_state=0).fit(Xs)
    print(k, round(m.inertia_))

km = KMeans(n_clusters=4, n_init=10, random_state=0)
df["segment"] = km.fit_predict(Xs)

profile = df.groupby("segment")[features + ["next_month_spend"]].mean().round(1)
print("\nSegment profiles (centroid averages):\n", profile)

# --- 3. Supervised: predict next month's spend ---
Xtr, Xte, ytr, yte = train_test_split(X, df["next_month_spend"],
                                      test_size=0.2, random_state=0)
reg = LinearRegression().fit(Xtr, ytr)
print("\nR^2 on held-out customers:", round(r2_score(yte, reg.predict(Xte)), 3))
print("weights:", dict(zip(features, np.round(reg.coef_, 2))))

# --- 4. Picture the segments ---
cols_to_plot = features + ["next_month_spend"]
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, col in zip(axes, cols_to_plot):
    bars = ax.bar(profile.index.astype(str), profile[col], color="steelblue")
    ax.set_title(col.replace("_", " "))
    ax.set_xlabel("segment")
    ax.bar_label(bars, fmt="%.0f", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
fig.suptitle("What each discovered segment looks like (centroid averages)")
plt.tight_layout()
plt.savefig("plots/06_segment_profiles.png", dpi=150, bbox_inches="tight")
plt.show()
```

### 6.2 Graph walkthrough — `plots/06_segment_profiles.png`

Four small bar charts, one per feature/target, with segment 0–3 on the X axis. Because K-Means doesn't name anything, **your job is to read this table and name the groups yourself** (numbers will differ slightly for you — read the shape, not the digits):

- **One segment with ~8 orders/month but a ~£45 basket, high app usage** → _"Weekly regulars."_ Reliable revenue, low margin per order. Action: subscription / loyalty nudge, not discounts.
- **One segment with ~6.5 orders and a ~£120 basket** → _"Big-basket families."_ The most valuable group. Action: protect them, early access to new lines, generous free-delivery thresholds.
- **One segment with ~1.5 orders and low app visits** → _"Occasional browsers."_ Casual interest, low spend.
- **One segment with ~2 orders, low app usage, and a long gap since last order** → _"Lapsing."_ The rescue group.

Notice the **last chart, `next_month_spend`**, is the payoff: it converts a fuzzy "segment" into **money per customer**. That's where supervised and unsupervised meet.

### 6.3 What the business actually does with this

| Segment             | Avg. spend next month | Action                                           | Why                                                 |
| ------------------- | --------------------- | ------------------------------------------------ | --------------------------------------------------- |
| Big-basket families | Highest               | Retain: free delivery threshold, concierge picks | Losing one costs far more than any discount offered |
| Weekly regulars     | Medium–high           | Grow basket: "add 3 items for £5" prompts        | Already loyal; raise order value, don't discount    |
| Occasional browsers | Low                   | Activate: first-repeat-order voucher             | Cheap to test, clear upside                         |
| Lapsing             | Low, falling          | Win-back email with a hard deadline              | Highest _relative_ uplift potential, or let them go |

**The economics.** A 10% off voucher costs ~£12 on a £120 basket. Offered blindly to all 600 customers, that's a large spend for mostly-wasted margin. Offered only where the predicted spend uplift exceeds the discount, it becomes a **targeted** campaign. That shift — from "everyone gets 10% off" to "these 180 customers get it, those 120 get free delivery, those 150 get nothing" — is the entire commercial value of this tutorial.

**Bonus insight:** the regression weights tell you _which behaviour to push_. If `orders_per_month` carries the biggest weight, the lever is **frequency**, and the loyalty scheme matters more than the pricing page. That's a strategy answer for free, from a `.fit()` call.

---

## 7. Common beginner mistakes

1. **Evaluating on training data.** Always split. `train_test_split` is your friend.
2. **Data leakage.** A feature that secretly encodes the answer (e.g. `refund_issued` when predicting churn) makes scores look amazing and production fail. Ask of every column: _"would I actually know this at prediction time?"_
3. **Forgetting to scale** before anything distance-based (K-Means, k-NN, SVM, PCA).
4. **Believing the clusters are real.** K-Means will happily carve any blob into `k` groups, even pure noise. Check the elbow, and sanity-check with a domain expert.
5. **Assuming correlation is causation.** Weights show association, not cause.
6. **Chasing R² = 0.99.** In real business data that usually means leakage or overfitting, not genius.
7. **Treating cluster numbers as ordered.** Segment 3 is not "more" anything than segment 1.

---

## 8. Glossary

**Bias (intercept)** · **Weight (coefficient)** · **Residual** · **Loss function** · **MSE / RMSE** · **R²** · **Sigmoid** · **Decision boundary** · **Centroid** · **Inertia / WCSS** · **Elbow method** · **Feature scaling** · **Overfitting** · **Train/test split** · **Data leakage** · **Inference**

---

## 9. Where to go next

1. **Measure classification properly** — confusion matrix, precision, recall, F1, ROC-AUC.
2. **Try non-linear models** — `RandomForestRegressor`, `GradientBoostingRegressor`; compare R² against your linear baseline.
3. **Judge clusters numerically** — silhouette score instead of eyeballing.
4. **Compress features** — `PCA` to visualise 20-feature customer data in 2-D.
5. **Close the loop** — train, deploy, and check predictions against reality next month. A model nobody monitors is a model that silently rots.

**The one-sentence summary:** supervised learning predicts a number or a label from examples that came with answers; unsupervised learning finds hidden groups in examples that didn't — and the real business value appears when you use the second to find the audience and the first to price the decision.

```

Want me to also emit this as a single runnable `ml_intro.py` (all six plots in one script), or split it into a `plots/`-producing notebook-style file?
```
