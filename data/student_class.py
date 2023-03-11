import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = 'students'

    id_student = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    birthday = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    id_stepik = None