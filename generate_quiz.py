from data import db_session
from data.group_class import Group, GroupForm
from data.question_class import Question, QuestionForm
from data.student_class import Student, StudentForm
from data.quiz_class import Quiz, QuizForm
from data.test_class import Test
from random import choice


def generate_quiz(id_student, date_quiz=None, groups=[]):
    # Создаёт quiz для одного студента
    db_sess = db_session.create_session()

    query_question = db_sess.query(Question).filter(Question.id_group.in_(groups)).all()

    quiz = Quiz(id_student=id_student, date=date_quiz)
    db_sess.add(quiz)
    db_sess.commit()

    used_questions = []
    for i in range(5):
        test = Test(id_quiz=quiz.id_quiz)

        id_quest = choice(query_question).id_question
        while id_quest in used_questions:
            id_quest = choice(query_question).id_question
        test.id_question = id_quest

        used_questions.append(id_quest)

        db_sess.add(test)

    db_sess.commit()


def generate_full(id_students, groups=[]):
    # Создаёт quiz для всех студентов
    db_sess = db_session.create_session()

    if not groups:
        for i in range(len(db_sess.query(Group).all())):
            groups.append(i + 1)

    for id_student in id_students:
        generate_quiz(id_student, groups=groups)
