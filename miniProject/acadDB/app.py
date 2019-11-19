from flask import Flask,render_template, request, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "alpha"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mini_project'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        cur = mysql.connection.cursor()
        opValue = cur.execute("SELECT * FROM students")
        students = cur.fetchall()
    except Exception as e:
        print(e)
        return "Some error Occured : check log for more details"
    return render_template('students.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    try:
        if request.method == 'GET':
            return render_template('add.html')
        elif request.method == 'POST':
            studentDetails = request.form
            rollno = studentDetails['rollno']
            name = studentDetails['name']
            email = studentDetails['email']
            phone = studentDetails['contact']
            sex = studentDetails['sex']
            branch = studentDetails['branch']
            sem = studentDetails['sem']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO students VALUES(%s, %s, %s, %s, %s, %s, %s)", (rollno, name,email, phone, sex, branch, sem))
            mysql.connection.commit()
            cur.close()
            return redirect('/')
    except Exception as e:
        print(e)
        return "Some error Occured : check entered data"
    return render_template('add.html')

@app.route('/delete/<string:id>')
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE rollno=%s", [id])
        mysql.connection.commit()
        flash('%s Student Deleted Successfully', (id))
        return redirect('/')
    except Exception as e:
        print(e)
        return "Some error occured, check log"
        


if __name__ == '__main__':
    app.run(debug=True)