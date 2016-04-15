import sqlite3
from datetime import datetime
from Quiz import Quiz, question_types
from flask import g
import dateutil.parser
import dateutil.easter

import hashlib


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("C:\\Project\\PythonProjects\\SpatiumQuiz\\spatiumdb.db",
                                           detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

    return db


def get_admin(login, password):
    password_md5 = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM admins WHERE login=? AND md5_password=?', (login, password_md5))
    fetched = cur.fetchone()
    cur.close()
    return fetched


def add_quiz(quiz):
    conn = get_db()
    conn.execute("INSERT INTO quiz (name,start,finish) VALUES (?,?,?)",
                 (quiz.name, quiz.start.isoformat(), quiz.finish.isoformat()))
    conn.commit()


def add_question(question):
    conn = get_db()
    conn.execute("INSERT INTO questions (e_id, type, data) VALUES (?,?,?)",
                 (question.e_id, question.type, question.data_to_string()))
    conn.commit()


def fetch_all_quizzes():
    conn = get_db()
    quizzes = []
    cur = conn.cursor()
    for var in cur.execute('SELECT id,name,start,finish FROM quiz ORDER BY start').fetchall():
        quizzes.append(Quiz(
            int(var[0]),
            str(var[1]),
            dateutil.parser.parse(str(var[2])),
            dateutil.parser.parse(str(var[3])),
        ))
    cur.close()
    return quizzes


def fetch_all_questions_by_eid(e_id):
    conn = get_db()
    questions = []
    cur = conn.cursor()
    for var in cur.execute('SELECT e_id,id,type,data  FROM questions  WHERE e_id=? ORDER BY id ASC', (e_id)).fetchall():
        questions.append(question_types[str(var[2])](
            int(var[0]),
            int(var[1]),
            str(var[2]),
            str(var[3]),
        ))
    cur.close()
    return questions


def fetch_quiz_by_id(q_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT id,name,start,finish FROM quiz WHERE id=?', q_id)
    res = cur.fetchone()
    res = Quiz(
        int(res[0]),
        str(res[1]),
        dateutil.parser.parse(str(res[2])),
        dateutil.parser.parse(str(res[3])),
    )
    cur.close()
    return res


def fetch_question_by_id(e_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT e_id,id,type,data FROM questions WHERE id=?', e_id)
    res = cur.fetchone()

    res = question_types[str(res[2])](
        int(res[0]),
        int(res[1]),
        str(res[2]),
        str(res[3]),
    )

    cur.close()
    return res


def update_question(question):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE questions SET data = ? WHERE id=?', (question.data_to_string(), question.q_id))
    conn.commit()
    cur.close()


def delete_question_by_id(question_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM questions WHERE id=?', question_id)
    conn.commit()
    cur.close()
