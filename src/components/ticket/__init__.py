from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from src import *
from src.models.ticket import Ticket
from src.models.order import Order

ticket_blueprint = Blueprint('ticket', __name__, template_folder='../../templates')

@ticket_blueprint.route('/create',methods = ['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        ticket = Ticket(title=request.form['title'], quantity=request.form['quantity'], event_id = request.form['event_id'])
        db.session.add(ticket)
        db.session.commit()
        return "OK"
    pass


@ticket_blueprint.route('/purchase',methods = ['GET','POST'])
@login_required
def purchase():
    if request.method == 'POST':
        event = Event.query.get(request.form['event_id'])
        order = Order(
            event_id = event.id, 
            user_id=current_user.id
            )
        db.session.add(order)
        db.session.commit()
        order_items = []
        for ticket in event.tickets():
            quantity = int(request.form[ticket.title])
            if quantity > 0:
                for _ in range(quantity):
                    order_item = OrderItem(
                        order_id=order.id, 
                        ticket_id=ticket.id
                        )
                    ticket.quantity -= 1
                    order_items.append(order_item)
        db.session.add_all(order_items)
        db.session.commit()
    return redirect(url_for('user.orders'))