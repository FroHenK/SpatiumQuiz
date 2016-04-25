from views import app
from flask import request, render_template, session, redirect, url_for
import sqldb
from Quiz import Quiz, question_types
import dateutil.parser
import json
from datetime import datetime

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,datetime):
            return o.isoformat()
        return o.__dict__


@app.route('/get_json_quizzes/')
def get_json_quizzes():
    quizzes = [i for i in sqldb.fetch_all_quizzes()]
    print(json.dumps(quizzes,cls=MyEncoder))
    for i in quizzes:
        print(i.id)
        i.questions = sqldb.fetch_all_questions_by_eid(i.id)
    return json.dumps(quizzes,cls=MyEncoder)
