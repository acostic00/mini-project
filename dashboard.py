import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def dashboard_page(conn):
    st.title("📊 HRMS Dashboard")
    st.caption("High-level overview of employees, payroll & attendance")
    st.divider()

    # ---------------- DATA ----------------
    employees = pd.read_sql("SELECT * FROM employee", conn)
    attendance = pd.read_sql("SELECT * FROM attendance", conn)

    if employees.empty:
        st.warning("No employee data available")
        return

    # ---------------- KPIs ----------------
    col1, col2, col3, col4 = st.columns(4)

    total_employees = len(employees)
    total_departments = employees["department"].nunique()
    avg_salary = int(employees["salary"].mean())

    current_month = datetime.now().month
    current_year = datetime.now().year

    monthly_attendance = attendance[
        (pd.to_datetime(attendance.date).dt.month == current_month) &
        (pd.to_datetime(attendance.date).dt.year == current_year) &
        (attendance.status == "Present")
    ]

    attendance_rate = (
        len(monthly_attendance) / (total_employees * 30)
    ) * 100 if total_employees else 0

    col1.metric("👥 Employees", total_employees)
    col2.metric("🏢 Departments", total_departments)
    col3.metric("💰 Avg Salary", f"₹{avg_salary:,}")
    col4.metric("🕒 Attendance Rate", f"{attendance_rate:.1f}%")

    st.divider()

    # ---------------- EMPLOYEES BY DEPARTMENT ----------------
    st.subheader("🏢 Employees by Department")
    dept_fig = px.bar(
        employees,
        x="department",
        title="Employee Distribution",
        color="department"
    )
    st.plotly_chart(dept_fig, use_container_width=True)

    # ---------------- SALARY DISTRIBUTION ----------------
    st.subheader("💸 Salary Distribution")
    salary_fig = px.histogram(
        employees,
        x="salary",
        nbins=10,
        title="Salary Spread"
    )
    st.plotly_chart(salary_fig, use_container_width=True)

    # ---------------- ATTENDANCE TREND ----------------
    st.subheader("📈 Monthly Attendance Trend")

    if not attendance.empty:
        attendance["date"] = pd.to_datetime(attendance["date"])
        monthly = attendance[attendance.status == "Present"]
        monthly = monthly.groupby(monthly["date"].dt.to_period("M")).size().reset_index(name="Present Days")
        monthly["date"] = monthly["date"].astype(str)

        att_fig = px.line(
            monthly,
            x="date",
            y="Present Days",
            markers=True,
            title="Monthly Attendance Trend"
        )
        st.plotly_chart(att_fig, use_container_width=True)

    # ---------------- INSIGHTS ----------------
    st.divider()
    st.subheader("🧠 Quick Insights")

    top_paid = employees.sort_values("salary", ascending=False).iloc[0]

    st.success(
        f"💼 Top Paid Employee: **{top_paid.name}** "
        f"(₹{top_paid.salary:,})"
    )
