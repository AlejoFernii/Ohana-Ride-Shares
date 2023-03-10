from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import ride, user, booked

@app.route('/home')
def home_page():
    if not session['user_id']:
        return redirect('/')

    session_user = {
        'id':session['user_id']
    }
    current_user = user.User.get_one(session_user)
    if not current_user:
        return redirect('/')
    # all_likes = like.Like.get_all_likes()
    all_rides = ride.Ride.get_all_with_user()
    all_users = user.User.get_all()
    # all_comments = comment.Comment.get_all_comments_with_creator() 

    all_bookings = booked.Booked.get_all()

    

    return render_template('home.html', all_users=all_users, current_user=current_user, all_rides=all_rides, all_bookings=all_bookings)
    