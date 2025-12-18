import streamlit as st
import pandas as pd
import calendar
from datetime import date

def payroll_page(conn):
    st.header("💰 Payroll & Payslip Generator")
    st.caption("Monthly payroll calculation with downloadable payslips")
    st.divider()

    # ------------------ MONTH / YEAR ------------------
    month_name = st.selectbox("Month", list(calendar.month_name)[1:])
    month_num = list(calendar.month_name).index(month_name)
    year = st.selectbox("Year", range(2023, 2031))

    # ------------------ DATA ------------------
    employees = pd.read_sql("SELECT * FROM employee", conn)
    attendance = pd.read_sql("SELECT * FROM attendance", conn)

    if employees.empty:
        st.warning("No employees found")
        return

    # ------------------ PAYROLL CALCULATION ------------------
    payroll = []

    for _, emp in employees.iterrows():
        present_days = attendance[
            (attendance.emp_id == emp.id) &
            (attendance.status == "Present") &
            (pd.to_datetime(attendance.date).dt.month == month_num) &
            (pd.to_datetime(attendance.date).dt.year == year)
        ].shape[0]

        daily_salary = emp.salary / 30
        salary_payable = round(present_days * daily_salary, 2)

        payroll.append({
            "Employee ID": emp.id,
            "Employee Name": emp.name,
            "Department": emp.department,
            "Role": emp.role,
            "Monthly Salary": emp.salary,
            "Present Days": present_days,
            "Salary Payable": salary_payable
        })

    payroll_df = pd.DataFrame(payroll)
    st.dataframe(payroll_df, use_container_width=True)

    # ------------------ PAYSLIP GENERATOR ------------------
    st.divider()
    st.subheader("📄 Generate Payslip")

    emp_id = st.selectbox(
        "Select Employee",
        employees["id"],
        format_func=lambda x: employees.loc[employees.id == x, "name"].values[0]
    )

    emp = employees[employees.id == emp_id].iloc[0]
    emp_pay = payroll_df[payroll_df["Employee ID"] == emp_id].iloc[0]

    payslip_text = f"""
PAYSLIP – {month_name} {year}

Employee Name : {emp.name}
Department    : {emp.department}
Role          : {emp.role}

Monthly Salary: ₹{emp.salary}
Present Days  : {emp_pay['Present Days']}
Daily Salary  : ₹{emp.salary / 30:.2f}

----------------------------------
Salary Payable: ₹{emp_pay['Salary Payable']}
----------------------------------

Generated on  : {date.today()}
"""

    st.text_area("Payslip Preview", payslip_text, height=280)

    st.download_button(
        label="⬇️ Download Payslip",
        data=payslip_text,
        file_name=f"Payslip_{emp.name}_{month_name}_{year}.txt"
    )
