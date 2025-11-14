# ==================== SETUP INSTRUCTIONS ====================

SETUP INSTRUCTIONS:

1. Install PostgreSQL:

   - Windows: Download from https://www.postgresql.org/download/windows/
   - Mac: brew install postgresql
   - Linux: sudo apt-get install postgresql postgresql-contrib

2. Start PostgreSQL service:

   - Windows: Use Services or pg_ctl
   - Mac: brew services start postgresql
   - Linux: sudo service postgresql start

3. Run the database script:
   psql -U postgres -f db_script.sql

4. Create virtual environment:
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate

5. Install dependencies:
   pip install -r requirements.txt

6. Copy .env.example to .env and update values:
   cp .env.example .env

7. Update .env file with your actual values:

   - DATABASE_URL (PostgreSQL connection string)
   - SECRET_KEY (generate a secure random string)
   - SMTP credentials (for email functionality)

8. Run the application:
   python main.py

   Or with uvicorn:
   uvicorn main:app --reload

9. Access the API:

   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

10. Test the endpoints:
    - POST /api/auth/register - Register new user
    - POST /api/auth/login - Login user
    - POST /api/auth/verify-otp - Verify email with OTP
    - POST /api/auth/forgot-password - Request password reset
    - POST /api/auth/reset-password - Reset password with OTP
    - GET /api/auth/me - Get current user info (requires auth)
    - GET /api/auth/admin/users - Get all users (admin only)

API AUTHENTICATION:
Use Bearer token in Authorization header:
Authorization: Bearer <your_access_token>

DATABASE CONNECTION STRING FORMAT:
postgresql://username:password@host:port/database_name

Example:
postgresql://postgres:mypassword@localhost:5432/auth_db
