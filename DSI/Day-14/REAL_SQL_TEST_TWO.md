# SQL TEST 2

---

## Query 01 — Count Unique Transactions

**Question:** How many unique transactions are there in the transactions table?

### Business Scenario

The operations and finance teams need a reliable count of all distinct purchase events
recorded in the system. Duplicate transaction IDs can appear due to data pipeline retries
or ETL errors. Knowing the true unique transaction volume is the starting point for
calculating revenue, average basket size, and year-over-year growth — all critical inputs
for competitive benchmarking and board-level reporting.

```sql
select count(distinct(transaction_id)) as trans_count   -- counts only unique transaction IDs, aliased as trans_count;
                                                         -- using DISTINCT prevents double-counting duplicate rows
from grocery_db.transactions;                            -- source table that holds every sales transaction
```

**What each line does:**
| Clause | Purpose |
|---|---|
| `count(distinct(transaction_id))` | Counts every transaction ID exactly once, regardless of how many times a row appears |
| `as trans_count` | Gives the result column a human-readable name for dashboards and reports |
| `from grocery_db.transactions` | Reads from the transactions table in the grocery_db schema |

---

## Query 02 — Customer Breakdown by Mailer Type for Delivery Club Campaign

**Question:** How many customers were in each mailer_type category for the delivery club campaign?

### Business Scenario

The marketing team ran the "Delivery Club" campaign using multiple contact channels
(e.g., letter, email, SMS). Before reporting ROI or designing the next campaign,
leadership needs to know how the audience was split across each channel. If one mailer
type dramatically outperforms another in conversion rate, the company can reallocate
budget to the winning channel — a direct lever on campaign profitability.

```sql
select
    mailer_type,                                -- the communication channel used (e.g., 'Mailer 1', 'Mailer 2', 'Control')
    count(distinct(customer_id)) as customers   -- counts unique customers per channel; avoids inflating numbers if a
                                                -- customer appears in the table multiple times
from
    grocery_db.campaign_data                    -- table storing campaign assignment records for each customer
where
    campaign_name = 'delivery club'             -- filters to only the rows belonging to the Delivery Club campaign;
                                                -- without this, the counts would include all campaigns
group by
    mailer_type;                                -- creates one result row per unique mailer_type value so we can
                                                -- compare channels side by side
```

**What each line does:**
| Clause | Purpose |
|---|---|
| `select mailer_type` | Returns the channel name for each group |
| `count(distinct(customer_id))` | Counts each customer once per channel group |
| `from grocery_db.campaign_data` | Source table containing campaign assignments |
| `where campaign_name = 'delivery club'` | Narrows the dataset to the single campaign under review |
| `group by mailer_type` | Aggregates rows by channel so `COUNT` applies within each channel |

---

## Query 03 — Customer Gender Distribution

**Question:** How many customers of each gender are in the customer base?

### Business Scenario

Understanding the gender split of the customer base is a foundational demographic insight.
Retailers use this data to tailor product ranges, promotional messaging, and personalised
recommendations. If 70 % of high-value customers are female, the buying team can skew
seasonal ranges accordingly, strengthening relevance and reducing mark-down risk —
both of which directly protect gross margin.

```sql
select
    gender,                                     -- the demographic attribute being analysed
    count(distinct(customer_id)) as customer_count  -- counts each customer exactly once per gender group;
                                                    -- DISTINCT guards against duplicate customer rows in the table
from
    grocery_db.customer_details                 -- master customer table holding demographic attributes
group by
    gender;                                     -- produces one row per gender value (e.g., 'M', 'F', 'Unspecified')
                                                -- so the counts are broken out by segment
```

**What each line does:**
| Clause | Purpose |
|---|---|
| `select gender` | Returns the gender label for each group |
| `count(distinct(customer_id))` | Counts unique customers in that gender group |
| `from grocery_db.customer_details` | Source table containing customer demographics |
| `group by gender` | Splits the aggregation by gender so each group gets its own count |

---

## Query 04 — Total Sales by Product Area for July 2020

**Question:** What were the total sales for each product area during July 2020?

### Business Scenario

At the end of every month, the category management team reviews sales performance by
department (e.g., Produce, Bakery, Dairy, Frozen). This query powers that monthly
performance report. Departments running below target can trigger immediate actions:
promotional pricing, end-cap placement changes, or supplier renegotiations. Departments
exceeding targets validate current strategies and may unlock further investment —
both decisions directly tied to staying ahead of competitors.

```sql
select
    b.product_area_name,                        -- the human-readable department name pulled from the lookup table
    sum(a.sales_cost) as total_sales            -- adds up every individual line-item sale within the department
                                                -- for the period; aliased to total_sales for clarity
from
    grocery_db.transactions a                   -- 'a' is an alias for the transactions table; holds every
                                                -- individual purchase line with its cost and date
inner join
    grocery_db.product_areas b                  -- 'b' is an alias for the product areas lookup table;
    on a.product_area_id = b.product_area_id    -- the JOIN condition links each transaction to its department
                                                -- using the shared product_area_id key; INNER JOIN means
                                                -- only transactions with a matching product area are included
where
    a.transaction_date between '2020-07-01'     -- restricts the dataset to transactions that occurred in July 2020;
    and '2020-07-31'                            -- BETWEEN is inclusive of both endpoints

group by
    b.product_area_name                         -- collapses all transactions in the same department into one row
                                                -- so SUM operates per department

order by
    total_sales desc;                           -- ranks departments from highest to lowest revenue,
                                                -- making it easy to identify top and bottom performers at a glance
```

**What each line does:**
| Clause | Purpose |
|---|---|
| `b.product_area_name` | Retrieves the department label from the lookup table |
| `sum(a.sales_cost) as total_sales` | Aggregates all line-item costs into a single department total |
| `from grocery_db.transactions a` | Primary data source; each row is one purchase line |
| `inner join grocery_db.product_areas b on ...` | Enriches transactions with the department name |
| `where a.transaction_date between ...` | Filters to the specific month being reported |
| `group by b.product_area_name` | Ensures `SUM` is calculated per department |
| `order by total_sales desc` | Sorts results so the highest-revenue department appears first |

---

## Query 05 — Customers with No Loyalty Score (Unscored Customers)

**Question:** Which customers exist in the customer details table but have no entry in the loyalty scores table?

### Business Scenario

The CRM and data science teams maintain a loyalty score for each customer to prioritise
retention offers and personalised promotions. Customers without a score fall outside
these programmes — they are invisible to the targeting model. Identifying this gap lets
the team either trigger a data enrichment process or assign a default score, ensuring
no revenue opportunity is left on the table. Closing data gaps like this directly
improves model accuracy and the effectiveness of every campaign that follows.

```sql
select
    distinct a.customer_id                      -- retrieves each missing customer once; DISTINCT removes duplicates
                                                -- in case the customer_details table has repeated customer rows
from
    grocery_db.customer_details a               -- 'a' aliases the full customer base — the "left" side of the join
left join
    grocery_db.loyalty_scores b                 -- 'b' aliases the loyalty scores table — the "right" side
    on a.customer_id = b.customer_id            -- matches customers across both tables using the shared key;
                                                -- a LEFT JOIN keeps ALL rows from 'a' regardless of whether
                                                -- a match exists in 'b'
where
    b.customer_id is null;                      -- filters to ONLY the rows where no match was found in the
                                                -- loyalty_scores table, meaning these customers have no score;
                                                -- this is the standard LEFT JOIN anti-join pattern
```

**What each line does:**
| Clause | Purpose |
|---|---|
| `distinct a.customer_id` | Returns each unscored customer ID exactly once |
| `from grocery_db.customer_details a` | The complete customer roster — all customers start here |
| `left join grocery_db.loyalty_scores b on ...` | Attempts to match each customer to a loyalty score row |
| `where b.customer_id is null` | Keeps only rows where the join found no match — i.e., the unscored customers |

> **Pattern note:** This `LEFT JOIN ... WHERE right_table.key IS NULL` construct is known
> as an **anti-join**. It is one of the most efficient ways to find records that exist in
> one table but are absent from another, and it outperforms `NOT IN` when the right-hand
> column may contain NULLs.

---

## Query 06 — High-Value, High-Frequency Customers in August 2020

**Question:** Return a list of customers who spent more than $500 AND had 5 or more unique transactions in August 2020.

### Business Scenario

Identifying customers who are both big spenders **and** frequent shoppers is one of the
most powerful segmentation moves a retailer can make. These dual-criteria customers are
your most engaged and most profitable shoppers — the top of your loyalty pyramid.
By pinpointing them month by month, the CRM team can:

- **Reward loyalty proactively** — surprise-and-delight offers before customers start to churn.
- **Benchmark performance** — track whether the number of "VIP" customers grows or shrinks month on month, a leading indicator of competitive positioning.
- **Inform range decisions** — what product areas do these customers consistently buy from? Strengthening those ranges locks in their spend and makes it harder for competitors to steal them.
- **Drive profitability** — a small increase in retention among this tier has an outsized impact on overall revenue because their basket sizes are already large.

```sql
select
  customer_id,                                       -- the unique identifier for each customer being evaluated
  sum(sales_cost) as total_sales,                    -- adds up all purchase amounts for the customer within the period;
                                                     -- aliased to total_sales for readability in downstream reports
  count(distinct(transaction_id)) as total_trans     -- counts how many separate shopping trips the customer made;
                                                     -- DISTINCT ensures each trip is counted once even if it
                                                     -- spans multiple line items in the raw data
from
  grocery_db.transactions                            -- the source table containing every purchase line item

where
  transaction_date between '2020-08-01'              -- restricts data to August 2020 only;
  and '2020-08-31'                                   -- BETWEEN is inclusive of both start and end dates,
                                                     -- so no August day is accidentally excluded

group by
  customer_id                                        -- collapses all rows for the same customer into a single
                                                     -- summary row so the aggregate functions work per customer

having
  sum(sales_cost) > 500 and                          -- post-aggregation filter: keeps only customers whose
                                                     -- total August spend exceeds $500
  count(distinct(transaction_id)) >= 5;              -- second post-aggregation filter: customer must also have
                                                     -- made at least 5 distinct shopping trips;
                                                     -- both conditions must be true (AND) for the row to appear
```

**What each line does:**
| Clause | Purpose |
|---|---|
| `customer_id` | Groups and identifies each customer in the result |
| `sum(sales_cost) as total_sales` | Totals every dollar spent by the customer in August |
| `count(distinct(transaction_id)) as total_trans` | Counts the number of separate shopping trips |
| `from grocery_db.transactions` | Source of all purchase records |
| `where transaction_date between ...` | Restricts the dataset to August 2020 |
| `group by customer_id` | Ensures aggregates are calculated per customer |
| `having sum(sales_cost) > 500` | Excludes customers who didn't reach the $500 spend threshold |
| `having count(distinct ...) >= 5` | Excludes customers who made fewer than 5 trips |

> **`WHERE` vs `HAVING` note:** `WHERE` filters rows **before** aggregation (here, limiting to
> August dates). `HAVING` filters **after** aggregation, which is why the spend and trip-count
> thresholds must go there — they depend on the aggregated totals, which don't exist yet at
> the `WHERE` stage.

---

## Query 07 — Duplicate Credit Scores in Customer Details

**Question:** Return a list of credit score values that appear more than once in the `customer_details` table.

### Business Scenario

Credit scores are used by the grocery retailer's financial services arm (e.g., buy-now-pay-later,
store credit cards, instalment plans) to assess customer risk before extending credit.
Identifying duplicate credit score **values** serves two strategic purposes:

- **Data quality audit** — if the same score value appears hundreds of times, it may indicate
  a data pipeline bug, a default/placeholder value being assigned instead of a real score, or
  a rounding issue that collapses distinct scores into the same bucket. Poor data quality leads
  to mispriced risk and potential regulatory exposure.
- **Risk concentration analysis** — knowing which score bands are heavily clustered tells the
  risk team where the portfolio is concentrated. Overexposure to a single score band (especially
  near the subprime boundary) is a competitive and financial risk.

```sql
select
  credit_score,                           -- the credit score value being evaluated for duplicates
  count(credit_score) as cs_score         -- counts how many customers share this exact score value;
                                          -- aliased to cs_score; a value > 1 confirms duplication
from
  grocery_db.customer_details             -- the master customer table that stores individual credit scores

group by
  credit_score                            -- groups all rows that have the same credit score value together
                                          -- so COUNT operates within each score bucket

having
  count(credit_score) > 1;               -- post-aggregation filter: only returns score values that appear
                                          -- in more than one row, i.e., the duplicates;
                                          -- score values that are unique (count = 1) are excluded
```

**What each line does:**
| Clause | Purpose |
|---|---|
| `credit_score` | The score value being inspected — returned so you know which scores are duplicated |
| `count(credit_score) as cs_score` | Counts how many records share each score value |
| `from grocery_db.customer_details` | Source table containing each customer's credit score |
| `group by credit_score` | Buckets all records with the same score together for counting |
| `having count(credit_score) > 1` | Filters to only the score values that appear more than once |

> **`NULL` handling note:** `COUNT(credit_score)` ignores `NULL` values. If some customers
> have no credit score on record, those rows are automatically excluded from this result —
> which is the correct behaviour here because a missing score cannot be "duplicated".

---

## Query 08 — Customer(s) with the 2nd Highest Credit Score (Nth-Rank Pattern)

**Question:** Return the `customer_id`(s) for the customer(s) who have the 2nd highest credit score. The code must also work for any Nth highest credit score.

### Business Scenario

Identifying customers ranked at a specific position in the credit score hierarchy is a
common task in both risk management and premium product targeting:

- **Premium offer targeting** — the top credit-score band is already receiving the best
  offers. The 2nd-highest band is the next upsell opportunity: a nudge campaign offering
  these customers a small credit-limit increase or an exclusive rewards product could
  convert them into the top tier and increase their spend and engagement.
- **Competitive retention** — high-credit-score customers are also the most attractive
  to rival lenders. Monitoring this cohort and acting on any churn signals is essential
  to protecting high-quality, low-risk revenue.
- **Regulatory reporting** — financial regulators sometimes require breakdowns by credit
  tier. A parameterisable Nth-rank query makes it trivial to pull any tier on demand.
- **Scalability** — by using `dense_rank()` rather than hard-coded `MAX - 1` logic, a
  single change to `cs_rank = N` produces the answer for any rank, future-proofing the
  query against new business questions.

```sql
-- Step 1 — Common Table Expression (CTE): rank every customer by their credit score
with credit_scores as (
  select
    customer_id,                                       -- the customer being ranked
    credit_score,                                      -- the raw score value used for ranking
    dense_rank() over (order by credit_score desc)     -- assigns a rank to each distinct credit score value;
      as cs_rank                                       -- ORDER BY DESC means the highest score gets rank 1;
                                                       -- DENSE_RANK ensures that if multiple customers share
                                                       -- the top score they all get rank 1, and the next
                                                       -- distinct score gets rank 2 (no gaps in ranking),
                                                       -- which is critical for the Nth-highest requirement;
                                                       -- ROW_NUMBER would skip rank positions and RANK would
                                                       -- leave gaps — DENSE_RANK is the correct choice here
  from
    grocery_db.customer_details                        -- source table containing customer credit scores

  where
    credit_score is not null                           -- excludes customers with no credit score on record;
                                                       -- NULL values cannot be ranked meaningfully and would
                                                       -- distort the rank assignments if included
)

-- Step 2 — Main query: retrieve the customer(s) at the desired rank
select
  customer_id                                          -- returns the ID(s) of all customers at the target rank;
                                                       -- there may be multiple customers tied at rank 2
from
  credit_scores                                        -- references the CTE defined above
where
  cs_rank = 2;                                         -- filters to rank 2 (2nd highest credit score);
                                                       -- change this value to any N to get the Nth highest —
                                                       -- e.g., cs_rank = 5 for the 5th highest credit score
```

**What each line does:**
| Clause | Purpose |
|---|---|
| `with credit_scores as (...)` | Defines a CTE — a named, reusable subquery scoped to this statement |
| `customer_id` (inside CTE) | Carries the customer identifier through to the ranking step |
| `credit_score` (inside CTE) | The value used to determine rank order |
| `dense_rank() over (order by credit_score desc)` | Assigns rank 1 to the highest score, rank 2 to the next distinct score, etc., with no gaps |
| `as cs_rank` | Names the rank column for use in the outer query's `WHERE` clause |
| `from grocery_db.customer_details` | Source of customer credit scores |
| `where credit_score is not null` | Prevents NULL scores from corrupting the ranking |
| `select customer_id from credit_scores` | Reads from the CTE result |
| `where cs_rank = 2` | Retrieves only customers ranked 2nd — change `2` to any `N` for the Nth highest |

> **Why `DENSE_RANK` and not `RANK` or `ROW_NUMBER`?**
>
> | Function       | Behaviour when scores are tied                                            | Suitable here?                                                                 |
> | -------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
> | `ROW_NUMBER()` | Assigns a unique sequential number — ties are broken arbitrarily          | No — tied customers at rank 2 would receive different numbers                  |
> | `RANK()`       | Leaves gaps after ties — e.g., two rank-1s mean the next is rank 3        | No — "rank 2" would be skipped entirely if there's a tie at rank 1             |
> | `DENSE_RANK()` | No gaps after ties — the next distinct value always gets the next integer | **Yes** — guarantees that rank 2 always refers to the 2nd distinct score value |
