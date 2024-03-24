from flask import Flask, render_template, request, g, redirect, url_for, session
import sqlite3

app = Flask(__name__)

# Configuration
DATABASE = 'database.db'
app.secret_key = 'your_secret_key'  # Define your secret key here

# Function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

# Initialize the database
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='example';")
        table_exists = cursor.fetchone()
        if not table_exists:
            with app.open_resource('schema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()
        else:
            print("Table 'example' already exists.")


# Teardown function to close the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username and password match in the database
        db = get_db()
        cursor = db.cursor()
        # cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        # Hack: 
        # Username:' OR '1'='1';--
        # Password: 
        cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password))

        user = cursor.fetchone()
        if user:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')


# Route to display data from the database
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # db = get_db()
    # cur = db.execute('SELECT * FROM example')
    # entries = cur.fetchall()
    return render_template('index.html', entries=[])

# Route for logout
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username already exists
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return render_template('register.html', error='Username already exists')
        else:
            # Insert new user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            db.commit()
            return redirect(url_for('login'))
    return render_template('register.html')


# Run the application
if __name__ == '__main__':
    init_db()
    app.secret_key = 'your_secret_key'  # Set your secret key here
    app.run(debug=True)
