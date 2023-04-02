import sqlalchemy

from data.db_session import SqlAlchemyBase
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'

    id_group = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, autoincrement=True)
    label = sqlalchemy.Column(sqlalchemy.String, nullable=True)


class GroupForm(FlaskForm):
    label = StringField('Название группы', validators=[DataRequired()])
    submit = SubmitField('Применить')
