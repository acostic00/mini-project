import streamlit as st
from database import get_connection, create_tables, seed_demo_data
from auth import login
from employees import employee_page
from attendance import attendance_page
from payroll import payroll_page
from hr_analytics import analytics_page 
from dashboard import dashboard_page
st.set_page_config("Professional HRMS", layout="wide")

login()

conn = get_connection()
create_tables(conn)
seed_demo_data(conn)

menu = st.sidebar.radio(
    "HRMS MENU",
    ["Dashboard", "Employees", "Attendance", "Payroll", "Analytics"]
)

if menu == "Dashboard":
    dashboard_page(conn)
elif menu == "Employees":
    employee_page(conn)
elif menu == "Attendance":
    attendance_page(conn)
elif menu == "Payroll":
    payroll_page(conn)
elif menu == "Analytics":
    analytics_page(conn)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
