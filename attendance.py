import streamlit as st
import pandas as pd
from datetime import date

def attendance_page(conn):
    st.header("🕒 Attendance Management")
    st.caption("Mark and view employee attendance")
    st.divider()

    employees = pd.read_sql("SELECT * FROM employee", conn)

    if employees.empty:
        st.warning("Add employees before marking attendance")
        return

    emp_id = st.selectbox(
        "Select Employee",
        employees["id"],
        format_func=lambda x: employees.loc[employees["id"] == x, "name"].values[0]
    )

    status = st.radio("Attendance Status", ["Present", "Absent"])
    today = str(date.today())

    if st.button("Mark Attendance"):
        already = conn.execute(
            "SELECT 1 FROM attendance WHERE emp_id=? AND date=?",
            (emp_id, today)
        ).fetchone()

        if already:
            st.warning("Attendance already marked for today")
        else:
            conn.execute(
                "INSERT INTO attendance (emp_id, date, status) VALUES (?, ?, ?)",
                (emp_id, today, status)
            )
            conn.commit()
            st.success("Attendance marked successfully")

    st.divider()

    # ---------- VIEW ATTENDANCE ----------
    st.subheader("📅 Attendance Records")

    records = pd.read_sql("""
        SELECT e.name, a.date, a.status
        FROM attendance a
        JOIN employee e ON a.emp_id = e.id
        ORDER BY a.date DESC
    """, conn)

    if records.empty:
        st.info("No attendance records yet")
        return

    records_display = records.rename(columns={
        "name": "Employee Name",
        "date": "Date",
        "status": "Status"
    })

    st.dataframe(records_display, use_container_width=True)
    st.caption("📌 Showing latest attendance first")
