# Fictional sample data

`sample_sales.csv` was authored for this repository on 2 November 2026 as a small, artificial example. It contains no customer information, real transactions or external source records. Values are illustrative units, not a documented currency.

This file makes the SQL/Python workflow executable. It is **not** the original database behind the historical totals and chart in the repository root, and was not reverse-engineered to match those totals.

| Column | Meaning |
| --- | --- |
| OrderID | Unique fictional order identifier |
| Category | Product category |
| Sales | Nonnegative illustrative sales amount |
| Profit | Illustrative profit amount |
| Region | Fictional grouping label |

Seven records total 800 units of sales and 130 units of profit. Expected category sales: Technology 450, Furniture 300 and Office Supplies 50. The region-profit query returns Southeast 72, South 48 and North 10.
