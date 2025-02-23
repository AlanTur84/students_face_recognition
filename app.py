from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database file path
DATABASE = 'attendance.db'

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Home route to display attendance records
@app.route('/')
def index():
    conn = get_db_connection()
    records = conn.execute('SELECT * FROM attendance').fetchall()
    conn.close()
    return render_template('index.html', records=records)

# Route to add a new student
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        # Save the student's name and image (you can extend this to handle images)
        conn = get_db_connection()
        conn.execute('INSERT INTO students (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Route to update student information
@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        conn.execute('UPDATE students SET name = ? WHERE id = ?', (name, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    conn.close()
    return render_template('update_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)