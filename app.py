from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_connection():
    conn = sqlite3.connect("employees.db")
    conn.row_factory = sqlite3.Row
    return conn

# create table
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            position TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    conn.close()
    return render_template('employees.html', employees=employees)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    email = request.form.get('email')
    position = request.form.get('position')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employees (name, email, position) VALUES (?, ?, ?)",
        (name, email, position)
    )
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == "__main__":
    app.run()