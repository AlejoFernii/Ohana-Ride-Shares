from flask_app import app
from flask_app.controllers import home, rides, users, bookings,messages

if __name__ == '__main__':
    app.run(debug=True)

