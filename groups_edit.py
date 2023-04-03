from main import db_sess
from flask import render_template, redirect, request, abort
from data.group_class import Group, GroupForm
from data import db_session


def g():
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


def g_edit(id):
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


def g_delete(id):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).filter(Group.id_group == id).first()
    if group:
        db_sess.delete(group)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/groups')
