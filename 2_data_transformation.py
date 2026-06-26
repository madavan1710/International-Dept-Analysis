import pandas as pd

df = pd.read_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\cleaned_debt_data.csv"
)

id_columns = [
    "Country Name",
    "Country Code",
    "Counterpart-Area Name",
    "Counterpart-Area Code",
    "Series Name",
    "Series Code"
]

df_long = pd.melt(
    df,
    id_vars=id_columns,
    var_name="Year",
    value_name="Debt_Value"
)

print(df_long.shape)
print(df_long.head())

print("\nMissing Debt Values")
print(df_long["Debt_Value"].isnull().sum())

# Remove Missing Debt Values
df_long = df_long.dropna(subset=["Debt_Value"])

print("\nShape After Removing Missing Debt Values")
print(df_long.shape)

# Save Final Analytical Dataset
df_long.to_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\final_debt_data.csv",
    index=False
)

print("\nFinal Analytical Dataset Saved")

print("\nFinal Dataset Columns")
print(df_long.columns)