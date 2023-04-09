from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя студента', validators=[DataRequired()])
    birthday = StringField("Дата рождения", validators=[DataRequired()])
    stepik_id = StringField("ID Stepik", validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')