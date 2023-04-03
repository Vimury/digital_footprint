from flask import Flask, render_template, redirect, request, abort

from data import db_session
from data.group_class import Group, GroupForm
from data.question_class import Question, QuestionForm
from data.student_class import Student, StudentForm
from groups_edit import g, g_edit, g_delete

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
def questions_edit(id):
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


@app.route("/students", methods=['GET', 'POST'])
def students():
    query_students = db_sess.query(Student).all()
    form = StudentForm()
    if form.validate_on_submit():
        student = Student()
        student.name = form.name.data
        student.birthday = form.date.data
        student.id_stepik = form.id_stepik.data
        db_sess.add(student)
        db_sess.commit()

        return redirect('/students')
    return render_template('students.html', query_students=query_students,
                           title="Студенты", form=form)


@app.route('/students/<int:id>', methods=['GET', 'POST'])
def students_edit(id):
    form = StudentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        student = db_sess.query(Student).filter(Student.id_student == id).first()
        if student:
            form.name.data = student.name
            form.date.data = student.birthday
            form.id_stepik.data = student.id_stepik
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        student = db_sess.query(Student).filter(Student.id_student == id).first()
        if student:
            student.name = form.name.data
            student.birthday = form.date.data
            student.id_stepik = form.id_stepik.data
            db_sess.commit()
            return redirect('/students')
        else:
            abort(404)
    return render_template('students_edit.html', title="ниЧиво?", form=form, id=student.id_student)


@app.route('/students_delete/<int:id>', methods=['GET', 'POST'])
def students_delete(id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id_student == id).first()
    if student:
        db_sess.delete(student)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/students')


@app.route('/groups', methods=['GET', 'POST'])
def groups():
    g()  # -> groups_edit


@app.route('/groups/<int:id>', methods=['GET', 'POST'])
def groups_edit(id):
    g_edit(id)  # -> groups_edit


@app.route('/groups_delete/<int:id>', methods=['GET', 'POST'])
def groups_delete(id):
    g_delete(id)  # -> groups_edit


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    db_sess = db_session.create_session()
    main()
