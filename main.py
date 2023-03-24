from flask import Flask, render_template, redirect

from data import db_session
from data.group_class import Group
from data.question_class import Question, QuestionForm

db_session.global_init("db/digital_footprint.db")

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run(host='127.0.0.1', port=8080)


# Тимур - страница Добавление, изменение и удаление данных вопросы
# Вова - страница Добавление, изменение и удаление данных groups
# Геор - страницы Добавление, изменение и удаление данных студенты

@app.route("/questions", methods=['GET', 'POST'])
def questions():
    query_questions = db_sess.query(Question).all()
    query_groups = db_sess.query(Group)
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question()
        question.texts = form.content.data
        question.id_group = query_groups.filter_by(label=form.title.data).first().id_group
        db_sess.add(question)
        db_sess.commit()

        return redirect('/questions')
    return render_template('questions.html', query_questions=query_questions, query_groups=query_groups,
                           title="Вопросы", form=form)

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    db_sess = db_session.create_session()
    # question = Question()
    # user = db_sess.query(Question).first()
    # print(user.texts)
    # print(user.group.label)
    # В принципе, это не очень сейчас нужно, но удалять я пока явно не буду
    main()

# abacaba, что ли
