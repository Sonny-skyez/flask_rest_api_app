import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", type=str, required=True, help="This field cannot be blank.")
    parser.add_argument("password", type=str, required=True, help="This field cannot be blank.")

    def post(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        data = UserRegister.parser.parse_args()
        if UserModel.find_user_by_username(data["username"]):
            return {"message": "Username already taken. Please try again."}, 400

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User '{}' created successfully".format(data["username"])}, 201
