# Power BI Dashboard Guide
Import data/processed/telco_churn_clean.csv and name the table Telco. Add measures from DAX_measures.dax. Format rate measures as percentages.

## Page 1 — Executive Overview
KPI cards: Total Customers, Churned Customers, Churn Rate, Retention Rate, Average Monthly Charges.
Charts: customer count by Churn; churn rate by Contract; churn rate by TenureGroup.
Slicers: Contract, InternetService, Gender.

## Page 2 — Customer Risk Analysis
Charts: churn rate by PaymentMethod, InternetService, TechSupport and TenureGroup.
Matrix: Contract x InternetService with customer count and churn rate.
Slicers: Contract, PaymentMethod, TechSupport.

## Page 3 — Customer Details
Table: customerID, tenure, TenureGroup, Contract, InternetService, PaymentMethod, MonthlyCharges, TotalCharges, Churn.
Add slicers and conditional formatting.

## QA
Check measures respond to slicers. Segment churn rate = churned customers in segment / all customers in segment. Display customer counts beside rates. Compare KPI totals with Python outputs. Avoid causal language.
