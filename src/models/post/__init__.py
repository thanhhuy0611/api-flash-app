from src import db

from src.models.user import Users

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    content =  db.Column(db.String,nullable= True)
    image_url = db.Column(db.String,nullable= True)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id),nullable = False)
    like_list = db.relationship('Like', backref=db.backref('post'), passive_deletes="all", lazy=True)
    comment_list = db.relationship('Comment', backref=db.backref('post'), passive_deletes="all" , lazy=True)

    def render(self):
        likes = [like.render() for like in self.like_list]
        comments = [comment.render() for comment in self.comment_list]
        return {
            "post_id":self.id,
            "content":self.content,
            "image_url":self.image_url,
            "user": {
                "id": self.user.id,
                "name": self.user.user_name 
            },
            "likes": {
                'count':len(likes),
                'liker_name':[like['owner'].user_name for like in likes],
                'liker_id':[like['owner'].id for like in likes]
            },
            "comment":{
                'count':len(comments),
            },
            "created_on":self.created_on,
            "updated_on":self.updated_on,
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content =  db.Column(db.String,nullable= False)  
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer,db.ForeignKey(Users.id),nullable = False)
    post_id = db.Column(db.Integer,db.ForeignKey(Post.id,  ondelete='CASCADE'),nullable = False)
    like_list = db.relationship('Like', backref=db.backref('comment'),  passive_deletes="all", lazy=True)
    
    def render(self):
        likes = [like.render() for like in self.like_list]
        likers = [like['owner'] for like in likes]
        return {
            'comment_id': self.id,
            'content':self.content,
            'owner': self.user.user_name,
             "likes": {
                'count':len(likes),
                'liker_name':[like['owner'].user_name for like in likes],
                'liker_id':[like['owner'].id for like in likes]
            },
            "created_on":self.created_on,
            "updated_on":self.updated_on,
        }


class Like(db.Model):
    id = db.Column(db.Integer, primary_key = True)  
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer,db.ForeignKey(Users.id),nullable = False)
    post_id = db.Column(db.Integer,db.ForeignKey(Post.id, ondelete='CASCADE'),nullable = True)
    comment_id = db.Column(db.Integer,db.ForeignKey(Comment.id, ondelete='CASCADE'),nullable = True)
    content =  db.Column(db.String,nullable= True)  

    def render(self):
        return {
            'like_id': self.id,
            'owner': self.user,
            "created_on":self.created_on,
            "updated_on":self.updated_on,
        }

db.create_all()
