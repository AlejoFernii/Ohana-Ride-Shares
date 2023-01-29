from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import ride,user,booked,message

@app.route('/driver/<int:ride_id>/<int:driver_id>')
def book_ride(ride_id,driver_id):

    data = {
        'driver_id':driver_id,
        'ride_id':ride_id
    }

    booked.Booked.save(data)

    return redirect('/home')

@app.route('/cancel/<int:id>')
def cancel_booking(id):

    data = {
        'id':id
    }
    booked.Booked.cancel(data)

    return redirect('/home')

@app.route('/view/booking/<int:id>')
def view_booking(id):
    if 'user_id' not in session:
        return redirect('/')


    data ={'id':id}
    one_Ride = booked.Booked.get_one(data)
    user_id={'id':session['user_id']}
    current_user = user.User.get_one(user_id)
    msms = message.Message.get_all_from_booking(data)
    for m in msms:
        one_Ride.messages.append(m)

    return render_template('view.html', one_Ride=one_Ride, current_user=current_user, booking=data)