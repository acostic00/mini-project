import streamlit as st
import pandas as pd
import plotly.express as px


def analytics_page(conn):
    st.title("📊 HR Analytics Dashboard")
    st.caption("Clear insights to support HR decision-making")
    st.divider()

    # ---------------- LOAD DATA ----------------
    employees = pd.read_sql("SELECT * FROM employee", conn)
    attendance = pd.read_sql("SELECT * FROM attendance", conn)

    if employees.empty:
        st.warning("No employee data available yet")
        return

    # ---------------- KPI SECTION ----------------
    st.subheader("📌 Key HR Metrics")

    col1, col2, col3 = st.columns(3)

    total_emp = len(employees)
    avg_salary = int(employees["salary"].mean())
    total_payroll = int(employees["salary"].sum())

    col1.metric("👥 Total Employees", total_emp)
    col2.metric("💰 Average Salary", f"₹{avg_salary:,}")
    col3.metric("🏦 Monthly Payroll", f"₹{total_payroll:,}")

    st.divider()

    # ---------------- DASHBOARD SUMMARY ----------------
    st.subheader("📊 Attendance Overview")

    if attendance.empty:
        st.info("Attendance data not available")
    else:
        summary_df = attendance.copy()
        summary_df["status"] = summary_df["status"].str.capitalize()

        status_count = summary_df["status"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]

        fig_summary = px.pie(
            status_count,
            names="Status",
            values="Count",
            hole=0.5,
            title="Overall Attendance Summary",
            color="Status",
            color_discrete_map={
                "Present": "#2ECC71",
                "Absent": "#E74C3C"
            }
        )

        fig_summary.update_traces(textinfo="percent+label")
        fig_summary.update_layout(
            legend_title="Attendance Status",
            showlegend=True
        )

        st.plotly_chart(fig_summary, use_container_width=True)


    # ---------------- EMPLOYEES BY DEPARTMENT ----------------
    st.subheader("🏢 Workforce Distribution")

    dept_df = employees["department"].value_counts().reset_index()
    dept_df.columns = ["Department", "Employee Count"]

    fig_dept = px.bar(
        dept_df,
        x="Department",
        y="Employee Count",
        color="Department",
        text="Employee Count",
        title="Employees by Department"
    )
    fig_dept.update_layout(showlegend=False)

    st.plotly_chart(fig_dept, use_container_width=True)

    # ---------------- SALARY ANALYSIS ----------------
    st.subheader("💸 Salary Insights")

    fig_salary = px.histogram(
        employees,
        x="salary",
        nbins=8,
        title="Salary Distribution",
        labels={"salary": "Monthly Salary (₹)"}
    )

    st.plotly_chart(fig_salary, use_container_width=True)

    # ---------------- ATTENDANCE ANALYTICS ----------------
    st.subheader("🕒 Attendance Analysis")

    if attendance.empty:
        st.info("Attendance data not available yet")
        return

    attendance["date"] = pd.to_datetime(attendance["date"], errors="coerce")

    attendance["month"] = attendance["date"].dt.strftime("%Y-%m")

    selected_month = st.selectbox(
        "Select Month",
        sorted(attendance["month"].dropna().unique())
    )

    month_data = attendance[attendance["month"] == selected_month]

    present_data = month_data[
        month_data["status"].str.lower() == "present"
    ]

    if present_data.empty:
        st.warning("No attendance records for this month")
        return

    att_summary = (
        present_data.groupby("emp_id")
        .size()
        .reset_index(name="Present Days")
    )

    att_summary = att_summary.merge(
        employees[["id", "name"]],
        left_on="emp_id",
        right_on="id",
        how="left"
    )

    fig_att = px.bar(
        att_summary,
        x="name",
        y="Present Days",
        title=f"Employee Attendance – {selected_month}",
        labels={"name": "Employee Name"}
    )

    st.plotly_chart(fig_att, use_container_width=True)

    # ---------------- ATTENDANCE TREND LINE ----------------
    st.subheader("📈 Attendance Trend Over Time")

    # Filter only Present records
    trend_data = attendance[
        attendance["status"].str.lower() == "present"
    ].copy()

    if trend_data.empty:
        st.info("No attendance trend data available")
        return

    # Convert date properly
    trend_data["date"] = pd.to_datetime(trend_data["date"], errors="coerce")

    # Group by date
    daily_attendance = (
        trend_data.groupby(trend_data["date"].dt.date)
        .size()
        .reset_index(name="Present Employees")
    )

    # Line chart
    fig_trend = px.line(
        daily_attendance,
        x="date",
        y="Present Employees",
        markers=True,
        title="Daily Attendance Trend",
        labels={
            "date": "Date",
            "Present Employees": "No. of Employees Present"
        }
    )

    fig_trend.update_traces(line=dict(width=3))
    fig_trend.update_layout(
        xaxis_title="Date",
        yaxis_title="Employees Present",
        hovermode="x unified"
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    # ---------------- HR INSIGHTS ----------------
    st.divider()
    st.subheader("🧠 HR Insights")

    st.markdown(
        """
        - Departments with more employees may need **additional HR policies**
        - Salary distribution helps identify **pay imbalance**
        - Attendance trends help detect **engagement or discipline issues**
        - This dashboard supports **data-driven HR decisions**
        """
    )
