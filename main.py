from flask import Flask
from data import db_session
from data.question_class import Question

db_session.global_init("db/digital_footprint.db")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()



if __name__ == '__main__':
    db_sess = db_session.create_session()
    question = Question()
    user = db_sess.query(Question).first()
    print(user.texts)
    print(user.group.label)
    main()