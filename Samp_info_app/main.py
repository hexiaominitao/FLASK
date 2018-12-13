from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(255))
    passwd = db.Column(db.String(255))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return "<User '{}'>".format(self.username)


tags = db.Table('post_tags', db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')))


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


from sqlalchemy import func


def sidebar_data():
    recent = Post.query.order_by(Post.publish_data.desc()).limit(5).all()
    top_tags = db.session.query(Tag, func.count(tags.c.post_id).label('total')).join(tags).group_by(Tag).order_by(
        'total DESC').limit(5).all()
    return recent, top_tags


import random, datetime
# user = User.query.get(1)
# tag_one = Tag('Python')
# tag_two = Tag('Flask')
# tag_three = Tag('Sqlalchemy')
# tag_four = Tag('Jinja')
# tag_list = [tag_one,tag_two,tag_three,tag_four]
#
# s = "Example text"
#
# for i in range(100):
#     new_post = Post("Post" + str(i))
#     new_post.user = user
#     new_post.publish_data = datetime.datetime.now()
#     new_post.text = s
#     new_post.tags = random.sample(tag_list,random.randint(1,3))
#     db.session.add(new_post)
#
# db.session.commit()

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentFrom(Form):
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    text = TextAreaField('Comment', validators=[DataRequired()])


@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    posts = Post.query.order_by(
        Post.publish_data.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()
    return render_template('index.html', posts=posts, recent=recent, top_tags=top_tags)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.data.desc()).all()
    recent, top_tags = sidebar_data()
    form = CommentFrom()
    if form.validate_on_submit():
        new_comment = Comment()
        new_comment.name = form.name.data
        new_comment.text = form.name.data
        new_comment.post_id = post_id
        new_comment.data = datetime.datetime.now()
        db.session.add(new_comment)
        db.session.commit()
        post = Post.query.get_or_404(post_id)
        tags = post.tags
        comments = post.comments.order_by(Comment.data.desc()).all()
        recent, top_tags = sidebar_data()

    return render_template('post.html', form=form, post=post, tags=tags, comments=comments, recent=recent,
                           top_tags=top_tags, )


@app.route('/tags/<string:tag_name>')
def tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_data.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('tag.html', tag=tag, posts=posts, recent=recent, top_tags=top_tags)


@app.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_data.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template('user.html', user=user, posts=posts, recent=recent, top_tags=top_tags)


if __name__ == "__main__":
    app.run()
