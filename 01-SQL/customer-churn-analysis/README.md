# Telecom Customer Churn Analysis

**End-to-end portfolio project | SQL · Python · Excel · Power BI**

## Business problem
Analyse customer churn for a fictional telecom provider, identify segments with higher observed churn, and recommend areas for retention teams to investigate.

## Dataset
IBM Telco Customer Churn sample: 7,043 customers and 21 columns.
Source: https://github.com/IBM/telco-customer-churn-on-icp4d
Raw CSV is in data/raw/. Preserve it unchanged.

## Quick start
```bash
python -m pip install -r requirements.txt
python scripts/run_analysis.py
```

## Workflow
1. Excel: inspect data quality and create PivotTables.
2. Python: clean TotalCharges, validate data, create tenure groups, analyse churn and export tables/charts.
3. SQL: run sql/customer_churn_analysis.sql in SQLite after importing the processed CSV as telco_churn.
4. Power BI: import data/processed/telco_churn_clean.csv, add powerbi/DAX_measures.dax measures, and follow powerbi/DASHBOARD_GUIDE.md.

## Business questions
- Overall churn and retention rates?
- Churn by contract, tenure, payment method, internet service and tech support?
- Monthly charges and tenure for churned vs retained customers?
- Which segments have elevated churn and meaningful sample sizes?

## Data preparation
TotalCharges is converted from text to numeric. The raw file is preserved. The 11 blank TotalCharges values in the sample correspond to zero-tenure accounts; these are retained, assigned numeric 0, and flagged by TotalChargesWasBlank. customerID is an identifier, not a model feature.

## Limitations
This is a cross-sectional educational sample for a fictional company. Associations do not prove causation. It has no cancellation reasons or monthly history. Do not claim a predictive model or proven revenue savings.

## Outputs
Generated cleaned CSV, data-quality report, business-insights report, summary tables and charts are saved under data/processed, reports and outputs.

## Credits
IBM Telco Customer Churn sample dataset. See source repository for original context and terms.
