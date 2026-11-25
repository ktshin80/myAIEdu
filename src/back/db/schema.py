SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    phone      TEXT,
    email      TEXT NOT NULL UNIQUE,
    persona    TEXT CHECK (persona IN ('worker', 'owner')),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS cohorts (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    start_date TEXT,
    capacity   INTEGER
);
CREATE TABLE IF NOT EXISTS enrollments (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL REFERENCES students(id),
    cohort_id  INTEGER NOT NULL REFERENCES cohorts(id),
    status     TEXT NOT NULL DEFAULT 'enrolled'
               CHECK (status IN ('enrolled', 'completed', 'dropped')),
    UNIQUE (student_id, cohort_id)
);
CREATE TABLE IF NOT EXISTS curriculum (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    week_start  INTEGER NOT NULL,
    week_end    INTEGER NOT NULL,
    title       TEXT NOT NULL,
    track       TEXT NOT NULL CHECK (track IN ('common', 'worker', 'owner')),
    deliverable TEXT
);
"""
