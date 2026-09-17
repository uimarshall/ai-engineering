# Chi-Square Test: Mailer A/B Test

## What This Example Does

This example tests whether the type of marketing mailer is related to whether a grocery customer signs up. It compares two mailer groups using a **chi-square test of independence**.

The business question is:

> Does signup behaviour depend on which mailer a customer received, or could the observed difference have happened by chance?

The Python file expects `grocery_database.xlsx` to be in the same directory as `chi2.py`. The workbook must contain a sheet named `campaign_data` with at least these columns:

- `mailer_type`: the group or mailer version received by the customer.
- `signup_flag`: the outcome, such as `1` for signup and `0` for no signup.

## Beginner Statistical Vocabulary

### Null hypothesis

The null hypothesis is the default assumption. Here it says that mailer type and signup are independent, meaning mailer type does not affect signup behaviour.

### Alternative hypothesis

The alternative hypothesis says that mailer type and signup are related. If supported, the mailer versions have different signup behaviour in the tested population.

### Observed frequencies

Observed frequencies are the counts actually found in the data. For example, the table can show how many people received Mailer 1 and signed up, or received Mailer 1 and did not sign up.

`pandas.crosstab()` creates this count table from the two categorical columns.

### Expected frequencies

Expected frequencies are the counts we would expect if mailer type had no relationship with signup. The chi-square test compares observed counts with these expected counts.

### Chi-square statistic

The chi-square statistic measures the overall distance between observed counts and expected counts. A larger value means the observed results differ more from what independence would predict.

### Degrees of freedom

`dof` means degrees of freedom. For a contingency table, it is calculated as:

```text
(number of rows - 1) * (number of columns - 1)
```

It tells the chi-square distribution which shape to use for the test.

### P-value

The p-value is the probability of seeing results this different, or even more different, if the null hypothesis were true. It is not the probability that the null hypothesis is true.

### Acceptance criteria, or alpha

The code uses `0.05`, commonly called alpha. This means the team accepts a 5% risk of calling a mailer effective when the observed difference was actually caused by random variation.

### What is `chi2.ppf()`?

`ppf` means **percent point function**. It is the inverse of a cumulative distribution function. In this code:

```python
critical_value = chi2.ppf(1 - acceptance_criteria, dof)
```

`chi2.ppf()` finds the chi-square value that leaves 5% of the distribution above it when alpha is `0.05`. This value is called the **critical value**. If the test statistic is greater than or equal to it, the result is statistically significant.

The p-value method and the critical-value method should lead to the same decision.

## How To Interpret This Example

The script prints the two signup rates, the chi-square statistic, the p-value, and the critical value. It then makes decisions using both methods.

The current data produces approximately:

- Mailer 1 signup rate: `0.328`, or `32.8%`.
- Mailer 2 signup rate: `0.378`, or `37.8%`.
- Chi-square statistic: `1.941`.
- P-value: `0.164`.
- Critical value: `3.841`.

Because the p-value is greater than `0.05` and the chi-square statistic is less than the critical value, the test does not reject the null hypothesis. The observed difference is not statistically significant at the 5% level.

This does **not** prove that the two mailers are exactly equally effective. It means that this dataset does not provide strong enough evidence to conclude that their signup rates differ.

## How This Can Drive Business Decisions

### Choosing a campaign version

Marketing can use this test before selecting a winning mailer. A statistically significant result supports choosing the version with the higher signup rate, provided the experiment was fair and the business value of each signup is understood.

### Avoiding premature conclusions

If one mailer has a higher rate but the p-value is above alpha, the team should avoid declaring a winner too quickly. It may collect more observations, repeat the experiment, or review whether the sample sizes were large enough.

### Estimating campaign value

Signup rate is only one business metric. A mailer with a higher signup rate may still be worse if it costs more, attracts low-value customers, produces more cancellations, or generates less revenue. Combine the test with:

- cost per mailer and cost per signup;
- customer lifetime value;
- purchase conversion after signup;
- average order value;
- unsubscribe or complaint rate;
- incremental revenue and profit.

### Customer segmentation

The same method can be applied separately to customer segments such as new customers, loyalty members, regions, or age groups. This can reveal that a mailer works for one segment but not another. Segment tests should be planned carefully because many separate tests increase the chance of false positives.

### Other experiments

The approach is not limited to printed mailers. It can compare email subject lines, website banners, checkout options, app messages, coupon designs, or onboarding flows whenever both the treatment and outcome are categorical.

## Recommended Business Decision Process

1. Define the decision before looking at the results, such as which mailer to send next month.
2. Choose the primary outcome, such as signup within 14 days.
3. Randomly assign comparable customers to each mailer group.
4. Keep the campaign period, audience rules, and measurement window consistent.
5. Check the signup rates and sample sizes.
6. Run the chi-square test and inspect the p-value.
7. Consider practical impact, cost, and profit in addition to statistical significance.
8. Document the decision and monitor the chosen campaign after launch.

## Important Limitations

- Statistical significance does not guarantee business significance.
- A small sample can miss a genuinely useful difference.
- A very large sample can make a tiny, commercially irrelevant difference significant.
- The test shows association; random assignment is needed to support a causal claim.
- Expected cell counts should generally be large enough for the chi-square approximation to be reliable.
- The Python file uses hard-coded signup-rate counts. For production analysis, calculate rates from the loaded data so the printed rates cannot become outdated.
- Do not repeatedly test many metrics or segments without accounting for multiple comparisons.

## Example Decision For This Dataset

Mailer 2 has a higher observed signup rate than Mailer 1, but the evidence is not statistically significant at alpha `0.05`. A reasonable action would be to avoid claiming that Mailer 2 is definitively better, check campaign cost and downstream revenue, and consider collecting more data or running a larger controlled experiment.
