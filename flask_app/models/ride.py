from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user,booked


from flask import flash


class Ride:
    DB = 'rideshare'

    def __init__(self, data):
        self.id = data['id']
        self.rider_id = data['rider_id']
        self.date = data['date']
        self.pick_up = data['pick_up']
        self.destination = data['destination']
        self.details = data['details']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.riders = []
        self.driver = False

    @classmethod
    def save(cls, data):
        query = "INSERT INTO rides (rider_id, date, pick_up, destination, details, created_at, updated_at) VALUES ( %(rider_id)s, DATE_FORMAT(%(date)s,'%%%%W %%%%M %%%%D %%%%Y'), %(pick_up)s, %(destination)s, %(details)s, NOW(), NOW() );"

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all_with_user(cls):

        query = "SELECT * FROM rides JOIN users ON rides.rider_id = users.id;"

        results = connectToMySQL(cls.DB).query_db(query)
        all_rides = []
        for row in results:
            one_ride = cls(row)

            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'pw': row['pw'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at'],
            }
            author = user.User(user_data)
            one_ride.creator = author

            all_rides.append(one_ride)
            all_bookings = booked.Booked.get_all()
            for book in all_bookings:
                for ride in all_rides:
                    if ride.id == book.ride_id.id:
                        all_rides.remove(ride)

        
        return all_rides

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM rides JOIN users ON rides.rider_id = users.id WHERE rides.id = %(id)s;"

        result = connectToMySQL(cls.DB).query_db(query, data)

        one_ride = cls(result[0])

        user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'pw': result[0]['pw'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at'],
        }
        author = user.User(user_data)
        one_ride.creator = author

        return one_ride

    @classmethod
    def update_ride(cls, data):
        query = "UPDATE rides SET date = DATE_FORMAT(%(date)s,'%%%%W %%%%M %%%%D %%%%Y'), pick_up = %(pick_up)s, destination = %(destination)s, details = %(details)s, updated_at = NOW() WHERE id = %(id)s;"

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def add_rider(cls, data):
        query = "SELECT * FROM rides JOIN users ON rides.rider_id = users.id WHERE rides.id = %(id)s;"

        result = connectToMySQL(cls.DB).query_db(query, data)

        one_ride = cls(result[0])

        user_data = {
            'id': result[0]['users.id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'pw': result[0]['pw'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at'],
        }
        author = user.User(user_data)
        one_ride.creator = author
        one_ride.riders.append(data['user_id'])

        return one_ride

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM rides WHERE id = %(id)s;"

        return connectToMySQL(cls.DB).query_db(query, data)

    @staticmethod
    def validate_ride(ride):
        is_valid = True
        if len(ride['date']) <= 0:
            flash("Ride Must Have A Date.", 'ride')
            is_valid = False
        if len(ride['pick_up']) <= 0:
            flash("Ride Must Have A Pick-Up Location", 'ride')
            is_valid = False
        if len(ride['destination']) <= 0:
            flash("Ride Must Have A Destination.", 'ride')
            is_valid = False
        if len(ride['details']) <= 0:
            flash("All Fields Required.", 'ride')
            is_valid = False
        # if Ride['is_under'] == None:
        #     flash("All Fields Required.", 'Ride' )
        #     is_valid=False
        return is_valid
