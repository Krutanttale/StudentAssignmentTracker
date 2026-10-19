# 📚 Student Assignment & Deadline Tracker (Desktop Application)

A simple **Student Assignment & Deadline Tracker** built using **Python (Tkinter)** and **MySQL** with **Docker** for database setup.  
It allows students to **add, view, update status, and delete assignments** while keeping track of subjects and deadlines.  
Designed as a practical project for learning Python GUI development and database connectivity.

---

## 🚀 Features

### 🔹 Frontend (Python Tkinter)
- Clean desktop interface with a table to display assignments
- Add assignments with title, subject, and deadline
- Select an assignment to view and edit its input fields
- Update assignment status between `Pending` and `Completed`
- Delete assignments with confirmation
- Clear input fields
- Validate required fields and deadline format (`YYYY-MM-DD`)
- Automatically numbered rows in the table

### 🔹 Backend (Python + MySQL)
- Connects to a MySQL database using `mysql-connector-python`
- Stores assignment records in the `Assignments` table
- Supports Create, Read, Update, and Delete (CRUD) operations
- Uses the real database ID internally, separate from the displayed row number
- Docker Compose configuration for MySQL 8.0
- Persistent database storage through a Docker volume

---

## 📂 Folder Structure

```text
STUDENT-ASSIGNMENT-TRACKER/
│
├── app.py
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Tech Stack

**Frontend:**
- Python
- Tkinter
- ttk widgets

**Backend & Database:**
- MySQL 8.0
- `mysql-connector-python`
- Docker
- Docker Compose

---

## 🧑‍💻 Installation & Setup (Local)

### 1️⃣ Clone the Repository

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd <YOUR-REPOSITORY-FOLDER>
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2️⃣ Install the Python Dependency

```bash
python -m pip install mysql-connector-python
```

### 3️⃣ Start MySQL with Docker

Make sure Docker Desktop is running. From the folder containing `docker-compose.yml`, run:

```bash
docker compose up -d
```

This starts the MySQL container and creates the `assignment_tracker` database. The database is available on port `3307` on your computer.

Check the container:

```bash
docker compose ps
```

Wait until MySQL has finished starting before launching the application.

### 4️⃣ Create the Assignments Table

The app checks whether the `subject` column exists, but it does not create the entire table automatically. If the `Assignments` table does not already exist, connect to MySQL:

```bash
docker exec -it assignment_db mysql -uroot -p
```

Enter the configured password, then run:

```sql
USE assignment_tracker;

CREATE TABLE IF NOT EXISTS Assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    subject VARCHAR(100) NOT NULL DEFAULT 'General',
    deadline DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending'
);
```

### 5️⃣ Run the Application

```bash
python app.py
```

The Student Assignment Tracker desktop window should open.

---

## 🖥️ How to Use

1. Enter the assignment title.
2. Enter the subject.
3. Enter the deadline in `YYYY-MM-DD` format, for example `2026-10-25`.
4. Click **Add Assignment** to save it.
5. Select an assignment and click **Update Status** to switch between `Pending` and `Completed`.
6. Select an assignment and click **Delete Assignment** to remove it after confirmation.
7. Click **Clear Fields** to reset the input fields.

---

## 🗄️ Database Configuration

The current application uses the following MySQL settings:

| Setting | Value |
|---|---|
| Host | `127.0.0.1` |
| Port | `3307` |
| User | `root` |
| Password | `root123` |
| Database | `assignment_tracker` |

These settings must match `docker-compose.yml` and `app.py`.

**Security note:** These are the credentials currently present in the project files. Do not use this configuration for a public or production deployment. Avoid committing real passwords to GitHub; use environment variables instead.

---

## 🐳 Docker Commands

Start the database:

```bash
docker compose up -d
```

Stop the database while retaining saved data:

```bash
docker compose down
```

Stop the database and delete its persistent volume (this permanently deletes the stored database data):

```bash
docker compose down -v
```

---

## 🔐 Future Improvements

- Search assignments by title or subject
- Filter assignments by status
- Highlight overdue and upcoming deadlines
- Add reminders for assignment deadlines
- Move database credentials into environment variables
- Add automated tests and application screenshots

---

## ✨ Project Information

👨‍💻 **Project:** Student Assignment & Deadline Tracker  
📚 **Category:** Python GUI and Database Management  
🛠️ **Version:** 1.0.0
