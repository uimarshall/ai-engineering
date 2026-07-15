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
