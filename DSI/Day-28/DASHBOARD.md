# The Concept of Dashboard in Tableau

## Table of Contents

1. [Introduction to Tableau Dashboards](#1-introduction-to-tableau-dashboards)
2. [Dashboard Components & Widgets](#2-dashboard-components--widgets)
3. [Dashboard Layout & Functionalities](#3-dashboard-layout--functionalities)
4. [Dashboard Interactivity](#4-dashboard-interactivity)
5. [Dashboard Design Best Practices](#5-dashboard-design-best-practices)
6. [Client Project Case Study — OmniCorp Retail Dashboard](#6-client-project-case-study--omnicorp-retail-dashboard)
7. [Summary & Cheat Sheet](#7-summary--cheat-sheet)

---

## 1. Introduction to Tableau Dashboards

### What is a Dashboard in Tableau?

A **dashboard** in Tableau is a **single-page, interactive visual display** that combines multiple worksheets, views, objects, and controls into one cohesive interface. It serves as a "single pane of glass" for decision-makers to monitor key metrics, explore trends, and derive actionable insights — all without flipping between tabs.

```
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTIVE DASHBOARD                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────────┐  │
│  │ Total   │  │ Avg Rev │  │ CAC     │  │ Active      │  │
│  │ Sales   │  │ /Cust   │  │ $124.50 │  │ Customers   │  │
│  │ $5.2M   │  │ $2,450  │  │         │  │ 2,150       │  │
│  └─────────┘  └─────────┘  └─────────┘  └──────────────┘  │
├───────────────────────┬─────────────────────────────────────┤
│                       │                                     │
│  Sales by Category    │  Sales vs Target (%)                │
│  (Bar Chart)          │  (Bullet Chart)                     │
│                       │                                     │
├───────────────────────┼─────────────────────────────────────┤
│                       │                                     │
│  Monthly Trend        │  Top 5 Customers                   │
│  (Line Chart)         │  (Table)                           │
│                       │                                     │
├───────────────────────┴─────────────────────────────────────┤
│  [Region: ▼ All]  [Category: ▼ All]  [Date Range: ▼]       │
└─────────────────────────────────────────────────────────────┘
```

### Why Use Dashboards?

| Problem Without Dashboards                          | Solution With Dashboards                                                 |
| --------------------------------------------------- | ------------------------------------------------------------------------ |
| Users flip through 10+ tabs to get the full picture | All relevant views are on ONE page                                       |
| No connection between charts                        | Dashboard actions link charts together (click a bar → filter everything) |
| Static reports need re-running                      | Live/connected data refreshes automatically                              |
| Hard to spot correlations side-by-side              | Side-by-side layout reveals patterns instantly                           |
| Decision-making is slow                             | Interactive filters let users explore their own questions                |

### Dashboard vs Worksheet — Key Differences

| Feature        | Worksheet                             | Dashboard                                                 |
| -------------- | ------------------------------------- | --------------------------------------------------------- |
| Scope          | Single chart/graph/table              | Multiple sheets + objects combined                        |
| Interactivity  | Filters within one view               | Cross-sheet filter/highlight/URL actions                  |
| Layout         | Auto-generated (Columns/Rows shelves) | Manual layout (tiled or floating)                         |
| Objects        | Charts only                           | Charts + text + images + web pages + containers + buttons |
| Device Support | Single resolution                     | Device preview for desktop/tablet/phone                   |

---

## 2. Dashboard Components & Widgets

Tableau provides a rich set of **dashboard objects** (widgets) that go beyond just worksheets. These are found in the left sidebar under the **Dashboard** tab → **Objects** pane.

### 2.1 Sheets (Worksheets)

The primary building block. Each sheet is a chart, table, or map you created in a worksheet tab.

**Types of sheets you can add:**

| Sheet Type      | Example Use                |
| --------------- | -------------------------- |
| Bar Chart       | Sales by Category          |
| Line Chart      | Monthly Revenue Trend      |
| Scatter Plot    | Sales vs Profit by Product |
| Heatmap         | Profit by Region & Store   |
| Text Table      | Top 10 Customers           |
| Highlight Table | Product Performance Matrix |
| Map             | Sales by State             |
| Pie Chart       | Market Share by Segment    |
| Bullet Chart    | Actual vs Target           |
| Gantt Chart     | Project Timelines          |

> **Note:** Any worksheet you create becomes available to add to the dashboard. You can also **duplicate** sheets for reuse with different filters.

### 2.2 Horizontal & Vertical Containers

**Layout Containers** are the most important layout tool in Tableau dashboards. They automatically resize and reorganize their contents when the dashboard is resized.

#### Horizontal Container

Arranges its children **side-by-side** (left to right).

```
┌─────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Sheet A  │  │ Sheet B  │  │   Sheet C    │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
│  ←─────── Horizontal Container ───────────────→ │
└─────────────────────────────────────────────────┘
```

**Use when:** You want charts to sit next to each other and auto-resize width.

#### Vertical Container

Arranges its children **top-to-bottom** (stacked vertically).

```
┌─────────────────────────────────┐
│  ┌──────────────────────────┐  │
│  │       Sheet A            │  │
│  └──────────────────────────┘  │
│  ┌──────────────────────────┐  │
│  │       Sheet B            │  │
│  └──────────────────────────┘  │
│           ↑                    │
│     Vertical Container         │
└─────────────────────────────────┘
```

**Use when:** You want stacked sections that auto-resize height.

#### Nesting Containers

The real power comes from **nesting** containers inside each other:

```
┌──────────────────────────────────────────────┐
│       Vertical Container (Master)            │
│  ┌────────────────────────────────────────┐  │
│  │  Header: Horizontal Container          │  │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │  │
│  │  │ KPI  │ │ KPI  │ │ KPI  │ │ KPI  │  │  │
│  │  │  1   │ │  2   │ │  3   │ │  4   │  │  │
│  │  └──────┘ └──────┘ └──────┘ └──────┘  │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │  Body: Horizontal Container            │  │
│  │  ┌─────────────┐ ┌──────────────────┐  │  │
│  │  │  Chart Left │ │    Chart Right   │  │  │
│  │  └─────────────┘ └──────────────────┘  │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │  Footer: Filters Container            │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

### 2.3 Text Object

Used to add titles, headings, labels, instructions, or annotations.

**Common uses:**

- Dashboard title
- KPI value labels
- Section headings
- Data source disclaimer
- Instructions for users ("Click a bar to filter")

**Tip:** Use HTML formatting within text objects for bold, italic, bullet points, and colored text.

### 2.4 Image Object

Add logos, icons, branding elements, or visual separators.

**Supported formats:** PNG, JPG, GIF, BMP

**Common uses:**

- Company logo in the header
- Brand icons (e.g., social media icons)
- Background design elements
- Arrow or divider graphics

### 2.5 Blank Object

An invisible, transparent spacer used to add **whitespace** or padding between elements.

**Why use it:** Good dashboard design requires breathing room. A blank object gives you pixel-level control over spacing that containers alone cannot provide.

### 2.6 Web Page Object

Embed an external website or web application **inside** your Tableau dashboard.

**Common uses:**

- Embedded CRM or ERP system
- Google Maps / Bing Maps
- Company intranet page
- Live news or stock ticker
- Embedded video tutorial

> **Important:** Web Page objects use iframes. Some websites block iframe embedding. Test your URL first.

### 2.7 Extension Object (Dashboard Extensions)

Extensions are **custom-built web applications** that run inside Tableau dashboards. They extend Tableau's native capabilities.

**Examples of what extensions can do:**

- Custom visualizations (e.g., Sankey diagrams, network graphs)
- Advanced text editing (rich text in tooltips/titles)
- Power BI-style slicers
- Custom parameter input widgets (sliders, date pickers)
- Real-time data feeds (e.g., live stock prices)
- Export to PDF/PPT with specific formatting

**How to get extensions:**

- Tableau Extension Gallery (built-in)
- Custom-built using the Tableau Extensions API (JavaScript + HTML)

### 2.8 Download Object (PDF/Image/Crosstab)

Add buttons that allow users to **export** the dashboard or specific views.

| Export Type | What It Does                             |
| ----------- | ---------------------------------------- |
| PDF         | Export entire dashboard as printable PDF |
| Image       | Export as PNG image (current state)      |
| Crosstab    | Export underlying data as CSV            |
| PowerPoint  | Export sheets to PowerPoint slides       |

### 2.9 Navigation Object

Add buttons or links that navigate to **other dashboards, worksheets, or story points** within the same workbook.

**Use cases:**

- "Drill Down" button that takes you to a detailed dashboard
- Navigation menu with tabs for different departments
- Back/Forward buttons for story-based presentations

---

## 3. Dashboard Layout & Functionalities

### 3.1 Tiled vs Floating Layout

Every object on a dashboard can be placed in one of two modes:

| Layout Type  | Behavior                                                                       | Best For                                                       |
| ------------ | ------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| **Tiled**    | Objects snap to a grid and resize automatically to fill available space        | Responsive dashboards, consistent layouts across devices       |
| **Floating** | Objects can be placed anywhere with pixel-precision, overlapping other objects | Custom designs, logos on top of charts, fixed-position legends |

#### When to Use Tiled vs Floating

```
Tiled Layout:
┌─────────────────────┬─────────────────────┐
│  Chart A (tiled)    │  Chart B (tiled)    │
│                     │                     │
│  Auto-resizes       │  Auto-resizes       │
└─────────────────────┴─────────────────────┘
✓ Responsive across devices
✓ Easier to maintain
✓ Predictable behavior

Floating Layout:
┌─────────────────────────────────────────┐
│  Chart A (floating)                     │
│              ┌──────────────────────┐   │
│              │  Chart B (floating)  │   │
│              │  Overlapping chart   │   │
│              └──────────────────────┘   │
│  ┌──┐                                   │
│  │LO│  ← Logo floating on top           │
│  └──┘                                   │
└─────────────────────────────────────────┘
✗ May not resize well on different screens
✓ Maximum design flexibility
```

**Recommended approach:** Use **tiled** as default for most objects. Use **floating** only for:

- Logos and branding elements
- Custom legend placement
- Overlapping design effects
- Fixed-position filter buttons

### 3.2 Sizing Behavior

Each object has a **sizing behavior** setting that controls how it responds when the dashboard is resized.

| Option         | What It Does                                             |
| -------------- | -------------------------------------------------------- |
| **Fixed Size** | Object stays at exact pixel dimensions — no resizing     |
| **Range**      | Object has a min and max size; resizes within that range |
| **At Least**   | Object has a minimum size but can grow                   |
| **At Most**    | Object has a maximum size but can shrink                 |
| **Exactly**    | Object is exactly one size (same as Fixed)               |

**Container-level sizing:** When you set sizing behavior on a container, all its children are affected. This is the key to creating **responsive dashboards**.

### 3.3 Dashboard Size & Range Presets

Tableau offers preset dashboard sizes for common screen resolutions:

| Preset          | Resolution    | Aspect Ratio | Best For                  |
| --------------- | ------------- | ------------ | ------------------------- |
| Desktop         | 1000 x 800 px | ~5:4         | Standard monitors         |
| Desktop (Large) | 1200 x 900 px | 4:3          | Wide-screen monitors      |
| Laptop          | 1366 x 768 px | 16:9         | Laptop screens            |
| Tablet          | 800 x 600 px  | 4:3          | iPads and tablets         |
| Phone           | 360 x 640 px  | 9:16         | Mobile phones             |
| Custom          | User-defined  | Any          | Specific display hardware |

> **Pro Tip:** Use **Device Preview** (Dashboard → Device Preview) to test how your dashboard looks on desktop, tablet, and phone simultaneously. You can create **device-specific layouts** that show/hide elements per device type.

### 3.4 Show/Hide Buttons & Toggle Containers

A powerful feature for **progressive disclosure** — show details only when the user needs them.

**How it works:**

1. Create a **parameter** (boolean: Show/Hide)
2. Create a **calculated field** that references the parameter
3. Add a **Show/Hide button** on the dashboard
4. When clicked, the button toggles visibility of a container

**Use cases:**

- "Show Filters" toggle to reveal/hide a filter panel
- "Show Details" toggle to reveal a detailed table
- "Show Methodology" toggle for explanations
- Expandable/collapsible sections (like accordion menus)

### 3.5 Object Layering & Ordering

When using floating items, you can control which object appears on top:

- **Bring to Front** — Make an object visible above everything else
- **Send to Back** — Push an object behind others
- **Reorder** — Use the Item Hierarchy pane (lower-left in Dashboard view)

This is essential for floating overlays like logos, custom legends, and pop-up tooltip-like boxes.

---

## 4. Dashboard Interactivity

The true power of Tableau dashboards comes from **interactivity**. A static dashboard is just a report — an interactive dashboard is a **conversation with data**.

### 4.1 Filter Actions

**Filter Actions** let users click, select, or hover on a mark in one sheet to filter all other sheets on the dashboard.

```
User clicks "Technology" bar in "Sales by Category"

    ┌────────────────────┐
    │ Sales by Category  │
    │                    │
    │ ████████ Technology│──┐
    │ ██████  Office Supp│  │  Filter Action (Click)
    │ ████    Furniture  │  │
    └────────────────────┘  │
                            ▼
    ┌───────────────────────┬──────────────────────┐
    │ Monthly Trend         │ Top 5 Customers      │
    │ (Now shows Technology │ (Now shows only      │
    │  trend only)          │  Technology cust.)   │
    └───────────────────────┴──────────────────────┘
```

**Configuration:**

| Setting            | Options                                    |
| ------------------ | ------------------------------------------ |
| Source Sheet       | Which sheet triggers the action            |
| Target Sheets      | Which sheets get filtered (All / Selected) |
| Action Type        | Hover / Select / Menu                      |
| Clearing Selection | Show All / Exclude All                     |

**Use cases:**

- Click a category to drill down across all charts
- Click a region on a map to filter all related metrics
- Click a bar to see month-by-month breakdown
- Hover over a product to highlight it in related charts

### 4.2 Highlight Actions

**Highlight Actions** do not filter data — they **visually emphasize** matching marks across sheets while keeping all data visible.

```
User hovers over "Technology" in Sales by Category

    ┌────────────────────┐
    │ Sales by Category  │
    │                    │
    │ ████████ Technology│──┐
    │ ░░░░░░  Office     │  │  Highlight Action (Hover)
    │ ░░░░░░  Furniture  │  │
    └────────────────────┘  │
                            ▼
    ┌───────────────────────┬──────────────────────┐
    │ Monthly Trend         │ Top 5 Customers      │
    │ (Technology line is   │ (Technology customers │
    │  BOLD; others dim)    │  highlighted in blue) │
    └───────────────────────┴──────────────────────┘
```

**When to use Highlight instead of Filter:**

- When you want to show **context** (e.g., "Here's Technology, and here's how it compares to others")
- When filtering would remove too much data from view
- When comparing a selected item against the overall trend

### 4.3 URL Actions

**URL Actions** open a web page or external system when a user clicks a mark. This bridges Tableau dashboards with external applications.

**Common use cases:**

- Click a customer name → open CRM profile in Salesforce/Dynamics
- Click a product → open product detail page in e-commerce system
- Click an order ID → open the order in ERP system
- Click a location → open Google Maps with the address
- Click "View Report" → generate and download a PDF

**URL with dynamic parameters:**

```
https://crm.company.com/customer?id=<Customer ID>
https://maps.google.com/?q=<City>, <State>
https://analytics.example.com/report?date=<Order Date>&region=<Region>
```

> The angle brackets `< >` let you dynamically insert field values from the clicked mark into the URL.

### 4.4 Parameter Actions

**Parameter Actions** let users change parameter values by interacting with marks. This creates dynamic calculations based on user clicks.

**Example:** User clicks a month on a trend line, and all KPI tiles update to show values for that month.

```
User clicks "March" in Monthly Trend

  ┌───────────────────────────────────┐
  │  Monthly Trend (Line Chart)      │
  │              ╱╲                   │
  │  ╱╲        ╱  ╲   ●← Click      │
  │ ╱  ╲      ╱    ╲   March         │
  │╱    ╲────╱      ╲──────────      │
  │ Jan  Feb Mar Apr May Jun         │
  └───────────────────────────────────┘
                    │
                    ▼ Parameter Action
  ┌───────────────────────────────────┐
  │  KPI Tiles update to March values│
  │  ┌──────┐ ┌──────┐ ┌──────────┐  │
  │  │Sales │ │Profit│ │Customers │  │
  │  │$450K │ │$52K  │ │ 1,450    │  │
  │  └──────┘ └──────┘ └──────────┘  │
  └───────────────────────────────────┘
```

### 4.5 Set Actions

**Set Actions** allow users to select marks and add/remove them from a **set** (a subset of data). This is more powerful than filters because sets can be used in calculations.

**Example:** User clicks products to create a "High Potential Products" set, and a calculated field computes "Sales Outside Set vs Sales Inside Set" in real time.

**Use cases:**

- Compare selected products vs the rest
- Cohort analysis (select a group and track them over time)
- What-if analysis (select hypothetical scenarios)
- Competitive analysis (select competitor products)

### 4.6 Quick Filters

Quick Filters are filter controls **directly placed on the dashboard** (not triggered by clicks on marks).

**Types of quick filters:**

| Filter Type                | Best For                                       |
| -------------------------- | ---------------------------------------------- |
| Single Value (Dropdown)    | Selecting one item from a list                 |
| Multiple Values (Dropdown) | Selecting multiple items                       |
| Single Value (List)        | Small number of items, visible list            |
| Multiple Values (List)     | Visible checklist                              |
| Single Value (Slider)      | Numeric range with slider                      |
| Wildcard Match             | Search/filter by text pattern                  |
| Relative Date              | "Last 30 days", "This quarter", "Year to date" |

**Best practice:** Place all quick filters in a **filters bar** at the top or bottom of the dashboard for consistency.

### 4.7 Legends & Parameter Controls

**Legends:** Color, size, and shape legends from your worksheets can be added to the dashboard for end-user reference.

**Parameter Controls:** These show parameter input widgets (dropdown, slider, type-in) directly on the dashboard so users can control "what-if" scenarios.

```
┌──────────────────────────────────────────────────────────┐
│  [Region: ▼ All]  [Category: ▼ All]  [Date Range: ─────]│
│                                                          │
│  Color Legend:   Size Legend:    Parameter: Top N       │
│  ■ High Profit   ● Large Sales   [5 ▼]                  │
│  ■ Medium        ● Medium                               │
│  ■ Low Profit    ● Small                                │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Dashboard Design Best Practices

### 5.1 Visual Hierarchy

Organize your dashboard so the **most important information** catches the eye first.

```
Visual Hierarchy Flow (Top-left to Bottom-right):

                    ┌─────────────────────────────┐
                    │  KPI TILES (Most Important) │ ← Largest, most prominent
                    │  Total Sales  Profit  CAC   │
                    └─────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │  Overview Charts              │
                    │  (Bar, Bullet, Trend)         │ ← Medium importance
                    └───────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │  Detail Tables / Scatter     │ ← Supporting detail
                    └───────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │  Filters & Controls           │ ← Utility
                    └───────────────────────────────┘
```

**Size signals importance:**

- KPI tiles: 2–3x larger text than chart titles
- Chart titles: Bold, 14–16px
- Axis labels: Smaller, 10–12px

### 5.2 Layout Principles

| Principle                | Explanation                                                            |
| ------------------------ | ---------------------------------------------------------------------- |
| **F-Pattern**            | Users scan left-to-right, top-to-bottom. Place key metrics at top-left |
| **Golden Ratio**         | Consider a 60/40 split for main chart vs supporting chart              |
| **Grid Alignment**       | Align elements to an invisible grid for consistency                    |
| **Minimum 10px Padding** | Never let elements touch — whitespace improves readability             |
| **Consistent Margins**   | Use the same margin size throughout the dashboard                      |
| **Group Related Items**  | Place related charts next to each other (e.g., sales + profit)         |

### 5.3 Color Principles

| Do                                                      | Don't                                                      |
| ------------------------------------------------------- | ---------------------------------------------------------- |
| Use a **consistent color palette** (3–5 colors max)     | Use rainbow colors everywhere                              |
| Use **diverging colors** for good/bad (e.g., green/red) | Use red/green for non-categorical data (colorblind issues) |
| Use **sequential colors** for magnitude (light→dark)    | Overuse bright, saturated colors                           |
| Use **company brand colors** for client dashboards      | Use default Tableau 10 colors in production                |

**Color-blind safe palette:**

- Blue (safe for most color blindness)
- Orange (contrasts well with blue)
- Gray (neutral background)
- Avoid: Red/Green combined, Yellow on White

### 5.4 Dashboard Size & Screen Targets

**Always design for your user's screen:**

| Scenario                 | Target Size | Notes                              |
| ------------------------ | ----------- | ---------------------------------- |
| Executive on 27" monitor | 1600 x 900  | Lots of space, use it wisely       |
| Manager on 15" laptop    | 1366 x 768  | Most common — design for this      |
| Tablet (iPad)            | 1024 x 768  | Consider mobile layout             |
| Phone                    | 360 x 640   | Create separate phone layout       |
| TV / Wall Display        | 1920 x 1080 | Consider readability from distance |

> **Pro tip:** Use **Range** sizing with a minimum of 1000x768 and maximum of 1920x1080 to support most screens.

### 5.5 Performance Best Practices

| Optimization                                                      | Impact                 |
| ----------------------------------------------------------------- | ---------------------- |
| **Use data extracts** (.hyper) instead of live connections        | 3–10x faster           |
| **Limit number of filters** per dashboard (< 8)                   | Faster response        |
| **Reduce number of marks** — use Top N, aggregation, or sampling  | Faster rendering       |
| **Avoid LOD-in-LOD nesting** — pre-compute in calculated fields   | Faster queries         |
| **Minimize floating objects** — prefer tiled layout               | Smoother resizing      |
| **Use context filters** sparingly (each one triggers a new query) | Faster filtering       |
| **Hide unused fields** in the data source                         | Cleaner workbook       |
| **Limit dashboard sheets** to 10–15 max                           | Manageable performance |

### 5.6 Accessibility

- Ensure sufficient **color contrast** (text on background)
- Use **descriptive tooltips** that work without color
- Add **text labels** on charts (don't rely solely on color legends)
- Provide **keyboard navigation** where possible
- Use **clear, readable fonts** (Arial, Tableau Bold, not fancy script fonts)

---

## 6. Client Project Case Study — OmniCorp Retail Dashboard

### Client Background

**OmniCorp Retail** is a mid-size retail chain operating across 4 regions (East, West, Central, South) with 15 store locations. They sell products across 3 categories (Furniture, Office Supplies, Technology) with 17 sub-categories.

### Business Problem

OmniCorp's management needs a **single-pane-of-glass dashboard** that answers:

1. **Sales Performance:** How are we tracking against targets at Category, Region, and Store level?
2. **Customer Health:** What's our customer acquisition cost? Who are our high-value customers?
3. **Operational Efficiency:** What are our top/bottom performing products? Where are we losing money?
4. **Trend Analysis:** Are we growing month-over-month? What's our customer retention rate?

### Dashboard Structure & Widgets Used

```
┌──────────────────────────────────────────────────────────────────┐
│  HEADER ROW — Horizontal Container                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────────┐  │
│  │ KPI Tile │  │ KPI Tile │  │ KPI Tile │  │   KPI Tile     │  │
│  │TotalSales│  │Avg Rev/  │  │CAC (LOD) │  │ Active Cust.   │  │
│  │  $5.2M   │  │Customer  │  │ $124.50  │  │ (LOD)  2,150   │  │
│  │ Text Obj │  │  $2,450  │  │          │  │                │  │
│  └──────────┘  └──────────┘  └──────────┘  └────────────────┘  │
│                             (Text + Sheet with BAN/SC)           │
├──────────────────────────────────────────────────────────────────┤
│  BODY ROW — Horizontal Container                                 │
│  ┌─────────────────────────────┬───────────────────────────────┐ │
│  │  Sales by Category         │  Sales vs Target (%)          │ │
│  │  (Bar Chart - Sheet)       │  (Bullet Chart - Sheet)       │ │
│  │                             │                               │ │
│  │  [Furniture    ██████]     │  Furniture    ████████░░░ 85% │ │
│  │  [Office Supp  ███████]    │  Office Supp  █████████░ 92% │ │
│  │  [Technology   ████████]   │  Technology   ██████████ 101%│ │
│  └─────────────────────────────┴───────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│  BODY ROW 2 — Horizontal Container                               │
│  ┌─────────────────────────────┬───────────────────────────────┐ │
│  │  Monthly Sales Trend       │  Top 5 Customers              │ │
│  │  (Line Chart - Sheet)      │  (Table - Sheet)              │ │
│  │                             │                               │ │
│  │  ██  ██                     │  1. ABC Corp   $52,000       │ │
│  │    ██  ██  ██               │  2. XYZ Inc    $48,500       │ │
│  │      ██  ██                 │  3. ...                      │ │
│  └─────────────────────────────┴───────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│  BODY ROW 3 — Horizontal Container                               │
│  ┌─────────────────────────────┬───────────────────────────────┐ │
│  │  Profit by Region/Store    │  Product Performance          │ │
│  │  (Heatmap - Sheet)         │  (Scatter Plot - Sheet)       │ │
│  └─────────────────────────────┴───────────────────────────────┘ │
├──────────────────────────────────────────────────────────────────┤
│  FOOTER — Quick Filters & Controls (Horizontal Container)        │
│  [Region: ▼ All][Category: ▼ All][Date: ────────][Top N: 5 ▼]  │
└──────────────────────────────────────────────────────────────────┘
```

### Detailed Sheet Walkthrough

#### Sheet 1: KPI Tiles

| Widget     | Type                      | Description                                                                  |
| ---------- | ------------------------- | ---------------------------------------------------------------------------- |
| KPI Values | Sheet (Bar-in-Text / BAN) | 4 KPI tiles showing Total Sales, Avg Revenue/Customer, CAC, Active Customers |
| KPI Labels | Text Object               | "Total Sales", "CAC", etc. as headings above each tile                       |
| Spacers    | Blank Objects             | 10px gaps between KPI tiles for readability                                  |

**LOD usage:** `{ FIXED [Customer ID] : SUM([Sales]) }` for per-customer revenue, `{ FIXED [Channel] : COUNTD([Customer ID]) }` for CAC calculation.

#### Sheet 2: Sales by Category

| Widget       | Type                | Description                                     |
| ------------ | ------------------- | ----------------------------------------------- |
| Chart        | Bar Chart (Sheet)   | Horizontal bars showing SUM(Sales) per Category |
| Color Legend | Automatically added | Gradient coloring by sales amount               |
| Tooltip      | Enhanced with LOD   | Shows actual sales + % of total + % of target   |

#### Sheet 3: Sales vs Target (Bullet Chart)

| Widget         | Type                 | Description                                                              |
| -------------- | -------------------- | ------------------------------------------------------------------------ |
| Chart          | Bullet Chart (Sheet) | Shows actual sales as bar, target as reference line                      |
| Color          | Conditional          | Green if ≥ 100% of target, Yellow if 80–99%, Red if < 80%                |
| Reference Line | LOD calculated field | `{ FIXED [Category], DATETRUNC('month', [Order Date]) : SUM([Target]) }` |

#### Sheet 4: Monthly Sales Trend

| Widget    | Type                  | Description                                                                     |
| --------- | --------------------- | ------------------------------------------------------------------------------- |
| Chart     | Line Chart (Sheet)    | Continuous line showing sales over time                                         |
| Dual Axis | 2nd axis as reference | Overall average sales benchmark using `{ EXCLUDE [Order Date] : AVG([Sales]) }` |
| Tooltip   | MoM change            | Month-over-month percentage change (table calculation)                          |

#### Sheet 5: Top 5 Customers

| Widget    | Type               | Description                                                  |
| --------- | ------------------ | ------------------------------------------------------------ |
| Table     | Text Table (Sheet) | Customer Name, Total Sales, Orders, Avg Order Value, Tenure  |
| Ranking   | Top N filter       | Parameter-driven: user can switch between Top 5/10/15/20/All |
| Highlight | Conditional        | High-value customers (SUM > $5K) highlighted in green        |

**LOD usage:** `{ FIXED [Customer ID] : SUM([Sales]) }`, `{ FIXED [Customer ID] : COUNTD([Order ID]) }`, `{ FIXED [Customer ID] : MIN([Order Date]) }` for tenure.

#### Sheet 6: Profit by Region/Store (Heatmap)

| Widget       | Type            | Description                                         |
| ------------ | --------------- | --------------------------------------------------- |
| Chart        | Heatmap (Sheet) | Squares colored by Profit, sized by Sales           |
| Color Legend | Sequential      | Green (high profit) → Yellow → Red (loss)           |
| Detail       | Category        | Each square is broken down by Category within Store |

**LOD usage:** `{ EXCLUDE [Store Name] : AVG([Profit]) }` for store vs region comparison.

#### Sheet 7: Product Performance (Scatter Plot)

| Widget          | Type                        | Description                                                                        |
| --------------- | --------------------------- | ---------------------------------------------------------------------------------- |
| Chart           | Scatter Plot (Sheet)        | X = Sales, Y = Profit, Color = Discount %                                          |
| Reference Lines | Quadrants                   | Average sales line + average profit line (4 quadrants)                             |
| Tooltip         | Performance vs category avg | `(SUM([Profit])/SUM([Sales])) - { FIXED [Category] : SUM([Profit])/SUM([Sales]) }` |

### Dashboard Interactivity Setup

| Action Type          | Source                    | Target                          | Behavior                                                                         |
| -------------------- | ------------------------- | ------------------------------- | -------------------------------------------------------------------------------- |
| **Filter Action**    | Sales by Category (click) | All 7 sheets                    | Click a category → all charts filter to that category                            |
| **Filter Action**    | Profit Heatmap (click)    | Product Scatter + Top Customers | Click a store region → see related products & customers                          |
| **Highlight Action** | Product Scatter (hover)   | Profit Heatmap                  | Hover a sub-category → highlight across heatmap                                  |
| **URL Action**       | Top 5 Customers (click)   | External CRM                    | Click customer name → opens `https://crm.omnicorp.com/customer?id=<Customer ID>` |
| **Parameter Action** | Monthly Trend (click)     | KPI Tiles                       | Click a month → KPI tiles update to show that month's values                     |

### Quick Filters (Footer)

| Filter          | Type                 | Purpose                                  |
| --------------- | -------------------- | ---------------------------------------- |
| Region          | Dropdown (Single)    | Filter all sheets by region              |
| Category        | Dropdown (Single)    | Filter all sheets by category            |
| Date Range      | Slider (Range)       | Filter by date range                     |
| Top N Customers | Parameter (Dropdown) | Switch between Top 5/10/15/20/All        |
| High Value Only | Boolean/Custom       | Toggle to show only high-value customers |

### What the Client Gains

With this dashboard, OmniCorp's management can:

1. **Monitor real-time performance** — 4 KPI tiles refresh with live data
2. **Drill into any category** — Click "Technology" and see all related metrics
3. **Track target achievement** — Bullet charts show exactly where they're falling short
4. **Identify customer trends** — Top customers, tenure, acquisition cost
5. **Spot product issues** — Scatter plot reveals low-profit, high-sales products
6. **Make data-driven decisions** — All in one page, no tab switching

---

## 7. Summary & Cheat Sheet

### Dashboard Building Blocks

```
Dashboard = Layout Containers + Sheets + Objects + Interactivity

Layout Containers:  Horizontal  │  Vertical  │  Nesting
Sheets:             Bar  │  Line  │  Map  │  Table  │  Scatter  │  Heatmap
Objects:            Text  │  Image  │  Blank  │  Web  │  Download  │  Extension
Interactivity:      Filter  │  Highlight  │  URL  │  Parameter  │  Set Actions
Controls:           Quick Filters  │  Legends  │  Parameter Controls
```

### Quick Reference — When to Use Which Widget

| You Want To...               | Use This Widget      |
| ---------------------------- | -------------------- |
| Display a chart              | Sheet (worksheet)    |
| Arrange items side-by-side   | Horizontal Container |
| Stack items vertically       | Vertical Container   |
| Add a title or label         | Text Object          |
| Add a company logo           | Image Object         |
| Create spacing between items | Blank Object         |
| Embed a website              | Web Page Object      |
| Add custom functionality     | Extension Object     |
| Let users export data        | Download Object      |
| Navigate to another view     | Navigation Object    |

### Quick Reference — When to Use Which Action

| You Want Users To...                               | Use This Action  |
| -------------------------------------------------- | ---------------- |
| Click a chart → filter other charts                | Filter Action    |
| Hover → highlight matching data (keep all visible) | Highlight Action |
| Click a customer → open CRM                        | URL Action       |
| Click a data point → change a calculation          | Parameter Action |
| Select marks → create a subset for analysis        | Set Action       |

### Dashboard Design Checklist

- [ ] Dashboard addresses **one main business question**
- [ ] Most important KPI is at **top-left**
- [ ] Layout uses **containers** (not random floating items)
- [ ] **Color palette** is consistent (3–5 colors max)
- [ ] **Filters** are grouped in one area (top or bottom)
- [ ] **Tooltips** are informative, not just field names
- [ ] Dashboard works on **target device resolution**
- [ ] Performance is optimized (extracts, limited marks)
- [ ] **Whitespace** is used between elements (≥ 10px)
- [ ] **Data source** is clearly labeled
- [ ] **Navigation** is intuitive — user doesn't need training
- [ ] **Interactivity** is tested (all actions work correctly)

### Common Pitfalls to Avoid

| Pitfall               | Why It's Bad                       | Fix                                     |
| --------------------- | ---------------------------------- | --------------------------------------- |
| Too many sheets (15+) | Cluttered, slow, overwhelming      | Group into sub-dashboards or use tabs   |
| No whitespace         | Hard to read, looks unprofessional | Use Blank Objects + padding             |
| Rainbow colors        | Confusing, no visual hierarchy     | Limit palette to 3–5 brand colors       |
| Ignoring screen size  | Doesn't fit user's monitor         | Use Range sizing + Device Preview       |
| No interactivity      | Just a PDF in Tableau form         | Add filter/highlight actions            |
| Floating everything   | Resizing breaks layout             | Use Tiled + Containers as default       |
| Weak tooltips         | Users don't understand data        | Add meaningful descriptions to tooltips |

---

> **Key Takeaway:** A Tableau dashboard is not just a collection of charts — it is a **curated, interactive experience** that tells a data story, enables exploration, and drives decision-making. The best dashboards are simple, focused, and designed for the specific audience that will use them.
