import json
import requests
from datetime import datetime

url = "https://raw.githubusercontent.com/lcnlvrz/opensalary/main/salaries.json"
response = requests.get(url)
if response.status_code == 200:
    salaries = response.json()
else:
    raise Exception("Failed to fetch data")

output = {
    "last_updated": datetime.now().isoformat(),
    "source": "OpenSalaryData (MIT)",
    "currency": "USD",
    "roles": {}
}

for entry in salaries:
    role = entry.get("role", "").strip().title()
    level = entry.get("experience_level", "").title()
    rate = entry.get("hourly_rate")

    if not (role and level and isinstance(rate, (int, float))):
        continue

    if role not in output["roles"]:
        output["roles"][role] = {}

    output["roles"][role][level] = {
        "hourly": round(rate),
        "daily": round(rate * 8),
        "project": round(rate * 30)
    }

with open("freelance_rate_benchmarks_combined.json", "w") as f:
    json.dump(output, f, indent=2)
