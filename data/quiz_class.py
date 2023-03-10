import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Quiz(SqlAlchemyBase):
    __tablename__ = 'quizzes'

    id_quiz = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    id_student = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("students.id_student"))