from flask import Flask, request, redirect, render_template
from dotenv import load_dotenv
import pymysql
import os

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route("/")
def home():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM tasks
        ORDER BY created_at DESC
    """)

    tasks = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks
    )


@app.route("/add", methods=["POST"])
def add_task():

    person_name = request.form["person_name"]
    task_name = request.form["task_name"]
    status = request.form["status"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks
        (
            person_name,
            task_name,
            status
        )
        VALUES (%s, %s, %s)
        """,
        (
            person_name,
            task_name,
            status
        )
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_task(id):

    conn = get_connection()
    cur = conn.cursor()

    if request.method == "POST":

        person_name = request.form["person_name"]
        task_name = request.form["task_name"]
        status = request.form["status"]

        cur.execute(
            """
            UPDATE tasks
            SET person_name=%s,
                task_name=%s,
                status=%s
            WHERE id=%s
            """,
            (
                person_name,
                task_name,
                status,
                id
            )
        )

        conn.commit()
        conn.close()

        return redirect("/")

    cur.execute(
        """
        SELECT *
        FROM tasks
        WHERE id=%s
        """,
        (id,)
    )

    task = cur.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        task=task
    )


@app.route("/delete/<int:id>")
def delete_task(id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM tasks
        WHERE id=%s
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/health")
def health():

    try:

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT 1")

        result = cur.fetchone()

        conn.close()

        if result:

            return {
                "status": "healthy",
                "application": "running",
                "database": "connected"
            }, 200

        return {
            "status": "unhealthy"
        }, 500

    except Exception as e:

        return {
            "status": "unhealthy",
            "error": str(e)
        }, 500

@app.route("/health")
def health():
    return {"status":"broken"}, 500

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
