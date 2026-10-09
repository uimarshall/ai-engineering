# ============================================================================
# Feature Selection in Machine Learning - Univariate Testing (filter methods)
# Companion script to feature_selection_univariate.md
# Run with:  python feature_selection_univariate.py
# Figures are written to ./plots/ and then displayed.
# ============================================================================

# ============================================================================
# 0. SETUP - imports, output folder, reproducibility
# ============================================================================
import os  # os -> create the plots folder

import matplotlib.pyplot as plt  # matplotlib -> draw the figures
import numpy as np  # numpy -> fast numeric arrays
import pandas as pd  # pandas -> tabular data (DataFrame)
from sklearn.datasets import load_breast_cancer  # bundled dataset, works offline
from sklearn.datasets import load_diabetes  # bundled regression dataset
from sklearn.feature_selection import SelectKBest  # keeps the "best k" features
from sklearn.feature_selection import SelectPercentile  # keeps the top X% of features
from sklearn.feature_selection import VarianceThreshold  # drops low-variance columns
from sklearn.feature_selection import chi2  # chi-square score function
from sklearn.feature_selection import f_classif  # ANOVA F for classification
from sklearn.feature_selection import f_regression  # F score for regression
from sklearn.feature_selection import mutual_info_classif  # MI for classification
from sklearn.feature_selection import r_regression  # Pearson r for regression
from sklearn.linear_model import LogisticRegression  # a simple, fast classifier
from sklearn.metrics import roc_auc_score  # evaluation metric (0.5 = random)
from sklearn.model_selection import train_test_split  # train/test split helper
from sklearn.pipeline import Pipeline  # chains steps without leakage
from sklearn.preprocessing import StandardScaler  # scales features for the model
from sklearn.utils import Bunch  # dataset loader result when return_X_y=False

PLOTS_DIR = "plots"  # every figure is saved in here
os.makedirs(PLOTS_DIR, exist_ok=True)  # create the folder if it is missing
RANDOM_STATE = 42  # fixed seed -> reproducible output
np.random.seed(RANDOM_STATE)  # seed numpy's legacy random module


# ============================================================================
# 1. HELPER - save every figure to ./plots/ AND display it
# ============================================================================
def save_and_show(fig, filename):
    """Save a matplotlib figure to disk, then show it on screen."""
    path = os.path.join(PLOTS_DIR, filename)  # build the output path
    fig.savefig(path, dpi=120, bbox_inches="tight")  # write the PNG to ./plots/
    plt.show()  # display the figure interactively
    print(f"  saved -> {path}")  # tell the user where it went


# ============================================================================
# 2. DATA - a real, bundled dataset (no internet needed)
# ============================================================================
def load_breast_cancer_data():
    """Load the breast-cancer dataset: 569 rows, 30 numeric features."""
    bunch = load_breast_cancer(as_frame=True, return_X_y=False)  # returns a Bunch object
    if not isinstance(bunch, Bunch):
        raise TypeError("Expected load_breast_cancer to return a Bunch.")
    X = bunch.data.copy()  # features -> pandas DataFrame
    y = bunch.target.copy()  # target -> 0 = malignant, 1 = benign
    print("Dataset shape:", X.shape)  # 569 rows x 30 columns
    print("Class balance:", y.value_counts().to_dict())  # how many of each class
    return X, y  # hand back both pieces


# ============================================================================
# 3. VARIANCE THRESHOLD - the cheapest cleaning filter
# ============================================================================
def demo_variance_threshold(X):
    """Show how VarianceThreshold removes constant / almost-constant columns."""
    print("\n[1] VarianceThreshold")
    X_demo = X.copy()  # work on a copy, never mutate the original
    X_demo["constant_feature"] = 1.0  # identical value in every row -> variance 0
    X_demo["almost_constant"] = 0.0  # mostly zeros ...
    X_demo.loc[X_demo.index[:3], "almost_constant"] = (
        1.0  # ... except 3 rows -> tiny variance
    )

    variances = X_demo.var(axis=0)  # per-column variance (sigma squared)
    print(
        "  constant_feature variance:", round(variances["constant_feature"], 6)
    )  # 0.0
    print(
        "  almost_constant variance :", round(variances["almost_constant"], 8)
    )  # ~1e-5

    selector = VarianceThreshold(threshold=0.01)  # drop anything with variance <= 0.01
    X_reduced = selector.fit_transform(X_demo)  # fit + transform in one call
    kept = X_demo.columns[selector.get_support()]  # boolean mask -> names of survivors
    print(f"  kept {X_reduced.shape[1]} of {X_demo.shape[1]} columns")
    print("  dropped:", sorted(set(X_demo.columns) - set(kept)))

    fig, ax = plt.subplots(figsize=(11, 5))  # new figure, 11x5 inches
    order = variances.sort_values().index  # sort columns by variance, smallest first
    ax.bar(
        range(len(order)), variances[order].values, color="indianred"
    )  # one bar per column
    ax.set_yscale("log")  # log scale: variances span many orders
    ax.axhline(
        0.01, color="black", linestyle="--", label="threshold = 0.01"
    )  # decision line
    ax.set_xticks(range(len(order)))  # one tick per bar
    ax.set_xticklabels(order, rotation=90, fontsize=7)  # rotate names so they fit
    ax.set_ylabel("Variance (log scale)")  # y-axis label
    ax.set_title("Per-feature variance - everything below the dashed line is dropped")
    ax.legend()  # show the legend
    fig.tight_layout()  # avoid overlapping labels
    save_and_show(fig, "01_variance_threshold.png")  # save to plots/ and show


# ============================================================================
# 4. CHI-SQUARE - for count/frequency features and a categorical target
# ============================================================================
def demo_chi2():
    """Simulate text-like word counts and find the words that predict the label."""
    print("\n[2] Chi-square test on count features (text-like data)")
    rng = np.random.default_rng(RANDOM_STATE)  # modern, seeded random generator

    n = 600  # number of documents (rows)
    word_a = rng.poisson(6, n)  # "word_a" appears ~6 times per doc
    word_b = rng.poisson(5, n)  # "word_b" ~5 times
    word_c = rng.poisson(4, n)  # "word_c" ~4 times (weak signal)
    word_d = rng.poisson(3, n)  # "word_d" ~3 times (weak signal)
    y = ((word_a + word_b) > 10).astype(int)  # label depends ONLY on word_a and word_b

    noise = rng.poisson(3, size=(n, 6))  # 6 pure-noise count features
    X = np.column_stack([word_a, word_b, word_c, word_d])  # stack the 4 real words
    X = np.hstack([X, noise])  # append the 6 noise columns
    names = ["word_a", "word_b", "word_c", "word_d"] + [
        f"noise_{i+1}" for i in range(6)
    ]

    scores, pvals = chi2(X, y)  # chi2 score + p-value for each column
    df = pd.DataFrame({"feature": names, "chi2": scores, "p_value": pvals})
    df = df.sort_values("chi2", ascending=False)  # best features first
    print(df.head(6).to_string(index=False))  # show the top 6

    colors = [
        "seagreen" if pv < 0.05 else "lightgray" for pv in df["p_value"]
    ]  # highlight significant
    fig, ax = plt.subplots(figsize=(9, 5))  # new figure
    ax.bar(df["feature"], df["chi2"], color=colors)  # bar per feature
    ax.set_ylabel("chi2 score")  # y-axis label
    ax.set_title("Chi-square scores (green = statistically significant, p < 0.05)")
    ax.tick_params(axis="x", rotation=45)  # rotate feature names
    fig.tight_layout()  # tidy up spacing
    save_and_show(fig, "02_chi2_scores.png")  # save + show


# ============================================================================
# 5. ANOVA F-TEST - continuous features, categorical target
# ============================================================================
def demo_f_classif(X, y):
    """Rank the 30 breast-cancer features with the ANOVA F-test."""
    print("\n[3] ANOVA F-test (f_classif)")
    F, p = f_classif(X, y)  # F value + p-value per feature
    df = pd.DataFrame({"feature": X.columns, "F": F, "p": p})
    df = df.sort_values("F", ascending=False)  # strongest features first
    print(df.head(5).to_string(index=False))  # print the top 5

    top = df.head(15).iloc[::-1]  # 15 best, reversed for horizontal bars
    fig, ax = plt.subplots(figsize=(9, 7))  # new figure
    ax.barh(top["feature"], top["F"], color="steelblue")  # horizontal bars
    ax.set_xlabel("ANOVA F value (higher = classes are better separated)")
    ax.set_title("Top 15 features by ANOVA F-test - breast cancer")
    fig.tight_layout()  # tidy spacing
    save_and_show(fig, "03_f_classif_top15.png")  # save + show


# ============================================================================
# 6. MUTUAL INFORMATION - also catches non-linear relationships
# ============================================================================
def demo_mutual_information(X, y):
    """Compare the MI ranking against the ANOVA F ranking."""
    print("\n[4] Mutual information vs ANOVA F")
    mi = mutual_info_classif(X, y, random_state=RANDOM_STATE)  # MI score per feature
    F, _ = f_classif(X, y)  # F score per feature (p ignored here)
    df = pd.DataFrame({"feature": X.columns, "mi": mi, "F": F})
    top = df.sort_values("mi", ascending=False).head(15).iloc[::-1]  # 15 best by MI

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))  # 1 row, 2 side-by-side panels
    axes[0].barh(top["feature"], top["mi"], color="seagreen")  # left panel: MI
    axes[0].set_title("Top 15 by mutual information")  # panel title
    axes[0].set_xlabel("MI score (bits)")  # panel x-label
    axes[1].barh(top["feature"], top["F"], color="steelblue")  # right panel: F
    axes[1].set_title("Same 15 features, ANOVA F")  # panel title
    axes[1].set_xlabel("F value")  # panel x-label
    fig.tight_layout()  # tidy spacing
    save_and_show(fig, "04_mi_vs_f.png")  # save + show

    fig2, ax = plt.subplots(figsize=(8, 6))  # scatter figure
    ax.scatter(df["F"], df["mi"], alpha=0.7, color="darkorange")  # F vs MI per feature
    for _, row in df.nlargest(5, "mi").iterrows():  # label only the top 5
        ax.annotate(
            row["feature"], (row["F"], row["mi"]), fontsize=8
        )  # tiny text labels
    ax.set_xlabel("ANOVA F value")  # x-axis label
    ax.set_ylabel("Mutual information")  # y-axis label
    ax.set_title("Do F and MI agree? (usually yes, with disagreements at the edges)")
    fig2.tight_layout()  # tidy spacing
    save_and_show(fig2, "05_mi_vs_f_scatter.png")  # save + show


# ============================================================================
# 7. SELECTKBEST - how many features are actually enough?
# ============================================================================
def demo_selectkbest(X, y):
    """Sweep k and measure test ROC-AUC, with a leakage-free pipeline."""
    print("\n[5] SelectKBest: performance vs number of features")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=RANDOM_STATE
    )  # 75/25 split, keep class ratio

    k_values = [1, 2, 3, 5, 8, 10, 15, 20, 25, 30]  # candidate feature counts
    aucs = []  # will collect one AUC per k

    for k in k_values:  # loop over the candidates
        pipe = Pipeline(
            [  # a pipeline = safe + no leakage
                ("scaler", StandardScaler()),  # scale features for logistic regression
                (
                    "select",
                    SelectKBest(score_func=f_classif, k=k),
                ),  # keep the best k by ANOVA F
                ("clf", LogisticRegression(max_iter=5000)),  # train the classifier
            ]
        )
        pipe.fit(X_train, y_train)  # fit ONLY on the training split
        proba = pipe.predict_proba(X_test)[:, 1]  # predicted probability of class 1
        aucs.append(roc_auc_score(y_test, proba))  # score on the untouched test split

    baseline_pipe = Pipeline(
        [  # control: no feature selection at all
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=5000)),
        ]
    )
    baseline_pipe.fit(X_train, y_train)  # fit the baseline
    baseline = float(
        roc_auc_score(y_test, baseline_pipe.predict_proba(X_test)[:, 1])
    )  # baseline AUC

    pct_pipe = Pipeline(
        [  # alternative: keep a percentage
            ("scaler", StandardScaler()),
            (
                "select",
                SelectPercentile(score_func=f_classif, percentile=50),
            ),  # top 50%
            ("clf", LogisticRegression(max_iter=5000)),
        ]
    )
    pct_pipe.fit(X_train, y_train)  # fit the percentile pipeline
    n_pct = int(pct_pipe.named_steps["select"].get_support().sum())  # how many survived
    auc_pct = roc_auc_score(
        y_test, pct_pipe.predict_proba(X_test)[:, 1]
    )  # its test AUC

    print(f"  baseline (all {X.shape[1]} features) AUC: {baseline:.3f}")
    print(f"  SelectPercentile(50%) kept {n_pct} features -> AUC {auc_pct:.3f}")

    fig, ax = plt.subplots(figsize=(9, 5))  # new figure
    ax.plot(k_values, aucs, marker="o", label="SelectKBest + LogisticRegression")
    ax.axhline(
        baseline,
        color="black",
        linestyle="--",
        label=f"all features (AUC = {baseline:.3f})",
    )  # baseline reference line
    ax.set_xlabel("k = number of selected features")  # x-axis label
    ax.set_ylabel("Test ROC-AUC")  # y-axis label
    ax.set_title("Performance vs number of univariately selected features")
    ax.legend()  # show the legend
    ax.grid(alpha=0.3)  # light grid for readability
    fig.tight_layout()  # tidy spacing
    save_and_show(fig, "06_auc_vs_k.png")  # save + show


# ============================================================================
# 8. MULTIPLE TESTING - with 10,000 features, 500 "significant" ones are luck
# ============================================================================
def benjamini_hochberg(p_values, alpha=0.05):
    """Benjamini-Hochberg FDR control. Returns a boolean 'keep' mask."""
    p = np.asarray(p_values, dtype=float)  # ensure we work with a numpy array
    m = p.size  # number of tests (features)
    order = np.argsort(p)  # indices that sort p ascending
    ranked = p[order]  # p-values sorted ascending
    thresholds = alpha * np.arange(1, m + 1) / m  # BH threshold line: alpha * i / m
    below = ranked <= thresholds  # which sorted p-values beat their line
    if not below.any():  # nothing survives ...
        return np.zeros(m, dtype=bool)  # ... so return an all-False mask
    k_max = np.max(np.where(below)[0])  # largest rank that passed
    cutoff = ranked[k_max]  # its p-value becomes the cutoff
    return p <= cutoff  # keep everything at or below the cutoff


def demo_multiple_testing(X, y):
    """Compare raw p-values, Bonferroni and Benjamini-Hochberg."""
    print("\n[6] Multiple testing correction")
    _, p = f_classif(X, y)  # we only need the p-values here
    raw = p < 0.05  # naive: p-value below 5%
    bonferroni = p < (0.05 / len(p))  # strict: divide alpha by number of tests
    bh = benjamini_hochberg(
        p, alpha=0.05
    )  # balanced: controls the false-discovery rate
    print(f"  uncorrected p < 0.05 : {int(raw.sum())} features")
    print(f"  Bonferroni corrected : {int(bonferroni.sum())} features")
    print(f"  Benjamini-Hochberg   : {int(bh.sum())} features")
    print(f"  smallest p-value     : {p.min():.3e}")


# ============================================================================
# 9. REGRESSION - f_regression and Pearson r when the target is numeric
# ============================================================================
def demo_regression_univariate():
    """Rank diabetes-progression features with f_regression and Pearson r."""
    print("\n[7] Regression flavour: f_regression and r_regression (diabetes dataset)")
    diabetes = load_diabetes(as_frame=True, return_X_y=False)
    if not isinstance(diabetes, Bunch):
        raise TypeError("Expected load_diabetes to return a Bunch.")
    X, y = diabetes.data, diabetes.target

    F, p = f_regression(X, y)  # F statistic + p-value per feature
    r = r_regression(X, y)  # Pearson correlation per feature
    df = pd.DataFrame({"feature": X.columns, "F": F, "p": p, "r": r})
    df["abs_r"] = df["r"].abs()  # magnitude of the correlation
    top = (
        df.sort_values("abs_r", ascending=False).head(10).iloc[::-1]
    )  # 10 strongest, reversed

    colors = [
        "indianred" if v < 0 else "steelblue" for v in top["r"]
    ]  # red = negative, blue = positive
    fig, ax = plt.subplots(figsize=(9, 6))  # new figure
    ax.barh(top["feature"], top["r"], color=colors)  # horizontal bars of r
    ax.axvline(0, color="black", linewidth=1)  # zero line = "no linear relationship"
    ax.set_xlabel("Pearson r  (blue = positive, red = negative)")
    ax.set_title("Top 10 diabetes features by |Pearson r|")
    fig.tight_layout()  # tidy spacing
    save_and_show(fig, "07_regression_scores.png")  # save + show

    print(
        df.sort_values("F", ascending=False).head(5).to_string(index=False)
    )  # top 5 by F


# ============================================================================
# 10. REDUNDANCY - univariate tests love duplicated features
# ============================================================================
def demo_redundancy(X, y):
    """Show how highly correlated features all get high scores (they are clones)."""
    print("\n[8] Redundancy check on the top features")
    F, _ = f_classif(X, y)  # score every feature
    top_features = X.columns[np.argsort(F)[::-1][:8]]  # names of the 8 best features
    corr = X[list(top_features)].corr()  # 8x8 correlation matrix

    fig, ax = plt.subplots(figsize=(9, 7))  # new figure
    im = ax.imshow(
        corr.values, cmap="coolwarm", vmin=-1, vmax=1
    )  # heatmap of correlations
    ax.set_xticks(range(len(top_features)))  # x tick positions
    ax.set_xticklabels(top_features, rotation=90, fontsize=8)  # x tick labels
    ax.set_yticks(range(len(top_features)))  # y tick positions
    ax.set_yticklabels(top_features, fontsize=8)  # y tick labels
    for i in range(len(top_features)):  # loop over rows ...
        for j in range(len(top_features)):  # ... and columns
            ax.text(
                j,
                i,
                f"{corr.values[i, j]:.2f}",  # write the number in the cell
                ha="center",
                va="center",
                fontsize=7,
            )
    fig.colorbar(im, ax=ax, shrink=0.8, label="correlation")  # colour scale
    ax.set_title("Correlation between the 8 best ANOVA features")
    fig.tight_layout()  # tidy spacing
    save_and_show(fig, "08_redundancy_heatmap.png")  # save + show

    pairs = [
        (a, b, corr.loc[a, b])
        for i, a in enumerate(top_features)
        for b in top_features[i + 1 :]
        if abs(corr.loc[a, b]) > 0.9
    ]  # near-duplicate pairs
    if pairs:  # only print when we found something
        a, b, value = pairs[0]  # take the first example
        print(
            f"  {len(pairs)} pairs with |r| > 0.9, e.g. '{a}' vs '{b}' (r = {value:.3f})"
        )


# ============================================================================
# 11. MAIN - run every demo in order
# ============================================================================
if __name__ == "__main__":  # only run when executed directly
    X, y = load_breast_cancer_data()  # step 1: load the data
    demo_variance_threshold(X)  # step 2: clean dead columns
    demo_chi2()  # step 3: chi-square on count data
    demo_f_classif(X, y)  # step 4: ANOVA F on continuous data
    demo_mutual_information(X, y)  # step 5: MI vs F comparison
    demo_selectkbest(X, y)  # step 6: choose how many features
    demo_multiple_testing(X, y)  # step 7: correct the p-values
    demo_regression_univariate()  # step 8: the regression flavour
    demo_redundancy(X, y)  # step 9: spot duplicated features
    print("\nAll done. Figures are in the 'plots/' folder.")  # closing message
