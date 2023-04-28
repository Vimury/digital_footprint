import datetime

import sqlalchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField
from wtforms import SubmitField
from wtforms.validators import DataRequired

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin


class Student(SqlAlchemyBase, UserMixin):
    __tablename__ = 'students'

    id_student = sqlalchemy.Column(sqlalchemy.Integer,
                                   primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    birthday = sqlalchemy.Column(sqlalchemy.String,
                                 default=str(datetime.datetime.now))
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    id_stepik = sqlalchemy.Column(sqlalchemy.String,
                                  default="НЕТУ")

    def get_id(self):
        return self.id_student


class StudentForm(FlaskForm):
    name = StringField('ФИО', validators=[DataRequired()])
    date = StringField("Дата рождения", validators=[DataRequired()])
    id_stepik = StringField('ID Stepik', validators=[DataRequired()])
    submit = SubmitField('Применить')
