from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin

from .extensions import bcrypt

db = SQLAlchemy()

tags = db.Table(
    'post_tags', db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

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
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    roles = db.relationship('Role', secondary=roles, backref=db.backref('users', lazy='dynamic'))
    # report = db.relationship('Sample', backref='user', lazy='dynamic')

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

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))
    text = db.Column(db.Text())
    publish_data = db.Column(db.DateTime())
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('post', lazy='dynamic'))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    text = db.Column(db.Text())
    data = db.Column(db.DateTime())
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Fastqc(db.Model):
    __tablename__ = "fastqc"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    迈景编号 = db.Column(db.String(50), nullable=False)
    样本编号 = db.Column(db.String(50))
    Reads数 = db.Column(db.Integer())
    Reads占比 = db.Column(db.Float())
    Base数 = db.Column(db.Integer())
    Q20 = db.Column(db.Float())
    Q30 = db.Column(db.Float())
    GC比例 = db.Column(db.Float())
    N比例 = db.Column(db.Float())

    def __repr__(seif):
        return '<Fastqc {}>'.format(seif.迈景编号)


class Bamqc(db.Model):
    __tablename__ = "bamqc"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    迈景编号 = db.Column(db.String(50), nullable=False)
    样本编号 = db.Column(db.String(50))
    样本类型 = db.Column(db.String(50))
    平台 = db.Column(db.String(50))
    总reads数 = db.Column(db.Integer())
    数据量 = db.Column(db.Float())
    比对率 = db.Column(db.Float())
    PCR重复 = db.Column(db.Float())
    在靶率 = db.Column(db.Float())
    平均深度 = db.Column(db.Float())
    平均深度_去重 = db.Column(db.Float())
    均一性0 = db.Column(db.Float())
    均一性10 = db.Column(db.Float())
    均一性20 = db.Column(db.Float())
    均一性50 = db.Column(db.Float())
    均一性100 = db.Column(db.Float())
    均一性200 = db.Column(db.Float())
    均一性300 = db.Column(db.Float())

    def __repr__(seif):
        return '<Bamqc {}>'.format(seif.迈景编号)


class Sample(db.Model):
    __tablename__ = "sample"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    序号 = db.Column(db.String(50), nullable=False)
    迈景编号 = db.Column(db.String(50), nullable=False)
    PI姓名 = db.Column(db.String(50), nullable=True)
    销售代表 = db.Column(db.String(50), nullable=True)
    申请单号 = db.Column(db.String(50), nullable=True)
    患者姓名 = db.Column(db.String(50), nullable=True)
    病人性别 = db.Column(db.String(50), nullable=True)
    病人年龄 = db.Column(db.String(50), nullable=True)
    民族 = db.Column(db.String(50), nullable=True)
    籍贯 = db.Column(db.String(50), nullable=True)
    检测项目 = db.Column(db.String(500), nullable=True)
    病人联系方式 = db.Column(db.String(50), nullable=True)
    病人身份证号码 = db.Column(db.String(50), nullable=True)
    病人地址 = db.Column(db.String(50), nullable=True)
    门诊住院号 = db.Column(db.String(50), nullable=True)
    医生姓名 = db.Column(db.String(50), nullable=True)
    医院名称 = db.Column(db.String(50), nullable=True)
    科室 = db.Column(db.String(50), nullable=True)
    病理号 = db.Column(db.String(50), nullable=True)
    临床诊断 = db.Column(db.String(500), nullable=True)
    临床诊断日期 = db.Column(db.String(50), nullable=True)
    病理诊断 = db.Column(db.String(500), nullable=True)
    病理诊断日期 = db.Column(db.String(50), nullable=True)
    病理样本收到日期 = db.Column(db.String(50), nullable=True)
    组织大小 = db.Column(db.String(50), nullable=True)
    病理审核 = db.Column(db.String(500), nullable=True)
    标本内细胞总量 = db.Column(db.String(50), nullable=True)
    肿瘤细胞含量 = db.Column(db.String(50), nullable=True)
    特殊说明 = db.Column(db.String(50), nullable=True)
    镜下所见 = db.Column(db.String(500), nullable=True)
    病理报告人 = db.Column(db.String(10), nullable=True)
    是否接受化疗 = db.Column(db.String(50), nullable=True)
    化疗开始时间 = db.Column(db.String(50), nullable=True)
    化疗结束时间 = db.Column(db.String(50), nullable=True)
    化疗治疗效果 = db.Column(db.String(50), nullable=True)
    是否靶向药治疗 = db.Column(db.String(50), nullable=True)
    靶向药治疗开始时间 = db.Column(db.String(50), nullable=True)
    靶向药治疗结束时间 = db.Column(db.String(50), nullable=True)
    靶向药治疗治疗效果 = db.Column(db.String(50), nullable=True)
    是否放疗 = db.Column(db.String(50), nullable=True)
    放疗开始时间 = db.Column(db.String(50), nullable=True)
    放疗结束时间 = db.Column(db.String(50), nullable=True)
    放疗治疗效果 = db.Column(db.String(50), nullable=True)
    有无家族遗传疾病 = db.Column(db.String(50), nullable=True)
    有无其他基因疾病 = db.Column(db.String(50), nullable=True)
    有无吸烟史 = db.Column(db.String(50), nullable=True)
    项目类型 = db.Column(db.String(50), nullable=True)
    样本来源 = db.Column(db.String(50), nullable=True)
    采样方式 = db.Column(db.String(50), nullable=True)
    样本类型 = db.Column(db.String(50), nullable=True)
    数量 = db.Column(db.String(50), nullable=True)
    运输方式 = db.Column(db.String(50), nullable=True)
    状态是否正常 = db.Column(db.String(50), nullable=True)
    送检人 = db.Column(db.String(50), nullable=True)
    送检日期 = db.Column(db.String(50), nullable=True)
    收样人 = db.Column(db.String(50), nullable=True)
    收样日期 = db.Column(db.String(50), nullable=True)
    检测日期 = db.Column(db.String(50), nullable=True)
    报告发出时间 = db.Column(db.String(50), nullable=True)
    报告收件人 = db.Column(db.String(50), nullable=True)
    联系电话 = db.Column(db.String(50), nullable=True)
    联系地址 = db.Column(db.String(50), nullable=True)
    备注 = db.Column(db.String(500), nullable=True)
    申请单病理报告扫描件命名 = db.Column(db.String(50), nullable=True)
    不出报告原因 = db.Column(db.String(200), nullable=True)
    录入 = db.Column(db.String(50), nullable=True)
    审核 = db.Column(db.String(50), nullable=True)
    病理报告时间 = db.Column(db.Date, index=True)
    # 报告制作人 = db.Column(db.Integer(), db.ForeignKey('user.id'))
    report = db.relationship('Report', backref='report', lazy='dynamic')

    def __repr__(seif):
        return '<Sample {}>'.format(seif.迈景编号)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sam = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    mutation = db.Column(db.String(4096), nullable=True)

    sample = db.Column(db.Integer(), db.ForeignKey('sample.id'))
    rna_qc = db.Column(db.String(50), nullable=True)
    # dna_qc = db.Column(db.String(50), nullable=True)
    # qc = db.Column(db.String(4096), nullable=True)

