import os
import sqlite3
from pathlib import Path

from flask import (
    Flask, render_template, request,
    session, redirect, url_for, flash
)

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "Please configure the FLASK_SECRET_KEY environment variable."
    )

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "database.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        )""")

    conn.commit()
    conn.close()

    print("Database location:", DATABASE)
    print("Database exists:", DATABASE.exists())
    print("Students table is ready!")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        age = request.form.get("age", "").strip()
        city = request.form.get("city", "").strip()

        if not username:
            return render_template(
                "form.html",
                error="Please enter your username."
            )

        if not age or not age.isdigit():
            return render_template(
                "form.html",
                error="Please enter a valid age."
            )

        age = int(age)

        if age < 1 or age > 120:
            return render_template(
                "form.html",
                error="Age must be between 1 and 120."
            )

        if not city:
            return render_template(
                "form.html",
                error="Please enter your city."
            )

        conn = get_db_connection()

        try:
            conn.execute(
                """
                INSERT INTO students (username, age, city)
                VALUES (?, ?, ?)
                """,
                (username, age, city)
            )

            conn.commit()

            print("Student details saved successfully!")
            print("Username:", username)
            print("Age:", age)
            print("City:", city)
            print("Database path:", DATABASE)

        except sqlite3.Error as e:
            print("Database error:", e)

            return render_template(
                "form.html",
                error="Unable to save details to the database."
            )

        finally:
            conn.close()

        session["username"] = username
        session["age"] = age
        session["city"] = city

        flash("Your details have been saved successfully!", "success")

        return redirect(url_for("profile"))

    return render_template("form.html")

@app.route("/check-database")
def check_database():

    conn = get_db_connection()

    try:
        students = conn.execute(
            "SELECT * FROM students"
        ).fetchall()

        return {
            "database_path": str(DATABASE),
            "total_records": len(students),
            "students": [dict(student) for student in students]
        }

    finally:
        conn.close()


@app.route("/profile")
def profile():

    username = session.get("username")

    if not username:
        flash("Please enter your details first.", "error")
        return redirect(url_for("login"))

    return render_template(
        "profile.html",
        username=username,
        age=session.get("age"),
        city=session.get("city")
    )


@app.route("/students")
def students():

    conn = get_db_connection()

    try:
        student_records = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()
    finally:
        conn.close()

    return render_template(
        "students.html",
        students=student_records
    )


@app.route("/logout", methods=["POST"])
def logout():

    session.clear()

    flash("You have been logged out successfully!", "success")

    return redirect(url_for("home"))


@app.route("/logmessage")
def logmess():
    return render_template("logout.html")

@app.route("/students")
def stude():
    conn = get_db_connection()

    try:
        student_records = conn.execute(
            "SELECT * FROM students ORDER BY id DESC"
        ).fetchall()
    finally:
        conn.close()

    return render_template(
        "students.html",
        students=student_records
    )


if __name__ == "__main__":
    create_table()
    app.run(debug=True)