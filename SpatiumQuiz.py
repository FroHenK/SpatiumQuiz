from flask import Flask, render_template

from sqldb import fetch_all_quizes
from Quiz import TextAnswerQuestion

'''Tested on Python 3.5.1'''

app = Flask(__name__)
# keep this really secret
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def main_page():
    t = fetch_all_quizes()
    return render_template("quizList.html", quizez=t)


def get_app():
    return app


if __name__ == '__main__':
    import views

    views.init(app)

    app.run(debug=True)
