from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

##import __init__.src (app,db,model,..)
from src import *

## define blue print (class = (url_prefix, route to view))
event_blueprint = Blueprint('event', __name__, template_folder='../../templates')

## 'root/event/create'
@event_blueprint.route('/create',methods = ['GET','POST'])
@login_required
def create():
  if request.method == 'POST':
    new_event = Event(
      name = request.form['name'],
      contain = request.form['contain'],
      banner_url = request.form['banner_url'],
      location = request.form['location'],
      user_id = current_user.id,
    )
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('user.dashboard',id = current_user.id))
  return render_template('/event/create.html')


## delete event
@event_blueprint.route('/delete/<id>',methods = ['GET','POST'])
@login_required
def delete(id):
  event = Event.query.get(id)
  if not event:
    return "there is no such post"
  if current_user.id == event.user_id: 
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('user.dashboard', id = current_user.id))
  return render_template('/event/view.html', event = event)


##Edit a event
@event_blueprint.route('/<id>/edit',methods=['GET','POST'])
@login_required
def edit(id):
    event = Event.query.get(id)
    if request.method == "POST":
        event.title = request.form['name']
        event.contain = request.form['contain']
        event.banner_url = request.form['banner_url'],
        event.location = request.form['location']
        db.session.commit()
        return redirect(url_for('event.view',id = id))
    return render_template('event/edit.html',event = event)

## 'root/event/view/<id>'
@event_blueprint.route('/view/<id>',methods = ['GET','POST'])
@login_required
def view(id):
  event = Event.query.get(id)
  return render_template('/event/view.html', event = event)


##Rating
@event_blueprint.route('/<id>/rating', methods=['GET','POST'])
@login_required
def rating(id):
    if request.method == "POST":
        rating = Rating(
            body = request.form["body"],
            stars = 5, ## how to get value form view.html from
            user_id = current_user.id,
            event_id = id
        )
    print(rating.stars,'star')
    db.session.add(rating)
    db.session.commit()
    return redirect(url_for('event.view',id = id))