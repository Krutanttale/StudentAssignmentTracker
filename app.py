
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import mysql.connector

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "root123",
    "database": "assignment_tracker"
}


class AssignmentTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Assignment & Deadline Tracker")
        self.root.geometry("900x600")
        self.root.configure(bg="#F2F5FA")

        self.conn = None
        self.cursor = None

        self.build_ui()

        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()

            self.cursor.execute(
                "SHOW COLUMNS FROM Assignments LIKE 'subject'"
            )
            if not self.cursor.fetchone():
                self.cursor.execute("""
                    ALTER TABLE Assignments
                    ADD COLUMN subject VARCHAR(100)
                    NOT NULL DEFAULT 'General'
                """)

            self.conn.commit()
            self.load_data()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Database Connection Error",
                f"Could not connect to MySQL.\n\n{error}"
            )

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def build_ui(self):
        tk.Label(
            self.root,
            text="STUDENT ASSIGNMENT TRACKER",
            font=("Arial", 20, "bold"),
            bg="#203864",
            fg="white",
            pady=18
        ).pack(fill="x")

        form = tk.Frame(self.root, bg="#F2F5FA", padx=20, pady=15)
        form.pack(fill="x")

        tk.Label(
            form, text="Assignment Title", bg="#F2F5FA"
        ).grid(row=0, column=0, sticky="w", padx=5)

        self.title_entry = tk.Entry(form, width=25)
        self.title_entry.grid(row=1, column=0, padx=5, pady=7)

        tk.Label(
            form, text="Subject", bg="#F2F5FA"
        ).grid(row=0, column=1, sticky="w", padx=5)

        self.subject_entry = tk.Entry(form, width=22)
        self.subject_entry.grid(row=1, column=1, padx=5, pady=7)

        tk.Label(
            form, text="Deadline (YYYY-MM-DD)", bg="#F2F5FA"
        ).grid(row=0, column=2, sticky="w", padx=5)

        self.deadline_entry = tk.Entry(form, width=20)
        self.deadline_entry.grid(row=1, column=2, padx=5, pady=7)
        self.deadline_entry.insert(0, date.today().isoformat())

        buttons = tk.Frame(self.root, bg="#F2F5FA")
        buttons.pack(pady=8)

        ttk.Button(
            buttons, text="Add Assignment",
            command=self.add_assignment
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            buttons, text="Update Status",
            command=self.update_status
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            buttons, text="Delete Assignment",
            command=self.delete_assignment
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            buttons, text="Clear Fields",
            command=self.clear_fields
        ).grid(row=0, column=3, padx=5)

        table_frame = tk.Frame(self.root, padx=20, pady=15)
        table_frame.pack(fill="both", expand=True)

        columns = ("number", "title", "subject", "deadline", "status")

        self.table = ttk.Treeview(
            table_frame, columns=columns,
            show="headings", height=13
        )

        headings = {
            "number": "No.",
            "title": "Assignment Title",
            "subject": "Subject",
            "deadline": "Deadline",
            "status": "Status"
        }

        widths = {
            "number": 55,
            "title": 260,
            "subject": 180,
            "deadline": 150,
            "status": 120
        }

        for column in columns:
            self.table.heading(column, text=headings[column])
            self.table.column(
                column, width=widths[column], anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.table.bind(
            "<<TreeviewSelect>>", self.select_assignment
        )

        tk.Label(
            self.root,
            text="Database: MySQL | Container: Docker",
            bg="#203864", fg="white", pady=9
        ).pack(fill="x")

    def load_data(self):
        if not self.cursor:
            return

        for item in self.table.get_children():
            self.table.delete(item)

        self.cursor.execute("""
            SELECT assignment_id, title, subject, deadline, status
            FROM Assignments
            ORDER BY assignment_id ASC
        """)

        rows = self.cursor.fetchall()

        # Keep the real database ID separate from the visible row number.
        for number, row in enumerate(rows, start=1):
            db_id, title, subject, deadline, status = row

            self.table.insert(
                "", "end",
                iid=str(db_id),
                values=(number, title, subject, deadline, status)
            )

    def add_assignment(self):
        title = self.title_entry.get().strip()
        subject = self.subject_entry.get().strip()
        deadline = self.deadline_entry.get().strip()

        if not title or not subject or not deadline:
            messagebox.showwarning(
                "Missing Information", "Please fill in all fields."
            )
            return

        try:
            date.fromisoformat(deadline)
        except ValueError:
            messagebox.showwarning(
                "Invalid Date", "Use YYYY-MM-DD format."
            )
            return

        try:
            self.cursor.execute("""
                INSERT INTO Assignments (title, subject, deadline, status)
                VALUES (%s, %s, %s, 'Pending')
            """, (title, subject, deadline))

            self.conn.commit()
            self.load_data()
            self.clear_fields()

            messagebox.showinfo(
                "Success", "Assignment added successfully!"
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

    def select_assignment(self, event=None):
        selected = self.table.selection()
        if not selected:
            return

        values = self.table.item(selected[0], "values")

        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, values[1])

        self.subject_entry.delete(0, tk.END)
        self.subject_entry.insert(0, values[2])

        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, str(values[3]))

    def update_status(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Select Assignment", "Select an assignment first."
            )
            return

        # iid contains the actual database ID, not the visible row number.
        db_id = int(selected[0])
        values = self.table.item(selected[0], "values")
        new_status = (
            "Completed" if values[4] == "Pending" else "Pending"
        )

        try:
            self.cursor.execute("""
                UPDATE Assignments
                SET status = %s
                WHERE assignment_id = %s
            """, (new_status, db_id))

            self.conn.commit()
            self.load_data()

            messagebox.showinfo(
                "Updated", f"Status changed to {new_status}."
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

    def delete_assignment(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning(
                "Select Assignment", "Select an assignment to delete."
            )
            return

        db_id = int(selected[0])
        values = self.table.item(selected[0], "values")

        if not messagebox.askyesno(
            "Confirm Delete", f"Delete '{values[1]}'?"
        ):
            return

        try:
            self.cursor.execute("""
                DELETE FROM Assignments
                WHERE assignment_id = %s
            """, (db_id,))

            self.conn.commit()
            self.load_data()
            self.clear_fields()

            messagebox.showinfo(
                "Deleted", "Assignment deleted successfully."
            )
        except mysql.connector.Error as error:
            messagebox.showerror("Database Error", str(error))

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.deadline_entry.insert(0, date.today().isoformat())

        for item in self.table.selection():
            self.table.selection_remove(item)

    def close_app(self):
        if self.cursor:
            self.cursor.close()

        if self.conn and self.conn.is_connected():
            self.conn.close()

        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = AssignmentTracker(root)
    root.mainloop()
