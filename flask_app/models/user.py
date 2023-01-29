from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ride
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = 'rideshare'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pw = data['pw']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_admin = False
        self.rides = []

    @classmethod
    def create(cls, data):
        query = """ INSERT INTO users (first_name, last_name, email, pw, created_at, updated_at)
                    VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw)s, NOW(),NOW()); """

        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"

        result = connectToMySQL(cls.DB).query_db(query, data)

        return cls(result[0])

    @classmethod
    def get_user_with_all_rides(cls, data):
        query = "SELECT * FROM users LEFT JOIN rides ON users.id=rides.rider_id WHERE users.id = %(id)s;"

        results = connectToMySQL(cls.DB).query_db(query, data)

        
        all_rides = []
        for row in results:

            user_data = {
            'id': row['id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'pw': row['pw'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at'],
        }
            req_ride = cls(row)
            

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
            one_ride = ride.Ride(ride_data)
            

            req_ride.rides.append(one_ride)
            all_rides.append(req_ride)


        return all_rides

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        return connectToMySQL(cls.DB).query_db(query)

    # @classmethod
    # def get_by_username(cls,data):
    #     query = "SELECT * FROM users WHERE username = %(username)s;"
    #     result = connectToMySQL('wall').query_db(query,data)
    #     if len(result) < 1:
    #         return False
    #     return cls(result[0])

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate(member):
        is_valid = True
        if len(member['first_name']) <= 0:
            flash("First Name Required.", 'reg')
            is_valid = False
        if len(member['last_name']) <= 0:
            flash("Last Name Required.", 'reg')
            is_valid = False
        if len(member['pw']) < 8:
            flash("Password Must Be At Least 8 Characters.", 'reg')
            is_valid = False
        if not EMAIL_REGEX.match(member['email']):
            flash("Invalid Email Format.", 'reg')
            is_valid = False
        if member['conpw'] != member['pw']:
            flash("Password Must Match.", 'reg')
            is_valid = False
        return is_valid
