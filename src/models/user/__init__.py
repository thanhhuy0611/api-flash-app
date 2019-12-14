from flask_login import LoginManager, UserMixin
from src import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin


#DEFINING MODELS

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    email = db.Column(db.String,nullable= False,unique = True)
    password = db.Column(db.String,nullable = True,unique = False)
    user_name =  db.Column(db.String,nullable= False)
    list_post = db.relationship('Post', backref='user',lazy = True)
    list_like = db.relationship('Like', backref='user',lazy = True)
    list_comment = db.relationship('Comment', backref='user', lazy = True)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())
    
    def render_follow(self):
        array_followers = [{'id':follower.follower.id, 'name':follower.follower.user_name} for follower in self.list_follower]
        array_following = [{'id':following.following.id, 'name':following.following.user_name} for following in self.list_following]
        return {
            'count_followers':len(array_followers),
            'list_followers':array_followers,
            'count_following':len(array_following),
            'list_following':array_following,
        }
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)

class Follow(db.Model):
    # data of table
    id = db.Column(db.Integer, primary_key = True)
    follower_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    following_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    # relationship to Users:
    follower = db.relationship("Users", foreign_keys=[follower_id],backref='list_following')
    following = db.relationship("Users", foreign_keys=[following_id],backref='list_follower')

class Token(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uuid = db.Column(db.String,nullable= True)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    user = db.relationship(Users)

class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id), nullable=False)
    user = db.relationship(Users)



# setup login manager
login_manager = LoginManager()

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Token ', '', 1)
        token = Token.query.filter_by(uuid=api_key).first()
        if token:
            return token.user
    return None

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
