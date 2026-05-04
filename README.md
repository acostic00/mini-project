# 🏢 Professional HRMS – Human Resource Management System

A modern **Human Resource Management System (HRMS)** built using **Python, Streamlit, SQLite, and Plotly**.
This application automates core HR operations such as employee management, attendance tracking, payroll processing, and analytics visualization.

---

## 🚀 Features

* 🔐 **Admin Authentication**
* 👥 **Employee Management (CRUD)**
  Add, update, delete, and view employee records
* 🕒 **Attendance Tracking**
  Daily attendance with Present/Absent status
* 💰 **Payroll System**
  Automatic salary calculation based on attendance
* 📄 **Payslip Generator**
  Download employee payslips
* 📊 **HR Analytics Dashboard**

  * Department-wise employee distribution
  * Salary insights
  * Attendance summary (pie chart)
  * Attendance trend line (time-series)
* 📈 **Interactive Charts** using Plotly
* 🗄️ **SQLite Database Integration**
* 🧩 **Modular Code Architecture**

---

## 🛠️ Tech Stack

| Layer           | Technology   |
| --------------- | ------------ |
| Frontend        | Streamlit    |
| Backend         | Python       |
| Database        | SQLite       |
| Data Processing | Pandas       |
| Visualization   | Plotly       |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```
hrms-python/
│
├── app.py               # Main application entry point
├── database.py          # DB connection & table creation
├── auth.py              # Login authentication
├── employees.py         # Employee CRUD operations
├── attendance.py        # Attendance management
├── payroll.py           # Payroll & payslip generation
├── hr_analytics.py      # Analytics & visualization
│
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation
├── .gitignore           # Ignored files
```

---

## ▶️ How to Run Locally

```bash
# Clone the repository
git clone https://github.com/<your-username>/mini-project.git

# Navigate to project folder
cd mini-project

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m streamlit run app.py
```

---

## 🔐 Demo Credentials

```
Username: admin
Password: admin123
```

> ⚠️ Note: These credentials are for demo/academic purposes only.

---

## 📊 Database Schema

### Employee Table

| Column     | Description    |
| ---------- | -------------- |
| id         | Primary Key    |
| name       | Employee name  |
| department | Department     |
| role       | Job role       |
| salary     | Monthly salary |

### Attendance Table

| Column | Description               |
| ------ | ------------------------- |
| id     | Primary Key               |
| emp_id | Employee ID (Foreign Key) |
| date   | Attendance date           |
| status | Present / Absent          |

---

## 📸 Screenshots

> Add screenshots here for better presentation

* Dashboard
* Employee Management
* Attendance Page
* Payroll Page
* Analytics Dashboard

---

## 🎯 Project Highlights

* End-to-end HR workflow automation
* Real-world payroll logic implementation
* Data-driven HR analytics
* Clean modular architecture
* Beginner-friendly yet scalable design

---

## 🔮 Future Enhancements

* Role-based access (Admin / HR / Employee)
* Email payslip delivery
* Leave management system
* Cloud database (MySQL/PostgreSQL)
* REST API backend (Spring Boot / FastAPI)
* Deployment on Streamlit Cloud

---

## 📌 Academic Note

This project was developed as part of an academic mini-project and demonstrates:

* CRUD operations
* Database integration
* Business logic implementation
* Data analytics and visualization

---

## 👨‍💻 Author

**Praful Jain P**
B.E – Computer Science (AI)
Mini Project – HRMS

---
