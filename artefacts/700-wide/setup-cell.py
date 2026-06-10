# Cell 1 — environment setup for local Jupyter / Google Colab

import sys
get_ipython().system('{sys.executable} -m pip install --quiet "duckdb>=1.4" pandas numpy')

import duckdb
import pandas as pd
import os
import random
import numpy as np
from datetime import datetime

con = duckdb.connect(database=":memory:")

con.execute("""
CREATE TABLE hello_world (
    id INTEGER,
    message VARCHAR,
    created_at TIMESTAMP
)
""")

rows = [
    (1, "Hello from DuckDB", datetime.now()),
    (2, "Notebook environment ready", datetime.now()),
    (3, "Nordstar kata workspace", datetime.now()),
]

con.executemany(
    "INSERT INTO hello_world (id, message, created_at) VALUES (?, ?, ?)",
    rows,
)

result_df = con.execute(
    "SELECT id, message, created_at FROM hello_world ORDER BY id"
).df()

print(result_df)
print("Environment ready ✓")
