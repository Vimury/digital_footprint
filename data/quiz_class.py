import datetime
import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, IntegerField
from wtforms.validators import DataRequired

from .db_session import SqlAlchemyBase


class Quiz(SqlAlchemyBase):
    __tablename__ = 'quizzes'

    id_quiz = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                             default=datetime.datetime.now)
    id_student = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("students.id_student"))


class QuizForm(FlaskForm):
    date = StringField("Дата проведения", validators=[DataRequired()], default=datetime.datetime.now())
    answers = FieldList(StringField("Ответ:"), min_entries=5)
    submit = SubmitField("Отправить")


class CheckQuizForm(FlaskForm):
    comments = FieldList(StringField("Комментарий:"), min_entries=5)
    marks = FieldList(IntegerField("Оценка:"), validators=[DataRequired()], min_entries=5)
    submit = SubmitField("Оценить")
