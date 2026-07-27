# Client Dashboard: OmniCorp Retail Sales & Customer Intelligence

## Client Background

**OmniCorp Retail** is a mid-size retail chain operating across 4 regions (East, West, Central, South) with 15 store locations. They sell products across 3 categories (Furniture, Office Supplies, Technology) with 17 sub-categories.

### Business Problem

OmniCorp's management needs a **single-pane-of-glass dashboard** that answers:

1. **Sales Performance:** How are we tracking against targets at the Category, Region, and Store level?
2. **Customer Health:** What's our customer acquisition cost? Who are our high-value customers?
3. **Operational Efficiency:** What are our top/bottom performing products? Where are we losing money?
4. **Trend Analysis:** Are we growing month-over-month? What's our customer retention rate?

### Why LOD?

The challenge is that **different questions require different levels of granularity**, but management wants all answers in a single dashboard view. LOD expressions solve this by allowing us to compute metrics at varying granularities **independent** of the chart dimensions.

---

## Dashboard Overview

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│  HEADER: KPI TILES (Overall Business Health)                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐  │
│  │ Total   │ │ Avg Rev │ │ CAC     │ │ Active Customers │  │
│  │ Sales   │ │ /Customer│ │ (LOD)   │ │ (LOD)            │  │
│  │ $5.2M   │ │ $2,450  │ │ $124.50 │ │ 2,150            │  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│                              │                               │
│  Sales by Category          │  Sales vs Target (%)          │
│  (Bar Chart)                │  (Bullet Chart)               │
│                              │                               │
│  [Furniture    ██████]     │  Furniture    ████████░░░ 85% │
│  [Office Supp  ███████]    │  Office Supp  █████████░ 92% │
│  [Technology   ████████]   │  Technology   ██████████ 101%│
│                              │                               │
├─────────────────────────────────────────────────────────────┤
│                              │                               │
│  Monthly Sales Trend        │  Top 5 Customers             │
│  (Line Chart)               │  (Table)                     │
│                              │                               │
│  ██                          │  1. ABC Corp   $52,000      │
│    ██  ██                    │  2. XYZ Inc    $48,500      │
│      ██  ██  ██              │  3. ...                     │
│  ──────────────────          │                               │
│  LOD: FIXED trunc(month)    │  LOD: FIXED Customer ID      │
│                              │                               │
├─────────────────────────────────────────────────────────────┤
│                              │                               │
│  Profit by Region/Store     │  Product Performance         │
│  (Heatmap)                  │  (Scatter: Sales vs Profit)  │
│                              │                               │
│  East   West   Cent   South │  ●               ●           │
│  ┌─────┬─────┬─────┬─────┐│    ●  ●    ●                   │
│  │ ██  │ ██  │ ██  │ ██  ││       ●  ●  ●    ●            │
│  │ ██  │ ██  │ ██  │ ██  ││          ●  ●  ●              │
│  └─────┴─────┴─────┴─────┘│  ────────────────────────     │
│  LOD: EXCLUDE [Category]   │  LOD: FIXED [Sub-Category]   │
│                              │                               │
├─────────────────────────────────────────────────────────────┤
│  FOOTER: Filters & Interactive Controls                     │
│  [Region: ▼ All]  [Category: ▼ All]  [Date Range: ▼]       │
│  [Customer Segment: ▼ All]  [High Value: ▼ Yes/No/All]    │
└─────────────────────────────────────────────────────────────┘
```

---

## Dashboard Sheets (Worksheets) Detail

### Sheet 1: KPI Tiles

| KPI                                 | Calculation                                                                                   | LOD Used            | Purpose                                  |
| ----------------------------------- | --------------------------------------------------------------------------------------------- | ------------------- | ---------------------------------------- |
| **Total Sales**                     | `SUM([Sales])`                                                                                | No LOD (simple agg) | Overall revenue                          |
| **Avg Revenue Per Customer**        | `AVG({ FIXED [Customer ID] : SUM([Sales]) })`                                                 | **FIXED LOD**       | True per-customer average                |
| **Customer Acquisition Cost (CAC)** | `{ FIXED [Channel] : SUM([Marketing Spend]) } / { FIXED [Channel] : COUNTD([Customer ID]) }`  | **FIXED LOD** (x2)  | Cost to acquire a customer per channel   |
| **Active Customers**                | `COUNTD({ FIXED [Customer ID] : MIN([Last Purchase Date]) > DATEADD('month', -3, TODAY()) })` | **FIXED LOD**       | Customers who purchased in last 3 months |

---

### Sheet 2: Sales by Category

**Chart Type:** Horizontal Bar Chart

**Rows:** `[Category]`

**Columns:** `SUM([Sales])`

**Color:** `SUM([Sales])` (gradient)

**Tooltip Enhancement (LOD):**

```
Category: <Category>
Sales: <SUM(Sales)>
% of Total Sales: <SUM([Sales]) / { SUM([Sales]) }>
% of Category Target: <SUM([Sales]) / { FIXED [Category] : SUM([Target]) }>
```

> **LOD Insight:** The `% of Total Sales` uses a bare LOD `{ SUM([Sales]) }` to compute the grand total denominator, ignoring any view filters. This means even if you filter to one region, it still shows the global percentage.

---

### Sheet 3: Sales vs Target (Bullet Chart)

**Chart Type:** Bullet Chart

**Rows:** `[Category]`

**Columns:**

- `SUM([Sales])` (bar)
- `{ FIXED [Category], DATETRUNC('month', [Order Date]) : SUM([Target]) }` (reference line)

**LOD Calculated Field `Monthly Target by Category`:**

```tableau
{ FIXED [Category], DATETRUNC('month', [Order Date]) : SUM([Target]) }
```

**LOD Calculated Field `Target Achievement %`:**

```tableau
SUM([Sales]) / { FIXED [Category], DATETRUNC('month', [Order Date]) : SUM([Target]) }
```

> **LOD Insight:** FIXED LOD at Category + Month level ensures the target is correctly attributed even when the view is at the yearly level or filtered by store. Without LOD, the SUM(Target) would incorrectly aggregate across all months in view.

---

### Sheet 4: Monthly Sales Trend

**Chart Type:** Continuous Line Chart

**Columns:** `MONTH([Order Date])` (continuous)

**Rows:** `SUM([Sales])`

**Dual Axis:**

- 1st Axis: `SUM([Sales])`
- 2nd Axis: `{ EXCLUDE [Order Date] : AVG([Sales]) }` (overall average as benchmark line)

**LOD Calculated Field `Overall Avg Sales Benchmark`:**

```tableau
{ EXCLUDE [Order Date] : AVG([Sales]) }
```

**LOD Calculated Field `MoM Change %`:**

```tableau
(SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))
```

_(Note: LOOKUP is a table calculation, combined with the LOD benchmark)_

> **LOD Insight:** The EXCLUDE LOD removes the date dimension, computing the overall average sales across all time. This serves as a static benchmark line that doesn't change when you filter to specific months.

---

### Sheet 5: Top 5 Customers

**Chart Type:** Table (Text Table)

**Rows:** `[Customer Name]` (Top 5 filtered by `SUM([Sales])`)

**Columns:**

- `SUM([Sales])`
- `{ FIXED [Customer ID] : COUNTD([Order ID]) }` (Total Orders per Customer)
- `{ FIXED [Customer ID] : AVG([Sales]) }` (Avg Order Value)
- `{ FIXED [Customer ID] : MIN([Order Date]) }` (First Purchase Date)
- `{ FIXED [Customer ID] : MAX([Order Date]) }` (Last Purchase Date)

**LOD Calculated Fields:**

1. **Total Orders Per Customer**

```tableau
{ FIXED [Customer ID] : COUNTD([Order ID]) }
```

2. **Avg Order Value Per Customer**

```tableau
{ FIXED [Customer ID] : AVG([Sales]) }
```

3. **Customer Tenure (Days)**

```tableau
DATEDIFF('day',
  { FIXED [Customer ID] : MIN([Order Date]) },
  { FIXED [Customer ID] : MAX([Order Date]) }
)
```

4. **Is High Value Customer**

```tableau
{ FIXED [Customer ID] : SUM([Sales]) } > 5000
```

> **LOD Insight:** All customer-level metrics use FIXED LOD on [Customer ID]. This ensures that even though the underlying data has multiple rows per customer (one per product purchased), the metrics are computed once per customer. The `Is High Value Customer` flag can then be used as a dashboard filter.

---

### Sheet 6: Profit by Region/Store (Heatmap)

**Chart Type:** Heatmap (Square marks)

**Rows:** `[Region]`

**Columns:** `[Store Name]`

**Color:** `SUM([Profit])`

**Size:** `SUM([Sales])`

**Detail:** `[Category]`

**LOD Calculated Field `Region Profit Share %`:**

```tableau
SUM([Profit]) / { EXCLUDE [Store Name], [Category] : SUM([Profit]) }
```

**LOD Calculated Field `Store vs Region Avg Profit`:**

```tableau
SUM([Profit]) - { EXCLUDE [Store Name] : AVG([Profit]) }
```

> **LOD Insight:** EXCLUDE LOD removes Store Name to compute the region-wide average profit. Each store's profit is compared against this regional baseline. This works even if Store Name is in the view.

---

### Sheet 7: Product Performance Scatter Plot

**Chart Type:** Scatter Plot

**Columns:** `SUM([Sales])`

**Rows:** `SUM([Profit])`

**Detail:** `[Sub-Category]`

**Color:** `AVG([Discount])`

**LOD Calculated Field `Category Avg Profit Margin`:**

```tableau
{ FIXED [Category] : SUM([Profit]) / SUM([Sales]) }
```

**LOD Calculated Field `Performance vs Category Avg`:**

```tableau
(SUM([Profit]) / SUM([Sales])) - { FIXED [Category] : SUM([Profit]) / SUM([Sales]) }
```

> **LOD Insight:** FIXED at Category level computes the average profit margin for the parent category. Each sub-category is then compared against its category average, revealing which sub-categories over/under-perform relative to their peers.

---

## Dashboard Interactivity & Actions

### Filter Actions

| Filter              | Type           | Affects                 | LOD Consideration                                             |
| ------------------- | -------------- | ----------------------- | ------------------------------------------------------------- |
| Region              | Quick Filter   | All sheets              | FIXED LODs ignore this unless promoted to Context Filter      |
| Category            | Quick Filter   | All sheets              | FIXED LODs on Category will still compute correctly           |
| Date Range          | Range Filter   | All sheets              | EXCLUDE/INCLUDE LODs respect this; FIXED needs Context Filter |
| High Value Customer | Boolean Filter | Customer-related sheets | Works because it's a row-level flag (derived from FIXED LOD)  |

### Context Filter Strategy

Because FIXED LOD ignores dimension filters, we need a strategy:

1. **For "Region" filter**: Use Context Filter when the user wants `% of Total` to recalculate within the filtered region. Otherwise, FIXED LODs retain global context.

2. **For "Date Range" filter**: Use Context Filter so FIXED LODs like `First Purchase Date` and `Customer Tenure` respect the selected date range.

3. **Add "Apply to Context" button** with clear labeling so users understand when they're narrowing vs exploring the full dataset.

### Dashboard Actions

| Action Type          | Source                    | Target           | Effect                                             |
| -------------------- | ------------------------- | ---------------- | -------------------------------------------------- |
| **Filter Action**    | Sales by Category (click) | All sheets       | Click a category to filter entire dashboard        |
| **URL Action**       | Top 5 Customers           | External CRM     | Click customer name to open CRM profile            |
| **Highlight Action** | Product Scatter (hover)   | Profit Heatmap   | Hover a sub-category to highlight across dashboard |
| **Parameter Action** | Monthly Trend (click)     | Target reference | Click a month to update target comparison          |

---

## Parameters for Dynamic Analysis

### Parameter 1: `Top N Customers`

**Data Type:** Integer

**Allowable Values:** 5, 10, 15, 20, 50, All

**Calculated Field `Top N Filter`:**

```tableau
RANK({ FIXED [Customer ID] : SUM([Sales]) }) <= [Top N Customers] OR [Top N Customers] = 999
```

### Parameter 2: `Sales Benchmark Type`

**Data Type:** String

**Allowable Values:** "Overall Avg", "Category Avg", "Region Avg"

**Calculated Field `Dynamic Benchmark`:**

```tableau
CASE [Sales Benchmark Type]
  WHEN "Overall Avg" THEN { AVG([Sales]) }
  WHEN "Category Avg" THEN { FIXED [Category] : AVG([Sales]) }
  WHEN "Region Avg" THEN { FIXED [Region] : AVG([Sales]) }
END
```

### Parameter 3: `Target Year`

**Data Type:** Integer

**Allowable Values:** 2023, 2024, 2025

**Usage:** Filters `SUM([Target])` to the selected year, while `SUM([Sales])` may span multiple years for comparison.

---

## Data Model Requirements

The dashboard requires a **star schema** data model:

```
┌──────────────┐      ┌──────────────────┐
│   DimStore   │      │   DimCustomer    │
│──────────────│      │──────────────────│
│ Store ID (PK)│◄────┐│ Customer ID (PK) │◄────┐
│ Region       │     ││ Customer Name    │     │
│ Store Name   │     ││ Segment          │     │
│ Store Manager│     ││ Channel          │     │
│ Open Date    │     ││ Acquisition Date │     │
└──────────────┘     ││ Customer Tier    │     │
                     │└──────────────────┘     │
┌──────────────┐     │                         │
│   DimProduct │     │                         │
│──────────────│     │                         │
│ Product ID   │◄────┤                         │
│ Product Name │     │                         │
│ Category     │     │                         │
│ Sub-Category │     │                         │
│ Unit Cost    │     │                         │
│ Unit Price   │     │                         │
└──────────────┘     │                         │
                     │                         │
┌────────────────────┴─────────────────────────┘
│           FactSales
│────────────────────────────
│ Order ID (PK)
│ Order Date
│ Ship Date
│ Customer ID (FK)
│ Store ID (FK)
│ Product ID (FK)
│ Sales
│ Quantity
│ Discount
│ Profit
│ Shipping Cost
│────────────────────────────
│                   FactMarketing
│────────────────────────────
│ Channel
│ Campaign
│ Date
│ Impressions
│ Clicks
│ Spend
└────────────────────────────
```

---

## LOD Expressions Cheat Sheet (for this dashboard)

| #   | Expression                                                               | Type     | What It Does                                          |
| --- | ------------------------------------------------------------------------ | -------- | ----------------------------------------------------- |
| 1   | `{ SUM([Sales]) }`                                                       | Bare LOD | Grand total of sales (single value)                   |
| 2   | `{ FIXED [Customer ID] : SUM([Sales]) }`                                 | FIXED    | Total sales per customer                              |
| 3   | `{ FIXED [Category] : SUM([Target]) }`                                   | FIXED    | Target per category (ignores view filters)            |
| 4   | `{ FIXED [Customer ID] : COUNTD([Order ID]) }`                           | FIXED    | Order count per customer                              |
| 5   | `{ FIXED [Customer ID] : MIN([Order Date]) }`                            | FIXED    | First purchase date per customer                      |
| 6   | `{ FIXED [Category], DATETRUNC('month', [Order Date]) : SUM([Target]) }` | FIXED    | Monthly target per category                           |
| 7   | `{ FIXED [Channel] : SUM([Marketing Spend]) }`                           | FIXED    | Total marketing spend per channel                     |
| 8   | `{ FIXED [Channel] : COUNTD([Customer ID]) }`                            | FIXED    | Unique customers acquired per channel                 |
| 9   | `{ FIXED [Category] : SUM([Profit]) / SUM([Sales]) }`                    | FIXED    | Profit margin per category                            |
| 10  | `{ EXCLUDE [Order Date] : AVG([Sales]) }`                                | EXCLUDE  | Overall average sales (ignoring dates)                |
| 11  | `{ EXCLUDE [Store Name], [Category] : SUM([Profit]) }`                   | EXCLUDE  | Total profit removing store & category (region total) |
| 12  | `{ EXCLUDE [Store Name] : AVG([Profit]) }`                               | EXCLUDE  | Region average profit (removing store)                |
| 13  | `{ INCLUDE [Customer ID] : AVG([Sales]) }`                               | INCLUDE  | Avg sales per customer added to view level            |
| 14  | `{ INCLUDE [Order ID] : COUNTD([Product ID]) }`                          | INCLUDE  | Products per order added to any view                  |

---

## Testing & Validation

### LOD Verification Checklist

| Test                            | Expected Behavior                                | Pass/Fail |
| ------------------------------- | ------------------------------------------------ | --------- |
| **FIXED ignores Region filter** | % of Total still shows global %                  | ✅        |
| **FIXED with Context Filter**   | % of Total recalculates within filtered region   | ✅        |
| **EXCLUDE removes Category**    | Region total on heatmap is across ALL categories | ✅        |
| **INCLUDE adds Customer**       | Avg Sales Per Customer is higher than Avg Sales  | ✅        |
| **Bare LOD `{SUM([Sales])}`**   | Returns a single value, not affected by any dims | ✅        |
| **Nested LOD in LOD**           | Complex calc like CAC works correctly            | ✅        |
| **Dashboard filter sync**       | All sheets respond to filter actions             | ✅        |

### Common Pitfalls to Avoid

1. ❌ **Using FIXED when INCLUDE is needed** — If you want the metric to respect user filters, don't use FIXED unless you promote to Context Filter.
2. ❌ **Forgetting aggregation inside LOD** — `{FIXED [Category] : [Sales]}` fails; must be `{FIXED [Category] : SUM([Sales])}`.
3. ❌ **High cardinality INCLUDE** — `{INCLUDE [Order ID]}` with millions of orders will impact performance.
4. ❌ **Mixing LOD and Table Calcs** — LOD computes in the database, Table Calcs compute in the client. Order of operations matters.

---

## Deployment Notes

### Performance Optimization

1. **Extract your data source** — LODs push computation to the database; extracts reduce the load.
2. **Use context filters sparingly** — Each context filter triggers a new query.
3. **Limit INCLUDE cardinality** — Avoid INCLUDE on high-cardinality dimensions (like Order ID with 100k+ values).
4. **Aggregate at source** — If possible, pre-aggregate daily data to weekly in the database.

### Suggested Folders in Tableau

```
OmniCorp Dashboard (v1.0)/
├── Data Sources/
│   ├── OmniCorp Sales (Extract)
│   └── OmniCorp Targets (Extract)
├── Parameters/
│   ├── Top N Customers
│   ├── Sales Benchmark Type
│   └── Target Year
├── Calculated Fields/
│   ├── LOD - Customer Level/
│   │   ├── Total Sales Per Customer
│   │   ├── Avg Order Value Per Customer
│   │   ├── Customer Tenure
│   │   ├── Is High Value Customer
│   │   └── Total Orders Per Customer
│   ├── LOD - Category Level/
│   │   ├── % of Category Total
│   │   ├── Monthly Target by Category
│   │   ├── Target Achievement %
│   │   └── Category Avg Profit Margin
│   ├── LOD - Region Level/
│   │   ├── Region Profit Share %
│   │   ├── Store vs Region Avg Profit
│   │   └── Region Avg Sales
│   └── LOD - Global Level/
│       ├── Grand Total Sales
│       ├── Overall Avg Sales Benchmark
│       └── CAC (Customer Acquisition Cost)
├── Sheets/
│   ├── 01 - KPI Tiles
│   ├── 02 - Sales by Category
│   ├── 03 - Sales vs Target
│   ├── 04 - Monthly Sales Trend
│   ├── 05 - Top N Customers
│   ├── 06 - Profit Heatmap
│   └── 07 - Product Scatter
└── Dashboards/
    └── 01 - OmniCorp Executive Dashboard (Main)
```

---

## Summary

This dashboard demonstrates **14 distinct LOD expressions** across **3 LOD types** (FIXED, INCLUDE, EXCLUDE) in a cohesive, real-world business scenario. The key learning outcomes are:

1. **FIXED LOD** for customer-level, category-level, and channel-level metrics that need to persist across view changes
2. **EXCLUDE LOD** for computing benchmarks and regional subtotals by removing dimensions from the view
3. **INCLUDE LOD** for adding granularity to compute per-customer or per-order averages at higher levels
4. **Bare LOD** for grand total computations like `% of Overall Total`

The dashboard is filterable, interactive, and built for executive decision-making — all powered by Level of Detail expressions.
