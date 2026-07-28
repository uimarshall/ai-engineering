## MORE INSIGHT ABOUT CALCULATED FIELD

---

## 1. The Relationship Triangle: Calculated Fields ↔ Dimensions ↔ Measures

A calculated field in Tableau sits **between** dimensions and measures, acting as a bridge that can transform one into the other or combine both. Understanding this relationship is critical because it determines:

- **What chart type** you can build
- **How the visualization responds** to filters and slicing
- **Whether Tableau treats the output** as a blue pill (Dimension) or green pill (Measure)

### How Calculated Fields Interact with Both

```
                    ┌─────────────────────────┐
                    │   CALCULATED FIELD       │
                    │  (transform/create new)  │
                    └──────────┬──────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐    ┌────────────┐    ┌──────────┐
        │DIMENSION │◄──►│  HYBRID    │◄──►│ MEASURE  │
        │(categorical) │  │ (LOD)      │    │(numeric) │
        └──────────┘    └────────────┘    └──────────┘
```

### Three Possible Outputs

| Calculated Field Output     | Tableau Pill Color | What It Does                                      | Example Formula                                |
| --------------------------- | ------------------ | ------------------------------------------------- | ---------------------------------------------- |
| **Dimension (categorical)** | Blue               | Creates new groupings, labels, or segments        | `IF [Sales] > 1000 THEN "High" ELSE "Low" END` |
| **Measure (numeric)**       | Green              | Creates new KPIs, ratios, or derived numbers      | `SUM([Profit]) / SUM([Sales])`                 |
| **Hybrid (LOD)**            | Blue or Green      | Operates at a different granularity than the view | `{ FIXED [Customer ID] : SUM([Sales]) }`       |

### Why This Matters

1. **If you output a dimension**, you can use it to slice measures — e.g., drag "Sales Tier" to Color to see High vs. Low sales performance.
2. **If you output a measure**, you can plot it against dimensions — e.g., drag "Profit Margin" to Rows against "Category".
3. **If you use LOD**, the granularity _inside the curly braces_ may differ from what's in the view, giving you powerful multi-level analysis.

### The Data Type Distinction

When you create a calculated field, Tableau auto-detects whether the result is a dimension or measure based on the **output data type**:

| Formula                                        | Output Type         | Detected As        |
| ---------------------------------------------- | ------------------- | ------------------ |
| `[Profit] - [Discount]`                        | Number (continuous) | Measure            |
| `DATEDIFF('day', [Start], [End])`              | Number (continuous) | Measure            |
| `DATENAME('month', [Order Date])`              | String (discrete)   | Dimension          |
| `IF [Sales] > 500 THEN "High" ELSE "Low" END`  | String (discrete)   | Dimension          |
| `[Order Date] >= DATEADD('day', -30, TODAY())` | Boolean             | Dimension (filter) |

> **Key insight**: You can manually change the role — right-click a calculated field and switch between Dimension / Measure / Attribute / etc. This changes how it behaves in the view.

---

## 2. Three Categories of Calculated Fields by Relationship Type

### Category A: Dimension-Outputting Calculated Fields

These return categorical or discrete values. They **expand** or **refine** how you group your data.

| Purpose             | Example Formula                                                                         | Business Use         |
| ------------------- | --------------------------------------------------------------------------------------- | -------------------- |
| **Segmentation**    | `IF [Sales] > 5000 THEN "Platinum" ELSEIF [Sales] > 1000 THEN "Gold" ELSE "Silver" END` | Customer tiering     |
| **Flagging**        | `IIF([Profit] < 0, "At Risk", "Healthy")`                                               | Profitability alert  |
| **Binning**         | `IF [Age] < 25 THEN "18-25" ELSEIF [Age] < 40 THEN "26-40" ELSE "40+" END`              | Demographic grouping |
| **Date extraction** | `DATENAME('quarter', [Order Date]) + " " + STR(DATEPART('year', [Order Date]))`         | "Q1 2026" labels     |
| **Bucketing**       | `INT([Sales] / 1000) * 1000 + " - " + (INT([Sales] / 1000) + 1) * 1000`                 | Sales range buckets  |

**View behavior**: These appear as blue pills. They create headers, slices, and can be used to color/size marks by category.

### Category B: Measure-Outputting Calculated Fields

These return numeric values. They **create** or **transform** KPIs and metrics.

| Purpose          | Example Formula                                                             | Business Use            |
| ---------------- | --------------------------------------------------------------------------- | ----------------------- |
| **Ratio**        | `SUM([Profit]) / SUM([Sales])`                                              | Profit margin           |
| **Growth**       | `(SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))` | Year-over-Year growth   |
| **Index**        | `SUM([Sales]) / TOTAL(SUM([Sales]))`                                        | % of total              |
| **Weighted avg** | `SUM([Price] * [Quantity]) / SUM([Quantity])`                               | Weighted average price  |
| **Forecast**     | `WINDOW_AVG(SUM([Sales]), -3, 0)`                                           | 4-period moving average |

**View behavior**: These appear as green pills. They get placed on Rows, Columns, or Marks shelves (Size, Color as a continuous ramp).

### Category C: Hybrid (LOD) Calculated Fields

These use Level of Detail (LOD) expressions to **operate at a different granularity** than the view.

| Expression Type | What It Does                                    | Example                                    | Granularity                        |
| --------------- | ----------------------------------------------- | ------------------------------------------ | ---------------------------------- |
| `FIXED`         | Computes at specified dimensions, ignoring view | `{ FIXED [Customer ID] : SUM([Sales]) }`   | Customer level, regardless of view |
| `INCLUDE`       | Adds dimensions to the view level               | `{ INCLUDE [Customer ID] : AVG([Sales]) }` | View level + Customer              |
| `EXCLUDE`       | Removes dimensions from the view level          | `{ EXCLUDE [Month] : AVG([Sales]) }`       | View level - Month                 |

These are the most powerful because they let you **compute a measure grouped by one set of dimensions, then use it in a view grouped by a different set**.

---

## 3. How to Decide: Calculated Field vs. Data Source Transformation

Not every metric should be a calculated field. Here's the decision framework:

| Criteria             | Use Calculated Field (Tableau)  | Use Transformation (SQL/Python)    |
| -------------------- | ------------------------------- | ---------------------------------- |
| **Data size**        | < 1M rows                       | > 10M rows (pre-compute for speed) |
| **Update frequency** | Data changes frequently         | Static or batch-updated data       |
| **Reusability**      | Across many workbooks           | In one specific pipeline           |
| **Complexity**       | Simple to moderate logic        | Complex joins or aggregations      |
| **Governance**       | Team needs standard definitions | Central data team controls logic   |
| **Exploration**      | Ad-hoc analysis                 | Production dashboard               |

---

## 4. Business Application Examples Across Industries

### 🏪 Retail & E-Commerce

**Use case**: Customer Lifetime Value (CLV) segmentation

| Component        | Field                                          | Role                    |
| ---------------- | ---------------------------------------------- | ----------------------- |
| Dimension        | Customer Segment, Region, Category             | Slicing the data        |
| Measure          | Sales, Profit, Quantity                        | Base metrics            |
| Calculated Field | `{ FIXED [Customer ID] : SUM([Profit]) }`      | Customer Lifetime Value |
| Calculated Field | `{ FIXED [Customer ID] : COUNTD([Order ID]) }` | Purchase Frequency      |

**Business insight**: "Our top 10% of customers by CLV generate 45% of total profit, and they're concentrated in the Technology category in the West region."

| Calculated Field            | Formula                                                                     | What It Tells You                         |
| --------------------------- | --------------------------------------------------------------------------- | ----------------------------------------- |
| **Basket Size**             | `{ INCLUDE [Order ID] : COUNTD([Product ID]) }`                             | Avg products per order                    |
| **Repeat Purchase Rate**    | `COUNTD([Order ID]) / COUNTD([Customer ID])`                                | Orders per customer (loyalty)             |
| **Discount Impact**         | `SUM([Sales]) - SUM([Sales] * (1 - [Discount]))`                            | Revenue lost to discounts                 |
| **Category Penetration %**  | `COUNTD([Customer ID]) / TOTAL(COUNTD([Customer ID]))`                      | % of total customers buying each category |
| **Month-over-Month Growth** | `(SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))` | MoM revenue trend                         |

---

### 💰 Finance & Accounting

**Use case**: Profitability analysis by department

| Component        | Field                                          | Role                 |
| ---------------- | ---------------------------------------------- | -------------------- |
| Dimension        | Department, Account Type, Quarter              | Slicing              |
| Measure          | Revenue, Expense, Headcount                    | Base metrics         |
| Calculated Field | `SUM([Revenue] - [Expenses]) / SUM([Revenue])` | Profit Margin %      |
| Calculated Field | `SUM([Revenue]) / SUM([Headcount])`            | Revenue per Employee |

| Calculated Field         | Formula                                                                           | What It Tells You              |
| ------------------------ | --------------------------------------------------------------------------------- | ------------------------------ |
| **Variance %**           | `(SUM([Actual]) - SUM([Budget])) / SUM([Budget])`                                 | Budget vs. actual performance  |
| **Expense Ratio**        | `SUM([Operating Expenses]) / SUM([Revenue])`                                      | Cost efficiency                |
| **Return on Investment** | `(SUM([Gain]) - SUM([Cost])) / SUM([Cost])`                                       | ROI per project                |
| **Contribution Margin**  | `SUM([Revenue]) - SUM([Variable Costs])`                                          | Profitability by product       |
| **YoY Revenue Growth**   | `(SUM([Revenue]) - LOOKUP(SUM([Revenue]), -4)) / ABS(LOOKUP(SUM([Revenue]), -4))` | Annual growth (quarterly data) |

**Business insight**: "The R&D department shows a negative variance (-8%) against budget, but their expense ratio is the lowest in the company at 12% — indicating efficient spending relative to revenue generated."

---

### 📢 Marketing & Advertising

**Use case**: Channel performance & customer acquisition

| Component        | Field                                   | Role                 |
| ---------------- | --------------------------------------- | -------------------- |
| Dimension        | Channel, Campaign, Segment              | Slicing              |
| Measure          | Spend, Impressions, Clicks, Conversions | Base metrics         |
| Calculated Field | `SUM([Spend]) / SUM([Clicks])`          | Cost Per Click (CPC) |
| Calculated Field | `SUM([Conversions]) / SUM([Clicks])`    | Conversion Rate      |

| Calculated Field                     | Formula                                                                            | What It Tells You                      |
| ------------------------------------ | ---------------------------------------------------------------------------------- | -------------------------------------- |
| **Customer Acquisition Cost (CAC)**  | `{ FIXED [Channel] : SUM([Spend]) } / { FIXED [Channel] : COUNTD([Customer ID]) }` | Cost to acquire a customer per channel |
| **Return on Marketing Spend (ROMI)** | `(SUM([Revenue Attributed]) - SUM([Spend])) / SUM([Spend])`                        | Revenue generated per $ spent          |
| **Click-Through Rate (CTR)**         | `SUM([Clicks]) / SUM([Impressions])`                                               | Ad engagement                          |
| **Customer Lifetime Value : CAC**    | `{ FIXED [Customer ID] : SUM([Profit]) } / [CAC]`                                  | Is CAC justified?                      |
| **Attribution Coefficient**          | `SUM([Revenue Attributed]) / TOTAL(SUM([Revenue Attributed]))`                     | % of revenue by touchpoint             |

**Business insight**: "Social media has the lowest CAC ($12) but also a lower ROMI (2.1x) compared to Email ($18 CAC, 6.8x ROMI). Shifting 20% of social budget to email could increase total ROMI by 15%."

---

### 👥 Human Resources

**Use case**: Employee retention & workforce planning

| Component        | Field                                               | Role                   |
| ---------------- | --------------------------------------------------- | ---------------------- |
| Dimension        | Department, Tenure Band, Gender, Location           | Slicing                |
| Measure          | Employee Count, Salary, Years of Service            | Base metrics           |
| Calculated Field | `DATEDIFF('year', [Hire Date], TODAY())`            | Current Tenure (Years) |
| Calculated Field | `COUNTD([Employee ID]) / COUNTD([Total Employees])` | Attrition Rate         |

| Calculated Field       | Formula                                                                                                                 | What It Tells You                      |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| **Attrition Flag**     | `IIF([Status] = "Terminated" AND [Term Date] >= DATEADD('month', -12, TODAY()), 1, 0)`                                  | Employee who left in last 12 months    |
| **Tenure Bucket**      | `INT(DATEDIFF('year', [Hire Date], TODAY()) / 3) * 3 + "-" + (INT(DATEDIFF('year', [Hire Date], TODAY()) / 3) + 1) * 3` | "0-3 yrs", "3-6 yrs", etc.             |
| **Salary Ratio**       | `[Salary] / { FIXED [Job Role] : AVG([Salary]) }`                                                                       | Salary vs. role average (equity check) |
| **Promotion Velocity** | `DATEDIFF('month', [Last Promotion], TODAY())`                                                                          | Months since last promotion            |
| **Headcount Forecast** | `WINDOW_SUM(SUM([Headcount]), 0, 3)` + `WINDOW_SUM(SUM([Hires]), 0, 3)` - `WINDOW_SUM(SUM([Terminations]), 0, 3)`       | Projected headcount next 3 months      |

**Business insight**: "Attrition is highest among employees with 1-3 years tenure (24%), and lowest among those with 6+ years (6%). The average time since last promotion for departing employees is 18 months — suggesting career growth is a key retention driver."

---

### 🏭 Operations & Supply Chain

**Use case**: Inventory efficiency & order fulfillment

| Component        | Field                                                | Role               |
| ---------------- | ---------------------------------------------------- | ------------------ |
| Dimension        | Warehouse, SKU Category, Supplier                    | Slicing            |
| Measure          | Stock Level, Orders, Lead Time                       | Base metrics       |
| Calculated Field | `SUM([Orders Shipped]) / SUM([Orders Placed])`       | Fill Rate %        |
| Calculated Field | `SUM([Cost of Goods Sold]) / AVG([Inventory Value])` | Inventory Turnover |

| Calculated Field       | Formula                                                                                                 | What It Tells You                             |
| ---------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| **Days of Inventory**  | `AVG([Inventory Value]) / (SUM([COGS]) / 365)`                                                          | Days until stock runs out                     |
| **Stockout Flag**      | `IIF([Stock Level] = 0, "Out of Stock", IIF([Stock Level] < [Reorder Point], "Low Stock", "Adequate"))` | Inventory status alert                        |
| **On-Time Delivery %** | `SUM(IIF([Delivered Date] <= [Promised Date], 1, 0)) / COUNTD([Order ID])`                              | % of orders delivered on time                 |
| **Lead Time Variance** | `AVG([Actual Lead Time]) - AVG([Expected Lead Time])`                                                   | Supplier reliability                          |
| **Carrying Cost**      | `AVG([Inventory Value]) * 0.25`                                                                         | 25% carrying cost assumption on avg inventory |

**Business insight**: "Warehouse 3 has 42 days of inventory (highest) but the lowest fill rate (78%). This indicates an overstock problem with the wrong SKUs — excess capital tied up in slow-moving items while fast-movers are out of stock."

---

### 🏥 Healthcare

**Use case**: Patient outcomes & operational efficiency

| Component        | Field                                                | Role               |
| ---------------- | ---------------------------------------------------- | ------------------ |
| Dimension        | Ward, Doctor, Diagnosis, Admission Month             | Slicing            |
| Measure          | Patients, Length of Stay, Cost                       | Base metrics       |
| Calculated Field | `SUM([Readmitted Patients]) / SUM([Total Patients])` | Readmission Rate % |
| Calculated Field | `AVG([Discharge Date] - [Admission Date])`           | Avg Length of Stay |

| Calculated Field         | Formula                                                                                                   | What It Tells You              |
| ------------------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **Bed Occupancy Rate**   | `SUM([Occupied Bed Days]) / (COUNTD([Bed ID]) * DATEDIFF('day', [Start Date], [End Date]))`               | % of beds utilized             |
| **Patient Acuity Index** | `AVG([Nursing Hours per Patient]) / AVG([Total Nursing Hours])`                                           | Resource intensity per patient |
| **Cost per Case**        | `SUM([Total Cost]) / COUNTD([Patient ID])`                                                                | Avg treatment cost             |
| **Mortality Risk Score** | `IIF([Age] > 75 AND [Comorbidity Count] > 3, "High", IIF([Age] > 60, "Medium", "Low"))`                   | Risk stratification            |
| **Wait Time Band**       | `IF [Wait Time] < 15 THEN "Under 15 min" ELSEIF [Wait Time] < 30 THEN "15-30 min" ELSE "Over 30 min" END` | ER wait time categories        |

**Business insight**: "The Cardiology ward has a readmission rate of 18% — 6 points above the hospital average. Patients with 'High' mortality risk scores account for 70% of these readmissions. A targeted follow-up program for high-risk cardiac patients could reduce readmissions by 40%."

---

## 5. Quick Reference: Calculated Field ↔ Dimension ↔ Measure Decision Table

When building a calculated field, ask yourself:

| Question                                             | If Answer Is... | Then Output Is...                            | Example                           |
| ---------------------------------------------------- | --------------- | -------------------------------------------- | --------------------------------- |
| "Do I want to create a new group or label?"          | Yes             | Dimension                                    | Sales Tier (High/Medium/Low)      |
| "Do I want to compute a new number?"                 | Yes             | Measure                                      | Profit Margin %                   |
| "Does my calculation need to ignore the view level?" | Yes             | LOD (often measure)                          | Total Sales (FIXED)               |
| "Do I need to filter based on a condition?"          | Yes             | Boolean Dimension                            | `[Sales] > 1000`                  |
| "Am I extracting part of a date?"                    | Yes             | Dimension (if string) or Measure (if number) | `DATENAME('month', [Date])` → Dim |
| "Am I combining two fields?"                         | Yes             | Depends on output                            | `[First] + " " + [Last]` → Dim    |

---

## 6. Summary: The Power of Understanding This Relationship

```
Raw Data Columns
    │
    ├── Dimension (Category, Region) → Slicing
    │
    ├── Measure (Sales, Profit) → Aggregating
    │
    └── Calculated Field
         │
         ├── Outputs Dimension → New way to slice
         ├── Outputs Measure → New KPI to analyze
         └── Uses LOD → Multi-granularity insights
```

### Why This Matters for Business

1. **Better dashboards**: You know exactly when to create a dimension field (for filtering/coloring) vs. a measure field (for value axes).
2. **Cleaner analysis**: Calculated fields let you embed business rules directly into Tableau, so every stakeholder sees the same "Gold Customer" or "High Risk" definition.
3. **Deeper insights**: LOD expressions let you ask questions like "What percentage of total sales does each customer represent?" — combining both dimension- and measure-like behaviors.
4. **Faster decisions**: Instead of exporting data to Excel to compute ratios or segments, you do it live in Tableau with drag-and-drop calculated fields.

### Final Thought

> **Dimensions tell you _what_ to look at. Measures tell you _how much_. Calculated fields tell you _what you didn't know you had_ — they are the bridge between your raw data and your business insights.**

---

## Appendix: Common Patterns — Dimension vs. Measure Output

| Input(s)                | Calculation Pattern                            | Output Role                 | Typical Use                     |
| ----------------------- | ---------------------------------------------- | --------------------------- | ------------------------------- |
| 1 Measure               | `[Sales] * 1.1`                                | Measure                     | Forecasting                     |
| 1 Dimension             | `LEFT([Customer Name], 1)`                     | Dimension                   | Alphabetical grouping           |
| 1 Measure + 1 Measure   | `SUM([Profit]) / SUM([Sales])`                 | Measure                     | Ratio                           |
| 1 Dimension + 1 Measure | `IF [Sales] > 1000 THEN "High" ELSE "Low" END` | Dimension                   | Conditional grouping            |
| 2 Dimensions            | `[City] + ", " + [State]`                      | Dimension                   | Concatenation                   |
| LOD (FIXED)             | `{ FIXED [Customer ID] : SUM([Sales]) }`       | Measure (at customer level) | Per-customer metric             |
| LOD (INCLUDE)           | `{ INCLUDE [Customer ID] : AVG([Sales]) }`     | Measure (hybrid)            | Avg customer value at any level |
| Table Calc              | `RUNNING_SUM(SUM([Sales]))`                    | Measure (table)             | Cumulative totals               |
