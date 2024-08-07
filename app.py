from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from dotenv import load_dotenv
import os
import bcrypt
import random
import string

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    user = db.relationship('User', backref=db.backref('articles', lazy=True))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=35)])
    submit = SubmitField('Register')

class DeployForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Deploy')

class EditForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Update')

@app.route('/')
def index():
    return render_template('index.html', logo_text="My Logo")

@app.route('/about')
def about():
    return render_template('about.html', logo_text="My Logo")

@app.route('/services')
def services():
    return render_template('services.html', logo_text="My Logo")

@app.route('/contact')
def contact():
    return render_template('contact.html', logo_text="My Logo")

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin/login.html', form=form, logo_text="My Logo")

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('admin_login'))
    articles = Article.query.all()
    return render_template('admin/index.html', articles=articles, logo_text="My Logo")

@app.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=form.username.data, password=hashed.decode('utf-8'), role='user')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('user/register.html', form=form, logo_text="My Logo")

@app.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('user/login.html', form=form, logo_text="My Logo")

@app.route('/user/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/user/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    articles = Article.query.filter_by(user_id=user_id).all()
    return render_template('user/dashboard.html', articles=articles, logo_text="My Logo")

def generate_slug(title):
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    return f"{title.replace(' ', '-')}-{random_string}"

@app.route('/user/deploy', methods=['GET', 'POST'])
def deploy():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    form = DeployForm()
    if form.validate_on_submit():
        slug = generate_slug(form.title.data)
        new_article = Article(
            user_id=session['user_id'],
            title=form.title.data,
            name=form.name.data,
            company=form.company.data,
            content=form.content.data,
            slug=slug
        )
        db.session.add(new_article)
        db.session.commit()
        flash(f'Article deployed successfully! View it <a href="{url_for("view_article", slug=new_article.slug)}">here</a>.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('user/deploy.html', form=form, logo_text="My Logo")

@app.route('/user/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    article = Article.query.get_or_404(article_id)
    if article.user_id != session['user_id']:
        return redirect(url_for('dashboard'))
    form = EditForm(obj=article)
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.commit()
        flash('Article updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('user/edit.html', form=form, article_id=article_id, logo_text="My Logo")

@app.route('/user/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    article = Article.query.get_or_404(article_id)
    if article.user_id == session['user_id']:
        db.session.delete(article)
        db.session.commit()
        flash('Article deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/article/<slug>')
def view_article(slug):
    article = Article.query.filter_by(slug=slug).first_or_404()
    return render_template('article.html', article=article, logo_text=article.company)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
