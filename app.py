import sqlite3
from flask import Flask, render_template, request, redirect,session

app = Flask(__name__)
app.secret_key="secret123"


@app.route('/')
def home():
    if "user" in session:
        return render_template('index.html')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()

        conn.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid credentials"

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except:
            return "User already exists!"

        conn.close()
        return redirect('/login')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

@app.route('/result', methods=['POST'])
def result():
    qualification = request.form['qualification'].lower()
    sector = request.form['sector']
    interest = request.form.get('interest', '').lower()

    jobs = []

    if "b.tech" in qualification or "btech" in qualification:
        if sector == "Private":
            if "coding" in interest:
                jobs = ["Software Developer", "Web Developer", "AI Engineer"]
            elif "design" in interest:
                jobs = ["UI/UX Designer", "Graphic Designer"]
            else:
                jobs = ["Data Analyst", "IT Support"]
        else:
            jobs = ["GATE", "PSU Jobs", "UPSC"]

    elif "diploma" in qualification:
        jobs = ["Technician", "Junior Engineer"]

    else:
        jobs = ["Explore general career options"]
    print("form submitted")
    return render_template('result.html', jobs=jobs)

def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')

    conn.commit()
    conn.close()

init_db()
if __name__ == '__main__':
    app.run()