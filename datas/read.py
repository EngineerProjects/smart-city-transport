import pandas as pd

df = pd.read_parquet("data/yellow_trip/yellow_tripdata_2023-01.parquet")

print(df.head())
print(df.shape)
print(df.info())