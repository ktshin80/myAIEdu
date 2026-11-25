from ..models.student import Student

_COLUMNS = "id, name, phone, email, persona, created_at"


def get_by_email(conn, email):
    row = conn.execute(f"SELECT {_COLUMNS} FROM students WHERE email = ?", (email,)).fetchone()
    return Student(**dict(row)) if row else None


def add(conn, name, phone, email, persona):
    student_id = conn.execute(
        "INSERT INTO students (name, phone, email, persona) VALUES (?, ?, ?, ?)",
        (name, phone, email, persona)).lastrowid
    row = conn.execute(f"SELECT {_COLUMNS} FROM students WHERE id = ?", (student_id,)).fetchone()
    return Student(**dict(row))
