from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, validators, PasswordField, SubmitField,SelectField
from itsdangerous import URLSafeTimedSerializer
import requests
from requests.exceptions import HTTPError

    
###import model
# from src.models.user import Users, Blog, Comment
# from src import app

##import __init__.src (app,db,model,..)
from src import *

## define blue print (class = (url_prefix, route to view))
user_blueprint = Blueprint('user', __name__, template_folder='../../templates/user')


## Create form validation class
class EmailForm(FlaskForm):
    email = StringField(
        'Email', validators=[
            validators.DataRequired(), 
            validators.Email("Please enter correct email!")
            ])
    submit = SubmitField('Send')

class PasswordForm(FlaskForm):
    password = PasswordField(
        'New password', validators=[
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm password', validators=[validators.DataRequired()])
    submit = SubmitField('Change password')

class RegisterForm(FlaskForm):
    user_name = StringField(
        "User name", validators=[
            validators.DataRequired(), 
            validators.Length(min=3,max=20,message="Need to be in between 3 and 20")
    ])
    user_type = SelectField(
        "You are guest or organiser", 
        validators=[validators.DataRequired()],
        choices=[('org', 'Organiser'), ('gue', 'Guest')]
    )
    email = StringField(
        "Email", validators=[
            validators.DataRequired(), 
            validators.Length(min=3,max=200,message="Need to be in between 3 and 20"), 
            validators.Email("Please enter correct email!")
    ])
    password = PasswordField(
        'Password', validators=[
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm password', validators=[validators.DataRequired()])
    submit = SubmitField('Sign up')

## reset password
@user_blueprint.route('/reset',methods=["GET","POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        print('username',user.user_name)
        ##config token
        ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        token = ts.dumps(user.email, salt='recover-password-secret')
        print('token',token)
        send_email(token,user.email,user.user_name)
        # Redirect to the main login form here with a "password reset email sent!"
    else:
        for field, errs in form.errors.items():
            flash(f"{field}: {errs[0]}",'danger')
    return render_template('reset.html', form=form)
#define send email func 
def send_email(token,email,name):
    domain_name = 'sandboxae05f1ada35142198d4234a824ae31a9.mailgun.org'
    url = f"https://api.mailgun.net/v3/{domain_name}/messages"
    try: 
        reponse = requests.post(
            url,
            auth=("api", app.config['API_KEY']),
            data={"from": "ADMIN - Ticket box <thanhhuy0611@gmail.com>",
                "to": [email, "thanhhuy0611@gmail.com"],
                "subject": "TICKET BOX-FORGET PASSWORD",
                "html": render_template('email_recover.html',token = token)}
        )
        print(reponse)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}') 
    except Exception as err:
        print(f'Other error occurred: {err}')  
    else:
        print('Success!')


## set new password
@user_blueprint.route('/new_password/<token>',methods = ['GET','POST'])
def new_password(token):
    form = PasswordForm()
    print('token',token)
    ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    email = ts.loads(token,salt='recover-password-secret', max_age = 600)
    user = Users.query.filter_by(email = email).first()
    if not user:
        flash('INVALID TOKEN, PLEASE TRY AGAIN','danger')
    else:
        
        if request.method == "POST":    
            if form.validate_on_submit():
                user.set_password(form.password.data)
                login_user(user)
                return redirect(url_for('home'))
            else:
                for field,error in form.errors.items():
                    flash(f'{field}: {error[0]}','danger')
    return render_template('new_password.html',form = form)

## dashboard root/user/<id>
@user_blueprint.route('/<id>',methods=["GET","POST"])
@login_required
def dashboard(id):
    user = Users.query.get(id)
    events =  Event.query.filter_by(user_id = id).order_by(Event.created_on.desc()).all()
    return render_template('user/dashboard.html',events = events)



###########____REFER___#################
# comment------------------------------------------

## delete comment
# @user_blueprint.route('/<id>/comments/<id_comment>', methods=['GET','POST'])
# @login_required
# def delete_comment(id,id_comment):
#     ref = request.args.get('ref')
#     print('ref',ref)
#     comment = Comment.query.filter_by(id = id_comment).first()
#     db.session.delete(comment)
#     db.session.commit()
#     return redirect(url_for(ref, id= id))


##-----###################################################
