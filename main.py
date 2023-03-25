from flask import Flask, render_template, redirect, request, abort

from data import db_session
from data.group_class import Group
from data.question_class import Question, QuestionForm

db_session.global_init("db/digital_footprint.db")

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run(host='127.0.0.1', port=8080, debug=True)


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


@app.route('/questions/<int:id>', methods=['GET', 'POST'])
def edit_questions(id):
    form = QuestionForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id_question == id).first()
        group = db_sess.query(Group)
        form.title.data = group.filter_by(id_group=question.id_group).first().label
        if question:
            form.content.data = question.texts
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id_question == id).first()
        group = db_sess.query(Group)
        if question:
            question.texts = form.content.data
            db_sess.commit()
            return redirect('/questions')
        else:
            abort(404)
    return render_template('questions_edit.html', title="ниЧиво?", form=form, id=question.id_question)


@app.route('/questions_delete/<int:id>', methods=['GET', 'POST'])
def questions_delete(id):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.id_question == id).first()
    if question:
        db_sess.delete(question)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/questions')


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
