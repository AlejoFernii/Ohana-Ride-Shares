from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, ride
from flask import flash


class Booked:
    DB = 'rideshare'

    def __init__(self, data):
        self.id = data['id']
        self.driver_id = data['driver_id']
        self.ride_id = data['ride_id']
        self.created_at = data['created_at']
        self.messages = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO booked ( driver_id, ride_id, created_at ) VALUES ( %(driver_id)s, %(ride_id)s, NOW() );"

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM booked JOIN users ON booked.driver_id = users.id JOIN rides ON booked.ride_id = rides.id;"

        results = connectToMySQL(cls.DB).query_db(query)

        all_bookings = []
        for row in results:
            one_booking = cls(row)
            print(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'pw': row['pw'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            author = user.User(user_data)
            one_booking.driver_id = author
            
            ride_data = {
                "id": row['rides.id'],
                "rider_id": row['rider_id'],
                "date": row['date'],
                "pick_up": row['pick_up'],
                "destination": row['destination'],
                "details": row['details'],
                "created_at": row['rides.created_at'],
                "updated_at": row['rides.updated_at']
            }

            req_ride = ride.Ride(ride_data)

            one_booking.ride_id = req_ride
            req_id = {'id': row['rider_id']}
            req_author = user.User.get_one(req_id)

            one_booking.ride_id.creator = req_author


            all_bookings.append(one_booking)

        return all_bookings


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM booked JOIN users ON booked.driver_id = users.id JOIN rides ON booked.ride_id = rides.id WHERE booked.id = %(id)s;"

        result = connectToMySQL(cls.DB).query_db(query,data)
        print(result)

        one_booking = cls(result[0])
        for row in result:
            # print(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'pw': row['pw'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at'],
            }
            author = user.User(user_data)
            one_booking.driver_id = author
            
            ride_data = {
                "id": row['rides.id'],
                "rider_id": row['rider_id'],
                "date": row['date'],
                "pick_up": row['pick_up'],
                "destination": row['destination'],
                "details": row['details'],
                "created_at": row['rides.created_at'],
                "updated_at": row['rides.updated_at']
            }

            req_ride = ride.Ride(ride_data)

            one_booking.ride_id = req_ride
            req_id = {'id': row['rider_id']}
            req_author = user.User.get_one(req_id)

            one_booking.ride_id.creator = req_author


        return one_booking


    @classmethod
    def cancel(cls,data):
        query = "DELETE FROM booked WHERE id = %(id)s;"

        return connectToMySQL(cls.DB).query_db(query,data)
    # @staticmethod
    # def validate_booking(data):

    #     is_valid = True

    #     all_bookings = Booked.get_all()
    #     for book in all_bookings:
    #         if data['driver_id'] == book['driver_id'] and data['ride_id'] == book['ride_id']:
    #             flash("You have already agreed to drive")

