# Create a Sample Dashboard for a Client Using LOD

This directory contains a complete, real-world reference implementation of a **Retail Sales & Customer Intelligence Dashboard** built for a fictional client **"OmniCorp Retail"**, powered by **Level of Detail (LOD) Expressions** in Tableau.

---

## 📂 What's Inside

| File                                             | Description                                                                                            |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| [`DASHBOARD_DESIGN.md`](./DASHBOARD_DESIGN.md)   | Complete dashboard layout, sheet designs, interactivity, data model, deployment notes                  |
| [`CALCULATED_FIELDS.md`](./CALCULATED_FIELDS.md) | 40 calculated field definitions with LOD expressions — ready to use in Tableau                         |
| [`SAMPLE_DATA.md`](./SAMPLE_DATA.md)             | Star schema data model with sample data for stores, customers, products, sales, marketing, and targets |

---

## 🚀 Quick Start

1. **Review the Dashboard Design** → [`DASHBOARD_DESIGN.md`](./DASHBOARD_DESIGN.md)
   - Understand the 7-sheet layout (KPI tiles, bar charts, bullet charts, trend lines, heatmaps, scatter plots)
   - See how LOD expressions power each visualization

2. **Load the Calculated Fields** → [`CALCULATED_FIELDS.md`](./CALCULATED_FIELDS.md)
   - 40 ready-to-use Tableau calculated fields
   - Organized by LOD type: FIXED, INCLUDE, EXCLUDE, and Bare LOD
   - Covers Customer-level, Category-level, Region-level, and Channel-level analytics

3. **Set Up the Data** → [`SAMPLE_DATA.md`](./SAMPLE_DATA.md)
   - Star schema with 5 tables (DimStore, DimCustomer, DimProduct, FactSales, FactMarketing, FactTargets)
   - Sample rows and SQL generation scripts

---

## 🧩 LOD Expressions Used (14 Unique Expressions)

| Type         | Count | Purpose                                                             |
| ------------ | ----- | ------------------------------------------------------------------- |
| **FIXED**    | 9     | Customer metrics, category targets, channel CAC, product benchmarks |
| **EXCLUDE**  | 3     | Regional subtotals, overall benchmarks, store comparisons           |
| **INCLUDE**  | 2     | Per-customer averages, per-order basket analysis                    |
| **Bare LOD** | 2     | Grand total, overall profit margin                                  |

---

## 🎯 Key Dashboard Features

- **KPI Tiles** — Total Sales, Avg Revenue Per Customer, CAC, Active Customers
- **Sales vs Target** — Bullet charts with FIXED LOD for monthly targets
- **Customer Deep-Dive** — CLV, tenure, recency, high-value flags
- **Profit Heatmap** — Store-by-Region with EXCLUDE LOD for regional benchmarks
- **Product Scatter** — Sub-category performance vs category average
- **Interactive Filters** — Context Filter strategy for FIXED LODs
- **Dynamic Parameters** — Top N customers, benchmark switching

---

## 📊 Business Questions Answered

| Question                                                 | LOD Expression Used                                                                     |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| What's the true average revenue per customer?            | `{ FIXED [Customer ID] : SUM([Sales]) }`                                                |
| How much does it cost to acquire a customer per channel? | `{ FIXED [Channel] : SUM([Spend]) } / { FIXED [Channel] : COUNTD([Customer ID]) }`      |
| Are we hitting monthly targets by category?              | `SUM([Sales]) / { FIXED [Category], DATETRUNC('month', [Order Date]) : SUM([Target]) }` |
| Which stores are above/below their region average?       | `SUM([Profit]) - { EXCLUDE [Store Name] : AVG([Profit]) }`                              |
| Who are our top 10% high-value customers?                | `{ FIXED [Customer ID] : SUM([Sales]) } > 5000`                                         |
| How does each month compare to the overall average?      | `{ EXCLUDE [Order Date] : AVG([Sales]) }`                                               |
| What's the average basket size by category?              | `{ INCLUDE [Order ID] : COUNTD([Product ID]) }`                                         |

---

## 📚 LOD Types Covered

```
┌─────────────────────────────────────────────────────────────┐
│                      LOD EXPRESSIONS                        │
├──────────────┬──────────────────────────────────────────────┤
│  🔒 FIXED    │ "{ FIXED [Dim] : AGG(Measure) }"             │
│              │ Ignores view dimensions. Perfect for:         │
│              │ • Per-customer metrics                        │
│              │ • Category/region targets                     │
│              │ • Channel-level CAC                           │
├──────────────┼──────────────────────────────────────────────┤
│  ➕ INCLUDE  │ "{ INCLUDE [Dim] : AGG(Measure) }"           │
│              │ Adds dimensions to view level. Perfect for:   │
│              │ • Per-customer avg at region level            │
│              │ • Per-order basket size at category level     │
├──────────────┼──────────────────────────────────────────────┤
│  ➖ EXCLUDE  │ "{ EXCLUDE [Dim] : AGG(Measure) }"           │
│              │ Removes dimensions from view. Perfect for:    │
│              │ • Regional subtotals within store view        │
│              │ • Overall benchmarks in trend charts          │
├──────────────┼──────────────────────────────────────────────┤
│  📦 BARE     │ "{ AGG(Measure) }"                            │
│              │ Single global value. Perfect for:             │
│              │ • % of grand total                            │
│              │ • Overall profit margin                       │
└──────────────┴──────────────────────────────────────────────┘
```

---

## ▶️ Next Steps

1. Open the **[Dashboard Design](./DASHBOARD_DESIGN.md)** for the full layout and interactivity details
2. Copy the **[Calculated Fields](./CALCULATED_FIELDS.md)** into your Tableau workbook
3. Use the **[Sample Data](./SAMPLE_DATA.md)** schema to populate your data source
4. Build the 7 sheets and assemble into the executive dashboard

---

_This implementation was built for **OmniCorp Retail**, a fictional company. All data and scenarios are for educational purposes to demonstrate LOD expression usage in Tableau._
