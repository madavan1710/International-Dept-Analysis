import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL Connection
engine = create_engine(
    "postgresql+psycopg2://postgres:1127@localhost:5432/international_debt_analysis"
)

# Load debt_data CSV
debt_data = pd.read_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\debt_data.csv"
)

print("Debt Data Rows:")
print(len(debt_data))

# Insert into PostgreSQL in chunks
debt_data.to_sql(
    "debt_data",
    engine,
    if_exists="append",
    index=False,
    chunksize=10000,
    method="multi"
)

print("Debt Data Loaded Successfully!")