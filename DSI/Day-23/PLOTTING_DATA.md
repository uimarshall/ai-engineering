# How Data is Plotted in Tableau & The Role of "Marks"

## How Data is Plotted in Tableau

In Tableau, data is plotted using a simple but powerful mental formula:

```
Dimension(s) + Measure(s) + Marks = Chart
```

### The Core Workflow for Plotting Data

1. **Connect to a data source** (Excel, CSV, SQL database, cloud data)
2. **Drag a Dimension** (categorical field like Region, Category, Month) to **Columns** or **Rows** — this defines how data is sliced/grouped
3. **Drag a Measure** (numeric field like Sales, Profit, Quantity) to **Columns** or **Rows** — this defines what is being aggregated
4. **Select a Mark Type** on the Marks card — this defines how the data appears visually (bar, line, circle, etc.)
5. **Enhance with Marks properties** — drag fields to Color, Size, Label, Detail, or Tooltip on the Marks card

### Example: Building a Bar Chart

| Step | Action                                     | Result                                                  |
| ---- | ------------------------------------------ | ------------------------------------------------------- |
| 1    | Drag **Category** to Columns               | Groups data into Furniture, Office Supplies, Technology |
| 2    | Drag **Sales** to Rows                     | Tableau computes `SUM(Sales)` for each category         |
| 3    | Marks card auto-selects **Bar**            | A bar chart appears                                     |
| 4    | Drag **Profit** to **Color** on Marks card | Bars are colored green/red by profitability             |

Tableau automatically aggregates Measures (default is `SUM`), and Dimensions slice the data into discrete groups. The combination creates the view.

---

## The Role of "Marks" in Tableau

**Marks** control **how each individual data point is visually represented** on the chart. They are the visual encoding layer of your visualization.

### Mark Types (the "shape" of data points)

| Mark Type          | Best Used For                | Example                            |
| ------------------ | ---------------------------- | ---------------------------------- |
| **Bar**            | Comparing categorical values | Sales by Region                    |
| **Line**           | Trends over time             | Monthly Sales Trend                |
| **Circle / Point** | Scatter plots, correlations  | Sales vs Profit scatter plot       |
| **Square**         | Density or heatmaps          | Population density                 |
| **Shape**          | Custom icons per category    | Map markers by store type          |
| **Text**           | Table / heatmap with values  | Sales table by Category and Region |
| **Map**            | Geographic data              | Sales by State on a map            |
| **Area**           | Volume over time             | Cumulative sales over months       |
| **Pie**            | Proportions (use sparingly)  | Market share by product            |

### The Marks Card Properties

When you select a mark type, the **Marks card** gives you these encoding channels:

| Property    | What It Does                           | Example Use                                        |
| ----------- | -------------------------------------- | -------------------------------------------------- |
| **Color**   | Encodes values as colors               | Make negative Profit bars red, positive green      |
| **Size**    | Encodes values as varying sizes        | Larger circles = higher sales                      |
| **Label**   | Displays values or text on marks       | Show exact Sales number on each bar                |
| **Detail**  | Adds granularity without visual change | Add Customer ID to Detail for precise tooltip data |
| **Tooltip** | Controls hover-over text               | Show Product, Sales, and Profit on hover           |

### Why Marks Matter

- **Color** helps you spot patterns instantly (e.g., profitable vs unprofitable regions)
- **Size** helps compare magnitude at a glance (e.g., bigger dots = more orders)
- **Label** makes exact values readable without guessing
- **Changing the mark type** can completely change the story the data tells (e.g., a line chart shows trends, a bar chart shows comparisons)

### Common Beginner Mistake

Forgetting that you can drag fields to multiple Marks card properties simultaneously. For example, in a scatter plot you can have:

- X-axis = `SUM(Sales)`
- Y-axis = `SUM(Profit)`
- **Color** = Category (to distinguish product types)
- **Size** = Quantity (to show order volume)
- **Label** = Product Name (to identify top performers)

All of this is driven by the Marks card.

### Quick Analogy

Think of Marks like this:

- **Mark Type** = the _type of paintbrush_ you choose (bar, line, dot)
- **Color / Size / Label** = the _colors, brush thickness, and labels_ you apply with that brush

The data (Dimensions + Measures) tells Tableau _where_ to draw — **Marks tell it _how_ to draw**.
