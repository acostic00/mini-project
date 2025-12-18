import streamlit as st
import pandas as pd

def employee_page(conn):
    st.header("👥 Employee Management")
    st.caption("Add, view and manage employees")
    st.divider()

    # ---------- ADD EMPLOYEE ----------
    st.subheader("➕ Add Employee")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Employee Name")
        department = st.text_input("Department")
    with col2:
        role = st.text_input("Role")
        salary = st.number_input("Monthly Salary (₹)", min_value=0)

    if st.button("Add Employee"):
        conn.execute(
            "INSERT INTO employee (name, department, role, salary) VALUES (?, ?, ?, ?)",
            (name, department, role, salary)
        )
        conn.commit()
        st.success("Employee added successfully")
        st.rerun()

    st.divider()

    # ---------- EMPLOYEE TABLE (EDITABLE) ----------
    st.subheader("📋 Employee Records (Editable)")
    
    df = pd.read_sql("SELECT * FROM employee", conn)
    
    if not df.empty:
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="emp_editor"
        )
    
        if st.button("💾 Save Changes"):
            conn.execute("DELETE FROM employee")
            edited_df.to_sql("employee", conn, if_exists="append", index=False)
            conn.commit()
            st.success("Changes saved successfully")
            st.rerun()
        else:
            st.info("No employees available")
    
    
        st.caption("📌 Sorted alphabetically by employee name")

    # ---------- DELETE ----------
    st.divider()
    st.subheader("🗑️ Delete Employee")

    emp_id = st.selectbox(
        "Select Employee ID to Delete",
        df["id"],
        format_func=lambda x: f"{x} - {df[df['id']==x]['name'].values[0]}"
    )

    if st.button("Delete Employee"):
        conn.execute("DELETE FROM employee WHERE id = ?", (emp_id,))
        conn.commit()
        st.success("Employee deleted successfully")
        st.rerun()
