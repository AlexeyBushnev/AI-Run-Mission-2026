import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

row_count = 500
dup_count = 10   # 2%
null_completion_count = 20  # 4%

categories = ["Data", "Engineering", "Design", "Business", "Security"]
statuses = ["completed", "in_progress", "dropped"]
status_probs = [0.70, 0.20, 0.10]

date_formats = [
    lambda d: d.strftime("%Y-%m-%d"),
    lambda d: d.strftime("%m/%d/%Y"),
    lambda d: d.strftime("%B %d %Y"),
]

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
span_days = (end_date - start_date).days

rows = []
for i in range(row_count - dup_count):
    event_id = f"EVT-{10000 + i:05d}"
    student_id = random.randint(1000, 9999)
    event_dt = start_date + timedelta(days=random.randint(0, span_days))
    event_date = random.choice(date_formats)(event_dt)
    course_category = random.choice(categories)
    completion_pct = round(random.uniform(0, 100), 2)
    time_spent_minutes = random.randint(10, 480)
    status = random.choices(statuses, weights=status_probs, k=1)[0]
    rows.append(
        {
            "event_id": event_id,
            "student_id": student_id,
            "event_date": event_date,
            "course_category": course_category,
            "completion_pct": completion_pct,
            "time_spent_minutes": time_spent_minutes,
            "status": status,
        }
    )

dup_idx = np.random.choice(len(rows), size=dup_count, replace=False)
for idx in dup_idx:
    dup = rows[idx].copy()
    dup["student_id"] = max(1000, dup["student_id"] - random.randint(0, 15))
    rows.append(dup)

null_idx = np.random.choice(len(rows), size=null_completion_count, replace=False)
for idx in null_idx:
    rows[idx]["completion_pct"] = None

df = pd.DataFrame(rows)
df.to_csv("course_completions_raw.csv", index=False)

print("total rows:", len(df))
print("null completion_pct count:", int(df["completion_pct"].isna().sum()))
print("duplicate event_id count:", int(df["event_id"].duplicated().sum()))
