from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username", type=str, required=True, help="This field cannot be blank."
    )
    parser.add_argument(
        "password", type=str, required=True, help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_user_by_username(data["username"]):
            return {"message": "Username already taken. Please try again."}, 400

        user = UserModel(**data)

        try:
            user.save_to_db()
        except:
            return {"message": "An error occurred while trying to insert new user."}, 500

        return (
            {"message": "User '{}' created successfully".format(data["username"])},
            201,
        )
