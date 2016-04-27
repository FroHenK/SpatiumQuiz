from views import app
from flask import request, render_template, session, redirect, url_for
from sqldb import get_admin, add_quiz, fetch_all_questions_by_eid, fetch_quiz_by_id, fetch_question_by_id, \
    update_question, add_question, delete_question_by_id,delete_quiz_by_id
from Quiz import Quiz, question_types
import dateutil.parser
import datetime
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


# Quizzes and questions
@app.route('/admin/add_quiz/', methods=['POST', 'GET'])
def admin_add_quiz():
    if ADMIN_ID not in session:
        return redirect(url_for('login_admin'))
    if request.method == 'POST':
        quiz_name = str(request.form['quiz_name'])
        #quiz_datetime1 = dateutil.parser.parse(request.form['quiz_datetime1'])
       # quiz_datetime2 = dateutil.parser.parse(request.form['quiz_datetime2'])
        #add_quiz(Quiz(0, quiz_name, min(quiz_datetime1, quiz_datetime2), max(quiz_datetime1, quiz_datetime2)))
        add_quiz(Quiz(0, quiz_name, datetime.datetime.now(), datetime.datetime.now()))#TODO do something with datetimes
        return redirect(url_for('main_page'))

    return render_template('addQuiz.html')


@app.route('/admin/quiz/add_question/<quiz_id>/<question_type>', methods=['POST', 'GET'])
def admin_add_question(quiz_id, question_type):
    if ADMIN_ID not in session:
        return redirect(url_for('login_admin'))
    if request.method == 'POST':
        question_new = question_types[question_type](quiz_id, 0, question_type, None)
        question_new.edit_response_parse(request.form)
        add_question(question_new)
        return redirect(url_for('admin_quiz', quiz_id=question_new.e_id))

    return question_types[question_type].add_page(
        url_for('admin_add_question', quiz_id=quiz_id, question_type=question_type))


@app.route('/admin/quiz/<quiz_id>/')
def admin_quiz(quiz_id):
    if ADMIN_ID not in session:
        return redirect(url_for('login_admin'))
    return render_template('showQuizAdmin.html', current_quiz=fetch_quiz_by_id(quiz_id),
                           questions=fetch_all_questions_by_eid(quiz_id), question_types=question_types)


@app.route('/admin/quiz/remove/<quiz_id>/')
def admin_remove_quiz(quiz_id):
    if ADMIN_ID not in session:
        return redirect(url_for('login_admin'))
    delete_quiz_by_id(quiz_id)
    return redirect(url_for('main_page'))


@app.route('/admin/question/edit/<q_id>/', methods=['POST', 'GET'])
def admin_edit_question(q_id):
    if ADMIN_ID not in session:
        return redirect(url_for('login_admin'))
    question_by_id = fetch_question_by_id(q_id)

    if request.method == 'POST':
        question_by_id.edit_response_parse(request.form)
        update_question(question_by_id)
        return redirect(url_for('admin_quiz', quiz_id=question_by_id.e_id))

    return question_by_id.edit_page(url_for('admin_edit_question', q_id=question_by_id.q_id))


@app.route('/admin/question/delete/<q_id>/')
def admin_delete_question(q_id):
    if ADMIN_ID not in session:
        return redirect(url_for('login_admin'))
    question_by_id = fetch_question_by_id(q_id)
    delete_question_by_id(q_id)
    return redirect(url_for('admin_quiz', quiz_id=question_by_id.e_id))
