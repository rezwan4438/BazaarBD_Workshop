# Lab 1 Class Code: Taming a messy dataset

# %% 1. Core types and f-strings
city = "Dhaka" 
orders = 1040
aov = 5122.5
is_active = True
print(f" {city} has {orders:,} orders with an average order value of {aov:,.2f}. Active? {is_active}")

# %% 2.1 Lists and Dictionaries
city_data = {
    "name": "Dhaka",
    "orders": 1040,
    "aov": 5122.5,
    "is_active": True
}
print(type(city_data))
print(f" {city_data['name']} has {city_data['orders']:,} orders with an average order value of {city_data['aov']:,.2f}. Active? {city_data['is_active']}")
# %% 2.2 Lists and Dictionaries - Another Example
cities = ["Dhaka", "Chattogram", "Sylhet"]        
cities.append("Khulna")
print(type(cities))
print(cities)
city_fix = {"Dacca": "Dhaka", "Chittagong": "Chattogram"}  
print(city_fix["Dacca"])  
print(city_fix.get("Dacca" ,"Dacca"))  
# %% 3. Loops, comprehensions and functions
prices = [1200, 850, 4300]
with_vat = [round(p * 1.15) for p in prices]
print(with_vat)      

def clean_phone(raw: str) -> str:
    """Keep digits only and return the last 11 characters."""
    digits = "".join(ch for ch in raw if ch.isdigit())
    return digits[-11:]

print(clean_phone("+88 01712-345678"))

# %% 4. Files and paths
from pathlib import Path
import csv, json

RAW = Path("data/raw")                
with open(RAW / "products_raw.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
print(len(rows), rows[0])

with open("first_row.json", "w", encoding="utf-8") as f:
    json.dump(rows[0], f, ensure_ascii=False, indent=2)  

# %% 5.1 Pandas Fundamentals - Series and DataFrame
import pandas as pd
df = pd.DataFrame({"city": ["Dhaka", "Sylhet", "Chattogram", "Dacca", "Sylhet"], "orders": [1040, 251, 1500, 800, 251]})
print(type(df))
print(df)

print(type(df["city"]))
print(df["city"])

print(type(df[["city", "orders"]]))
print(df[["city", "orders"]])

# %% 5.2 Pandas Fundamentals - Inspecting a DataFrame

print(df.shape)
print(df.dtypes)
print(df.head())
print(df.info())

# %% 5.2 Pandas Fundamentals - Inspecting a DataFrame (continued) 
print(df.describe(include="all"))



# %% 5.2 Pandas Fundamentals - Inspecting a DataFrame (continued)
print(df.isna().sum())          
print(df.duplicated().sum())     
print(df["city"].value_counts(dropna=False))   

# %% 5.3 Pandas Fundamentals - Indexing and Slicing
print(df["city"]) #print(df.city)
print(df.loc[0])
print(df.loc[0, "city"])
print(df.loc[0:2, ["city", "orders"]])
print(df.iloc[0:2, 0:2])

# %% 5.4 Pandas Fundamentals - Filtering
print((df[df["orders"] > 500]))
print(df[(df["orders"] > 500) | (df["city"] == "Sylhet")])
print(df[df["city"].isin(["Dhaka", "Sylhet"])])

# %% 5.5 New columns and sorting
df["orders_with_vat"] = round(df["orders"] * 1.15)
print(df)
df.sort_values(by="orders_with_vat", ascending=False, inplace=True)
print(df)

# %% 
