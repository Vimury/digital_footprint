import sqlalchemy

from data.db_session import SqlAlchemyBase


class Test(SqlAlchemyBase):
    __tablename__ = 'tests'

    id_test = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    id_question = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("questions.id_question"))
    id_quiz = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("quizzes.id_quiz"))
    stud_answers = sqlalchemy.Column(sqlalchemy.String)
