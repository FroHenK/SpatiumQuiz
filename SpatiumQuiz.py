from flask import Flask, render_template,g

from sqldb import fetch_all_quizzes
from Quiz import TextAnswerQuestion
import re

from jinja2 import evalcontextfilter, Markup, escape

'''Tested on Python 3.5.1'''

app = Flask(__name__)
# keep this really secret
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def main_page():
    t = fetch_all_quizzes()
    return render_template("quizList.html", quizzes=t)

@app.before_request
def before_request():
    g.enumerate = enumerate

def get_app():
    return app


if __name__ == '__main__':
    import views

    views.init(app)

    app.run(host='0.0.0.0', port=80,threaded=True)

