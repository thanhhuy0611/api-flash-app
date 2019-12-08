from flask import Flask, render_template, request, redirect, url_for, flash, request, jsonify
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
# from .config import Config
from werkzeug.security import check_password_hash, generate_password_hash
from flask_migrate import Migrate
from flask_cors import CORS
import uuid
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__, static_folder='static')

app.config.from_object('config.Config')

#config SQLAlchemy
db = SQLAlchemy(app)
from .facebooklogin.cli import create_db
#-------------------------------------------------
##  import models
from src.models.user import *
from src.models.event import *
from src.models.ticket import *
from src.models.order import *
from src.models.post import *

db.create_all()


migrate = Migrate(app, db)

CORS(app)
## set up flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# set current_user
@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    return None

#-------------------------------------------------------
## import controlers file
from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')
from src.components.event import event_blueprint
app.register_blueprint(event_blueprint, url_prefix='/event')
from src.components.ticket import ticket_blueprint
app.register_blueprint(ticket_blueprint, url_prefix='/ticket')
from .facebooklogin.oauth import blueprint
app.register_blueprint(blueprint, url_prefix="/login")

# show all post
@app.route('/postlist',methods=["GET","POST"])
@login_required
def post_list():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.updated_on.desc()).all()
        filter = request.args.get('filter')
        if filter == 'most-recently':
            posts = Post.query.order_by(Event.updated_on.desc()).all()
        # if filter == 'top-viewed':
        #     posts = Blog.query.order_by(Blog.view_count.desc()).all()
        return jsonify(
            success=True,
            posts=[post.render() for post in posts]
        )

# delete post
@app.route('/postdelete', methods=['GET','POST'])
@login_required
def delete_post():
    if request.method == "POST":
        post = Post.query.filter_by(id=request.get_json()['id']).first()
        if post:
            db.session.delete(post)
            db.session.commit()
            return jsonify(success=True)
        if not post:
            return jsonify(success=False,status='post is not exist')

# edit post
@app.route('/editpost', methods=['GET','POST'])
@login_required
def edit_post():
    if request.method == "POST":
        post = Post.query.filter_by(id = request.get_json()['id']).first()
        if post:
            post.content = request.get_json()['content'],
            post.image_url = request.get_json()['image_url'],
            db.session.commit()
            return jsonify(success=True)
        if not post:
            return jsonify(success=False,status='post is not exist')

# create post
@app.route('/createpost', methods=['GET','POST'])
@login_required
def create_post():
    if request.method == "POST":
        post = Post(
            content = request.get_json()['content'],
            image_url = request.get_json()['image_url'],
            user_id = current_user.id
        )
        db.session.add(post)
        db.session.commit()
        return jsonify(success=True)

#get current user
@app.route('/currentuser')
@login_required
def get_current_user():
    return jsonify(
        user_id=current_user.id,
        user_name=current_user.user_name,
    )

# sign up account
@app.route('/signup', methods=["GET","POST"])
def sign_up():
    if request.method == "POST":
        dt = request.get_json()
        is_email_exits = Users.query.filter_by(email = dt['email']).first()
        if is_email_exits:
            return jsonify({'success':False, 'status':'Email already exists'})
        if not is_email_exits:
            new_user =  Users(
                email = dt['email'],        
                user_name = dt['name'],
            )
            new_user.set_password(dt['password'])
            db.session.add(new_user)
            db.session.commit()
            user = Users.query.filter_by(email = dt['email']).first()
            if user:
                new_token =  Token(
                    uuid = uuid.uuid4().hex,
                    user_id = user.id
                )
                db.session.add(new_token)
                db.session.commit()
            return jsonify({'token': new_token.uuid,
                            'success':True,    
                })


# check account login
@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(email = request.get_json()["email"]).first()
        if not user:
            return jsonify({'success':False, 'status':'Email is not correct'})
        if user:
            if user.check_password(request.get_json()['password']):
                new_token =  Token(
                    uuid = uuid.uuid4().hex,
                    user_id = user.id
                )
                db.session.add(new_token)
                db.session.commit()
                return jsonify({'success':True, 'token':new_token.uuid})
            else:
                return jsonify({'success':False, 'status':'Password is not correct'})


# logout 
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    if request.method == "POST":
        user_token = Token.query.filter_by(user_id = current_user.id).first()
        db.session.delete(user_token)
        db.session.commit()
        return jsonify({"success": True})
        




