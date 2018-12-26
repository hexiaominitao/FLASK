import datetime, os, xlrd
from os import path
from sqlalchemy import func, or_
from flask import render_template, Blueprint, redirect, url_for, abort, request, current_app, flash
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed

from ..models import db, Post, Tag, Comment, User, tags, Fastqc, Bamqc, Sample
from ..forms import CommentFrom, PostForm, SampleUploadForm, FastqUploadForm, BamUploadForm
from ..extensions import poster_permission, admin_permission, default_permission, file_bam_qc, file_fastq_qc, \
    file_sample_info, excel_rd, file_to_df
from ..tasks import send_mail

sam_bp = Blueprint('sam_bp', __name__, template_folder=path.join(path.pardir, 'templates', 'samp'), url_prefix="/samp")


# template_folder=path.join(path.pardir,'templates','sam_app')
def sidebar_data():
    recent = Post.query.order_by(Post.publish_data.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(tags.c.post_id).label('total')).join(tags).group_by(Tag).order_by(
        'total DESC').limit(5).all()
    return recent, top_tags


def float_to_percent(float_value):
    per = '{}%'.format((str(round(float_value,4) * 100))[:5])
    return per
sam_bp.add_app_template_filter(float_to_percent,'float_to_percent') #添加jinja2过滤器



@sam_bp.route('/',methods=['GET','POST'])
def index():
    # if request.method == 'GET':
    #     send_mail()
    return render_template('index.html')


@sam_bp.route('/new/', methods=['GET', 'POST'])
@login_required
@default_permission.require(http_exception=403)
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data)
        new_post.text = form.text.data
        new_post.publish_data = datetime.datetime.now()

        db.session.add(new_post)
        db.session.commit()

    return render_template('new.html', form=form)


# @sam_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# @poster_permission.require(http_exception=403)
# def edit_post(id):
#     post = Post.query.get_or_404(id)
#     permission = Permission(UserNeed(post.user_id))
#     if permission.can() or admin_permission.can():
#
#         form = PostForm()
#
#         if form.validate_on_submit():
#             post.title = form.title.data
#             post.text = form.text.data
#             post.publish_data = datetime.datetime.now()
#
#             db.session.add(post)
#             db.session.commit()
#
#             return redirect(url_for('.post', post_id=post.id))
#
#         form.text.data = post.text
#
#         return render_template('edit.html', post=post, form=form)
#     abort(403)


@sam_bp.route('/fileupload/', methods=['GET', 'POST'])
@login_required
@default_permission.require(http_exception=403)
def upload_sam():
    path_zip = current_app.config['UPLOADED_FILESAM_DEST']
    if request.method == 'GET':
        for file in os.listdir(path_zip):
            os.remove(os.path.join(path_zip, file))
    filename = None
    sam_form = SampleUploadForm()
    fastq_form = FastqUploadForm()
    bam_form = BamUploadForm()

    def sample_info(item_sample):
        Value = rows[title_ex.index(item_sample)]

        if type(Value) is float and Value > 1:
            Value = int(Value)
        if Value == '0%':
            Value = '0'
        return str(Value)

    if sam_form.validate_on_submit():
        for filename in request.files.getlist('file'):
            file_sample_info.save(filename)
        for file in os.listdir(path_zip):
            if file:
                wb_e = xlrd.open_workbook(os.path.join(path_zip, file))
                table = wb_e.sheets()[0]
                title_ex = table.row_values(0)

                if '报告收件人' in title_ex:
                    id_sa = title_ex.index('迈景编号')
                    cols = table.col_values(id_sa)
                    cols.pop(0)
                    for sample_id in cols:
                        sam = cols.index(sample_id) + 1
                        rows = (table.row_values(sam))

                        samp_info = Sample(序号=sample_info('序号'), 迈景编号=sample_info('迈景编号'),
                                           PI姓名=sample_info('PI姓名'), 销售代表=sample_info('销售代表'),
                                           申请单号=sample_info('申请单号'), 患者姓名=sample_info('患者姓名'),
                                           病人性别=sample_info('病人性别'), 病人年龄=sample_info('病人年龄'),
                                           民族=sample_info('民族'), 籍贯=sample_info('籍贯'),
                                           检测项目=sample_info('检测项目'), 病人联系方式=sample_info('病人联系方式'),
                                           病人身份证号码=sample_info('病人身份证号码'), 病人地址=sample_info('病人地址'),
                                           门诊住院号=sample_info('门诊/住院号'), 医生姓名=sample_info('医生姓名'),
                                           医院名称=sample_info('医院名称'), 科室=sample_info('科室'),
                                           病理号=sample_info('病理号'), 临床诊断=sample_info('临床诊断'),
                                           临床诊断日期=sample_info('诊断日期'), 病理诊断=sample_info('病理诊断'),
                                           病理诊断日期=sample_info('诊断日期'),
                                           病理样本收到日期=sample_info('病理样本收到日期'),
                                           组织大小=sample_info('组织大小（单位mm）'),
                                           病理审核=sample_info('病理审核'), 标本内细胞总量=sample_info('标本内细胞总量'),
                                           肿瘤细胞含量=sample_info('肿瘤细胞含量'), 特殊说明=sample_info('特殊说明'),
                                           是否接受化疗=sample_info('是否接受化疗'), 化疗开始时间=sample_info('开始时间'),
                                           化疗结束时间=sample_info('结束时间'), 化疗治疗效果=sample_info('治疗效果'),
                                           是否靶向药治疗=sample_info('是否靶向药治疗'),
                                           靶向药治疗开始时间=sample_info('开始时间'),
                                           靶向药治疗结束时间=sample_info('结束时间'),
                                           靶向药治疗治疗效果=sample_info('治疗效果'),
                                           是否放疗=sample_info('是否放疗'), 放疗开始时间=sample_info('起始时间'),
                                           放疗结束时间=sample_info('结束时间'), 放疗治疗效果=sample_info('治疗效果'),
                                           有无家族遗传疾病=sample_info('有无家族遗传疾病'),
                                           有无其他基因疾病=sample_info('有无其他基因疾病'),
                                           有无吸烟史=sample_info('有无吸烟史'), 项目类型=sample_info('项目类型'),
                                           样本来源=sample_info('样本来源'), 采样方式=sample_info('采样方式'),
                                           样本类型=sample_info('样本类型'), 数量=sample_info('数量'),
                                           运输方式=sample_info('运输方式'), 状态是否正常=sample_info('状态是否正常'),
                                           送检人=sample_info('送检人'), 送检日期=sample_info('送检日期'),
                                           收样人=sample_info('收样人'), 收样日期=sample_info('收样日期'),
                                           检测日期=sample_info('检测日期'), 报告发出时间=sample_info('报告发出时间'),
                                           报告收件人=sample_info('报告收件人'), 联系电话=sample_info('联系电话'),
                                           联系地址=sample_info('联系地址'), 备注=sample_info('备注'),
                                           申请单病理报告扫描件命名=sample_info('申请单、病理报告扫描件命名'),
                                           不出报告原因=sample_info('不出报告原因'), 录入=sample_info('录入'),
                                           审核=sample_info('审核'), 报告制作人=current_user.id)
                        if Sample.query.filter(Sample.迈景编号 == sample_id).first():
                            pass
                        else:
                            db.session.add(samp_info)
                            db.session.commit()
                            flash('成功上传样本信息登记表')
                    os.remove(os.path.join(path_zip, file))

    if fastq_form.validate_on_submit():
        for filename in request.files.getlist('file'):
            file_fastq_qc.save(filename)

        for file in os.listdir(path_zip):
            if file:
                file_vcf = path.join(path_zip, file)
                df, index_qc = file_to_df(file_vcf)

                for item in index_qc:
                    fastq_info = Fastqc(迈景编号=str(df.loc[item]['Runname']),
                                        样本编号=item,
                                        Reads数=int(df.loc[item]['Reads_num']),
                                        Reads占比=float(df.loc[item]['Reads_p']),
                                        Q20=float(df.loc[item]['Q20']),
                                        Q30=float(df.loc[item]['Q30']),
                                        GC比例=float(df.loc[item]['GC_rate']),
                                        N比例=int(df.loc[item]['N_couunt']))
                    # Base数 = int(df.loc[item]['Base_num']),
                    if Bamqc.query.filter(Fastqc.样本编号 == item).first():
                        pass
                    else:
                        db.session.add(fastq_info)
                        db.session.commit()
                        flash('成功上传')
                os.remove(os.path.join(path_zip, file))

    if bam_form.validate_on_submit():
        for filename in request.files.getlist('file'):
            file_bam_qc.save(filename)
        for file in os.listdir(path_zip):
            if file:
                wb_e = xlrd.open_workbook(os.path.join(path_zip, file))
                table = wb_e.sheets()[0]
                title_ex = table.row_values(0)

                if '[Total] Raw Reads (All reads)' in title_ex:
                    id_sa = title_ex.index('SAMPLE')
                    cols = table.col_values(id_sa)
                    cols.pop(0)
                    for sample_id in cols:
                        sam = cols.index(sample_id) + 1
                        rows = (table.row_values(sam))

                        bam_info = Bamqc(迈景编号=sample_info('SAMPLE')[:-1],
                                         样本编号=sample_info('SAMPLE'),
                                         样本类型=sample_info('sample type'),
                                         平台=sample_info('platform'),
                                         总reads数=sample_info('[Total] Raw Reads (All reads)'),
                                         数据量=sample_info('[Total] Raw Data(Mb)'),
                                         比对率=sample_info('[Total] Fraction of Mapped Reads'),
                                         PCR重复=sample_info('[Total] Fraction of PCR duplicate reads'),
                                         在靶率=sample_info('[Target] Fraction of Target Data in mapped data'),
                                         平均深度=sample_info('[Target] Average depth'),
                                         平均深度_去重=sample_info('[Target] Average depth(rmdup)'),
                                         均一性0=sample_info('[Target] Fraction Region covered > 0% AD'),
                                         均一性10=sample_info('[Target] Fraction Region covered > 10% AD'),
                                         均一性20=sample_info('[Target] Fraction Region covered > 20% AD'),
                                         均一性50=sample_info('[Target] Fraction Region covered > 50% AD'),
                                         均一性100=sample_info('[Target] Fraction Region covered > 100% AD'),
                                         均一性200=sample_info('[Target] Fraction Region covered > 200% AD'),
                                         均一性300=sample_info('[Target] Fraction Region covered > 300% AD'))
                        if Bamqc.query.filter(Bamqc.样本编号 == sample_id).first():
                            pass
                        else:
                            db.session.add(bam_info)
                            db.session.commit()
                            flash('成功上传')
                    os.remove(os.path.join(path_zip, file))

    return render_template('upload.html', sam_form=sam_form, fastq_form=fastq_form, bam_form=bam_form)


@sam_bp.route('/sampleinfo/', methods=['GET', 'POST'])
def sample_info():
    report_id = (request.url).split('=')[-1]
    df = {
        'status': Sample.query.filter(
            or_(Sample.迈景编号 == report_id, Sample.迈景编号.endswith(report_id), Sample.申请单号 == report_id)).all()
    }
    return render_template('sampleinfo.html', **df, report_id=report_id)


@sam_bp.route('/sampleinfo/<sample_id>', methods=['GET', 'POST'])
@login_required
@default_permission.require(http_exception=403)
def sample_detail(sample_id):
    df = {
        'status': Sample.query.filter(Sample.迈景编号 == sample_id).all()
    }
    return render_template('sample_detail.html', **df, sample_id=sample_id)


@sam_bp.route('/fastqc/', methods=['GET', 'POST'])
def fastqc():
    df = Fastqc.query.all()
    run_name = []
    for row in df:
        run_name.append(row.迈景编号)

    def dedupe(items):
        seen = set()
        for item in items:
            if item not in seen:
                yield item
            seen.add(item)
        return seen

    status = list(dedupe(run_name))
    return render_template('fastqc-run.html', status=status)


@sam_bp.route('/fastqc/<run_name>', methods=['GET', 'POST'])
def fastq_qc(run_name):
    df = {
        'status': Fastqc.query.filter(Fastqc.迈景编号 == run_name).all()
    }
    return render_template('fastqc.html', **df, run_name=run_name)


@sam_bp.route('/bamqc/', methods=['GET', 'POST'])
def bam_qc():
    df = {
        'status': Bamqc.query.all()
    }
    return render_template('bamqc.html', **df)
