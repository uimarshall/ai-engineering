# 📊 Distributions in Data Science — A Complete Beginner's Guide

---

## Table of Contents

1. [What is a Distribution?](#1-what-is-a-distribution)
2. [The Normal Distribution](#2-the-normal-distribution)
3. [Symmetry: What It Means](#3-symmetry-what-it-means)
4. [Probability Density Function (PDF)](#4-probability-density-function-pdf)
5. [Cumulative Distribution Function (CDF)](#5-cumulative-distribution-function-cdf)
6. [Z-Scores: The Universal Translator](#6-z-scores-the-universal-translator)
7. [Variance](#7-variance)
8. [Standard Deviation](#8-standard-deviation)
9. [The Empirical Rule (68-95-99.7)](#9-the-empirical-rule-68-95-997)
10. [Real-World Examples](#10-real-world-examples)
11. [Company Use Cases](#11-company-use-cases)
12. [Complete Python Code Reference](#12-complete-python-code-reference)

---

## 1. What is a Distribution?

A **distribution** describes how data values are spread across a range. It tells you:

- Which values are common
- Which values are rare
- Where the "center" of the data sits
- How wide or narrow the data spreads

Think of it as a **map of your data's landscape**. Some landscapes have one tall peak (normal), some have two peaks (bimodal), and some are lopsided (skewed).

---

## 2. The Normal Distribution

The **Normal Distribution** (also called the Gaussian distribution or "bell curve") is the most important distribution in statistics. It appears everywhere in nature and business.

### Why is it called "Normal"?

Because so many natural phenomena follow this pattern:

- Heights of people in a population
- Measurement errors in experiments
- IQ scores (by design)
- Blood pressure readings
- Test scores in large classes

### The Formula

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$$

**Breaking it down piece by piece:**

| Symbol                                                | Meaning                                                      |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| $f(x)$                                                | The height of the curve at point $x$ (NOT a probability!)    |
| $\mu$ (mu)                                            | The **mean** — the center of the bell                        |
| $\sigma$ (sigma)                                      | The **standard deviation** — controls the width              |
| $\pi$                                                 | Pi (~3.14159)                                                |
| $e$                                                   | Euler's number (~2.71828)                                    |
| $\frac{1}{\sigma\sqrt{2\pi}}$                         | A normalization constant that ensures total area = 1         |
| $e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$ | The "bell shape" — peaks at $x=\mu$, decays as you move away |

**In plain English:** This formula draws a symmetric hill. The top of the hill is at the mean ($\mu$). The hill gets wider or narrower based on the standard deviation ($\sigma$). The total area under the hill always equals 1 (representing 100% probability).

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Create a normal distribution
x = np.linspace(-4, 4, 1000)  # 1000 points from -4 to 4
mu, sigma = 0, 1  # Standard normal: mean=0, sd=1

# Calculate the Probability Density Function
pdf = stats.norm.pdf(x, mu, sigma)

plt.plot(x, pdf, color='#2C3E50', linewidth=2.5)
plt.fill_between(x, pdf, alpha=0.3, color='#3498DB')
plt.title('Standard Normal Distribution N(0,1)')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.axvline(0, color='red', linestyle='--', label='Mean = 0')
plt.legend()
plt.show()
```

**What the code does:** It creates 1000 evenly spaced points between -4 and 4. For each point, `stats.norm.pdf()` calculates the height of the standard normal curve. The result is the classic bell shape.

---

## 3. Symmetry: What It Means

**Symmetry** means the left side of the distribution is a **mirror image** of the right side.

### Key Properties of a Symmetric Normal Distribution:

1. **Mean = Median = Mode**
   - The mean (average) sits exactly at the center
   - The median (middle value) is also at the center
   - The mode (most frequent value) is also at the center
   - All three measures of central tendency coincide at the peak

2. **50% of data lies on each side**
   - Exactly half the area under the curve is to the left of the mean
   - Exactly half is to the right

3. **Equal probabilities at equal distances**
   - The probability of being 1 SD above the mean equals the probability of being 1 SD below
   - $f(\mu + 1) = f(\mu - 1)$

```python
# Demonstrate symmetry
from scipy import stats

# For standard normal, f(-1) should equal f(1)
print(f"f(-1) = {stats.norm.pdf(-1, 0, 1):.6f}")
print(f"f(1)  = {stats.norm.pdf(1, 0, 1):.6f}")
print(f"Equal? {np.isclose(stats.norm.pdf(-1, 0, 1), stats.norm.pdf(1, 0, 1))}")

# Area left of mean = Area right of mean = 0.5
print(f"P(X < 0) = {stats.norm.cdf(0, 0, 1):.6f}")  # Exactly 0.5
```

**What the graph shows (Figure 1, Top-Left):** The bell curve with orange dots at z = -2, -1, 1, and 2. Notice how $f(-1) = 0.242$ and $f(1) = 0.242$ — identical! The green arrows show the left and right halves are perfect mirrors. The red dashed line marks where Mean = Median = Mode = 0.

> **💡 Business Insight:** Symmetry simplifies analysis. If customer satisfaction is normally distributed around 7/10, you know exactly as many customers rate 6 as rate 8. You can predict complaints and praise with equal confidence.

---

## 4. Probability Density Function (PDF)

The **PDF** tells you the **relative likelihood** of a random variable taking on a particular value.

### Critical Understanding: PDF values are NOT probabilities!

- The PDF can output values **greater than 1**
- The PDF at a single point is **not** the probability of that exact value
- **Probability = Area under the PDF curve** over an interval

$$\text{Probability}(a \leq X \leq b) = \int_{a}^{b} f(x) \, dx$$

**Breaking it down:**

- $f(x)$ = the PDF function (curve height)
- $\int_{a}^{b}$ = "sum up" the area from point $a$ to point $b$
- The result is the probability that $X$ falls between $a$ and $b$

```python
from scipy import stats

# PDF at a single point
pdf_at_zero = stats.norm.pdf(0, loc=0, scale=1)
print(f"PDF at x=0: {pdf_at_zero:.4f}")  # Output: ~0.3989

# This is NOT a probability! It's just the curve height.

# To get probability, we need AREA (use CDF)
prob_between_minus1_and_1 = stats.norm.cdf(1, 0, 1) - stats.norm.cdf(-1, 0, 1)
print(f"P(-1 < X < 1) = {prob_between_minus1_and_1:.4f}")  # Output: ~0.6827 (68.27%)
```

**What the graph shows (Figure 2, Top-Left):** The red curve is the PDF. At z=1, the PDF height is 0.242 — this is NOT 24.2% probability! The blue dashed curve is the CDF. At z=1, the CDF value is 0.841, meaning 84.1% of the area lies to the left. The shaded blue region under the PDF from -∞ to 1 visually represents this 84.1%.

> **Analogy:** Think of the PDF as a **population density map**. A city center has a high density value (many people per square mile), but that doesn't tell you the probability of finding a person at an exact GPS coordinate — it tells you the concentration in that area.

---

## 5. Cumulative Distribution Function (CDF)

The **CDF** gives you the **cumulative probability** — the probability that a random variable is **less than or equal to** a specific value.

$$F(x) = P(X \leq x) = \int_{-\infty}^{x} f(t) \, dt$$

**Breaking it down:**

- $F(x)$ = CDF value at point $x$
- $P(X \leq x)$ = probability that $X$ is less than or equal to $x$
- The integral sums up all PDF area from negative infinity up to $x$

### Properties of CDF:

- Always ranges from **0 to 1**
- $F(-\infty) = 0$ (nothing is below negative infinity)
- $F(+\infty) = 1$ (everything is below positive infinity)
- **Non-decreasing** — it only goes up or stays flat

```python
from scipy import stats

# CDF gives P(X <= x)
print(f"P(X <= 0)    = {stats.norm.cdf(0, 0, 1):.4f}")      # 0.5000 (50%)
print(f"P(X <= 1)    = {stats.norm.cdf(1, 0, 1):.4f}")      # 0.8413 (84.13%)
print(f"P(X <= -1)   = {stats.norm.cdf(-1, 0, 1):.4f}")     # 0.1587 (15.87%)
print(f"P(X <= 1.96) = {stats.norm.cdf(1.96, 0, 1):.4f}")   # 0.9750 (97.5%)

# Probability between two values
prob = stats.norm.cdf(1, 0, 1) - stats.norm.cdf(-1, 0, 1)
print(f"P(-1 < X < 1) = {prob:.4f}")  # 68.27%
```

**What the graph shows (Figure 2, Top-Left):** The blue dashed CDF curve starts near 0 on the far left, rises slowly at first, then steeply through the middle, then flattens near 1 on the right. At z=0, CDF = 0.5 (half the data is below the mean). At z=1, CDF ≈ 0.841 (84.1% of data is below 1 SD).

> **💡 Business Insight:** An e-commerce company uses CDF to answer: "What percentage of customers spend less than $50?" If CDF(50) = 0.70, then 70% of customers are low-spenders, suggesting a need for upselling strategies.

---

## 6. Z-Scores: The Universal Translator

A **z-score** tells you how many standard deviations a value is from the mean.

$$z = \frac{x - \mu}{\sigma}$$

**Breaking it down:**

- $z$ = z-score (standardized value)
- $x$ = the original data point
- $\mu$ = the mean of the distribution
- $\sigma$ = the standard deviation
- $(x - \mu)$ = how far the point is from the mean
- Dividing by $\sigma$ converts that distance into "number of standard deviations"

### Why Z-Scores Are Powerful:

1. **Universal comparison:** A z-score of +1.5 means the same thing whether you're talking about IQ, height, or stock returns
2. **Probability lookup:** Once you have a z-score, you can use standard normal tables
3. **Outlier detection:** Values with $|z| > 3$ are typically considered outliers

```python
import numpy as np

# Example: Compare test scores from different classes
# Class A: Mean = 70, SD = 10
# Class B: Mean = 80, SD = 15

student_a_score = 85  # Class A
student_b_score = 95  # Class B

# Calculate z-scores
z_a = (student_a_score - 70) / 10  # z = +1.5
z_b = (student_b_score - 80) / 15  # z = +1.0

print(f"Student A: Score = {student_a_score}, z = {z_a:.2f}")
print(f"Student B: Score = {student_b_score}, z = {z_b:.2f}")
print(f"Student A performed BETTER relative to their class!")

# Convert z-score back to original scale
original_from_z = 70 + (1.5 * 10)
print(f"z = +1.5 in Class A = Score of {original_from_z}")

# Using scipy for probabilities
from scipy import stats
print(f"P(Z < 1.5) = {stats.norm.cdf(1.5):.4f}")  # Student A is at 93.3rd percentile
print(f"P(Z < 1.0) = {stats.norm.cdf(1.0):.4f}")  # Student B is at 84.1st percentile
```

**What the graph shows (Figure 2, Top-Right):** Two histograms overlaid. The red histogram shows original adult heights (mean ~170cm, spread ~10cm). The blue histogram shows the same data converted to z-scores (mean = 0, spread = 1). Notice how 160cm (1 SD below mean) becomes z = -1.0, and 180cm (1 SD above mean) becomes z = +1.0. The shapes are identical — only the scale changed!

> **💡 Business Insight:** A bank uses z-scores to standardize credit metrics across different loan products. A credit score z-score of -2.5 triggers automatic rejection regardless of the product type.

---

## 7. Variance

**Variance** measures how far data points spread out from the mean. It quantifies the "spread" of the distribution.

### Population Variance:

$$\sigma^2 = \frac{\sum_{i=1}^{n} (x_i - \mu)^2}{N}$$

### Sample Variance (use this in practice!):

$$s^2 = \frac{\sum_{i=1}^{n} (x_i - \bar{x})^2}{n - 1}$$

**Breaking it down:**

| Symbol              | Meaning                                   |
| ------------------- | ----------------------------------------- |
| $\sigma^2$ or $s^2$ | Variance                                  |
| $\sum_{i=1}^{n}$    | "Sum of" all data points                  |
| $x_i$               | Each individual data point                |
| $\mu$ or $\bar{x}$  | The mean                                  |
| $(x_i - \mu)^2$     | Squared deviation from the mean           |
| $N$                 | Population size                           |
| $n - 1$             | Sample size minus 1 (Bessel's correction) |

### Why do we square the deviations?

1. **Eliminates negatives:** $(-5)^2 = 25$ and $(+5)^2 = 25$. Without squaring, positive and negative deviations would cancel out.
2. **Penalizes large deviations:** A deviation of 10 becomes 100, while a deviation of 2 becomes only 4. Large deviations "hurt" more.

### Why divide by n-1 for samples?

This is called **Bessel's correction**. When you calculate variance from a sample, you use the sample mean ($\bar{x}$), which is already fitted to your data. This makes the squared deviations slightly smaller than they would be for the true population. Dividing by $n-1$ instead of $n$ corrects this bias.

```python
import numpy as np

data = [45, 52, 58, 60, 65, 68, 70, 72, 75, 85]
mean_val = np.mean(data)

# Step-by-step variance calculation
deviations = [x - mean_val for x in data]
squared_devs = [d ** 2 for d in deviations]

print("Data Point | Deviation | Squared Deviation")
print("-" * 45)
for x, d, sd in zip(data, deviations, squared_devs):
    print(f"{x:10.1f} | {d:+9.1f} | {sd:17.1f}")

print(f"\\nSum of squared deviations: {sum(squared_devs):.1f}")

# Population variance (÷ N)
pop_var = sum(squared_devs) / len(data)
print(f"Population variance (÷{len(data)}): {pop_var:.2f}")

# Sample variance (÷ n-1) — USE THIS IN PRACTICE!
sample_var = sum(squared_devs) / (len(data) - 1)
print(f"Sample variance (÷{len(data)-1}): {sample_var:.2f}")

# Using NumPy
print(f"\\nNumPy population var: {np.var(data, ddof=0):.2f}")
print(f"NumPy sample var:     {np.var(data, ddof=1):.2f}")
```

**What the graph shows (Figure 3, Top-Left):** Blue dots represent 10 data points. The red dashed line is the mean (65.0). Black dashed lines connect each point to the mean, showing deviations. Green annotations show positive deviations (above mean), red shows negative deviations (below mean). The note explains that if we summed raw deviations, they'd cancel out.

**What the graph shows (Figure 3, Top-Right):** A bar chart of squared deviations. The first bar (400.0) is the largest because the point (45) is farthest from the mean. The purple dashed line shows the variance = 122.6, which is the average of all these squared values. The note explains that squaring both eliminates negatives AND penalizes large deviations.

**What the graph shows (Figure 3, Bottom-Right):** Two histograms of sample variances from 1000 samples. The red (biased, ÷n) is centered around 88 — it systematically underestimates the true population variance of 100. The green (unbiased, ÷n-1) is centered around 97.7 — much closer to the truth. This visually proves why we use n-1.

> **💡 Business Insight:** An investment firm compares variance of two stocks. Stock A has variance = 25, Stock B has variance = 100. Both have the same average return, but Stock B is 4x more volatile. Risk-averse investors choose Stock A.

---

## 8. Standard Deviation

**Standard Deviation (SD)** is simply the **square root of variance**. It brings the units back to the original scale.

$$\sigma = \sqrt{\sigma^2} = \sqrt{\frac{\sum_{i=1}^{n} (x_i - \mu)^2}{N}}$$

**Breaking it down:**

- $\sigma$ = standard deviation
- $\sqrt{\sigma^2}$ = square root of variance
- This "undoes" the squaring we did for variance

### Why use Standard Deviation instead of Variance?

| Measure            | Units                   | Interpretation              |
| ------------------ | ----------------------- | --------------------------- |
| Variance           | Dollars², cm², seconds² | Hard to interpret           |
| Standard Deviation | Dollars, cm, seconds    | Same units as original data |

**Example:** If data is in dollars:

- Variance = 1,000 dollars² (what does that even mean?)
- Standard Deviation = √1,000 = $31.62 (meaningful!)

```python
import numpy as np

data = [45, 52, 58, 60, 65, 68, 70, 72, 75, 85]

variance = np.var(data, ddof=1)  # Sample variance
std_dev = np.std(data, ddof=1)   # Sample standard deviation

print(f"Variance: {variance:.2f} (units squared)")
print(f"Standard Deviation: {std_dev:.2f} (original units)")
print(f"Verification: √{variance:.2f} = {np.sqrt(variance):.2f}")

# Practical interpretation
mean_val = np.mean(data)
print(f"\\nMean = {mean_val:.1f}")
print(f"Most data falls between {mean_val - std_dev:.1f} and {mean_val + std_dev:.1f}")
print(f"(Mean ± 1 SD = 68% of data)")
```

**What the graph shows (Figure 3, Bottom-Left):** Two distributions with the same mean (100) but different standard deviations. The green distribution (σ=5) is tall and narrow — data is tightly clustered. The red distribution (σ=20) is short and wide — data is very spread out. The note explains that SD is preferred because it's in original units.

**What the graph shows (Figure 1, Bottom-Right):** Three distributions all centered at μ=100 but with σ=5 (green), σ=15 (blue), and σ=30 (red). The green curve is very peaked — most values fall between 95 and 105. The red curve is very flat — values could reasonably fall between 40 and 160. Low σ means predictable and reliable; high σ means volatile and risky.

> **💡 Business Insight:** A supply chain manager monitors delivery times. Mean = 3 days, SD = 0.5 days means reliable delivery (customers trust the estimate). Mean = 3 days, SD = 2 days means unpredictable delivery (customers get frustrated). The manager investigates why SD is high.

---

## 9. The Empirical Rule (68-95-99.7)

For any normal distribution, the empirical rule tells you exactly what percentage of data falls within standard deviation bands.

| Range             | Percentage of Data |
| ----------------- | ------------------ |
| $\mu \pm 1\sigma$ | 68%                |
| $\mu \pm 2\sigma$ | 95%                |
| $\mu \pm 3\sigma$ | 99.7%              |

```python
from scipy import stats

# Verify the empirical rule for standard normal
within_1sd = stats.norm.cdf(1, 0, 1) - stats.norm.cdf(-1, 0, 1)
within_2sd = stats.norm.cdf(2, 0, 1) - stats.norm.cdf(-2, 0, 1)
within_3sd = stats.norm.cdf(3, 0, 1) - stats.norm.cdf(-3, 0, 1)

print(f"Within ±1 SD: {within_1sd*100:.2f}%")  # ~68.27%
print(f"Within ±2 SD: {within_2sd*100:.2f}%")  # ~95.45%
print(f"Within ±3 SD: {within_3sd*100:.2f}%")  # ~99.73%

# Apply to real data: IQ scores (μ=100, σ=15)
iq_mean, iq_sd = 100, 15
print(f"\\nIQ Score Ranges:")
print(f"68% of people score between {iq_mean - iq_sd} and {iq_mean + iq_sd}")
print(f"95% of people score between {iq_mean - 2*iq_sd} and {iq_mean + 2*iq_sd}")
print(f"99.7% of people score between {iq_mean - 3*iq_sd} and {iq_mean + 3*iq_sd}")
```

**What the graph shows (Figure 1, Top-Right):** The standard normal curve with three shaded regions. The inner green region (between -1 and +1) contains 68% of the area. The middle orange region (between -2 and +2) contains 95%. The outer red region (between -3 and +3) contains 99.7%. The note emphasizes: if you know just the mean and SD, you instantly know where most data points fall!

> **💡 Business Insight:** A shoe manufacturer knows adult male foot lengths are normally distributed with mean = 27cm, SD = 1.5cm. They know 68% of men need sizes between 25.5–28.5cm, so they stock those sizes most heavily. Sizes below 22.5cm or above 31.5cm are rare and stocked minimally.

---

## 10. Real-World Examples

### Example 1: Adult Heights

Heights in a homogeneous population follow a normal distribution remarkably well.

```python
import numpy as np
from scipy import stats

# Men's heights: μ = 175cm, σ = 7cm
# Women's heights: μ = 162cm, σ = 6cm

# What percentage of men are taller than 190cm?
z_190 = (190 - 175) / 7
pct_taller = 1 - stats.norm.cdf(z_190)
print(f"Men taller than 190cm: {pct_taller*100:.2f}%")  # ~1.6%

# What height are 95% of women shorter than?
height_95th = stats.norm.ppf(0.95, 162, 6)
print(f"95% of women are shorter than: {height_95th:.1f}cm")  # ~171.9cm
```

**What the graph shows (Figure 2, Bottom-Left):** Two bell curves — blue for men (centered at 175cm) and pink for women (centered at 162cm). The gray overlap region shows where height alone can't distinguish gender. The note explains that heights are a classic normal distribution example.

### Example 2: IQ Scores

IQ tests are **deliberately designed** to produce a normal distribution.

```python
# IQ: μ = 100, σ = 15 (by design!)

# What IQ corresponds to the 98th percentile?
iq_98th = stats.norm.ppf(0.98, 100, 15)
print(f"98th percentile IQ: {iq_98th:.1f}")  # ~130.8

# What percentile is an IQ of 85?
percentile_85 = stats.norm.cdf(85, 100, 15)
print(f"IQ of 85 is at the {percentile_85*100:.1f}th percentile")  # ~16th
```

**What the graph shows (Figure 2, Bottom-Right):** The IQ distribution with colored bands representing categories. Green (85-115) contains 68% of the population — "Average." Orange (70-85) is "Low Average." Blue (115-130) is "High Average." Purple (>130) is "Superior." Vertical dotted lines mark the 16th, 50th, 84th, and 98th percentiles.

---

## 11. Company Use Cases

### Use Case 1: Manufacturing Quality Control (Toyota, Samsung)

**Scenario:** A factory produces widgets with a target diameter of 10.0mm. Specifications allow ±0.5mm (9.5mm to 10.5mm).

**Statistical Approach:**

- Measure widget diameters and model as $N(\mu, \sigma^2)$
- Calculate what percentage falls outside specification limits
- Use z-scores: $z_{LSL} = \frac{9.5 - \mu}{\sigma}$, $z_{USL} = \frac{10.5 - \mu}{\sigma}$
- Defect rate = $P(X < LSL) + P(X > USL)$

```python
from scipy import stats

# Process measurements
measurements = np.random.normal(10.05, 0.15, 1000)  # Slightly off-center!
mu, sigma = np.mean(measurements), np.std(measurements, ddof=1)

LSL, USL = 9.5, 10.5
z_lsl = (LSL - mu) / sigma
z_usl = (USL - mu) / sigma

defect_rate = (stats.norm.cdf(z_lsl) + (1 - stats.norm.cdf(z_usl))) * 100
print(f"Defect Rate: {defect_rate:.3f}%")

# Six Sigma goal: < 0.00034% defects
if defect_rate < 0.00034:
    print("Six Sigma quality achieved! ✅")
else:
    print(f"Process needs improvement. Target: recalibrate to μ=10.0")
```

**What the graph shows (Figure 4, Top-Left):** The widget diameter distribution with red dashed lines at the specification limits (9.5mm and 10.5mm). The red shaded tails represent defective widgets. The process mean (orange dashed at 10.05mm) is slightly off the target (green at 10.0mm). The defect rate is calculated as 0.13% (~1 per 1000 units).

> **Business Impact:** Reducing defect rate from 1% to 0.1% saves millions in rework and warranty costs. Six Sigma methodology ( Motorola/GE) uses normal distribution to achieve 3.4 defects per million opportunities.

---

### Use Case 2: E-Commerce Order Values (Amazon, Shopify)

**Scenario:** Understanding customer spending patterns to optimize pricing and recommendations.

**Statistical Reality:** Order values are typically **right-skewed** (log-normal), not normal. Most orders are small, but a few whales spend thousands.

```python
import numpy as np

# Simulate e-commerce orders (right-skewed)
small_orders = np.random.normal(50, 15, 800)    # $50 average
medium_orders = np.random.normal(150, 30, 150)  # $150 average
large_orders = np.random.normal(400, 80, 50)    # $400 average (wholesale)

all_orders = np.concatenate([small_orders, medium_orders, large_orders])

print(f"Mean Order Value: ${np.mean(all_orders):.2f}")
print(f"Median Order Value: ${np.median(all_orders):.2f}")
print(f"Standard Deviation: ${np.std(all_orders, ddof=1):.2f}")

# For inventory/revenue planning, use mean
# For "typical customer" understanding, use median
```

**What the graph shows (Figure 4, Top-Right):** A right-skewed histogram of order values. The mean (red dashed, $84.17) is pulled right by large orders. The median (green dashed, $56.52) better represents the typical customer. The orange curve is a log-normal fit — a better model than normal for this data.

> **Business Impact:** Using mean for pricing decisions would overestimate typical willingness-to-pay. Using median for revenue forecasting would underestimate total revenue. Smart analysts report both: "Median customer spends $57, but mean is $84 due to high-value customers."

---

### Use Case 3: HR Performance Ratings (Microsoft, GE — historically)

**Scenario:** Companies sometimes force performance ratings into a normal distribution.

**Statistical Approach:**

- Assume performance follows $N(\mu, \sigma^2)$ on a 1-5 scale
- Top 15% → "Exceeds Expectations"
- Middle 70% → "Meets Expectations"
- Bottom 15% → "Below Expectations"

```python
from scipy import stats

# Find cutoff percentiles
top_cutoff = stats.norm.ppf(0.85, 3.5, 0.8)   # Top 15%
bottom_cutoff = stats.norm.ppf(0.15, 3.5, 0.8) # Bottom 15%

print(f"Ratings above {top_cutoff:.2f}: Exceeds")
print(f"Ratings below {bottom_cutoff:.2f}: Below")
print(f"Ratings between: Meets")
```

**What the graph shows (Figure 4, Bottom-Left):** A histogram of performance ratings with a normal curve overlaid. Red shaded left region = "Below Expectations" (bottom 15%). Orange middle = "Meets" (middle 70%). Green right = "Exceeds" (top 15%). The mean is 3.47.

> **Business Impact:** Forced distributions prevent "grade inflation" but can damage morale. Modern companies (Adobe, Deloitte) have moved away from this, but understanding the statistical basis helps HR professionals design fair evaluation systems.

---

### Use Case 4: A/B Testing (Google, Netflix, Meta)

**Scenario:** Testing whether a new website design increases conversion rates.

**Statistical Approach:**

- Daily conversion rates approximate a normal distribution (via Central Limit Theorem)
- Model control group as $N(\mu_c, \sigma_c^2/n)$ and treatment as $N(\mu_t, \sigma_t^2/n)$
- Run two-sample t-test to compare means
- If p-value < 0.05, the difference is statistically significant

```python
from scipy import stats
import numpy as np

# 30 days of data
np.random.seed(42)
control = np.random.normal(0.12, 0.02, 30)   # 12% conversion
treatment = np.random.normal(0.15, 0.02, 30) # 15% conversion

# Two-sample t-test
t_stat, p_value = stats.ttest_ind(treatment, control)

print(f"Control: {np.mean(control)*100:.2f}% ± {np.std(control, ddof=1)*100:.2f}%")
print(f"Treatment: {np.mean(treatment)*100:.2f}% ± {np.std(treatment, ddof=1)*100:.2f}%")
print(f"Lift: +{(np.mean(treatment)-np.mean(control))*100:.2f} percentage points")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value: {p_value:.4f}")
print(f"Result: {'SIGNIFICANT! Launch it! 🚀' if p_value < 0.05 else 'Not significant. Keep testing.'}")
```

**What the graph shows (Figure 4, Bottom-Right):** Daily conversion rates over 30 days. Gray circles = control group (old page), green squares = treatment (new page). The green distribution on the right side is shifted higher than the gray. The result box shows: Control 12.0%, Treatment 14.7%, lift of +2.6 percentage points, p-value = 0.0000 — highly significant.

> **Business Impact:** A 2.6 percentage point lift in conversion with 1 million daily visitors = 26,000 additional conversions per day. At $50 average order value, that's $1.3M additional daily revenue. Statistics validates whether this improvement is real or just noise.

---

## 12. Complete Python Code Reference

```python
"""
=================================================================
DISTRIBUTIONS IN DATA SCIENCE - COMPLETE PYTHON REFERENCE
=================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ---------------------------------------------------------------
# 1. NORMAL DISTRIBUTION BASICS
# ---------------------------------------------------------------

# Generate normal random data
data = np.random.normal(loc=100, scale=15, size=1000)
# loc = mean (μ), scale = standard deviation (σ), size = number of samples

# Probability Density Function (PDF)
x = np.linspace(50, 150, 1000)
pdf = stats.norm.pdf(x, loc=100, scale=15)
# pdf gives the HEIGHT of the curve at each point (NOT probability)

# Cumulative Distribution Function (CDF)
cdf = stats.norm.cdf(x, loc=100, scale=15)
# cdf gives P(X <= x) — the cumulative probability

# Percent Point Function (PPF) — inverse of CDF
value_at_95th_percentile = stats.norm.ppf(0.95, loc=100, scale=15)
# Returns the value below which 95% of data falls

# ---------------------------------------------------------------
# 2. Z-SCORES
# ---------------------------------------------------------------

def z_score(x, mean, std):
    """Convert any value to standard normal z-score."""
    return (x - mean) / std

def from_z_score(z, mean, std):
    """Convert z-score back to original scale."""
    return mean + (z * std)

# Example
original = 130  # IQ score
z = z_score(original, mean=100, std=15)  # z = 2.0
back_to_original = from_z_score(z, mean=100, std=15)  # 130

# ---------------------------------------------------------------
# 3. VARIANCE & STANDARD DEVIATION
# ---------------------------------------------------------------

data = [23, 45, 56, 78, 32, 45, 67, 89]

# Population variance (when you have ALL data)
pop_var = np.var(data, ddof=0)   # ddof=0 means divide by N

# Sample variance (when data is a SAMPLE from larger population)
sample_var = np.var(data, ddof=1)  # ddof=1 means divide by n-1

# Standard deviation
pop_std = np.std(data, ddof=0)
sample_std = np.std(data, ddof=1)

# Manual calculation
mean = np.mean(data)
squared_devs = [(x - mean) ** 2 for x in data]
manual_var = sum(squared_devs) / (len(data) - 1)  # Sample variance

# ---------------------------------------------------------------
# 4. EMPIRICAL RULE VERIFICATION
# ---------------------------------------------------------------

def empirical_rule(mean, std):
    """Print the 68-95-99.7 rule for any normal distribution."""
    print(f"μ = {mean}, σ = {std}")
    print(f"68% of data: {mean - std:.2f} to {mean + std:.2f}")
    print(f"95% of data: {mean - 2*std:.2f} to {mean + 2*std:.2f}")
    print(f"99.7% of data: {mean - 3*std:.2f} to {mean + 3*std:.2f}")

empirical_rule(100, 15)  # IQ scores example

# ---------------------------------------------------------------
# 5. PROBABILITY CALCULATIONS
# ---------------------------------------------------------------

# P(a < X < b) for normal distribution
def normal_probability(a, b, mean, std):
    """Calculate probability between a and b."""
    return stats.norm.cdf(b, mean, std) - stats.norm.cdf(a, mean, std)

# Example: P(85 < IQ < 115)
prob = normal_probability(85, 115, 100, 15)
print(f"P(85 < IQ < 115) = {prob:.4f}")  # Should be ~0.6827

# P(X > x) — right tail
prob_greater = 1 - stats.norm.cdf(130, 100, 15)
print(f"P(IQ > 130) = {prob_greater:.4f}")  # ~0.0228 (2.28%)

# ---------------------------------------------------------------
# 6. CHECKING IF DATA IS NORMAL
# ---------------------------------------------------------------

from scipy.stats import shapiro, normaltest

# Shapiro-Wilk test (best for small samples, n < 50)
data = np.random.normal(0, 1, 100)
stat, p = shapiro(data)
print(f"Shapiro p-value: {p:.4f}")
if p > 0.05:
    print("Data appears normally distributed")
else:
    print("Data is NOT normally distributed")

# ---------------------------------------------------------------
# 7. VISUALIZATION HELPERS
# ---------------------------------------------------------------

def plot_normal_with_rules(mean, std, title="Normal Distribution"):
    """Plot a normal distribution with 68-95-99.7 rule shaded."""
    x = np.linspace(mean - 4*std, mean + 4*std, 1000)
    y = stats.norm.pdf(x, mean, std)

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, 'k-', linewidth=2, label=f'N({mean}, {std}²)')

    # Shade regions
    colors = ['#2ECC71', '#F39C12', '#E74C3C']
    alphas = [0.4, 0.3, 0.2]
    for i, (z, color, alpha) in enumerate(zip([1, 2, 3], colors, alphas)):
        mask = (x >= mean - z*std) & (x <= mean + z*std)
        plt.fill_between(x[mask], y[mask], alpha=alpha, color=color,
                        label=f'±{z}σ: {stats.norm.cdf(z)-stats.norm.cdf(-z):.1%}')

    plt.axvline(mean, color='blue', linestyle='--', label=f'Mean = {mean}')
    plt.title(title)
    plt.xlabel('Value')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.show()

# Example usage
plot_normal_with_rules(100, 15, "IQ Score Distribution")
```

---

## 📥 Downloadable Charts

All visualizations from this guide are available for download:

1. **[Normal Distribution Basics](sandbox:///mnt/agents/output/dist_fig1_normal_basics.png)** — Symmetry, empirical rule, changing mean, changing SD
2. **[PDF, CDF & Real-World Examples](sandbox:///mnt/agents/output/dist_fig2_pdf_cdf_realworld.png)** — PDF vs CDF, z-scores, heights, IQ scores
3. **[Variance & Standard Deviation](sandbox:///mnt/agents/output/dist_fig3_variance_sd.png)** — Deviations, squared deviations, Bessel's correction
4. **[Business Use Cases](sandbox:///mnt/agents/output/dist_fig4_business_cases.png)** — Manufacturing, e-commerce, HR, A/B testing

---

## 🎯 Key Takeaways

| Concept                 | One-Sentence Summary                                                                |
| ----------------------- | ----------------------------------------------------------------------------------- |
| **Normal Distribution** | The bell curve — symmetric, mean=median=mode, appears everywhere in nature          |
| **Symmetry**            | Left side mirrors right side; 50% of data on each side of the mean                  |
| **PDF**                 | Curve height at a point — NOT a probability, but proportional to likelihood         |
| **CDF**                 | Cumulative probability P(X ≤ x) — area under PDF from -∞ to x                       |
| **Z-Score**             | Universal translator: $(x - \mu) / \sigma$ — converts any normal to standard normal |
| **Variance**            | Average of squared deviations — measures spread in squared units                    |
| **Standard Deviation**  | Square root of variance — measures spread in original units                         |
| **Empirical Rule**      | 68-95-99.7% of data falls within 1-2-3 standard deviations                          |
| **Bessel's Correction** | Divide by n-1 (not n) when calculating variance from a sample                       |

---

> **Remember:** The normal distribution is powerful because it appears naturally, is fully described by just two numbers (mean and standard deviation), and allows us to calculate precise probabilities. Master the normal distribution, and you've mastered the foundation of statistical thinking in data science.
