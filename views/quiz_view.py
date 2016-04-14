from flask import request, render_template, session, redirect, url_for
from sqldb import get_admin, fetch_all_questions_by_eid
from Quiz import Quiz
import dateutil.parser
from views import app


@app.route('/admin/quiz/<quiz_id>/')
def admin_quiz(quiz_id):
    return render_template('showQuiz.html', questions=fetch_all_questions_by_eid(quiz_id))


@app.route('/admin/question/delete/<q_id>/')
def admin_delete_question(q_id):
    return 'Oops... Not implemented yet'  # TODO Implement
