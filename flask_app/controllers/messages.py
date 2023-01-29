from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import ride,user,booked,message

@app.route('/message', methods = ['POST'])
def add_message():
    # m_val = request.form['message']
    # if not message.Message.validate_message(m_val):
    #     return redirect(request.referrer)
    
    message.Message.save(request.form)

    return redirect(request.referrer)