from flask import request, render_template, session, redirect, url_for
from markupsafe import Markup

from sqldb import get_admin, fetch_all_questions_by_eid, fetch_quiz_by_id
from Quiz import Quiz
import dateutil.parser
from views import app


# TODO All of this is ugly and bad performed(i guess?). Remake

@app.route('/quiz/<quiz_id>/')
def view_quiz_main(quiz_id):
    questions_by_eid = fetch_all_questions_by_eid(quiz_id)
    return render_template('showQuiz.html', current_quiz=fetch_quiz_by_id(quiz_id), questions=questions_by_eid,
                           Markup=Markup)


@app.route('/quiz/commit/<quiz_id>/',methods=['POST'])
def commit_quiz(quiz_id):
    questions_by_eid = fetch_all_questions_by_eid(quiz_id)
    total_score = questions_by_eid.__len__()
    your_score = 0
    for question in questions_by_eid:
        if question.is_answer_true(request.form[str(question.q_id)]):
            your_score += 1
    return render_template('quizResult.html', current_quiz=fetch_quiz_by_id(quiz_id), your_score=your_score,
                           total_score=total_score)
