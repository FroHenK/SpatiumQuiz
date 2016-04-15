from abc import ABCMeta, abstractmethod
import json
from flask import render_template
from markupsafe import Markup


class Quiz:
    def __init__(self, e_id, name, start, finish):
        self.id = e_id
        self.name = name
        self.start = start
        self.finish = finish


class Question:
    __metaclass__ = ABCMeta

    """e_id is id of Quiz, while q_id is for question id"""

    def __init__(self, e_id, q_id, q_type, data):
        self.type = q_type
        self.e_id = e_id
        self.q_id = q_id
        self.data = data

        if data is not None:
            self.parse_data(data)

    @abstractmethod
    def parse_data(self, data):
        pass

    @abstractmethod
    def is_answer_true(self, answer):
        pass

    @abstractmethod
    def data_to_string(self):
        pass

    @abstractmethod
    def edit_page(self, action):
        pass

    @abstractmethod
    def show_question(self, answer_id_name):
        pass


class TextAnswerQuestion(Question):
    """has 'answer', 'question', 'match_case'"""

    def __init__(self, e_id, q_id, q_type, data):
        self.answer = ''
        self.question = ''
        self.match_case = True
        super().__init__(e_id, q_id, q_type, data)

    def data_to_string(self):
        return json.dumps({'answer': self.answer
                              , 'question': self.question
                              , 'match_case': self.match_case})

    def is_answer_true(self, answer):
        if not self.match_case:
            return str(answer).lower() == str(self.answer).lower()

        return str(answer) == str(self.answer)

    def parse_data(self, data):
        loads = json.loads(str(data))
        self.answer = loads['answer']
        self.question = loads['question']
        self.match_case = loads['match_case']

    def edit_page(self, action):
        return render_template('questions/editTextAnswerQuestion.html', action=action, question=self)

    @staticmethod
    def add_page(action):
        return render_template('questions/editTextAnswerQuestion.html', action=action, question=None)

    def edit_response_parse(self, forms):
        self.answer = forms['question_answer']
        self.question = forms['question_question']
        self.match_case = 'question_match_case' in forms

    # needs Markup()
    def show_question(self, answer_id_name):
        return render_template('questions/showTextAnswerQuestion.html', answer_id_name=answer_id_name, question=self)


class PointOnMapQuestion(Question):
    """has 'answer', 'question', 'match_case'"""

    def __init__(self, e_id, q_id, q_type, data):
        self.answer = ''
        self.question = ''
        self.match_case = True
        self.lat=0.0
        self.lon = 0.0

        super().__init__(e_id, q_id, q_type, data)

    def data_to_string(self):
        return json.dumps({'answer': self.answer
                              , 'question': self.question
                              , 'match_case': self.match_case
                              , 'lat': self.lat
                              , 'lon': self.lon})

    def is_answer_true(self, answer):
        if not self.match_case:
            return str(answer).lower() == str(self.answer).lower()

        return str(answer) == str(self.answer)

    def parse_data(self, data):
        loads = json.loads(str(data))
        self.answer = loads['answer']
        self.question = loads['question']
        self.match_case = loads['match_case']
        self.lat = loads['lat']
        self.lon = loads['lon']

    def edit_page(self, action):
        return render_template('questions/editPointOnMapQuestion.html', action=action, question=self)

    @staticmethod
    def add_page(action):
        return render_template('questions/editPointOnMapQuestion.html', action=action, question=None)

    def edit_response_parse(self, forms):
        self.answer = forms['question_answer']
        self.question = forms['question_question']
        self.match_case = 'question_match_case' in forms
        self.lat=forms['question_lat']
        self.lon = forms['question_lon']

    # needs Markup()
    def show_question(self, answer_id_name):
        return render_template('questions/showPointOnMapQuestion.html', answer_id_name=answer_id_name, question=self)


question_types = {TextAnswerQuestion.__name__: TextAnswerQuestion,PointOnMapQuestion.__name__: PointOnMapQuestion}
