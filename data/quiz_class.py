import datetime
import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, TextAreaField
from wtforms.validators import DataRequired

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin


class Quiz(SqlAlchemyBase, UserMixin):
    __tablename__ = 'quizzes'
    id_quiz = sqlalchemy.Column(sqlalchemy.Integer,
                                primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.String)
    id_student = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("students.id_student"))


class QuizForm(FlaskForm):
    date = StringField("Дата проведения", validators=[DataRequired()], default=datetime.datetime.now())
    answers = FieldList(TextAreaField("Ответ:"), min_entries=5)
    submit = SubmitField("Отправить")


class CheckQuizForm(FlaskForm):
    comments = FieldList(TextAreaField("Комментарий:"), min_entries=5)
    submit = SubmitField("Оценить")
