from flask import Flask, render_template

from data import db_session
from data.group_class import Group
from data.question_class import Question

db_session.global_init("db/digital_footprint.db")

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()
# Тимур - страница Добавление, изменение и удаление данных вопросы
# Вова - страница Добавление, изменение и удаление данных groups
# Геор - страницы Добавление, изменение и удаление данных студенты

@app.route("/questions")
def questions():
    query_questions = db_sess.query(Question).all()
    query_groups = db_sess.query(Group)
    return render_template('questions.html', query_questions=query_questions, query_groups=query_groups)


if __name__ == '__main__':
    db_sess = db_session.create_session()
    # question = Question()
    # user = db_sess.query(Question).first()
    # print(user.texts)
    # print(user.group.label)
    # В принципе, это не очень сейчас нужно, но удалять я пока явно не буду
    main()
