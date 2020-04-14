import hashlib

import pymongo

from flask import Flask, request
from flask_restx import Api, Resource, reqparse, fields
from flask_cors import CORS
import Token

myclient = pymongo.MongoClient('mongodb://mongo:27017/')
mydb = myclient["API_USERS"]
print("server version:", myclient.server_info()["version"])

app = Flask(__name__)
CORS(app)
api = Api(app=app, version='0.1', title='Users Api', description='', validate=True)
users_arguments = reqparse.RequestParser()
users_arguments.add_argument('id', type=str, required=True)
users_arguments.add_argument('password', type=str, required=True)

user_definition = api.model('User Informations', {
    'id': fields.String(required=True),
    'password': fields.String(required=True)
})

user_definition2 = api.model('New password', {
    'new_password': fields.String(required=True)
})


@api.route("/users/")
class UsersList(Resource):
    @api.response(200, 'Flask REST API_USERS : Authentication success')
    @api.response(400, 'Flask REST API_USERS : Authentication error')
    @api.expect(users_arguments)
    def get(self):
        """
        returns a list of users
        """
        data = users_arguments.parse_args(request)
        password = data.get("password")
        user_id = data.get('id')
        cursor = mydb.users.find(
            {'id': data.get('id'), "password": hashlib.sha512(password.encode("utf-8")).hexdigest()}, {"_id": 0})

        data = []
        for user in cursor:
            data.append(user)
        if len(data) == 0:
            return {"response": None}, 400
        else:
            token = Token.getToken(user_id, hashlib.sha512(password.encode("utf-8")).hexdigest())
            return {"response": token}, 200

    @api.response(200, 'Flask REST API_USERS : User creation success')
    @api.response(400, 'Flask REST API_USERS : User already existing')
    @api.expect(user_definition)
    def post(self):
        """
        Add a new user to the list
        """
        data = request.get_json()
        id = data.get('id')
        password = data.get('password')
        if id and password:
            if mydb.users.find_one({"id": id}):
                return {"response": None}, 400
            else:
                mydb.users.insert_one({"id": id, "password": hashlib.sha512(password.encode("utf-8")).hexdigest()})
                return {"response": "User creation success"}, 200


@api.route("/users/<string:id>/<string:password>")
class User(Resource):
    @api.response(200, 'Flask REST API_USERS : User update success')
    @api.response(400, 'Flask REST API_USERS : Error : Invalid credentials')
    @api.expect(user_definition2)
    def put(self, id, password):
        """
        Edits a selected user
        """
        data = request.get_json()
        new_password = data.get("new_password")
        if mydb.users.find_one({"id": id, "password": hashlib.sha512(password.encode("utf-8")).hexdigest()}):
            mydb.users.update_one({'id': id},
                                  {'$set': {"password": hashlib.sha512(new_password.encode("utf-8")).hexdigest()}})
            return {"response": {"id": id, "password": hashlib.sha512(new_password.encode("utf-8")).hexdigest()}}, 200
        else:
            return {"response": None}, 400

    @api.response(200, 'Flask REST API_USERS : User delete success')
    @api.response(400, 'Flask REST API_USERS : Error :Invalid credentials')
    def delete(self, id, password):
        """
        Deletes a selected user
        """
        if mydb.users.find_one({"id": id, "password": hashlib.sha512(password.encode("utf-8")).hexdigest()}):
            mydb.users.delete_one({'id': id})
            return {"response": {"id": id, "password": hashlib.sha512(password.encode("utf-8")).hexdigest()}}, 200
        else:
            return {"response": None}, 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
