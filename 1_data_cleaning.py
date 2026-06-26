import pandas as pd

# Load Dataset
df = pd.read_csv(
    "data/IDS_ALLCountries_Data.csv",
    encoding="latin1"
)

# Basic Information
print("First 5 Rows")
print(df.head())

print("\nColumns")
print(df.columns)

print("\nShape")
print(df.shape)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

# Remove Duplicate Rows
df = df.drop_duplicates()

print("\nShape After Removing Duplicates")
print(df.shape)

# Save Cleaned Dataset
df.to_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\cleaned_debt_data.csv",
    index=False
)

print("\nCleaned Dataset Saved Successfully")

print("\nMissing Values in Key Columns")

print(df[
    [
        "Country Name",
        "Country Code",
        "Series Name",
        "Series Code"
    ]
].isnull().sum())

# Remove Rows with Missing Key Columns
df = df.dropna(
    subset=[
        "Country Name",
        "Country Code",
        "Series Name",
        "Series Code"
    ]
)

print("\nShape After Removing Invalid Rows")
print(df.shape)

# Save Final Cleaned Dataset
df.to_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\cleaned_debt_data.csv",
    index=False
)

print("\nFinal Cleaned Dataset Saved")

print("\nData Types")
print(df.dtypes)