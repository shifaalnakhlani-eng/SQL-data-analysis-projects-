-- SQLite. Import processed CSV as telco_churn.
-- Overall KPIs
SELECT COUNT(DISTINCT customerID) total_customers,
 SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END) churned_customers,
 ROUND(100.0*SUM(CASE WHEN Churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) churn_rate_pct
FROM telco_churn;

-- Churn by contract
SELECT Contract,COUNT(*) customers,SUM(ChurnFlag) churned,
 ROUND(100.0*SUM(ChurnFlag)/COUNT(*),2) churn_rate_pct
FROM telco_churn GROUP BY Contract ORDER BY churn_rate_pct DESC;

-- Churn by tenure group
SELECT TenureGroup,COUNT(*) customers,SUM(ChurnFlag) churned,
 ROUND(100.0*SUM(ChurnFlag)/COUNT(*),2) churn_rate_pct
FROM telco_churn GROUP BY TenureGroup ORDER BY MIN(tenure);

-- Churn by payment method and internet service
SELECT PaymentMethod,COUNT(*) customers,SUM(ChurnFlag) churned,
 ROUND(100.0*SUM(ChurnFlag)/COUNT(*),2) churn_rate_pct
FROM telco_churn GROUP BY PaymentMethod ORDER BY churn_rate_pct DESC;
SELECT InternetService,COUNT(*) customers,SUM(ChurnFlag) churned,
 ROUND(100.0*SUM(ChurnFlag)/COUNT(*),2) churn_rate_pct
FROM telco_churn GROUP BY InternetService ORDER BY churn_rate_pct DESC;

-- Churn by technical support
SELECT TechSupport,COUNT(*) customers,SUM(ChurnFlag) churned,
 ROUND(100.0*SUM(ChurnFlag)/COUNT(*),2) churn_rate_pct
FROM telco_churn GROUP BY TechSupport ORDER BY churn_rate_pct DESC;

-- Charges and tenure by churn status
SELECT Churn,COUNT(*) customers,ROUND(AVG(MonthlyCharges),2) avg_monthly_charges,
 ROUND(AVG(tenure),1) avg_tenure,ROUND(AVG(TotalCharges),2) avg_total_charges
FROM telco_churn GROUP BY Churn;

-- CTE and window function
WITH m AS (SELECT TenureGroup,COUNT(*) customers,SUM(ChurnFlag) churned,
 1.0*SUM(ChurnFlag)/COUNT(*) churn_rate FROM telco_churn GROUP BY TenureGroup)
SELECT *,ROUND(100*churn_rate,2) churn_rate_pct,
 DENSE_RANK() OVER(ORDER BY churn_rate DESC) churn_rank FROM m ORDER BY churn_rank;
