import sqlalchemy

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin


class Test(SqlAlchemyBase, UserMixin):
    __tablename__ = 'tests'

    id_test = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    id_question = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("questions.id_question"))
    id_quiz = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("quizzes.id_quiz"))
    stud_answers = sqlalchemy.Column(sqlalchemy.String)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    comment = sqlalchemy.Column(sqlalchemy.String)
