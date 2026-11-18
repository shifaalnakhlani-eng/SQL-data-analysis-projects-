from pathlib import Path
from urllib.request import urlretrieve
import hashlib
URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
OUT = Path(__file__).resolve().parents[1] / "data/raw/Telco-Customer-Churn.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)
if not OUT.exists():
    print("Downloading IBM sample dataset...")
    urlretrieve(URL, OUT)
print("Dataset:", OUT, f"({OUT.stat().st_size:,} bytes)")
print("SHA-256:", hashlib.sha256(OUT.read_bytes()).hexdigest())
