from abc import ABCMeta, abstractmethod
import json


class Quiz:
    def __init__(self, e_id, name, start, finish):
        self.id = e_id
        self.name = name
        self.start = start
        self.finish = finish
        super().__init__()


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


class TextAnswerQuestion(Question):
    """has 'answer', 'question', 'match_case'"""

    def __init__(self, e_id, q_id, q_type, data):
        super().__init__(e_id, q_id, q_type, data)
        self.answer = 'None'
        self.question = 'None'
        self.match_case = True

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


question_types = {TextAnswerQuestion.__name__:TextAnswerQuestion}
