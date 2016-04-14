from views import app
from flask import request, render_template, session, redirect, url_for
from sqldb import get_admin, add_quiz
from Quiz import Quiz
import dateutil.parser

ADMIN_ID = 'admin_id'


def session_enter_admin(admin):
    session[ADMIN_ID] = admin[0]


@app.route('/admin/login/', methods=['POST', 'GET'])
def login_admin():
    if request.method == 'GET':
        return render_template('loginAdmin.html')
    if request.method == 'POST':
        password = str(request.form['password'])
        login = str(request.form['login'])
        admin = get_admin(login, password)
        if admin != None:
            session_enter_admin(admin)
            return redirect(url_for('admin_panel'))
        return render_template('loginAdmin.html', entered_wrong_creds=True)


@app.route('/admin/')
def admin_panel():
    if ADMIN_ID not in session:
        return redirect(url_for('login_admin'))

    return render_template('indexAdmin.html')


@app.route('/admin/add_quiz/', methods=['POST', 'GET'])
def admin_add_quiz():
    if ADMIN_ID not in session:
        return redirect(url_for('login_admin'))
    if request.method == 'POST':
        quiz_name = str(request.form['quiz_name'])
        quiz_datetime1 = dateutil.parser.parse(request.form['quiz_datetime1'])
        quiz_datetime2 = dateutil.parser.parse(request.form['quiz_datetime2'])
        add_quiz(Quiz(0, quiz_name, min(quiz_datetime1, quiz_datetime2), max(quiz_datetime1, quiz_datetime2)))

        return redirect(url_for('main_page'))

    return render_template('addQuiz.html')
