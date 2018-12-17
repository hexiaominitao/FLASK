from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length,EqualTo,URL
from app.models import User,Post,Tag,Comment

class CommentFrom(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField('评论', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('用户名',[DataRequired(),Length(max=255)])
    password = PasswordField('密码',[DataRequired()])
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
    username = StringField('用户名',[DataRequired(),Length(max=255)])
    password = PasswordField('密码',[DataRequired(),Length(min=8)])
    confirm = PasswordField('确认密码',[DataRequired(),EqualTo('password')])
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

class PostForm(FlaskForm):
    title = StringField('标题',[DataRequired(),Length(max=255)])
    text = TextAreaField('文章内容',[DataRequired()])

