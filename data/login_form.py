from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField


class LoginForm(FlaskForm):
    name = StringField('Имя студента')
    birthday = StringField("Дата рождения")
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
