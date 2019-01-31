from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileRequired, FileAllowed  # 文件上传模块
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from app.models import User, Post, Tag, Comment, Sample
from wtforms.widgets import ListWidget, CheckboxInput

from .extensions import file_bam_qc, file_fastq_qc, file_sample_info, file_zip


class CommentFrom(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField('评论', validators=[DataRequired()])


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


class PostForm(FlaskForm):
    title = StringField('标题', [DataRequired(), Length(max=255)])
    text = TextAreaField('文章内容', [DataRequired()])


class SampleUploadForm(FlaskForm):
    file = FileField('上传文件', validators=[FileRequired(), FileAllowed(file_sample_info)])


class FastqUploadForm(FlaskForm):
    file = FileField('上传文件', validators=[FileRequired(), FileAllowed(file_fastq_qc)])


class BamUploadForm(FlaskForm):
    file = FileField('上传文件', validators=[FileRequired(), FileAllowed(file_bam_qc)])


class ZipUploadForm(FlaskForm):
    name = StringField('报告编号', [DataRequired(), Length(max=25)])
    file = FileField('上传文件', validators=[FileRequired(), FileAllowed(file_zip)])


class ItemFrom(FlaskForm):
    name = StringField('申请单号', [DataRequired(), Length(max=25)])
    sample_id = StringField('迈景编号', [DataRequired(), Length(max=25)])
    item = RadioField('检测项目', coerce=str)

    # 从数据库获取数据渲染到表单
    def __init__(self, report_id, *args, **kwargs):
        super(ItemFrom, self).__init__(*args, **kwargs)
        self.item.choices = [(cho, cho) for cho in
                             ((Sample.query.filter(Sample.申请单号 == report_id).first()).检测项目).split('、')]


class CheckForm(FlaskForm):
    item = BooleanField([DataRequired()])


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class FormProject(FlaskForm):
    Code = StringField('Code', [DataRequired(message='Please enter your code')])
    Tasks = MultiCheckboxField(DataRequired(message='Please tick your task'), choices=[('1', '1')])
