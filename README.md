# School Fees Management System

A comprehensive school fees management system built with Python Flask, SQLite, and Bootstrap.

## Features

- **Admin Login System**: Secure login with password hashing
- **Student Management**: Add, edit, delete, and search students
- **Class Management**: Pre-defined school classes (Foundation 1 - JHS 3)
- **Fees Setup**: Set term-based fees for each class
- **Payment Recording**: Record payments with automatic receipt generation
- **Dashboard**: Overview of key statistics
- **Reports**: Fees per class, students owing, fees per term
- **Export**: PDF and Excel export for reports
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. **Clone or download** the project files to your local machine.

2. **Install Python dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```
   python database/init_db.py
   ```

4. **(Optional) Add sample data**:
   ```
   python database/sample_data.py
   ```

## Environment Variables

- `SECRET_KEY`: Set this to a strong random value in production.
- `FLASK_ENV`: Set to `production` when deploying.
- `DATABASE_URL`: Optional PostgreSQL connection string. If set, the app uses PostgreSQL instead of local SQLite.

## PostgreSQL Migration

If you already have data in the local SQLite database at `database/school_fees.db`, use the migration helper to copy it into PostgreSQL:

```powershell
python migrate_sqlite_to_postgres.py --postgres "postgres://user:password@host:port/dbname"
```

Or, if `DATABASE_URL` is already set in your environment:

```powershell
$env:DATABASE_URL="postgres://user:password@host:port/dbname"
python migrate_sqlite_to_postgres.py
```

After migration, start the app with `DATABASE_URL` set so it uses PostgreSQL.

## Running the Application

1. **Start the Flask application**:
   ```
   python app.py
   ```

2. **Open your web browser** and go to:
   ```
   http://localhost:5000
   ```

3. **Login** with the default credentials:
   - Username: `admin`
   - Password: `admin123`

## Project Structure

```
school_fees_system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database/
│   ├── init_db.py        # Database initialization
│   ├── sample_data.py    # Sample data insertion
│   └── school_fees.db    # SQLite database (created automatically)
├── migrate_sqlite_to_postgres.py  # Optional SQLite-to-Postgres migration helper
├── models/
│   └── database.py       # Database models and operations
├── static/
│   ├── css/
│   │   └── style.css     # Custom CSS styles
│   └── js/
│       └── main.js       # Custom JavaScript
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── students.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── classes.html
│   ├── fees.html
│   ├── payments.html
│   ├── add_payment.html
│   ├── receipt.html
│   ├── reports.html
│   ├── report_fees_per_class.html
│   ├── report_students_owing.html
│   └── report_fees_per_term.html
└── README.md
```

## Usage Guide

### Managing Students
1. Go to **Students** in the navigation
2. Click **Add Student** to create new student records
3. Use the search bar to find students by name, ID, or class
4. Click **Edit** or **Delete** to modify student information

### Setting Up Fees
1. Go to **Fees** in the navigation
2. Select a class, term, and enter the fee amount
3. Click **Set Fee** to save the fee structure

### Recording Payments
1. Go to **Payments** in the navigation
2. Click **Record Payment**
3. Select a student, enter payment details
4. The system will automatically generate a receipt

### Viewing Reports
1. Go to **Reports** in the navigation
2. Choose from available reports:
   - Fees per Class
   - Students Owing Fees
   - Fees per Term
3. Export reports to PDF or Excel

## Free Hosting / Deployment
This project can be deployed to a free Python hosting service.

### Option 1: Render (free tier)
1. Create a GitHub repository for this project.
2. Sign up at https://render.com and connect your GitHub account.
3. Create a new Web Service and select this repository.
4. Set the build command to:
   ```bash
   pip install -r requirements.txt
   ```
5. Set the start command to:
   ```bash
   gunicorn app:app
   ```
6. Add environment variables:
   - `SECRET_KEY` = a strong random string
   - `FLASK_ENV` = `production`
   - `DATABASE_URL` = your Postgres connection string (optional, for persistent storage)

### Option 2: PythonAnywhere (free tier)
1. Sign up at https://www.pythonanywhere.com.
2. Upload the project files or clone your GitHub repo.
3. In the Web tab, set the working directory to the project folder.
4. Install dependencies in a Bash console:
   ```bash
   pip install -r requirements.txt
   ```
5. Set `FLASK_APP` to `app.py` and use the default WSGI config.
6. Add `SECRET_KEY` in a `bashrc` file or via PythonAnywhere environment settings.

### Recommended production settings
- Use `SECRET_KEY` from the environment
- Set `FLASK_ENV=production`
- Do not run debug mode in production
- Use a production WSGI server such as Gunicorn

## Database Schema

### Tables
- **users**: Admin user accounts
- **classes**: School classes
- **students**: Student information
- **fees_structure**: Fee amounts per class and term
- **payments**: Payment records with receipts

## Security Notes

- Change the default admin password after first login
- The application uses password hashing for security
- Session management is handled by Flask-Login

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **PDF Generation**: ReportLab
- **Excel Export**: OpenPyXL

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please check the code comments or create an issue in the repository.