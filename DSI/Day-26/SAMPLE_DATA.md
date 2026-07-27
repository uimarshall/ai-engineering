# Sample Data Schema — OmniCorp Retail Dashboard

This document defines the sample data tables used for the OmniCorp Retail Dashboard. You can use this schema to generate mock data in Tableau or load into a database.

---

## Table: `DimStore` (Store Dimension)

| Column          | Type         | Description             | Sample Values                        |
| --------------- | ------------ | ----------------------- | ------------------------------------ |
| `Store ID`      | Integer (PK) | Unique store identifier | 1, 2, 3, ...                         |
| `Store Name`    | String       | Store display name      | "OmniCorp Downtown", "OmniCorp Mall" |
| `Region`        | String       | Geographic region       | "East", "West", "Central", "South"   |
| `Store Manager` | String       | Manager's full name     | "Alice Johnson", "Bob Smith"         |
| `Open Date`     | Date         | When the store opened   | 2019-01-15                           |
| `Square Feet`   | Integer      | Store size in sq ft     | 12000                                |

### Sample Rows (15 stores)

| Store ID | Store Name        | Region  | Store Manager | Open Date  | Square Feet |
| -------- | ----------------- | ------- | ------------- | ---------- | ----------- |
| 1        | OmniCorp Downtown | East    | Alice Johnson | 2019-01-15 | 15000       |
| 2        | OmniCorp Mall     | East    | Bob Smith     | 2019-03-20 | 22000       |
| 3        | OmniCorp Airport  | West    | Carol Davis   | 2020-06-01 | 8000        |
| 4        | OmniCorp Plaza    | West    | David Wilson  | 2019-11-15 | 18000       |
| 5        | OmniCorp Square   | Central | Eve Martinez  | 2020-02-28 | 14000       |
| 6        | OmniCorp Heights  | Central | Frank Thomas  | 2021-07-10 | 10000       |
| 7        | OmniCorp Harbor   | South   | Grace Lee     | 2019-09-05 | 16000       |
| 8        | OmniCorp Crossing | South   | Henry Brown   | 2020-04-12 | 20000       |
| 9        | OmniCorp Metro    | East    | Irene Kim     | 2021-01-20 | 12000       |
| 10       | OmniCorp Valley   | West    | Jack White    | 2022-03-15 | 9000        |
| 11       | OmniCorp Ridge    | Central | Karen Chen    | 2022-08-01 | 7500        |
| 12       | OmniCorp Coast    | South   | Leo Garcia    | 2021-05-30 | 13000       |
| 13       | OmniCorp North    | East    | Maria Lopez   | 2023-02-14 | 11000       |
| 14       | OmniCorp Park     | West    | Nathan Adams  | 2023-06-20 | 9500        |
| 15       | OmniCorp Springs  | Central | Olivia Taylor | 2023-09-01 | 8500        |

---

## Table: `DimCustomer` (Customer Dimension)

| Column             | Type        | Description                      | Sample Values                                           |
| ------------------ | ----------- | -------------------------------- | ------------------------------------------------------- |
| `Customer ID`      | String (PK) | Unique customer identifier       | "CUST-0001"                                             |
| `Customer Name`    | String      | Customer's full name             | "John Doe"                                              |
| `Segment`          | String      | Customer segment                 | "Consumer", "Corporate", "Home Office"                  |
| `Channel`          | String      | Acquisition channel              | "Organic Search", "Paid Ad", "Referral", "Social Media" |
| `Acquisition Date` | Date        | When customer was first acquired | 2023-01-10                                              |
| `Customer Tier`    | String      | Loyalty tier                     | "Bronze", "Silver", "Gold", "Platinum"                  |
| `City`             | String      | Customer's city                  | "New York", "Los Angeles"                               |
| `State`            | String      | Customer's state                 | "NY", "CA"                                              |
| `Postal Code`      | String      | ZIP code                         | "10001"                                                 |

### Sample Rows (50 customers)

| Customer ID | Customer Name   | Segment     | Channel        | Acquisition Date | Tier     | City         | State |
| ----------- | --------------- | ----------- | -------------- | ---------------- | -------- | ------------ | ----- |
| CUST-0001   | John Doe        | Corporate   | Referral       | 2023-01-10       | Gold     | New York     | NY    |
| CUST-0002   | Jane Smith      | Consumer    | Organic Search | 2023-01-15       | Silver   | Los Angeles  | CA    |
| CUST-0003   | Robert Johnson  | Corporate   | Paid Ad        | 2023-02-01       | Platinum | Chicago      | IL    |
| CUST-0004   | Emily Davis     | Home Office | Social Media   | 2023-02-10       | Bronze   | Houston      | TX    |
| CUST-0005   | Michael Wilson  | Consumer    | Referral       | 2023-03-05       | Gold     | Phoenix      | AZ    |
| CUST-0006   | Sarah Brown     | Corporate   | Organic Search | 2023-03-12       | Silver   | Philadelphia | PA    |
| CUST-0007   | James Martinez  | Home Office | Paid Ad        | 2023-04-01       | Bronze   | San Antonio  | TX    |
| CUST-0008   | Jennifer Garcia | Consumer    | Social Media   | 2023-04-18       | Gold     | San Diego    | CA    |
| CUST-0009   | David Miller    | Corporate   | Referral       | 2023-05-02       | Platinum | Dallas       | TX    |
| CUST-0010   | Lisa Anderson   | Consumer    | Organic Search | 2023-05-20       | Silver   | San Jose     | CA    |

_(... 40 more customers following the same pattern)_

---

## Table: `DimProduct` (Product Dimension)

| Column         | Type        | Description               | Sample Values                                |
| -------------- | ----------- | ------------------------- | -------------------------------------------- |
| `Product ID`   | String (PK) | Unique product identifier | "PROD-FURN-001"                              |
| `Product Name` | String      | Product display name      | "Executive Desk", "Ergonomic Chair"          |
| `Category`     | String      | High-level category       | "Furniture", "Office Supplies", "Technology" |
| `Sub-Category` | String      | Mid-level category        | "Chairs", "Tables", "Phones", "Storage"      |
| `Unit Cost`    | Decimal     | Cost per unit             | 45.00                                        |
| `Unit Price`   | Decimal     | Selling price per unit    | 89.99                                        |
| `Supplier`     | String      | Supplier name             | "FurniPro", "TechWorld"                      |

### Sample Rows (30 products)

| Product ID    | Product Name         | Category        | Sub-Category | Unit Cost | Unit Price | Supplier     |
| ------------- | -------------------- | --------------- | ------------ | --------- | ---------- | ------------ |
| PROD-FURN-001 | Executive Desk       | Furniture       | Tables       | 350.00    | 699.99     | FurniPro     |
| PROD-FURN-002 | Ergonomic Chair      | Furniture       | Chairs       | 180.00    | 399.99     | ComfortPlus  |
| PROD-FURN-003 | Bookshelf 5-Tier     | Furniture       | Bookcases    | 90.00     | 199.99     | WoodCraft    |
| PROD-FURN-004 | Filing Cabinet       | Furniture       | Storage      | 65.00     | 149.99     | FurniPro     |
| PROD-FURN-005 | Conference Table     | Furniture       | Tables       | 520.00    | 999.99     | OfficeElite  |
| PROD-OFFS-001 | Stapler Set          | Office Supplies | Supplies     | 3.50      | 12.99      | OfficeBasics |
| PROD-OFFS-002 | Printer Paper (10pk) | Office Supplies | Paper        | 25.00     | 49.99      | PaperPro     |
| PROD-OFFS-003 | Binder Clips Set     | Office Supplies | Supplies     | 2.00      | 7.99       | OfficeBasics |
| PROD-OFFS-004 | Desk Organizer       | Office Supplies | Storage      | 15.00     | 34.99      | OrganizeIt   |
| PROD-OFFS-005 | Label Maker          | Office Supplies | Appliances   | 28.00     | 59.99      | TechWorld    |
| PROD-TECH-001 | USB-C Hub            | Technology      | Accessories  | 22.00     | 49.99      | TechWorld    |
| PROD-TECH-002 | Wireless Mouse       | Technology      | Accessories  | 18.00     | 39.99      | TechWorld    |
| PROD-TECH-003 | 27" Monitor          | Technology      | Phones       | 200.00    | 449.99     | DisplayPro   |
| PROD-TECH-004 | Mechanical Keyboard  | Technology      | Accessories  | 55.00     | 129.99     | TechWorld    |
| PROD-TECH-005 | Webcam 4K            | Technology      | Accessories  | 45.00     | 99.99      | VisualTech   |

_(... 15 more products following the same pattern)_

---

## Table: `FactSales` (Sales Fact Table)

| Column          | Type         | Description                                   |
| --------------- | ------------ | --------------------------------------------- |
| `Order ID`      | String (PK)  | Unique order identifier (e.g., "ORD-2024001") |
| `Order Date`    | Date         | Date the order was placed                     |
| `Ship Date`     | Date         | Date the order was shipped                    |
| `Ship Mode`     | String       | "Standard", "Express", "Overnight"            |
| `Customer ID`   | String (FK)  | References `DimCustomer`                      |
| `Store ID`      | Integer (FK) | References `DimStore`                         |
| `Product ID`    | String (FK)  | References `DimProduct`                       |
| `Sales`         | Decimal      | Revenue from this line item                   |
| `Quantity`      | Integer      | Number of units ordered                       |
| `Discount`      | Decimal      | Discount applied (0.00 - 0.80)                |
| `Profit`        | Decimal      | Profit from this line item (Sales - Cost)     |
| `Shipping Cost` | Decimal      | Cost to ship                                  |

### SQL to Generate Mock Sales Data (for reference)

```sql
-- Generate 5000+ sales transactions spanning 2023-2024
-- You can use this with a data generator or Tableau's data simulation

WITH date_series AS (
  SELECT
    DATEADD('day', seq, '2023-01-01') AS order_date
  FROM (
    SELECT ROW_NUMBER() OVER (ORDER BY 1) - 1 AS seq
    FROM information_schema.columns
    LIMIT 730
  )
)
SELECT
  'ORD-' || CAST(seq AS STRING) AS order_id,
  order_date,
  DATEADD('day', CAST(RANDOM() * 5 AS INT), order_date) AS ship_date,
  CASE CAST(RANDOM() * 3 AS INT)
    WHEN 0 THEN 'Standard'
    WHEN 1 THEN 'Express'
    WHEN 2 THEN 'Overnight'
  END AS ship_mode,
  'CUST-' || LPAD(CAST(RANDOM() * 49 + 1 AS STRING), 4, '0') AS customer_id,
  CAST(RANDOM() * 14 + 1 AS INT) AS store_id,
  'PROD-' || CASE CAST(RANDOM() * 2 AS INT)
    WHEN 0 THEN 'FURN-'
    WHEN 1 THEN 'OFFS-'
    WHEN 2 THEN 'TECH-'
  END || LPAD(CAST(RANDOM() * 4 + 1 AS STRING), 3, '0') AS product_id,
  ROUND(CAST(RANDOM() * 500 + 10 AS DECIMAL), 2) AS sales,
  CAST(RANDOM() * 10 + 1 AS INT) AS quantity,
  ROUND(CAST(RANDOM() * 0.6 AS DECIMAL), 2) AS discount,
  ROUND(CAST(RANDOM() * 100 - 20 AS DECIMAL), 2) AS profit,
  ROUND(CAST(RANDOM() * 30 + 5 AS DECIMAL), 2) AS shipping_cost
FROM date_series;
```

---

## Table: `FactMarketing` (Marketing Fact Table)

| Column        | Type    | Description                    |
| ------------- | ------- | ------------------------------ |
| `Channel`     | String  | Marketing channel              |
| `Campaign`    | String  | Campaign name                  |
| `Date`        | Date    | Date of the marketing activity |
| `Impressions` | Integer | Number of impressions          |
| `Clicks`      | Integer | Number of clicks               |
| `Spend`       | Decimal | Marketing spend in USD         |
| `Conversions` | Integer | Number of conversions          |

### Sample Rows

| Channel        | Campaign           | Date       | Impressions | Clicks | Spend   | Conversions |
| -------------- | ------------------ | ---------- | ----------- | ------ | ------- | ----------- |
| Organic Search | SEO Q1 2024        | 2024-01-01 | 45000       | 2300   | 0.00    | 45          |
| Paid Ad        | Google Ads - Brand | 2024-01-01 | 25000       | 1200   | 3500.00 | 28          |
| Social Media   | LinkedIn Campaign  | 2024-01-01 | 15000       | 450    | 1200.00 | 12          |
| Referral       | Partner Program    | 2024-01-01 | 0           | 0      | 500.00  | 8           |
| Organic Search | SEO Q1 2024        | 2024-01-02 | 42000       | 2100   | 0.00    | 38          |
| Paid Ad        | Google Ads - Brand | 2024-01-02 | 23500       | 1150   | 3400.00 | 25          |
| Social Media   | LinkedIn Campaign  | 2024-01-02 | 14200       | 420    | 1150.00 | 10          |
| Referral       | Partner Program    | 2024-01-02 | 0           | 0      | 480.00  | 6           |

---

## Table: `FactTargets` (Monthly Targets)

| Column            | Type    | Description                     |
| ----------------- | ------- | ------------------------------- |
| `Year`            | Integer | Target year                     |
| `Month`           | Integer | Target month (1-12)             |
| `Category`        | String  | Product category                |
| `Region`          | String  | Geographic region               |
| `Sales Target`    | Decimal | Monthly sales target            |
| `Profit Target`   | Decimal | Monthly profit target           |
| `Customer Target` | Integer | New customer acquisition target |

### Sample Rows

| Year | Month | Category        | Region  | Sales Target | Profit Target | Customer Target |
| ---- | ----- | --------------- | ------- | ------------ | ------------- | --------------- |
| 2024 | 1     | Furniture       | East    | 150000.00    | 30000.00      | 50              |
| 2024 | 1     | Furniture       | West    | 120000.00    | 24000.00      | 40              |
| 2024 | 1     | Furniture       | Central | 90000.00     | 18000.00      | 30              |
| 2024 | 1     | Furniture       | South   | 110000.00    | 22000.00      | 35              |
| 2024 | 1     | Office Supplies | East    | 130000.00    | 26000.00      | 55              |
| 2024 | 1     | Office Supplies | West    | 100000.00    | 20000.00      | 40              |
| 2024 | 1     | Office Supplies | Central | 80000.00     | 16000.00      | 30              |
| 2024 | 1     | Office Supplies | South   | 95000.00     | 19000.00      | 35              |
| 2024 | 1     | Technology      | East    | 180000.00    | 36000.00      | 45              |
| 2024 | 1     | Technology      | West    | 150000.00    | 30000.00      | 35              |
| 2024 | 1     | Technology      | Central | 110000.00    | 22000.00      | 25              |
| 2024 | 1     | Technology      | South   | 140000.00    | 28000.00      | 30              |

_(... repeat for months 2-12 for each year 2023-2024)_

---

## Using This Data in Tableau

### Option 1: Connect to a Database

1. Create the tables in PostgreSQL, MySQL, or SQL Server
2. Load the sample data
3. Connect Tableau to the database
4. Create relationships between tables (star schema)

### Option 2: Use Tableau Data Simulation

1. In Tableau Prep or Tableau Desktop, use the "Data Source" tab
2. Create a text file with sample data and connect via "Text File" connector
3. Define relationships manually

### Option 3: Excel/CSV Files

1. Create separate Excel files for each table
2. Connect Tableau to each file
3. Use Tableau's relationship model to join them

---

## Data Quality Notes

- **Sales** should be positive values ($10 - $5,000 per line item)
- **Profit** can be negative (discounted/returned items) to simulate real-world data
- **Discount** ranges from 0% to 80%
- **Quantity** ranges from 1 to 10 units per line
- **Customer IDs** have 1-to-many relationship with orders (repeat customers)
- **Store IDs** have 1-to-many relationship within each region (multiple stores per region)
