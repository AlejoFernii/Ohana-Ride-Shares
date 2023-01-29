from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import ride,user

@app.route('/create/Ride/<int:id>')
def create_page(id):

    user_id = {'id':id}
    current_user = user.User.get_one(user_id)

    return render_template('create.html',current_user=current_user)

@app.route('/create', methods=['POST'])
def create_Ride():
    data = request.form
    if not ride.Ride.validate_ride(data):
        return redirect(request.referrer)
    ride.Ride.save(data)

    return redirect('/home')

@app.route('/delete_ride/<int:id>')
def delete_ride(id):

    data = {
        'id':id
    }

    ride.Ride.destroy(data)

    return redirect('/home')


@app.route('/view/<int:id>')
def view_one(id):
    if 'user_id' not in session:
        return redirect('/')


    data ={'id':id}
    one_Ride = ride.Ride.get_one_with_user(data)
    user_id={'id':session['user_id']}
    current_user = user.User.get_one(user_id)
    return render_template('view.html', one_Ride=one_Ride, current_user=current_user)

@app.route('/edit/<int:id>')
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {'id':id}
    one_ride = ride.Ride.get_one_with_user(data)
    user_id={'id':session['user_id']}
    current_user = user.User.get_one(user_id)
    return render_template('edit.html', one_ride=one_ride, current_user=current_user)

@app.route('/edit/ride', methods = ['POST'])
def edit_Ride():
    
    if not ride.Ride.validate_ride(request.form):
        return redirect(request.referrer)

    ride.Ride.update_ride(request.form)
    Ride_id = request.form['id']

    return redirect('/home')


