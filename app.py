from flask import Flask, render_template, request, jsonify, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "skill_test_secret"

db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "callmesir@123"),
    database=os.getenv("DB_NAME", "skill_test")
)

cursor = db.cursor(buffered=True)

all_questions = {
    'python': [
        {"q": "1. Who created Python?", "options": ["Guido van Rossum", "James Gosling", "Dennis Ritchie", "Bjarne Stroustrup"], "ans": "Guido van Rossum"},
        {"q": "2. What is output? print(2**3*2)", "options": ["16", "12", "8", "64"], "ans": "16"},
        {"q": "3. Output? x=[1,2,3]; print(len(x))", "options": ["3", "2", "1", "0"], "ans": "3"},
        {"q": "4. Output? print('py'*3)", "options": ["pypypy", "py3", "ppp", "yyy"], "ans": "pypypy"},
        {"q": "5. Output? a=5; b=2; print(a//b)", "options": ["2", "2.5", "3", "1"], "ans": "2"},
        {"q": "6. Output? a=[1,2,3]; print(a[1:])", "options": ["[2, 3]", "[1, 2]", "[1]", "[3]"], "ans": "[2, 3]"},
        {"q": "7. Output? x=[1,2]; y=x; y.append(3); print(x)", "options": ["[1, 2, 3]", "[1, 2]", "[3]", "Error"], "ans": "[1, 2, 3]"},
        {"q": "8. Output? print([i*i for i in range(3)])", "options": ["[0, 1, 4]", "[1, 4, 9]", "[0, 1, 2]", "[1, 2, 3]"], "ans": "[0, 1, 4]"},
        {"q": "9. Output? a={'a':1}; print(a.get('b', 0))", "options": ["0", "1", "None", "Error"], "ans": "0"},
        {"q": "10. Output? print(bool([]) and bool([0]))", "options": ["False", "True", "[0]", "[]"], "ans": "False"}
    ],
    'java': [
        {"q": "1. Java created by?", "options": ["James Gosling", "Guido van Rossum", "Dennis Ritchie", "Linus Torvalds"], "ans": "James Gosling"},
        {"q": "2. Output? System.out.print(10/3);", "options": ["3", "3.33", "3.0", "Error"], "ans": "3"},
        {"q": "3. Output? String s=\"java\"; System.out.print(s.length());", "options": ["4", "3", "5", "0"], "ans": "4"},
        {"q": "4. Output? int a=5; System.out.print(a++);", "options": ["5", "6", "4", "Error"], "ans": "5"},
        {"q": "5. Output? System.out.print(2 + \"2\" + 2);", "options": ["222", "6", "42", "24"], "ans": "222"},
        {"q": "6. Output? int[] arr={1,2,3}; System.out.print(arr[1]);", "options": ["2", "1", "3", "0"], "ans": "2"},
        {"q": "7. Output? String s1=\"hi\"; String s2=\"hi\"; System.out.print(s1==s2);", "options": ["true", "false", "Error", "null"], "ans": "true"},
        {"q": "8. Output? for(int i=0;i<3;i++){ if(i==1) continue; System.out.print(i); }", "options": ["02", "012", "01", "2"], "ans": "02"},
        {"q": "9. What happens? int x=5/0;", "options": ["ArithmeticException", "0", "Compiles fine", "null"], "ans": "ArithmeticException"},
        {"q": "10. Output? System.out.print(Math.pow(2,3));", "options": ["8.0", "8", "6.0", "9.0"], "ans": "8.0"}
    ],
    'c': [
        {"q": "1. C created by?", "options": ["Dennis Ritchie", "James Gosling", "Guido van Rossum", "Ken Thompson"], "ans": "Dennis Ritchie"},
        {"q": "2. Output? int a=10/3; printf(\"%d\",a);", "options": ["3", "3.33", "3.00", "Error"], "ans": "3"},
        {"q": "3. Output? int a=5; printf(\"%d\", a++);", "options": ["5", "6", "4", "Error"], "ans": "5"},
        {"q": "4. Output? printf(\"%d\", 2*3+4);", "options": ["10", "14", "12", "6"], "ans": "10"},
        {"q": "5. Output? int arr[]={1,2,3}; printf(\"%d\", arr[0]);", "options": ["1", "2", "0", "3"], "ans": "1"},
        {"q": "6. Output? char s[]=\"hi\"; printf(\"%d\", strlen(s));", "options": ["2", "3", "1", "0"], "ans": "2"},
        {"q": "7. Output? int a=5; int *p=&a; printf(\"%d\", *p);", "options": ["5", "Address", "Error", "0"], "ans": "5"},
        {"q": "8. Output? int i=0; while(i<3){ i++; if(i==2) continue; printf(\"%d\",i); }", "options": ["13", "123", "12", "23"], "ans": "13"},
        {"q": "9. Output? printf(\"%d\", sizeof(int));", "options": ["4", "2", "8", "1"], "ans": "4"},
        {"q": "10. Output? int x=5; printf(\"%d\", x>>1);", "options": ["2", "10", "5", "1"], "ans": "2"}
    ]
}

@app.route('/')
def create_page():
    return render_template('create1.html')

@app.route('/login')
def login_page():
    return render_template('login1.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    number = request.form['phone']
    password = request.form['password']
    cpassword = request.form['confirm_password']

    if len(password) < 5:
        return render_template('create1.html', error="Password is weak")
    if len(number)!=10:
        return render_template('create1.html', error="Phone Number Must Be 10 Digits")
    if password!= cpassword:
        return render_template('create1.html', error="Incorrect Password")

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        return render_template('create1.html', error="Username already exists")

    cursor.execute("SELECT * FROM users WHERE number=%s", (number,))
    if cursor.fetchone():
        return render_template('create1.html', error="Phone number already exists")

    cursor.execute("INSERT INTO users (username, number, password) VALUES (%s, %s, %s)", (username, number, password))
    db.commit()
    return render_template('success.html', message="Account created successfully")

@app.route('/login_check', methods=['POST'])
def login_check():
    user_input = request.form['username']
    password = request.form['password']
    cursor.execute("SELECT * FROM users WHERE username=%s OR number=%s", (user_input, user_input))
    user = cursor.fetchone()
    if not user:
        return render_template('login1.html', error="Invalid username or number")
    if user[3]!= password:
        return render_template('login1.html', error="Incorrect password")

    # Save username in session
    session['username'] = user[1]
    cursor.execute("SELECT subject, score, total FROM results WHERE username=%s", (user[1],))
    results = cursor.fetchall()
    return render_template('home.html', results=results)

@app.route('/home_page')
def home_page():
    username = session.get('username')
    if not username:
        return render_template('login1.html', error="Login first")
    cursor.execute("SELECT subject, score, total FROM results WHERE username=%s", (username,))
    results = cursor.fetchall()
    return render_template('home.html', results=results)

@app.route('/quiz/<subject>')
def quiz(subject):
    questions = all_questions.get(subject, [])
    return render_template('quiz.html', subject=subject, questions=questions)

@app.route('/submit/<subject>', methods=['POST'])
def submit_quiz(subject):
    questions = all_questions.get(subject, [])
    score = 0
    for i in range(len(questions)):
        if request.form.get(f'q{i}') == questions[i]['ans']:
            score += 1

    username = session.get('username', 'guest')

    # Update if exists else insert
    cursor.execute("SELECT id FROM results WHERE username=%s AND subject=%s", (username, subject))
    existing = cursor.fetchone()
    if existing:
        cursor.execute("UPDATE results SET score=%s, total=%s WHERE username=%s AND subject=%s", (score, len(questions), username, subject))
    else:
        cursor.execute("INSERT INTO results (username, subject, score, total) VALUES (%s,%s,%s,%s)", (username, subject, score, len(questions)))
    db.commit()

    return render_template('result.html', subject=subject, score=score, total=len(questions))

@app.route('/api/<subject>')
def api(subject):
    return jsonify(all_questions.get(subject, []))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))