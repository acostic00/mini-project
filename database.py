import sqlite3

DB_NAME = "hrms.db"


def get_connection():
    """
    Returns a SQLite database connection
    """
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn


def create_tables(conn):
    """
    Creates required tables if they do not exist
    """
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        role TEXT,
        salary INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    conn.commit()


def seed_demo_data(conn):
    """
    Inserts demo data ONLY if employee table is empty
    """
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM employee")
    if cursor.fetchone()[0] > 0:
        return  # Data already exists

    employees = [
        ("Rahul Sharma", "Engineering", "Software Engineer", 60000),
        ("Ananya Patel", "HR", "HR Manager", 50000),
        ("Karthik R", "Finance", "Accountant", 45000),
        ("Neha Singh", "Engineering", "QA Engineer", 48000),
        ("Amit Verma", "Sales", "Sales Executive", 40000),
        ("Priya Nair", "Marketing", "Marketing Lead", 52000),
    ]

    cursor.executemany(
        "INSERT INTO employee (name, department, role, salary) VALUES (?, ?, ?, ?)",
        employees
    )

    attendance = [
        (1, "2025-02-01", "Present"),
        (1, "2025-02-02", "Present"),
        (1, "2025-02-03", "Absent"),

        (2, "2025-02-01", "Present"),
        (2, "2025-02-02", "Present"),

        (3, "2025-02-01", "Absent"),
        (3, "2025-02-02", "Present"),

        (4, "2025-02-01", "Present"),
        (4, "2025-02-02", "Present"),

        (5, "2025-02-01", "Present"),
        (5, "2025-02-02", "Absent"),

        (6, "2025-02-01", "Present"),
        (6, "2025-02-02", "Present"),
    ]

    cursor.executemany(
        "INSERT INTO attendance (emp_id, date, status) VALUES (?, ?, ?)",
        attendance
    )

    conn.commit()
