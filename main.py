from flask import Flask
from data import db_session

db_session.global_init("db/digital_footprint.db")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


if __name__ == '__main__':
    main()