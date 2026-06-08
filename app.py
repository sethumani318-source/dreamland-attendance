from flask import Flask, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

conn = sqlite3.connect("attendance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id TEXT,
    name TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == "DREAMLAND" and password == "08072004":
            return dashboard()

        return "<h2>Invalid Username or Password</h2>"

    return """
    <h2>DREAMLAND VENTURES LOGIN</h2>

    <form method="POST">
        Username:<br>
        <input name="username"><br><br>

        Password:<br>
        <input type="password" name="password"><br><br>

        <button type="submit">Login</button>
    </form>
    """

def dashboard():

    return """
    <h1>DREAMLAND DASHBOARD</h1>

    <h3>Mark Attendance</h3>

    <a href="/mark/EMP001/Gayathri">
        <button>EMP001 - Gayathri</button>
    </a>

    <br><br>

    <a href="/mark/EMP002/Ramanan">
        <button>EMP002 - Ramanan</button>
    </a>

    <br><br>

    <a href="/mark/EMP003/Manikkam">
        <button>EMP003 - Manikkam</button>
    </a>

    <br><br>

    <a href="/report">
        <button>Attendance Report</button>
    </a>
    """

@app.route("/mark/<emp_id>/<name>")
def mark(emp_id, name):

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    cursor.execute(
        "INSERT INTO attendance(emp_id,name,date,time) VALUES(?,?,?,?)",
        (emp_id, name, date, time)
    )

    conn.commit()

    return f"""
    <h2>Attendance Saved</h2>

    Employee: {name}<br>
    Date: {date}<br>
    Time: {time}<br><br>

    <a href="/">Back to Login</a>
    """

@app.route("/report")
def report():

    cursor.execute(
        "SELECT emp_id,name,date,time FROM attendance ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    html = """
    <h1>Attendance Report</h1>

    <table border="1" cellpadding="10">
    <tr>
        <th>Employee ID</th>
        <th>Name</th>
        <th>Date</th>
        <th>Time</th>
    </tr>
    """

    for row in rows:
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[3]}</td>
        </tr>
        """

    html += "</table>"

    return html

if __name__ == "__main__":
    app.run(debug=True)