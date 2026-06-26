import pandas as pd

# Load final transformed dataset
df = pd.read_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\final_debt_data.csv"
)

# Countries table data
countries = df[
    ["Country Code", "Country Name"]
].drop_duplicates()

countries.columns = [
    "country_code",
    "country_name"
]

print("Countries Shape:")
print(countries.shape)

# Save countries table data
countries.to_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\countries.csv",
    index=False
)

print("\nCountries CSV Saved")

# Indicators table data
indicators = df[
    ["Series Code", "Series Name"]
].drop_duplicates()

indicators.columns = [
    "series_code",
    "series_name"
]

print("\nIndicators Shape:")
print(indicators.shape)

# Save indicators table data
indicators.to_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\indicators.csv",
    index=False
)

print("\nIndicators CSV Saved")

# debt_data table data
debt_data = df[
    [
        "Country Code",
        "Series Code",
        "Year",
        "Debt_Value",
        "Counterpart-Area Name",
        "Counterpart-Area Code"
    ]
]

debt_data.columns = [
    "country_code",
    "series_code",
    "year",
    "debt_value",
    "counterpart_area_name",
    "counterpart_area_code"
]

print("\nDebt Data Shape:")
print(debt_data.shape)

# Save debt_data table data
debt_data.to_csv(
    r"D:\PROJECTS\PROJECT - 2\PYTHON\data\debt_data.csv",
    index=False
)

print("\nDebt Data CSV Saved")