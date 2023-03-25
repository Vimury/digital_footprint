import sqlalchemy

from data.db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    __tablename__ = 'groups'

    id_group = sqlalchemy.Column(sqlalchemy.Integer,
                                 primary_key=True, autoincrement=True)
    label = sqlalchemy.Column(sqlalchemy.String, nullable=True)
