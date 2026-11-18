from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/"data/raw/Telco-Customer-Churn.csv"
PROCESSED,TABLES,CHARTS,REPORTS=[ROOT/x for x in ["data/processed","outputs/tables","outputs/charts","reports"]]
for p in [PROCESSED,TABLES,CHARTS,REPORTS]: p.mkdir(parents=True,exist_ok=True)
if not RAW.exists(): raise FileNotFoundError("Run python scripts/download_data.py first.")
df=pd.read_csv(RAW)
required={"customerID","tenure","MonthlyCharges","TotalCharges","Churn"}
if required-set(df.columns): raise ValueError(f"Missing columns: {required-set(df.columns)}")
rows,cols=df.shape
dups=int(df.customerID.duplicated().sum())
df["TotalChargesWasBlank"]=df.TotalCharges.astype(str).str.strip().eq("")
df["TotalCharges"]=pd.to_numeric(df.TotalCharges,errors="coerce")
missing=int(df.TotalCharges.isna().sum())
zero_blank=int((df.TotalCharges.isna() & df.tenure.eq(0)).sum())
unexpected=int((df.TotalCharges.isna() & df.tenure.ne(0)).sum())
df.loc[df.TotalCharges.isna() & df.tenure.eq(0),"TotalCharges"]=0
df["TenureGroup"]=pd.cut(df.tenure,[-1,12,24,48,72],labels=["0-12 months","13-24 months","25-48 months","49-72 months"])
df["ChurnFlag"]=df.Churn.map({"Yes":1,"No":0})
if df.ChurnFlag.isna().any(): raise ValueError("Unexpected Churn values.")
df.to_csv(PROCESSED/"telco_churn_clean.csv",index=False)
def summary(col):
 x=df.groupby(col,observed=False).agg(total_customers=("customerID","nunique"),churned_customers=("ChurnFlag","sum"),avg_monthly_charges=("MonthlyCharges","mean"),avg_tenure=("tenure","mean")).reset_index()
 x["churn_rate_pct"]=100*x.churned_customers/x.total_customers
 return x.sort_values("churn_rate_pct",ascending=False)
k=pd.DataFrame([{"total_customers":df.customerID.nunique(),"churned_customers":int(df.ChurnFlag.sum()),"retained_customers":int((df.ChurnFlag==0).sum()),"churn_rate_pct":100*df.ChurnFlag.mean(),"retention_rate_pct":100*(1-df.ChurnFlag.mean()),"avg_monthly_charges":df.MonthlyCharges.mean()}])
k.to_csv(TABLES/"overall_kpis.csv",index=False)
for c in ["Contract","TenureGroup","PaymentMethod","InternetService","TechSupport","SeniorCitizen","PaperlessBilling"]: summary(c).to_csv(TABLES/f"churn_by_{c.lower()}.csv",index=False)
(df.groupby("Churn").agg(customer_count=("customerID","nunique"),avg_monthly_charges=("MonthlyCharges","mean"),avg_tenure=("tenure","mean"),avg_total_charges=("TotalCharges","mean")).reset_index().to_csv(TABLES/"charges_and_tenure_by_churn.csv",index=False))
(REPORTS/"data_quality_report.txt").write_text(f"Raw shape: {rows} x {cols}\nDuplicate IDs: {dups}\nMissing TotalCharges after conversion: {missing}\nBlank TotalCharges at tenure=0 (set to 0, original blank flagged): {zero_blank}\nMissing TotalCharges at nonzero tenure: {unexpected}\nRaw CSV preserved unchanged.\n",encoding="utf-8")
sns.set_theme(style="whitegrid")
for c in ["Contract","TenureGroup","PaymentMethod","InternetService","TechSupport"]:
 s=summary(c); plt.figure(figsize=(9,5)); sns.barplot(data=s,x=c,y="churn_rate_pct"); plt.title(f"Churn Rate by {c}"); plt.ylabel("Churn rate (%)"); plt.xticks(rotation=15,ha="right"); plt.tight_layout(); plt.savefig(CHARTS/f"churn_by_{c.lower()}.png",dpi=180); plt.close()
plt.figure(figsize=(8,5)); sns.boxplot(data=df,x="Churn",y="MonthlyCharges"); plt.title("Monthly Charges by Churn"); plt.tight_layout(); plt.savefig(CHARTS/"monthly_charges_by_churn.png",dpi=180); plt.close()
def top(s,c):
 r=s.iloc[0]; return f"{r[c]}: {r.churn_rate_pct:.1f}% ({int(r.churned_customers)}/{int(r.total_customers)})"
r=k.iloc[0]
(REPORTS/"business_insights.md").write_text(f"# Business Insights (generated)\n- Total customers: {int(r.total_customers):,}\n- Churned customers: {int(r.churned_customers):,}\n- Churn rate: {r.churn_rate_pct:.2f}%\n- Retention rate: {r.retention_rate_pct:.2f}%\n\n## Highest observed churn segments\n- Contract: {top(summary('Contract'),'Contract')}\n- Tenure: {top(summary('TenureGroup'),'TenureGroup')}\n- Payment method: {top(summary('PaymentMethod'),'PaymentMethod')}\n- Internet service: {top(summary('InternetService'),'InternetService')}\n- Tech support: {top(summary('TechSupport'),'TechSupport')}\n\nThese are descriptive associations, not proof of causation. Consider sample sizes alongside rates. Monthly charges associated with churned customers are not automatically revenue lost.\n",encoding="utf-8")
print("Analysis complete. Review generated reports and tables.")
