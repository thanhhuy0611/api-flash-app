from src import db

from src.models.user import Users
from src.models.ticket import Ticket

class Event(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    name = db.Column(db.String(1000),nullable= False)
    contain =  db.Column(db.String,nullable= False)
    location = db.Column(db.String,nullable= False)
    banner_url = db.Column(db.String,nullable= True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer,nullable = False)
    
    def tickets(self):
        tickets = Ticket.query.filter_by(event_id = self.id).all()
        return tickets

    def ratings(self):
        ratings = Rating.query.filter_by(event_id = self.id).all()
        for rating in ratings:
            rating.user = Users.query.get(rating.user_id)
        return ratings

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body =  db.Column(db.String,nullable= False)  
    stars = db.Column(db.Integer,nullable = False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.Integer,nullable = False)
    event_id = db.Column(db.Integer,nullable = False)

db.create_all()
