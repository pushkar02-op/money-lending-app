# Money Lending App

## 🚀 Setup & Run Instructions

### **1. Clone the Repository**

```sh
git clone https://github.com/YOUR_USERNAME/money-lending-app.git
cd money-lending-app
```

### **2. Set Up Virtual Environment**

```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### **3. Install Dependencies**

```sh
pip install -r requirements.txt
```

### **4. Configure Environment Variables**

Create a `.env` file in the root directory and add:

```
ENVIRONMENT=development
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_NAME=money_lending
DATABASE_USER=admin
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
```

### **5. Run the Application**

```sh
uvicorn main:app --reload
```

### **6. Run Tests**

```sh
pytest
```

---

## 📌 Project Overview

This is a **Money Lending Web Application** where an **Admin** assigns **Agents**, and **Agents** lend money on behalf of the Admin, tracking loans and repayments.

### **Tech Stack**

- **Frontend**: React (Planned for future)
- **Backend**: FastAPI (Python)
- **Database**: MySQL
- **Authentication**: JWT-based authentication
- **Deployment**: GitHub Actions for CI/CD (Planned)

### **Project Structure**

```
money-lending-app/
│── auth/            # Authentication module
│── config/          # Configuration settings
│── database.py      # Database connection
│── models/          # Database models
│── routes/          # API endpoints
│── schemas/         # Pydantic schemas
│── services/        # Business logic services
│── tests/           # Unit tests
│── main.py          # FastAPI app entry point
│── requirements.txt # Dependencies
│── .env             # Environment variables
│── .gitignore       # Git ignored files
│── README.md        # Project documentation
```

---

## 🔒 Security Best Practices

- **Hashed passwords** stored using bcrypt.
- **JWT authentication** with secure token expiration.
- **Role-Based Access Control (RBAC)** for Admins & Agents.
- **SQL Injection Prevention** using parameterized queries.
- **Logging & Error Handling** for system stability.

---

## 📚 API Endpoints (Planned)

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| POST   | `/auth/register` | Register a new user      |
| POST   | `/auth/login`    | Login and get JWT token  |
| GET    | `/users/me`      | Get current user profile |
| POST   | `/loans/create`  | Create a new loan        |
| GET    | `/loans/{id}`    | Get loan details         |
| POST   | `/payments/pay`  | Record a loan payment    |

---

## 🚀 Future Enhancements

- ✅ **Frontend UI in React**
- ✅ **Docker & Cloud Deployment**
- ✅ **Automated CI/CD with GitHub Actions**
- ✅ **Advanced Logging & Monitoring**

---

## 🥝 Contributing

1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Push to GitHub and open a Pull Request.

---

## 🐝 License

This project is licensed under the **MIT License**.
