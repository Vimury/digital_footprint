import datetime
import time
from flask import Flask, render_template, redirect

from data import db_session
from data.login_form import LoginForm
from data.question_class import Question
from data.student_class import Student
from data.quiz_class import Quiz, QuizForm
from data.register_form import RegisterForm
from data.test_class import Test
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from config import TIME_TEST
import math

from admin import admin

db_session.global_init("db/digital_footprint.db")

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.register_blueprint(admin)
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=False)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(student_id):
    db_sess = db_session.create_session()
    return db_sess.query(Student).get(student_id)


@app.template_filter('strptime')
def _jinja2_filter_datetime(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


@app.route('/waiting')
def waiting():
    time = datetime.datetime.utcnow()
    dl = datetime.timedelta(minutes=5, seconds=30)
    db_sess = db_session.create_session()
    current_quizzes = db_sess.query(Quiz).filter_by(id_student=current_user.id_student).all()
    return render_template('waiting.html', current_quizzes=current_quizzes,
                           time=time, dl=dl)


@app.route('/quiz/<int:id>', methods=['GET', 'POST'])
def quiz(id):
    db_sess = db_session.create_session()
    query_quiz = db_sess.query(Quiz).filter(Quiz.id_quiz == id).first()
    pytime = datetime.datetime.strptime(query_quiz.date, "%Y-%m-%d %H:%M:%S")
    js_time = int(time.mktime(pytime.timetuple())) * 1000
    tests = db_sess.query(Test).filter(Test.id_quiz == id).all()
    quests = []
    for i in tests:
        quests.append(db_sess.query(Question).filter(Question.id_question == i.id_question).first())
    form = QuizForm()
    if form.validate_on_submit():
        for i in range(5):
            tests[i].stud_answers = form.answers.data[i]
        db_sess.commit()
        return redirect("/")

    return render_template('quiz_page.html', id=id, questions_num=5,
                           query_questions=quests, title="Тестирование",
                           form=form, timer=TIME_TEST, time=js_time)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Student).filter(
            (Student.name == form.name.data) & (Student.birthday == form.birthday.data)).first()
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Student).filter(Student.name == form.name.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        student = Student(
            name=form.name.data,
            birthday=form.birthday.data,
            id_stepik=form.stepik_id.data
        )
        db_sess.add(student)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index")
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect("/results")
        else:
            return redirect("/my_quiz")
    return render_template('index.html')


@app.route('/my_quiz')
def my_quiz():
    db_sess = db_session.create_session()

    quizzes = db_sess.query(Quiz).filter(Quiz.id_student == current_user.id_student).all()[::-1]
    if quizzes:
        dates = []
        marks = []
        question_marks = []
        questions = []
        answers = []
        comments = []
        all_mark = 0
        for i in quizzes:
            dates.append(i.date)
            tests = db_sess.query(Test).filter(Test.id_quiz == i.id_quiz).all()
            sm = 0
            for test in tests:
                questions.append(db_sess.query(Question).filter(Question.id_question == test.id_question).first())
                answers.append(test.stud_answers if test.stud_answers else "")
                comments.append(test.comment if test.comment else "")
                question_marks.append(test.mark if test.mark else 0)
                sm += question_marks[-1]
            all_mark += sm
            marks.append(sm / 5)

        quizzes_count = []
        for i in db_sess.query(Quiz).all():
            if i.date not in quizzes_count:
                quizzes_count.append(i.date)

        all_mark /= (len(quizzes_count) * 5)

        return render_template('my_quizzes.html', len=len(quizzes), dates=dates, marks=marks, all_mark=all_mark,
                               questions=questions, answers=answers, comments=comments, title="Мои тесты",
                               question_marks=question_marks)
    else:
        return render_template('my_quizzes.html', len=0)


@app.template_filter('get_results')
def get_results(args):
    id_student = args[0]
    date = args[1]
    quiz = db_sess.query(Quiz).filter((Quiz.id_student == id_student) & (Quiz.date == date)).first()
    if quiz:
        mark = 0
        for i in db_sess.query(Test).filter(Test.id_quiz == quiz.id_quiz).all():
            if i.mark:
                mark += i.mark
        return mark
    return 0


@app.template_filter('get_outcome')
def get_results(args):
    id_student = args[0]
    count = args[1]
    mark = 0
    for j in db_sess.query(Quiz).filter(Quiz.id_student == id_student).all():
        for i in db_sess.query(Test).filter(
                Test.id_quiz == j.id_quiz):
            if i.mark:
                mark += i.mark
    return round(mark / count, 2)


@app.template_filter('get_mark')
def get_results(args):
    id_student = args[0]
    count = args[1]
    mark = 0
    for j in db_sess.query(Quiz).filter(Quiz.id_student == id_student).all():
        for i in db_sess.query(Test).filter(
                Test.id_quiz == j.id_quiz):
            if i.mark:
                mark += i.mark
    return math.ceil(mark / count)


if __name__ == '__main__':
    db_sess = db_session.create_session()
    main()
