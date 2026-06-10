-- emulated agent pipeline for online course completions
CREATE OR REPLACE VIEW bronze_raw AS
SELECT * FROM read_csv_auto('/mnt/data/course_completions_raw.csv', header=true, all_varchar=true);

CREATE OR REPLACE TABLE silver_clean AS
WITH typed AS (
    SELECT
        event_id,
        CAST(student_id AS INTEGER) AS student_id,
        event_date,
        course_category,
        TRY_CAST(completion_pct AS DOUBLE) AS completion_pct,
        CAST(time_spent_minutes AS INTEGER) AS time_spent_minutes,
        status
    FROM bronze_raw
),
non_nulls AS (
    SELECT * FROM typed WHERE completion_pct IS NOT NULL
),
standardized_dates AS (
    SELECT
        event_id,
        student_id,
        COALESCE(
            TRY_STRPTIME(event_date, '%Y-%m-%d'),
            TRY_STRPTIME(event_date, '%m/%d/%Y'),
            TRY_STRPTIME(event_date, '%B %d %Y')
        )::DATE AS event_date,
        course_category,
        completion_pct,
        time_spent_minutes,
        status
    FROM non_nulls
),
deduped AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY event_id ORDER BY student_id DESC) AS rn
    FROM standardized_dates
)
SELECT event_id, student_id, event_date, course_category, completion_pct, time_spent_minutes, status
FROM deduped WHERE rn = 1;

COPY silver_clean TO '/mnt/data/course_completions_clean.parquet' (FORMAT PARQUET);

CREATE OR REPLACE TABLE daily_completions_by_category AS
SELECT
    event_date,
    course_category,
    AVG(CASE WHEN status = 'completed' THEN completion_pct ELSE NULL END) AS avg_completion_pct,
    COUNT(DISTINCT CASE WHEN status = 'completed' THEN event_id ELSE NULL END) AS completion_count
FROM silver_clean
GROUP BY event_date, course_category;

COPY daily_completions_by_category TO '/mnt/data/daily_completions_by_category.parquet' (FORMAT PARQUET);

CREATE OR REPLACE TABLE dropout_rate AS
WITH per_day AS (
    SELECT
        event_date,
        COUNT(DISTINCT CASE WHEN status IN ('completed','in_progress','dropped') THEN event_id ELSE NULL END) AS total_enrollments,
        COUNT(DISTINCT CASE WHEN status = 'dropped' THEN event_id ELSE NULL END) AS dropped_count
    FROM silver_clean
    GROUP BY event_date
)
SELECT
    event_date,
    total_enrollments,
    dropped_count,
    ROUND(COALESCE((dropped_count * 100.0) / NULLIF(total_enrollments, 0), 0.0), 2) AS dropout_rate_pct
FROM per_day;

COPY dropout_rate TO '/mnt/data/dropout_rate.parquet' (FORMAT PARQUET);
