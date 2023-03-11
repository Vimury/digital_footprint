import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase):
    __tablename__ = 'questions'

    id_question = sqlalchemy.Column(sqlalchemy.Integer,
                                    primary_key=True, autoincrement=True)

    texts = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_group = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("groups.id_group"))
    group = orm.relationship('Group')

#     def add_question(self, id_quest: int, text: str, id_group: int):
#         self.id_questions.append(id_quest)
#         self.texts.append(text)
#         self.id_groups.append(id_group)
#
#
# class Tests:
#     def __init__(self):
#         self.id_questions = []
#         self.stud_answer = []
#         self.id_tests = []
#         self.id_quiz = []
#
#     def add_test(self, id_test, id_quest, id_quiz, stud_ans):
#         self.id_tests.append(id_test)
#         self.id_questions.append(id_quest)
#         self.id_quiz.append(id_quiz)
#         self.stud_answer.append(stud_ans)
