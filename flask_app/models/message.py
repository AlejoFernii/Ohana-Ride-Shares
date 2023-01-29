from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user,booked


from flask import flash

class Message:
    DB = 'rideshare'
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.booked_id = data['booked_id']
        self.message = data['message']
        self.time_posted= data['time_posted']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None


    @classmethod
    def save(cls,data):
        query ="INSERT INTO messages (user_id, booked_id, message, time_posted, created_at, updated_at) VALUES ( %(user_id)s, %(booked_id)s, %(message)s,DATE_FORMAT(NOW(),'%%%%r') ,NOW(), NOW() );"

        return connectToMySQL(cls.DB).query_db(query,data)


    @classmethod
    def get_all_from_booking(cls,data):
        query = "SELECT * FROM messages JOIN users ON messages.user_id = users.id JOIN booked ON messages.booked_id = booked.id WHERE booked.id = %(id)s;"

        results = connectToMySQL(cls.DB).query_db(query,data)

        all_messages = []
        for row in results:
            one_message = cls(row)

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
            one_message.creator = author

            all_messages.append(one_message)

        return all_messages


    # @classmethod
    # def time_posted(cls,data):
    #     query = "SELECT created_at FROM messages AS %r"




    @staticmethod
    def validate_message(m):
        is_valid = True
        if len(m['message']) <= 0 :
            flash('Message Cannot Be Blank')
            is_valid=False
        return is_valid