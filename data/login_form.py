from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField


class LoginForm(FlaskForm):
    name = StringField('Имя студента')
    birthday = StringField("Дата рождения")
    submit = SubmitField('Войти')