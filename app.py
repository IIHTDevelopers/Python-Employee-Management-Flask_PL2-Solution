from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# DB helper
def get_db_connection():
    conn = sqlite3.connect('employees.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. Intro to Routes
@app.route('/')
def index():
    return render_template('index.html')

# 2. Route Methods + Register User
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# 3. Login User
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (uname, pwd)).fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

# 4. Dashboard with Employee List
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    employees = conn.execute('SELECT * FROM employees').fetchall()
    conn.close()
    return render_template('dashboard.html', employees=employees)


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        salary = request.form['salary']
        age = request.form['age']
        address = request.form['address']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO employees (name, salary, age, address) VALUES (?, ?, ?, ?)',
            (name, salary, age, address)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))
    return render_template('add_employee.html')


# 6. Route Variables & Edit
@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = sqlite3.connect('employees.db')
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        salary = request.form['salary']
        address = request.form['address']

        cur.execute("""
            UPDATE employees
            SET name = ?, age = ?, salary = ?, address = ?
            WHERE id = ?
        """, (name, age, salary, address, id))

        conn.commit()
        conn.close()
        return redirect('/dashboard')

    else:
        cur.execute("SELECT * FROM employees WHERE id = ?", (id,))
        employee = cur.fetchone()
        conn.close()
        return render_template('edit_employee.html', employee=employee)


@app.route('/api/employee', methods=['POST'])
def add_employee_api():
    data = request.get_json()
    name = data.get('name')
    salary = data.get('salary')
    age = data.get('age')  # ✅ FIXED: use JSON key, not form
    address = data.get('address')

    conn = get_db_connection()
    conn.execute(
        'INSERT INTO employees (name, salary, age, address) VALUES (?, ?, ?, ?)',
        (name, salary, age, address)
    )
    conn.commit()
    conn.close()
    return jsonify({'status': 'Employee added'}), 201



@app.route('/employees', methods=['GET'])
def get_all_employees():
    try:
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        conn.close()

        employees = [
            {
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'department': row[3],
                'salary': row[4],
                'address': row[5]
            }
            for row in rows
        ]

        return jsonify({'status': 'success', 'employees': employees}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# 8. Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
