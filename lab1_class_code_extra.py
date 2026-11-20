# Lab 1 Class Code (Extra): practice cells for after class
# Everything here is self-contained. Run it cell by cell at home (Shift+Enter).

# %% 0. Imports
import pandas as pd
from pathlib import Path

# %% 1. Boolean masks: valid ranges and ~
ages = pd.Series([19, 22, -3, 20, 150, 21])
valid = ages.between(15, 80)
print(valid)
print(~valid)                                   # ~ means NOT
print((~valid).sum(), "rows break the rule")
print(ages[valid])
print(ages.where(valid))                        # keep the shape, put NaN in the bad rows

# %% 2. map: look values up
points = {"A": 4, "B": 3, "C": 2}
grades = pd.Series(["A", "C", "B", "F", "A"])
print(grades.map(points))                       # no rule for "F" -> NaN
print(grades.map(points).fillna(0))
print(grades.replace(points))                   # replace leaves unknown values unchanged

rooms = pd.Series({11: "R-101", 12: "R-102", 14: "R-104"})      # a Series acts as a lookup table
loans = pd.DataFrame({"loan_id": [1, 2, 3, 4], "member_id": [11, 14, 99, 12]})
print(loans["member_id"].map(rooms))            # like VLOOKUP

# %% 3. More merge types and indicator
students = pd.DataFrame({"sid": [1, 2, 3, 4], "name": ["Ria", "Sami", "Tithi", "Uday"]})
marks = pd.DataFrame({"sid": [1, 2, 2, 5], "course": ["DB", "DB", "ML", "DB"], "mark": [78, 64, 81, 90]})
print(students.merge(marks, on="sid", how="right"))                    # every mark; NaN if no student
print(students.merge(marks, on="sid", how="outer", indicator=True))    # everything, and where it came from

# %% 4. Pivot tables and concat
print(marks.pivot_table(index="sid", columns="course", values="mark", aggfunc="mean", fill_value=0))
term1 = pd.DataFrame({"sid": [1, 2], "gpa": [3.4, 3.1]})
term2 = pd.DataFrame({"sid": [3, 4], "gpa": [2.9, 3.8]})
print(pd.concat([term1, term2], ignore_index=True))                    # stack tables with the same columns

# %% 5. groupby with several keys
sales = pd.DataFrame({"shop": ["North", "South", "North", "East", "South", "North"],
                      "item": ["Tea", "Tea", "Snack", "Tea", "Snack", "Tea"],
                      "qty": [3, 2, 5, 1, 4, 2],
                      "price": [20, 20, 35, 20, 35, 20]})
sales["total"] = sales["qty"] * sales["price"]
print(sales.groupby(["shop", "item"])["total"].sum())
print(sales.groupby("shop").agg(n_sales=("item", "count"), revenue=("total", "sum"), avg_qty=("qty", "mean")))
print(sales.groupby("shop")["total"].sum().sort_values(ascending=False).head(2))

# %% 6. assert, count before and after, save and reload
books = pd.DataFrame({"book_id": [1, 2, 2, 3, 3, 4], "copies": [3, 5, 5, 2, 4, 1]})
n_before = len(books)
books = books.drop_duplicates(subset="book_id")
print(f"books: {n_before} -> {len(books)} rows ({n_before - len(books)} removed)")
assert books["book_id"].is_unique
assert books["copies"].gt(0).all(), "copies must be positive"
OUT = Path("data/clean_demo")
OUT.mkdir(parents=True, exist_ok=True)                      # never write into data/raw
books.to_csv(OUT / "books_demo.csv", index=False)           # index=False: no extra number column
print(pd.read_csv(OUT / "books_demo.csv"))

# %% 7. Leading zeros: why dtype matters
tickets = pd.DataFrame({"ticket": ["00123", "00456"], "seat": ["A1", "B2"]})
tickets.to_csv(OUT / "tickets_demo.csv", index=False)
print(pd.read_csv(OUT / "tickets_demo.csv"))                       # 123, 456: zeros lost
print(pd.read_csv(OUT / "tickets_demo.csv", dtype={"ticket": str}))

# %% 8. Small functions
def shout(s: pd.Series) -> pd.Series:
    """Strip spaces and upper-case a text column."""
    return s.str.strip().str.upper()

print(shout(pd.Series(["  cse ", "eee"])))

# %% 9. Dates: more .dt and date arithmetic
due = pd.to_datetime(pd.Series(["03/04/2026", "15/04/2026"]), format="%d/%m/%Y")
print(due.dt.year, due.dt.month, due.dt.day)
print(due.max() - due.min())

# %%