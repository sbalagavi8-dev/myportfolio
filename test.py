import pandas as pd

# Read directly from Dhan’s hosted CSV
url = "https://images.dhan.co/api-data/api-scrip-master-detailed.csv"
df = pd.read_csv(url)

# Lookup instrument type by securityId
security_id = 13631  # replace with your ID
instrument_type = df.loc[df['SECURITY_ID'] == security_id, 'INSTRUMENT_TYPE'].values

print(instrument_type)
