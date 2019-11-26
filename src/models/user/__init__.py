from flask_login import UserMixin
from src import db
from werkzeug.security import check_password_hash, generate_password_hash

#DEFINING MODELS

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    email = db.Column(db.String,nullable= False,unique = True)
    password = db.Column(db.String,nullable = False,unique = False)
    user_name =  db.Column(db.String,nullable= False)
    user_type = db.Column(db.String,nullable= False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)

