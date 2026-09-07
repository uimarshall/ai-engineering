# 📊 Statistics for Data Science — A Beginner's Comprehensive Guide

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Descriptive Statistics](#2-descriptive-statistics)
3. [Probability Distributions](#3-probability-distributions)
4. [Inferential Statistics](#4-inferential-statistics)
5. [Correlation & Regression](#5-correlation--regression)
6. [Sampling & Central Limit Theorem](#6-sampling--central-limit-theorem)
7. [Company Use Cases](#7-company-use-cases)
8. [Complete Python Code Reference](#8-complete-python-code-reference)

---

## 1. Introduction

**What is Statistics?**  
Statistics is the science of collecting, organizing, analyzing, interpreting, and presenting data. In data science, statistics is the **foundation** that allows us to turn raw numbers into actionable business insights.

**Why do Data Scientists need Statistics?**

- To understand patterns in customer behavior
- To make predictions about future trends
- To test whether a new feature actually works (A/B testing)
- To measure uncertainty and make confident decisions
- To communicate findings with numbers that back up claims

---

## 2. Descriptive Statistics

Descriptive statistics summarize and describe the main features of a dataset. Think of it as creating a "profile" of your data.

### 2.1 Measures of Central Tendency

These tell you **where the center of your data is**.

#### **Mean (Average)**

The sum of all values divided by the count of values.

$$\text{Mean} = \bar{x} = \frac{\sum_{i=1}^{n} x_i}{n}$$

**Breaking it down:**

- $\sum$ (sigma) means "sum of"
- $x_i$ = each individual data point
- $n$ = total number of data points
- $\bar{x}$ = the mean (x-bar)

```python
import numpy as np

salaries = [45, 52, 55, 58, 60, 62, 65, 68, 70, 72,
            75, 80, 85, 90, 95, 100, 110, 120, 150, 200]

mean_salary = np.mean(salaries)
print(f"Mean Salary: ${mean_salary:.1f}k")  # Output: $85.6k
```

**What the code does:** `np.mean()` adds all 20 salaries (total = $1,712k) and divides by 20, giving $85.6k.

**What the graph shows (Figure 1, Top-Left):** The histogram shows most employees earn $45k–$80k, but the **mean (red dashed line at $85.6k)** is pulled upward by the CEO's $200k salary. This is why the mean lies to the right of where most data clusters.

---

#### **Median**

The middle value when data is sorted. If there's an even number of values, it's the average of the two middle values.

```python
median_salary = np.median(salaries)
print(f"Median Salary: ${median_salary:.1f}k")  # Output: $73.5k
```

**What the code does:** Sorts the 20 salaries and averages the 10th ($72k) and 11th ($75k) values.

**What the graph shows (Figure 1, Top-Left):** The **median (green dashed line at $73.5k)** sits closer to where most employees actually earn. Unlike the mean, the median is **not affected by outliers** like the CEO's salary.

> **💡 Business Insight:** When reporting "average salary," companies often use median to avoid distortion from executive pay. When reporting "average revenue per customer," use mean if no extreme outliers exist.

---

#### **Mode**

The most frequently occurring value.

```python
from scipy import stats
mode_result = stats.mode(salaries, keepdims=True)
print(f"Mode: {mode_result.mode[0]}")  # May show multiple or no clear mode
```

---

### 2.2 Measures of Dispersion

These tell you **how spread out your data is**.

#### **Variance**

The average of squared differences from the mean.

$$\sigma^2 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n}$$

**Breaking it down:**

- $(x_i - \bar{x})$ = how far each point is from the mean (deviation)
- Squaring ensures all values are positive (so negative and positive deviations don't cancel)
- $\sum$ adds all these squared deviations
- Dividing by $n$ gives the average squared deviation

```python
variance = np.var(salaries, ddof=0)  # Population variance
sample_variance = np.var(salaries, ddof=1)  # Sample variance
print(f"Variance: {variance:.1f}")
```

---

#### **Standard Deviation (σ)**

The square root of variance — brings units back to the original scale.

$$\sigma = \sqrt{\sigma^2} = \sqrt{\frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n}}$$

```python
std_dev = np.std(salaries, ddof=1)
print(f"Standard Deviation: ${std_dev:.1f}k")
```

**What the graph shows (Figure 1, Bottom-Left):** Two companies both have average monthly sales of $70k. **Company A (blue, σ=5)** has a narrow, tall distribution — sales are predictable. **Company B (orange, σ=15)** is wide and flat — sales swing wildly. A business prefers lower standard deviation for predictable revenue.

> **💡 Business Insight:** A retail chain with low σ in daily sales can optimize staffing. A startup with high σ might need cash reserves for volatile months.

---

#### **Interquartile Range (IQR)**

The range of the middle 50% of data. Robust to outliers.

$$\text{IQR} = Q_3 - Q_1$$

Where:

- $Q_1$ (25th percentile) = value below which 25% of data falls
- $Q_3$ (75th percentile) = value below which 75% of data falls

```python
q1 = np.percentile(salaries, 25)
q3 = np.percentile(salaries, 75)
iqr = q3 - q1
print(f"Q1: ${q1:.1f}k, Q3: ${q3:.1f}k, IQR: ${iqr:.1f}k")
```

**What the graph shows (Figure 1, Top-Right):** The box plot's purple box spans from Q1 ($61.5k) to Q3 ($96.2k), so IQR = $34.8k. The red line inside is the median ($73.5k). The red dots above are outliers (CEO and senior executives).

---

### 2.3 Percentiles

Percentiles tell you **relative standing** — what percentage of data falls below a value.

```python
p10 = np.percentile(salaries, 10)   # Bottom 10%
p90 = np.percentile(salaries, 90)   # Top 10%
print(f"10th percentile: ${p10:.1f}k (bottom 10%)")
print(f"90th percentile: ${p90:.1f}k (top 10%)")
```

**What the graph shows (Figure 1, Bottom-Right):** In an exam score distribution, the 10th percentile (~60) means 10% of students scored below 60. The 90th percentile (~90) means 90% scored below 90 (top 10% scored above).

> **💡 Business Insight:** E-commerce sites use percentiles for pricing. "This hotel is priced lower than 75% of similar properties" uses the 75th percentile as a benchmark.

---

## 3. Probability Distributions

A probability distribution describes **how likely different outcomes are**.

### 3.1 Normal Distribution (Gaussian / Bell Curve)

The most important distribution in statistics. Many natural phenomena follow it.

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$$

**Breaking it down:**

- $\mu$ (mu) = mean (center of the bell)
- $\sigma$ (sigma) = standard deviation (width of the bell)
- $e$ = Euler's number (~2.718)
- The formula creates a symmetric bell shape where most data clusters around the mean

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Generate normal distribution data
heights = np.random.normal(loc=170, scale=10, size=1000)  # Mean=170cm, SD=10cm

# Probability Density Function
x = np.linspace(140, 200, 1000)
pdf = stats.norm.pdf(x, loc=170, scale=10)

plt.plot(x, pdf)
plt.title("Height Distribution: Mean=170cm, SD=10cm")
plt.show()
```

**The 68-95-99.7 Rule (Empirical Rule):**

- **68%** of data falls within $\mu \pm 1\sigma$
- **95%** of data falls within $\mu \pm 2\sigma$
- **99.7%** of data falls within $\mu \pm 3\sigma$

**What the graph shows (Figure 2, Top-Left):** The standard normal curve (mean=0, SD=1) with shaded regions. Between -1 and +1 (one SD), ~68% of area is shaded. Between -2 and +2, ~95%. This rule lets you quickly estimate probabilities without calculations.

> **💡 Business Insight:** A manufacturing company uses this to set quality control limits. If widget diameter should be 10cm ± 0.5cm, measurements outside $\mu \pm 3\sigma$ trigger alerts (only 0.3% chance if process is normal).

---

### 3.2 Binomial Distribution

Models the number of successes in **n independent trials** with the same probability of success.

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

**Breaking it down:**

- $\binom{n}{k} = \frac{n!}{k!(n-k)!}$ = number of ways to choose k successes from n trials
- $p^k$ = probability of k successes
- $(1-p)^{n-k}$ = probability of (n-k) failures
- $P(X=k)$ = probability of exactly k successes

```python
# Email campaign: 20 emails, 30% open rate
n, p = 20, 0.3
k_values = np.arange(0, 21)
probabilities = stats.binom.pmf(k_values, n, p)

for k, prob in zip(k_values, probabilities):
    print(f"P(X={k}) = {prob:.4f}")
```

**What the graph shows (Figure 2, Top-Right):** For 20 emails with 30% open probability, the most likely outcome is ~6 opens (peak of the red bars). The probability of 0 opens is nearly zero, and 20 opens is also nearly impossible.

> **💡 Business Insight:** Marketing teams use this to set realistic campaign expectations. "If we send 10,000 emails with 20% historical open rate, we expect 2,000 ± 40 opens (with 95% confidence)."

---

### 3.3 Poisson Distribution

Models the number of events occurring in a **fixed interval** of time or space.

$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

**Breaking it down:**

- $\lambda$ (lambda) = average rate of occurrence (mean number of events)
- $k$ = actual number of events we're calculating probability for
- $k!$ = k factorial (k × (k-1) × ... × 1)
- $e^{-\lambda}$ = decay factor based on average rate

```python
# Average 4 website crashes per week
lambda_val = 4
k_values = np.arange(0, 15)
probabilities = stats.poisson.pmf(k_values, lambda_val)

print(f"P(0 crashes) = {stats.poisson.pmf(0, lambda_val):.4f}")
print(f"P(4 crashes) = {stats.poisson.pmf(4, lambda_val):.4f}")
```

**What the graph shows (Figure 2, Bottom-Left):** With an average of 4 crashes/week, the probability is highest at exactly 4 crashes. The probability of 10+ crashes is very low (~0.5%).

> **💡 Business Insight:** IT operations use Poisson to determine staffing. "If we average 5 support tickets/hour, we need enough staff to handle 8 tickets (99th percentile) during peak."

---

### 3.4 Skewness

Skewness describes the **asymmetry** of a distribution.

**What the graph shows (Figure 2, Bottom-Right):**

- **Symmetric (blue):** Mean = Median = Mode. Example: Heights of adults.
- **Right-skewed/Positive skew (orange):** Tail extends right. Mean > Median. Example: Income distribution (most people earn modestly, few earn millions).
- **Left-skewed/Negative skew (green):** Tail extends left. Mean < Median. Example: Exam scores on an easy test (most score high, few score low).

```python
from scipy.stats import skew

data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 100]  # Right-skewed
print(f"Skewness: {skew(data):.2f}")  # Positive = right-skewed
```

> **💡 Business Insight:** E-commerce order values are typically right-skewed. The mean order value is inflated by a few big spenders. For inventory planning, use the median order value instead.

---

## 4. Inferential Statistics

Inferential statistics let you **make conclusions about a population** based on a sample.

### 4.1 Hypothesis Testing

A formal process to test claims using data.

**The Framework:**

1. **Null Hypothesis ($H_0$):** The default assumption (no effect, no difference)
2. **Alternative Hypothesis ($H_1$):** What you want to prove
3. **Test Statistic:** A number calculated from your sample
4. **p-value:** Probability of seeing your results if $H_0$ were true
5. **Decision:** Reject $H_0$ if p-value < significance level (usually 0.05)

**The t-statistic formula:**

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

**Breaking it down:**

- $\bar{x}$ = sample mean
- $\mu_0$ = hypothesized population mean (under $H_0$)
- $s$ = sample standard deviation
- $n$ = sample size
- $s / \sqrt{n}$ = **standard error** (how much sample means typically vary)
- The t-statistic measures: _"How many standard errors is our sample mean from the hypothesized mean?"_

```python
from scipy import stats
import numpy as np

# A/B Test: Does new button increase clicks?
# Control group (old button): 100 users, 12% click rate
# Treatment group (new button): 100 users, 18% click rate

control = np.random.binomial(1, 0.12, 100)
treatment = np.random.binomial(1, 0.18, 100)

# Two-sample t-test
t_stat, p_value = stats.ttest_ind(treatment, control)

print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("✅ SIGNIFICANT: New button performs better!")
else:
    print("❌ NOT SIGNIFICANT: Could be random chance.")
```

**What the graph shows (Figure 3, Top-Left):** The blue curve is the t-distribution under the null hypothesis (no difference). The red shaded "rejection regions" represent extreme values that would occur less than 5% of the time if $H_0$ were true. The green line shows our observed t-statistic (2.5) falling in the rejection region — we reject $H_0$!

> **💡 Business Insight:** Netflix runs thousands of A/B tests. A new thumbnail might increase watch time by 2%, but hypothesis testing confirms whether this improvement is real or just random variation.

---

### 4.2 Confidence Intervals

A confidence interval gives a **range of plausible values** for a population parameter.

$$\text{CI} = \bar{x} \pm t_{\alpha/2} \times \frac{s}{\sqrt{n}}$$

**Breaking it down:**

- $\bar{x}$ = sample mean (our best estimate)
- $t_{\alpha/2}$ = critical value from t-distribution (depends on confidence level and sample size)
- $\frac{s}{\sqrt{n}}$ = standard error
- The $\pm$ creates a range around our estimate

```python
import numpy as np
from scipy import stats

# Sample of 50 customers, average spend = $85, std = $20
sample_mean = 85
sample_std = 20
n = 50
confidence = 0.95

# Calculate confidence interval
se = sample_std / np.sqrt(n)  # Standard error
ci = stats.t.interval(confidence, df=n-1, loc=sample_mean, scale=se)

print(f"95% Confidence Interval: ${ci[0]:.2f} to ${ci[1]:.2f}")
# Output: We're 95% confident the true average spend is between ~$79 and ~$91
```

**What the graph shows (Figure 3, Top-Right):** 100 different samples were taken from a population with true mean = 100. Each dot is a sample mean. The blue band is the 95% confidence interval. About 95 green dots (sample means) fall inside — their CIs capture the true mean. About 5 red dots fall outside — their CIs miss.

> **💡 Business Insight:** A survey reports "Customer satisfaction is 78% ± 4%." The ±4% is the margin of error. Stakeholders know the true satisfaction is likely between 74% and 82%.

---

### 4.3 p-values Explained Simply

The **p-value** answers: _"If the null hypothesis were true, what is the probability of seeing results this extreme or more extreme?"_

- **p < 0.05:** Less than 5% chance results are due to luck → **Reject $H_0$**
- **p ≥ 0.05:** Results could reasonably happen by chance → **Fail to reject $H_0$**

> ⚠️ **Common Misconception:** p-value is NOT the probability that $H_0$ is true. It's the probability of the data given $H_0$, not the probability of $H_0$ given the data.

---

## 5. Correlation & Regression

### 5.1 Correlation

Correlation measures the **strength and direction** of a linear relationship between two variables.

**Pearson Correlation Coefficient:**

$$r = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n} (x_i - \bar{x})^2} \times \sqrt{\sum_{i=1}^{n} (y_i - \bar{y})^2}}$$

**Breaking it down:**

- **Numerator:** Covariance — measures how x and y vary together. Positive when both are above/below their means together.
- **Denominator:** Product of standard deviations of x and y — normalizes the covariance to a -1 to +1 scale.
- $r = +1$: Perfect positive linear relationship
- $r = -1$: Perfect negative linear relationship
- $r = 0$: No linear relationship

```python
import numpy as np
from scipy.stats import pearsonr

# Ad spend vs Sales
ad_spend = [10, 20, 30, 40, 50, 60, 70, 80]
sales = [15, 25, 35, 45, 55, 65, 75, 85]

r, p_value = pearsonr(ad_spend, sales)
print(f"Correlation: r = {r:.3f}, p-value = {p_value:.4f}")
# Output: r ≈ 1.0 (perfect positive correlation)
```

**What the graph shows (Figure 3, Bottom-Left):** Three scatter plots overlaid:

- **Green (positive, r≈0.85):** As ad spend increases, sales increase. The trend line slopes upward.
- **Red (negative, r≈-0.90):** As price increases, demand decreases. The trend line slopes downward.
- **Gray (no correlation, r≈0.05):** Points scattered randomly. No discernible pattern.

> **💡 Business Insight:** A retailer finds correlation = 0.7 between temperature and ice cream sales. They stock more inventory when weather forecasts predict heat waves.

---

### 5.2 Linear Regression

Regression predicts one variable from another by fitting a line.

**The Regression Line:**

$$\hat{y} = \beta_0 + \beta_1 x$$

Where:

- $\hat{y}$ = predicted value of y
- $\beta_0$ = y-intercept (value of y when x=0)
- $\beta_1$ = slope (change in y for each 1-unit change in x)
- $x$ = predictor variable

**How slopes are calculated:**

$$\beta_1 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n} (x_i - \bar{x})^2} = \frac{\text{Covariance}(x,y)}{\text{Variance}(x)}$$

$$\beta_0 = \bar{y} - \beta_1 \bar{x}$$

```python
from scipy import stats
import numpy as np

# Predict sales from ad spend
ad_spend = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
sales = np.array([12, 15, 18, 22, 25, 28, 32, 35, 38, 42])

slope, intercept, r_value, p_value, std_err = stats.linregress(ad_spend, sales)

print(f"Regression Equation: Sales = {slope:.2f} × AdSpend + {intercept:.2f}")
print(f"R-squared: {r_value**2:.3f}")
print(f"p-value: {p_value:.4f}")

# Predict sales for $15k ad spend
predicted_sales = slope * 15 + intercept
print(f"Predicted sales for $15k spend: ${predicted_sales:.2f}k")
```

**What the graph shows (Figure 3, Bottom-Right):** Blue dots are observed data. The red line is the best-fit regression line. The green dashed line shows the true underlying relationship. The vertical black dashed lines show **residuals** (differences between observed and predicted values). R² = 0.793 means 79.3% of sales variation is explained by ad spend.

> **💡 Business Insight:** A SaaS company uses regression to determine that each $1k spent on LinkedIn ads generates $2.96k in recurring revenue. They use this to justify increasing the ad budget.

---

## 6. Sampling & Central Limit Theorem

### 6.1 Sampling Methods

We rarely have data on an entire population, so we take **samples**.

| Method            | Description                                           | When to Use                          |
| ----------------- | ----------------------------------------------------- | ------------------------------------ |
| **Simple Random** | Every member has equal chance                         | Homogeneous population               |
| **Stratified**    | Divide into groups (strata), sample from each         | Population has distinct subgroups    |
| **Systematic**    | Select every k-th member                              | Ordered lists                        |
| **Cluster**       | Divide into clusters, randomly select entire clusters | Geographically dispersed populations |

```python
import numpy as np

population = np.arange(1, 10001)  # 10,000 customers

# Simple Random Sample
random_sample = np.random.choice(population, size=500, replace=False)

# Stratified Sample (by region)
regions = {'North': range(1, 2501), 'South': range(2501, 5001),
           'East': range(5001, 7501), 'West': range(7501, 10001)}
stratified_sample = []
for region, members in regions.items():
    stratified_sample.extend(np.random.choice(list(members), size=125, replace=False))
```

**What the graph shows (Figure 4, Top-Right):** The gray histogram is the full population. The red histogram (simple random) misses some low-satisfaction regions. The green histogram (stratified) better matches the population shape because it ensures representation from all regions.

---

### 6.2 Central Limit Theorem (CLT)

> **The CLT states:** No matter what shape the original population distribution has, the sampling distribution of the mean approaches a **normal distribution** as the sample size increases (typically n ≥ 30).

```python
import numpy as np
import matplotlib.pyplot as plt

# Original: Exponential distribution (very skewed!)
population = np.random.exponential(2, 100000)

# Sample means with different sizes
fig, axes = plt.subplots(1, 4, figsize=(16, 4))
sample_sizes = [1, 5, 30, 100]

for i, n in enumerate(sample_sizes):
    sample_means = [np.mean(np.random.choice(population, n)) for _ in range(10000)]
    axes[i].hist(sample_means, bins=50, density=True, color='steelblue', alpha=0.7)
    axes[i].set_title(f'Sample Size n = {n}')
    axes[i].set_xlabel('Sample Mean')

plt.suptitle('Central Limit Theorem: Any Distribution → Normal')
plt.tight_layout()
plt.show()
```

**What the graph shows (Figure 4, Top-Left):** The original exponential data (n=1, red) is highly right-skewed. As n increases to 5 (orange), 30 (green), and 100 (blue), the distribution of sample means becomes increasingly bell-shaped and normal — even though the original data was not normal at all!

> **💡 Business Insight:** This is why we can use normal-based methods (confidence intervals, z-tests) even when the underlying data is skewed — as long as our sample size is large enough (n ≥ 30).

---

## 7. Company Use Cases

### 7.1 E-Commerce: A/B Testing (Amazon, Shopify)

**Scenario:** Testing whether a new "Buy Now" button color increases conversions.

**Statistical Approach:**

- **$H_0$:** New button color has no effect on conversion rate
- **$H_1$:** New button color increases conversion rate
- Run experiment with 5,000 users seeing each version
- Calculate conversion rates and run two-proportion z-test
- If p-value < 0.05 and new version has higher rate, roll it out

**What the graph shows (Figure 4, Bottom-Right):** The control group (gray) centers around 12.5% conversion. The treatment group (green) centers around 15.5%. The 95% confidence interval for the difference is [1.76, 4.52], entirely above zero — the improvement is statistically significant.

---

### 7.2 Telecom: Customer Churn Prediction (Verizon, AT&T)

**Scenario:** Predicting which customers will cancel their subscription.

**Statistical Approach:**

- Track monthly churn rate (customers lost / total customers)
- Use survival analysis and logistic regression
- Identify high-risk segments (e.g., customers with declining usage)
- Proactively offer retention discounts

**What the graph shows (Figure 4, Bottom-Left):** Active customers (blue line) decline from 10,000 to ~3,800 over 12 months. Churn rate (red dashed line) rises from 8% to 13%. The alert at month 10 flags when churn exceeds 10%, triggering intervention.

---

### 7.3 Finance: Risk Assessment (JPMorgan, Goldman Sachs)

**Scenario:** Measuring portfolio risk using Value at Risk (VaR).

**Statistical Approach:**

- Model returns as normally distributed (via CLT)
- Calculate mean return and standard deviation
- VaR at 95% confidence = $\mu - 1.645 \times \sigma$
- "We are 95% confident losses won't exceed $X in the next day"

```python
returns = np.random.normal(0.001, 0.02, 252)  # Daily returns
mean_return = np.mean(returns)
std_return = np.std(returns)

# 95% VaR (one-tailed)
var_95 = mean_return - 1.645 * std_return
print(f"95% VaR: {var_95:.4f} ({var_95*100:.2f}%)")
# Interpretation: 5% chance of losing more than this amount
```

---

### 7.4 Healthcare: Clinical Trials (Pfizer, Moderna)

**Scenario:** Testing whether a new drug is effective.

**Statistical Approach:**

- **$H_0$:** Drug has no effect (placebo-equivalent)
- **$H_1$:** Drug reduces symptoms significantly
- Randomized controlled trial with treatment and control groups
- Calculate effect size and p-value
- FDA requires p < 0.05 for approval

---

### 7.5 Marketing: Customer Segmentation (Netflix, Spotify)

**Scenario:** Grouping customers by behavior for targeted campaigns.

**Statistical Approach:**

- Use descriptive statistics to profile each segment
- Calculate RFM scores (Recency, Frequency, Monetary)
- Apply clustering algorithms (k-means) which rely on variance and distance metrics
- Target high-value segments with personalized content

---

## 8. Complete Python Code Reference

```python
"""
=================================================================
STATISTICS FOR DATA SCIENCE - COMPLETE PYTHON REFERENCE
=================================================================
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

# ---------------------------------------------------------------
# 1. DESCRIPTIVE STATISTICS
# ---------------------------------------------------------------

data = [23, 45, 56, 78, 32, 45, 67, 89, 45, 23, 56, 78]

# Central Tendency
mean = np.mean(data)
median = np.median(data)
mode_result = stats.mode(data, keepdims=True)
mode = mode_result.mode[0]

# Dispersion
variance = np.var(data, ddof=1)      # Sample variance
std_dev = np.std(data, ddof=1)       # Sample standard deviation
data_range = np.max(data) - np.min(data)
iqr = stats.iqr(data)

# Percentiles
q1 = np.percentile(data, 25)
q2 = np.percentile(data, 50)  # Median
q3 = np.percentile(data, 75)
p10 = np.percentile(data, 10)
p90 = np.percentile(data, 90)

print(f"Mean: {mean}, Median: {median}, Mode: {mode}")
print(f"Std Dev: {std_dev}, IQR: {iqr}")
print(f"10th percentile: {p10}, 90th percentile: {p90}")

# ---------------------------------------------------------------
# 2. PROBABILITY DISTRIBUTIONS
# ---------------------------------------------------------------

# Normal Distribution
normal_data = np.random.normal(loc=100, scale=15, size=1000)
prob_less_than_110 = stats.norm.cdf(110, loc=100, scale=15)
# P(X < 110) when mean=100, sd=15

# Binomial Distribution
# Probability of exactly 3 heads in 10 flips (p=0.5)
binom_prob = stats.binom.pmf(3, n=10, p=0.5)

# Poisson Distribution
# Probability of exactly 5 events when average is 4
poisson_prob = stats.poisson.pmf(5, mu=4)

# ---------------------------------------------------------------
# 3. HYPOTHESIS TESTING
# ---------------------------------------------------------------

# One-sample t-test
# H0: Population mean = 50
sample = np.random.normal(52, 5, 30)
t_stat, p_value = stats.ttest_1samp(sample, 50)

# Two-sample t-test (independent)
group_a = np.random.normal(100, 10, 50)
group_b = np.random.normal(105, 10, 50)
t_stat, p_value = stats.ttest_ind(group_a, group_b)

# Paired t-test (before/after)
before = np.random.normal(70, 8, 30)
after = before + np.random.normal(5, 3, 30)  # Improvement
t_stat, p_value = stats.ttest_rel(before, after)

# ---------------------------------------------------------------
# 4. CONFIDENCE INTERVALS
# ---------------------------------------------------------------

sample = np.random.normal(85, 12, 100)
confidence = 0.95
se = stats.sem(sample)  # Standard error
ci = stats.t.interval(confidence, len(sample)-1,
                      loc=np.mean(sample), scale=se)
print(f"95% CI: {ci}")

# ---------------------------------------------------------------
# 5. CORRELATION & REGRESSION
# ---------------------------------------------------------------

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = np.array([2, 4, 5, 4, 5, 7, 8, 9, 11, 12])

# Correlation
r, p = stats.pearsonr(x, y)
rho, p_spearman = stats.spearmanr(x, y)  # Rank correlation

# Linear Regression
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
predictions = slope * x + intercept

# R-squared
r_squared = r_value ** 2

print(f"Equation: y = {slope:.2f}x + {intercept:.2f}")
print(f"R-squared: {r_squared:.3f}")

# ---------------------------------------------------------------
# 6. NORMALITY TESTS
# ---------------------------------------------------------------

data = np.random.normal(0, 1, 100)

# Shapiro-Wilk test (best for small samples, n < 50)
shapiro_stat, shapiro_p = stats.shapiro(data)

# Kolmogorov-Smirnov test
ks_stat, ks_p = stats.kstest(data, 'norm')

# Anderson-Darling test
anderson_result = stats.anderson(data, dist='norm')

# ---------------------------------------------------------------
# 7. EFFECT SIZE (Cohen's d)
# ---------------------------------------------------------------

def cohens_d(group1, group2):
    """Measures practical significance, not just statistical."""
    pooled_std = np.sqrt(((len(group1)-1)*np.var(group1, ddof=1) +
                          (len(group2)-1)*np.var(group2, ddof=1)) /
                         (len(group1) + len(group2) - 2))
    return (np.mean(group1) - np.mean(group2)) / pooled_std

# Interpretation: 0.2=small, 0.5=medium, 0.8=large effect
```

---

## 📥 Downloadable Charts

All visualizations from this guide are available for download:

1. **[Descriptive Statistics](sandbox:///mnt/agents/output/fig1_descriptive_stats.png)** — Central tendency, dispersion, box plots, percentiles
2. **[Probability Distributions](sandbox:///mnt/agents/output/fig2_probability_distributions.png)** — Normal, Binomial, Poisson, Skewness
3. **[Hypothesis Testing & Correlation](sandbox:///mnt/agents/output/fig3_hypothesis_correlation.png)** — t-tests, confidence intervals, correlation, regression
4. **[CLT & Business Applications](sandbox:///mnt/agents/output/fig4_clt_business.png)** — Central Limit Theorem, sampling, churn analysis, A/B testing

---

## 🎯 Key Takeaways

| Concept                   | One-Sentence Summary                                   |
| ------------------------- | ------------------------------------------------------ |
| **Mean**                  | The average; sensitive to outliers                     |
| **Median**                | The middle value; robust to outliers                   |
| **Standard Deviation**    | Average distance from the mean; measures spread        |
| **Normal Distribution**   | Bell curve; 68-95-99.7 rule applies                    |
| **Hypothesis Testing**    | Formal process to decide if results are real or luck   |
| **p-value**               | Probability of seeing these results if nothing changed |
| **Confidence Interval**   | Range where the true value likely lives                |
| **Correlation**           | Measures linear relationship strength (-1 to +1)       |
| **Regression**            | Predicts one variable from another using a line        |
| **Central Limit Theorem** | Sample means become normal regardless of original data |

---

> **Remember:** Statistics doesn't prove anything with 100% certainty. It quantifies uncertainty and helps you make **better decisions** with the data you have. The goal is not perfect knowledge — it's **better knowledge** than guessing.
