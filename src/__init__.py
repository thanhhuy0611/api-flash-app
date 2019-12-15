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
    if request.method == 'POST':
        post_id = request.get_json()['post_id']
        if not post_id == 'list':
            posts = Post.query.filter_by(id = post_id).first()
            return jsonify(
                success=True,
                posts=posts.render()
            )
        if post_id == 'list' :
            user_id = request.get_json()['user_id']
            if user_id:
                posts = Post.query.filter_by(user_id = user_id).order_by(Post.updated_on.desc()).all()
            else:
                posts = Post.query.order_by(Post.updated_on.desc()).limit(8)
            return jsonify(
                success=True,
                posts=[post.render() for post in posts]
            )

#load more
@app.route('/post/loadmore', methods=['GET','POST'])
@login_required
def load_more():
    last_post = request.get_json()['last_post']
    if request.method == "POST":
        posts = Post.query.filter(Post.id < last_post).order_by(Post.updated_on.desc()).limit(8)
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

#like post
@app.route('/likepost', methods=['GET','POST'])
@login_required
def like_post():
    dt = request.get_json()
    if request.method == "POST":
        like = Like.query.filter_by(post_id=dt['post_id'],user_id=current_user.id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return jsonify(success=True)
        if not like:
            like = Like(
                user_id=current_user.id,
                post_id=dt['post_id']   
            )
            db.session.add(like)
            db.session.commit()
            return jsonify(success=True)
#==========================================================================
#get comments
@app.route('/getcomment', methods=['GET','POST'])
@login_required
def get_comment():
    if request.method == 'POST':
        comment_id = request.get_json()['comment_id']
        if not comment_id == 'list':
            comment = Comment.query.filter_by(id = comment_id).first()
            return jsonify(
                success=True,
                comments=comment.render()
            )
        if comment_id == 'list' :
            comments = Comment.query.filter_by(post_id=request.get_json()['post_id']).order_by(Comment.updated_on.desc()).all()
            filter = request.args.get('filter')
            if filter == 'most-recently':
                comments = Comment.query.order_by(Event.updated_on.desc()).all()
            # if filter == 'top-viewed':
            #     comments = Blog.query.order_by(Blog.view_count.desc()).all()
            return jsonify(
                success=True,
                comments=[comment.render() for comment in comments]
            )


# create comment
@app.route('/createcomment', methods=['GET','POST'])
@login_required
def create_comment():
    if request.method == "POST":
        comment = Comment(
            content=request.get_json()['content'],
            post_id=request.get_json()['post_id'],
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        return jsonify(success=True)

# delete comment
@app.route('/commentdelete', methods=['GET','POST'])
@login_required
def delete_comment():
    if request.method == "POST":
        comment = Comment.query.filter_by(id=request.get_json()['id']).first()
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return jsonify(success=True)
        else:
            return jsonify(success=False,status='comment is not exist')

#like comment
@app.route('/likecomment', methods=['GET','POST'])
@login_required
def like_comment():
    dt = request.get_json()
    if request.method == "POST":
        like = Like.query.filter_by(comment_id=dt['comment_id'],user_id=current_user.id).first()
        if like:
            db.session.delete(like)
            db.session.commit()
            return jsonify(success=True)
        if not like:
            like = Like(
                user_id=current_user.id,
                comment_id=dt['comment_id']   
            )
            db.session.add(like)
            db.session.commit()
            return jsonify(success=True)

#=================================================================
#follow user
@app.route('/follow/<id>', methods=['GET'])
@login_required
def follow_user(id):
    follow = Follow.query.filter_by(follower_id=current_user.id, following_id=id).first()
    if follow:
        db.session.delete(follow)
        db.session.commit()
        return jsonify(success=True)
    if not follow:
        follow = Follow(
            follower_id=current_user.id,
            following_id=id   
        )
        db.session.add(follow)
        db.session.commit()
        return jsonify(success=True)

#list post following
@app.route('/post/following', methods=['GET'])
@login_required
def posts_following():
    user = Users.query.filter_by(id = current_user.id).first()
    return jsonify(posts=user.render_following_post())

#search
@app.route('/search',methods=['GET','POST'])
@login_required
def search():
    if request.method == "POST":
        key = request.get_json()["key"]
        search = f"%{key}%"
        posts = Post.query.filter(Post.content.like(search)).all()
        return jsonify(
                success=True,
                posts=[post.render() for post in posts]
            )

#get other user information
@app.route('/user/<id>',methods=['GET'])
@login_required
def get_user(id):
    user = Users.query.filter_by(id = id).first()
    return jsonify(
        user_id=user.id,
        user_name=user.user_name,
        follow=user.render_follow()
    )
#==========================================================================
#get current user
@app.route('/currentuser')
@login_required
def get_current_user():
    user = Users.query.filter_by(id = current_user.id).first()
    if user:
        return jsonify(
            user_id=current_user.id,
            user_name=current_user.user_name,
            follower_id=user.render_follow()
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
        




