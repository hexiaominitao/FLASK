from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, TimeField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from .models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', [DataRequired(), Length(max=255)])
    password = PasswordField('密码', [DataRequired()])
    remember = BooleanField('记住我')

    def validata(self):
        check_validate = super(LoginForm, self).validata()
        if not check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('账户或密码错误')
            return False
        if not self.user.check_password(self.password.data):
            self.username.errors.append('账户或密码错误')
            return False
        return True


class RegisterForm(FlaskForm):
    username = StringField('用户名', [DataRequired(), Length(max=255)])
    password = PasswordField('密码', [DataRequired(), Length(min=8)])
    confirm = PasswordField('确认密码', [DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()
        if check_validate:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('该用户名已存在，请换一个')
            return False
        return True


class SeqForm(FlaskForm):
    sample = StringField('样本编号', [DataRequired(), Length(max=255)])
    item = StringField('检测项目', [DataRequired(), Length(max=255)])
    index = StringField('Index', [DataRequired(), Length(max=255)])
    index_p5 = StringField('Index_p5', [DataRequired(), Length(max=255)])
    note = StringField('备注')


class RunForm(FlaskForm):
    runname = StringField('Run name', [DataRequired(), Length(max=255)])
    paltform = StringField('检测平台', [DataRequired(), Length(max=255)])
    start = StringField('上机时间', [DataRequired(), Length(max=255)])
    end = StringField('下机时间', [DataRequired(), Length(max=255)])


class AllSeqForm(FlaskForm):
    seqinfo = TextAreaField('上机信息', [DataRequired(), Length(max=2550)])


class IndexForm(FlaskForm):
    indexinfo = TextAreaField('index信息', [DataRequired(), Length(max=2550)])