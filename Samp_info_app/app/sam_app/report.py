from os import path
from flask import render_template, Blueprint, redirect, url_for, abort, request, current_app, flash, send_from_directory

from ..models import User
from ..forms import CheckForm,FormProject

rep_bp = Blueprint('rep_bp', __name__, template_folder=path.join(path.pardir, 'templates', 'rep'), url_prefix="/rep")


@rep_bp.route('/',methods=['GET','POST'])
def index():
    # if request.method == 'POST':
    #     s_option = request.values.getlist("s_option")
    #     for s in s_option:
    #         print(s)
    df = {
        "pages": User.query.all()
    }
    form = FormProject()
    if form.validate_on_submit():
        print()
    return render_template('seq.html',**df,form=form)


@rep_bp.route('/runinfo/')
def runinfo():
    return render_template('runinfo.html')


@rep_bp.route('/rep_mut/')
def rep_mut():
    return render_template('rep_mut.html')

@rep_bp.route('/seqinfo/')
def seqinfo():
    return render_template('seqinfo.html')


@rep_bp.route('/muinfo/')
def muinfo():
    return render_template('muinfo.html')


@rep_bp.route('/mufinfo/')
def mufinfo():
    return render_template('mufinfo.html')


@rep_bp.route('/musinfo/')
def musinfo():
    return render_template('musinfo.html')


@rep_bp.route('/repinfo/')
def repinfo():
    return render_template('repinfo.html')
