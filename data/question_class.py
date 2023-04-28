import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin


class Question(SqlAlchemyBase, UserMixin):
    __tablename__ = 'questions'

    id_question = sqlalchemy.Column(sqlalchemy.Integer,
                                    primary_key=True, autoincrement=True)
    texts = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    id_group = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey("groups.id_group"))
    group = orm.relationship('Group')


class QuestionForm(FlaskForm):
    title = StringField('Тема')
    content = TextAreaField("Вопрос")
    submit = SubmitField('Применить')
