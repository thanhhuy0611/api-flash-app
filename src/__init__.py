from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, validators, PasswordField, SubmitField


app = Flask(__name__, static_folder='static')
app.config.from_object('config.Config')

#config SQLAlchemy
db = SQLAlchemy(app)

#-------------------------------------------------
##  import models
from src.models.user import Users, Blog, Comment
from src.models.event import *

#import class WTForm
from src.components.user import *

migrate = Migrate(app, db)
## set up flask-login
login_manager= LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
# set current_user
@login_manager.user_loader
def load_user(id):
  return Users.query.filter_by(id = b).first()

#-------------------------------------------------------
## import controlers file
from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')
from src.components.event import event_blueprint
app.register_blueprint(event_blueprint, url_prefix='/event')

# set current_user
@login_manager.user_loader
def load_user(b):
    return Users.query.filter_by(id = b).first()

# show all event
@app.route('/',methods=["GET","POST"])
def home():
    events = Event.query.all()
    filter = request.args.get('filter')
    if filter == 'most-recently':
        events = Event.query.order_by(Event.created_on.desc()).all()
    # if filter == 'top-viewed':
    #     posts = Blog.query.order_by(Blog.view_count.desc()).all()
    return render_template('root/index.html',events = events, ref = 'home')

# sign up account
@app.route('/signup', methods=["GET","POST"])
def sign_up():
    form = RegisterForm()
    if not current_user.is_anonymous:
        return redirect(url_for('home'))
    if request.method == "POST":
        if form.validate_on_submit():
        #check email unique
            is_email_exits = Users.query.filter_by(email = form.email.data).first()
            print("emailcheck",is_email_exits)
            if is_email_exits:
                flash('Email is exits. Please try again!','danger')
            if not is_email_exits:
                print(form.user_type.data)
                new_user =  Users(
                    email = form.email.data,        
                    user_name = form.user_name.data,
                    user_type = form.user_type.data
                )
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('home'))
        else:
            for field,error in form.errors.items():
                flash(f'{field}: {error[0]}','danger')
    return render_template('root/signup.html', form = form)

# check account login
@app.route('/login', methods=["GET","POST"])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('home'))

    if request.method == "POST":
        user = Users.query.filter_by(email = request.form["email"]).first()
        if not user:
            flash('Email incorrect!','danger')
        if user:
            if user.check_password(request.form['password']):
                login_user(user)
                return redirect(url_for('user.dashboard',id = current_user.id))
            else:
                flash('Password incorrect!','danger')
    return render_template('root/login.html')

# logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




