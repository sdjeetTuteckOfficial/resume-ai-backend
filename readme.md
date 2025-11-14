---
# 🚀 Project Setup & Installation Guide

This guide will help you set up and run the application locally with PostgreSQL and FastAPI.
---

## 📦 Prerequisites

- **Python 3.8+**
- **PostgreSQL 12+**
- **pip & virtualenv**

---

## 🗄️ 1. Install PostgreSQL

### **Windows**

Download the installer:
[https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)

### **Mac**

```sh
brew install postgresql
```

### **Linux**

```sh
sudo apt-get install postgresql postgresql-contrib
```

---

## ▶️ 2. Start PostgreSQL Service

### **Windows**

Use **Services** or:

```sh
pg_ctl start
```

### **Mac**

```sh
brew services start postgresql
```

### **Linux**

```sh
sudo service postgresql start
```

---

## 🗃️ 3. Run the Database Script

```sh
psql -U postgres -f db_script.sql
```

---

## 🐍 4. Create Virtual Environment

```sh
python -m venv venv
```

Activate:

### **Mac/Linux**

```sh
source venv/bin/activate
```

### **Windows**

```sh
venv\Scripts\activate
```

---

## 📥 5. Install Dependencies

```sh
pip install -r requirements.txt
```

---

## 🔐 6. Configure Environment Variables

Copy example file:

```sh
cp .env.example .env
```

Update the following values in **.env**:

- `DATABASE_URL` → PostgreSQL connection string
- `SECRET_KEY` → Strong random key
- `SMTP_*` → Email credentials

**PostgreSQL connection string format:**

```
postgresql://username:password@host:port/database_name
```

Example:

```
postgresql://postgres:mypassword@localhost:5432/resume_ai_db
```

---

## 🚀 7. Run the Application

### Option 1 — Normal run

```sh
python main.py
```

### Option 2 — With Uvicorn (recommended)

```sh
uvicorn main:app --reload
```

---

## 🌐 8. Access API

- API Base URL → [http://localhost:8000](http://localhost:8000)
- Swagger Docs → [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 9. Test Authentication Endpoints

| Endpoint                    | Method | Description                      |
| --------------------------- | ------ | -------------------------------- |
| `/api/auth/register`        | POST   | Register new user                |
| `/api/auth/login`           | POST   | Login user                       |
| `/api/auth/verify-otp`      | POST   | Verify email OTP                 |
| `/api/auth/forgot-password` | POST   | Request password reset           |
| `/api/auth/reset-password`  | POST   | Reset password using OTP         |
| `/api/auth/me`              | GET    | Get current user (requires auth) |
| `/api/auth/admin/users`     | GET    | List all users (admin only)      |

---

## 🔑 Authentication

Use Bearer token in request header:

```
Authorization: Bearer <your_access_token>
```
