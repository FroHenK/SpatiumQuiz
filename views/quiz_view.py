from flask import request, render_template, session, redirect, url_for
from sqldb import get_admin, fetch_all_questions_by_eid,fetch_quiz_by_id
from Quiz import Quiz
import dateutil.parser
from views import app


@app.route('/quiz/<quiz_id>/')
def view_quiz_main(quiz_id):
    return render_template('showQuiz.html', current_quiz=fetch_quiz_by_id(quiz_id))
