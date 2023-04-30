from flask import Flask, render_template, flash , request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = "key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
#@app.before_first_request
def create_tables():
    db.create_all()
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(225))
    content = db.Column(db.Text)
    author = db.Column(db.String(225))
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)
class PostForm(FlaskForm):
    title = StringField("Title", validators =[DataRequired()])
    content = StringField("Content", validators =[DataRequired()])
    author = StringField("Author", validators =[DataRequired()])
    submit = SubmitField("Submit")
@app.route('/post', methods = ['GET', 'POST'])
def index():
    form = PostForm()
    if form.is_submitted() and form.validate():
        post = Posts(content = form.content.data, author = form.author.data, title = form.title.data)
        form.title.data = ""
        form.content.data = ""
        form.author.data = ""
        db.session.add(post)
        db.session.commit()
    our_posts = Posts.query.order_by(Posts.date_posted)
    return render_template('index.html', form = form, our_posts = our_posts)
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/feed', methods = ['GET', 'POST'])
def feed():
    our_posts = Posts.query.order_by(Posts.date_posted)
    return render_template('feed.html', our_posts = our_posts)
if __name__ == "__main__":
    app.run(debug=True)
