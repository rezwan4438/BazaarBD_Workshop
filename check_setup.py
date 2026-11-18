"""Run this once before the workshop:  python check_setup.py
It checks that your computer is ready. Every line should say OK."""
import sys, sqlite3, shutil, pathlib

ok_all = True
def report(name, ok, detail=""):
    global ok_all
    ok_all &= ok
    print(f"{'OK     ' if ok else 'PROBLEM'}  {name}  {detail}")

report("Python 3.10 or newer", sys.version_info >= (3, 10), sys.version.split()[0])
for mod in ("pandas", "matplotlib"):
    try:
        m = __import__(mod); report(mod, True, m.__version__)
    except ImportError:
        report(mod, False, f"missing: run  pip install {mod}")
report("sqlite3", True, "SQLite " + sqlite3.sqlite_version)
git = shutil.which("git")
report("Git", git is not None, "" if git else "not found: install from git-scm.com")
here = pathlib.Path(__file__).parent
for f in ("data/raw/customers_raw.csv", "data/raw/orders_raw.csv", "data/raw/products_raw.csv", "data/raw/order_items_raw.csv"):
    report(f, (here / f).exists())
print("\nAll good. See you at the workshop." if ok_all else "\nFix the PROBLEM lines (ask for help if stuck), then run again.")
