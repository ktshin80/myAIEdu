from ..models.cohort import Cohort


def list_all(conn):
    return [Cohort(**dict(r)) for r in conn.execute("SELECT * FROM cohorts ORDER BY id")]


def get(conn, cohort_id):
    row = conn.execute("SELECT * FROM cohorts WHERE id = ?", (cohort_id,)).fetchone()
    return Cohort(**dict(row)) if row else None
