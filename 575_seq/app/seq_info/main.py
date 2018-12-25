from os import path
from flask_login import login_user, logout_user
from flask import render_template, Blueprint, redirect, url_for, flash, current_app, session
from flask_principal import Identity, AnonymousIdentity, identity_changed

from app.models import db, User
from app.forms import LoginForm, RegisterForm

main = Blueprint(
    'main', __name__, template_folder=path.join(path.pardir, 'templates', 'main')
)


@main.route('/')
def index():
    return redirect(url_for('bp_seq.index'))


@main.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data
        ).one()
        login_user(user)
        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )
        flash('登录成功！！！', category='success')
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('bp_seq.index'))
        else:
            return redirect(url_for('main.register'))
    return render_template('login.html', form=form)


@main.route('/logout/', methods=['GET', 'POST'])
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )
    flash('注销成功', category='success')
    return redirect(url_for('bp_seq.index'))


@main.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)

        db.session.add(new_user)
        db.session.commit()

        flash('注册成功', category='success')
        return redirect(url_for('.login'))
    return render_template('register.html', form=form)
