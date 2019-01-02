from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin

from .ext import bcrypt

db = SQLAlchemy()

roles = db.Table(
    'role_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    passwd = db.Column(db.String(255))
    roles = db.relationship('Role', secondary=roles, backref=db.backref('users', lazy='dynamic'))
    seq_info = db.relationship('SeqInfo', backref='user', lazy='dynamic')

    # seq = db.relationship('SeqInfo', backref='user', lazy='dynamic')

    def __init__(self, username):
        self.username = username
        default = Role.query.filter_by(name="default").one()
        self.roles.append(default)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def set_password(self, password):
        self.passwd = bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.passwd, password)

    @property
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # def __init__(self, name,description):
    #     self.name = name
    #     self.description = description

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class RunInfo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    count = db.Column(db.Integer())
    start_T = db.Column(db.DateTime())
    end_T = db.Column(db.DateTime())
    paltform = db.Column(db.String(255))
    seq_info = db.relationship('SeqInfo', backref='run_info', lazy='dynamic')

    def __repr__(seif):
        return '<RunInfo {}>'.format(seif.name)

    def get_id(self):
        return str(self.id)


class SeqInfo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sample = db.Column(db.String(255))
    item = db.Column(db.String(255))
    index = db.Column(db.String(255))
    index_p5 = db.Column(db.String(255))
    note = db.Column(db.String(255))
    run_info_id = db.Column(db.Integer(), db.ForeignKey('run_info.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    # def __init__(self, sample):
    #     self.sample = sample

    def __repr__(self):
        return "<SeqInfo '{}'>".format(self.sample)


class SeqIndex(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    index = db.Column(db.String(255))
