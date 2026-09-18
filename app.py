from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="callmesir@123",
    database="skill_test"
)

cursor = db.cursor()

@app.route('/')
def create_page():
    return render_template('create.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    number = request.form['number']
    password = request.form['password']
    cpassword = request.form['cpassword']

    if len(password)<5:
        return render_template(
            'create.html',
            error="Password is weak"
        )

    if password!= cpassword:
        return render_template(
            'create.html',
            error="Incorrect password"
        )

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=%s OR number=%s
        """,
        (username, number)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        return render_template(
            'create.html',
            error="Username or phone already exists"
        )

    cursor.execute(
        """
        INSERT INTO users
        (username, number, password)
        VALUES (%s, %s, %s)
        """,
        (username, number, password)
    )

    db.commit()

    return render_template(
        'success.html',
        message="Account created successfully!"
    )

@app.route('/login_check', methods=['POST'])
def login_check():
    user_input = request.form['user_input']
    password = request.form['password']

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=%s OR number=%s
        """,
        (user_input, user_input)
    )

    user = cursor.fetchone()

    if not user:
        return render_template(
            'login.html',
            error="Invalid Username or Phone Number"
        )

    if user[3]!= password:
        return render_template(
            'login.html',
            error="Incorrect Password"
        )

    return render_template(
        'success.html',
        message="Account Created Succesfully"
    )

if __name__ == '__main__':
    app.run(debug=True)