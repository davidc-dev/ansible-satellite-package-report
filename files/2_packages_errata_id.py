import json
import pandas as pd

with open("combined.json", "r") as f:
    data = json.load(f)

rows = []
for errata_id, errata_data in data.items():
    for package in errata_data['packages']:
        if package.endswith('.i686'):
            package = package[:-5] # remove the last 5 characters (.i686)
        elif package.endswith('.x86_64'):
            package = package[:-7] # remove the last 7 characters (.x86_64)
        elif package.endswith('.noarch'):
            package = package[:-7] # remove the last 7 characters (.noarch)
        if package not in [row['package_name'] for row in rows]:
            rows.append({
                'package_name': package,
                'errata_id': errata_id,
            })

df = pd.DataFrame(rows)
df.to_csv('packages_errata.csv', index=False)

