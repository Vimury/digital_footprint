import datetime

from flask import Blueprint, render_template, redirect, request, abort

from data import db_session
from data.group_class import Group, GroupForm
from data.question_class import Question, QuestionForm
from data.student_class import Student, StudentForm
from data.quiz_class import Quiz, CheckQuizForm
from data.test_class import Test
from flask_login import login_user, current_user
from generate_quiz import generate_full

db_session.global_init("db/digital_footprint.db")

db_sess = db_session.create_session()
admin = Blueprint('admin', __name__)


def check_admin(func):
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            return func(*args, **kwargs)
        else:
            return redirect("/")

    wrapper.__name__ = func.__name__
    return wrapper


@admin.route("/questions", methods=['GET', 'POST'])
@check_admin
def questions():
    query_questions = db_sess.query(Question).all()
    query_groups = db_sess.query(Group)
    return render_template('questions.html', query_questions=query_questions, query_groups=query_groups,
                           title="Вопросы")


@admin.route('/results')
@check_admin
def table_view():
    dates = []
    for i in db_sess.query(Quiz).all():
        date = i.date
        if date not in dates:
            dates.append(date)

    students = db_sess.query(Student).filter(Student.is_admin != 1).all()

    return render_template('results.html', dates=dates, students=students, len=len(students), len_dates=len(dates))


@admin.route('/check_quiz', methods=['POST', 'GET'])
@check_admin
def check_quizzes():
    db_sess = db_session.create_session()

    quizzes = []
    dates = []
    for i in db_sess.query(Quiz).all():
        date = i.date
        if date not in dates:
            dates.append(date)
            quizzes.append([])
            for j in db_sess.query(Quiz).filter(Quiz.date == i.date):
                quizzes[-1].append(
                    (j.id_quiz, db_sess.query(Student).filter(Student.id_student == j.id_student).first().name))

    return render_template('check_quizzes.html', len=len(dates), dates=dates, title="Проверка тестов", quizzes=quizzes)


@admin.route('/check_quiz/<id>', methods=['POST', 'GET'])
@check_admin
def check_quiz(id):
    db_sess = db_session.create_session()
    quiz = db_sess.query(Quiz).filter(Quiz.id_quiz == id).first()
    student = db_sess.query(Student).filter(Student.id_student == quiz.id_student).first()
    tests = db_sess.query(Test).filter(Test.id_quiz == id).all()
    form = CheckQuizForm()
    quests = []
    answers = []
    for i in tests:
        quests.append(db_sess.query(Question).filter(Question.id_question == i.id_question).first())
        answers.append(i.stud_answers if i.stud_answers else "")
    if form.validate_on_submit():
        for i in range(5):
            tests[i].mark = request.form.get("flexRadioDefault" + str(i))
            tests[i].comment = form.comments.data[i]
        db_sess.commit()
        return redirect("/")
    return render_template("check_quiz.html", name=student.name, answers=answers, questions=quests, form=form)


@admin.route('/add_student', methods=['GET', 'POST'])
@check_admin
def add_student():
    form = StudentForm()
    if form.validate_on_submit() and login_user():
        student = Student()
        student.name = form.name.data
        student.birthday = form.date.data
        student.id_stepik = form.id_stepik.data
        db_sess.add(student)
        db_sess.commit()

        return redirect('/students')
    return render_template('add_student.html',
                           title="Студенты", form=form)


@admin.route('/groups_delete/<int:id>', methods=['GET', 'POST'])
@check_admin
def groups_delete(id):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).filter(Group.id_group == id).first()
    if group:
        db_sess.delete(group)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/groups')


@admin.route('/groups/<int:id>', methods=['GET', 'POST'])
@check_admin
def edit_groups(id):
    form = GroupForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        group = db_sess.query(Group).filter(Group.id_group == id).first()
        if group:
            form.label.data = group.label
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        group = db_sess.query(Group).filter(Group.id_group == id).first()
        if group:
            group.label = form.label.data
            db_sess.commit()
            return redirect('/groups')
        else:
            abort(404)
    return render_template('groups_edit.html', title="ниЧиво?", form=form, id=group.id_group)


@admin.route('/groups', methods=['GET', 'POST'])
@check_admin
def groups():
    query_groups = db_sess.query(Group).all()
    form = GroupForm()
    if form.validate_on_submit():
        group = Group()
        group.label = form.label.data
        db_sess.add(group)
        db_sess.commit()
        return redirect('/groups')
    return render_template('groups.html', query_groups=query_groups,
                           title="Группы", form=form)


@admin.route("/students", methods=['GET', 'POST'])
@check_admin
def students():
    query_students = db_sess.query(Student).filter(Student.is_admin == 0)
    return render_template('students.html', query_students=query_students,
                           title="Студенты")


@admin.route("/make_test", methods=['GET', 'POST'])
@check_admin
def choice_student_groups():
    query_students = db_sess.query(Student).filter(Student.is_admin == 0)
    query_groups = db_sess.query(Group).all()
    if request.method == "POST":
        groups = [i.id_group for i in query_groups if request.form.get(str(i.label))]
        if groups:
            students = [i.id_student for i in query_students if
                        request.form.get(str(i.name) + str(i.birthday))]
            generate_full(students, groups, datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            return redirect('/check_quiz')

    return render_template('make_test.html', query_students=query_students, query_groups=query_groups,
                           title="Выбрать студентов")


@admin.route('/students/<int:id>', methods=['GET', 'POST'])
@check_admin
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


@admin.route('/students_delete/<int:id>', methods=['GET', 'POST'])
@check_admin
def students_delete(id):
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id_student == id).first()
    if student:
        db_sess.delete(student)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/students')


@admin.route('/questions/add/<int:id>', methods=['GET', 'POST'])
@check_admin
def add_questions(id):
    query_questions = db_sess.query(Question).all()
    query_groups = db_sess.query(Group)
    form = QuestionForm()
    theme = query_groups.filter_by(id_group=id).first().label
    if form.validate_on_submit():
        question = Question()
        question.texts = form.content.data
        question.id_group = id
        db_sess.add(question)
        db_sess.commit()
    return render_template('questions_add.html', query_questions=query_questions, query_groups=query_groups,
                           title="Вопросы", form=form, theme=theme, id=id)


@admin.route('/questions/<int:id>', methods=['GET', 'POST'])
@check_admin
def edit_questions(id):
    form = QuestionForm()
    theme = 0
    if request.method == "GET":
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id_question == id).first()
        group = db_sess.query(Group)
        theme = group.filter_by(id_group=question.id_group).first().label
        if question:
            form.content.data = question.texts
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        question = db_sess.query(Question).filter(Question.id_question == id).first()
        if question:
            question.texts = form.content.data
            db_sess.commit()
            return redirect('/questions')
        else:
            abort(404)

    return render_template('questions_edit.html', title="ниЧиво?", form=form, id=id, theme=theme)


@admin.route('/questions_delete/<int:id>', methods=['GET', 'POST'])
@check_admin
def questions_delete(id):
    db_sess = db_session.create_session()
    question = db_sess.query(Question).filter(Question.id_question == id).first()
    if question:
        db_sess.delete(question)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/questions')
