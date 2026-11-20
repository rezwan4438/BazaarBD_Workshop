# Lab 1 Class Code: Taming a messy dataset

# %% 1. Core types and f-strings
city = "Dhaka" 
orders = 1040
aov = 5122.5
is_active = True
print(f" {city} has {orders:,} orders with an average order value of {aov:,.2f}. Active? {is_active}")

# %% practice cell
name = "Rezwan"
age = 43
print(f" Hello! I am {name} and I am {age} years old!")

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
print(city_fix.get("Dac" ,"Dacca"))  
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
print(df.iloc[2:4, :])

# %% 5.4 Pandas Fundamentals - Filtering
print((df[df["orders"] > 500]))
print(df[(df["orders"] > 500) | (df["city"] == "Sylhet")])
print(df[df["city"].isin(["Dhaka", "Sylhet"])])

# %% 5.5 New columns and sorting
df["orders_with_vat"] = round(df["orders"] * 1.15)
print(df)
df.sort_values(by="orders_with_vat", ascending=False, inplace=True)
print(df)

# %% 6.1 Cleaning - Duplicates: whole row or just the key?
books = pd.DataFrame({"book_id": [1, 2, 2, 3, 3, 4],
                      "title": ["Python 101", "Data Basics", "Data Basics", "SQL Handbook", "SQL Handbook (2nd ed.)", "AI Primer"],
                      "copies": [3, 5, 5, 2, 4, 1]})
print(books.duplicated().sum())                      # exact repeats of a whole row
print(books.duplicated(subset="book_id").sum())      # repeats of the key only
print(books.drop_duplicates(subset="book_id"))       # keeps the first; keep="last" is also possible

# %% 6.2 Cleaning - Text methods on a Series
dept = pd.Series(["  cse", "EEE ", "Cse", "bba", " BBA ", None])
print(dept.str.strip().str.upper().value_counts(dropna=False))   # None stays missing: nothing crashes
print(dept.str.strip().str.upper().replace({"EEE": "EE"}))        # replace one value with another

# %% 6.3 Cleaning - Looking inside text: contains, extract and \D
codes = pd.Series(["Room 4-12", "room 7-03", "Lab 2-15", "Hall 9-01"])
print(codes[codes.str.contains("room", case=False)])
print(codes.str.extract(r"(\d+)-(\d+)"))                        # () marks what to capture
print(codes.str.replace(r"\D", "", regex=True).str[-2:])        # \D = any non-digit; keep last 2 characters

# %% 6.4 Cleaning - Text to numbers: to_numeric
fines = pd.Series(["10", "25", "5 BDT", "N/A", "40"])
# pd.to_numeric(fines)                                  # try it live: ValueError, the whole run stops
print(pd.to_numeric(fines, errors="coerce"))            # unparseable -> NaN
print(pd.to_numeric(fines.str.replace("BDT", "", regex=False).str.strip(), errors="coerce"))

# %% 6.5 Cleaning - Text to dates: to_datetime and .dt
due = pd.Series(["03/04/2026", "15/04/2026", "31/02/2026", "soon"])
print(pd.to_datetime(due, format="%d/%m/%Y", errors="coerce"))     # day first: 3 April
print(pd.to_datetime(due, errors="coerce"))                         # Pandas guesses: 4 March! Compare
due = pd.to_datetime(due, format="%d/%m/%Y", errors="coerce")
print(due.dt.month_name(), due.dt.day_name())                       # .dt works only on real dates

# %% 6.6 Cleaning - Missing values: detect, then decide
members = pd.DataFrame({"member_id": [11, 12, 13, 14, 15],
                        "name": ["Anika", "Biplob", "Chaity", "Dipto", "Eshita"],
                        "faculty": ["Science", None, "Arts", None, "Science"],
                        "year": [1, 2, None, 3, 2],
                        "email": ["a@x.com", None, "c@x.com", "d@x.com", None],
                        "alt_email": [None, "b2@x.com", None, None, "e2@x.com"]})
print(members.isna().sum())
members["faculty"] = members["faculty"].fillna("Unknown")                # a label
members["year"] = members["year"].fillna(members["year"].median())       # a statistic
members["email"] = members["email"].fillna(members["alt_email"])         # another column
print(members)

# %% 6.7 Cleaning - Is it in the other table? isin
loans = pd.DataFrame({"loan_id": [1, 2, 3, 4], "member_id": [11, 14, 99, 12], "book_id": [1, 2, 3, 9]})
print(loans["member_id"].isin(members["member_id"]))
print(loans[~loans["member_id"].isin(members["member_id"])])     # ~ means NOT: member 99 does not exist

# %% 7.1 Transforming - Group and aggregate
sales = pd.DataFrame({"shop": ["North", "South", "North", "East", "South", "North"],
                      "item": ["Tea", "Tea", "Snack", "Tea", "Snack", "Tea"],
                      "qty": [3, 2, 5, 1, 4, 2],
                      "price": [20, 20, 35, 20, 35, 20]})
sales["total"] = sales["qty"] * sales["price"]
print(sales.groupby("shop")["total"].sum())                          # split -> apply -> combine
print(sales.groupby("shop").agg(n_sales=("item", "count"), revenue=("total", "sum")))

# %% 7.2 Transforming - Merge (join)
students = pd.DataFrame({"sid": [1, 2, 3, 4], "name": ["Ria", "Sami", "Tithi", "Uday"]})
marks = pd.DataFrame({"sid": [1, 2, 2, 5], "course": ["DB", "DB", "ML", "DB"], "mark": [78, 64, 81, 90]})
print(students.merge(marks, on="sid", how="inner"))                  # only ids found in both
print(students.merge(marks, on="sid", how="left"))                   # every student; NaN if no marks

# %% 