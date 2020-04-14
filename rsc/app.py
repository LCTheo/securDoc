

from importlib.metadata import files

from flask import Flask, request, send_file, render_template
from flask_restx import Api, Resource, reqparse
import os
from os import path
from werkzeug.utils import secure_filename
from flask_cors import CORS
import Auth

app = Flask(__name__)
CORS(app)
api = Api(app=app, version='1.0', title='Resources Doc API', validate=True)
token_argument = reqparse.RequestParser()
token_argument.add_argument('token', type=str, required=True)
data_argument = api.parser()
data_argument.add_argument('token', type=str, required=True)
data_argument.add_argument('Data', type=files, required=True)
if path.exists("./Resource"):
    os.mkdir("./Resource")


@app.route('/upload/')
def upload_form():
    return render_template('upload.html')


@api.route("/rsc/<string:user_id>")
class ResourcesList(Resource):

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.expect(token_argument)
    def get(self, user_id):
        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):
                if path.exists("./Resources/"+user_id):
                    return {'response': os.listdir("./Resources/"+user_id)}, 200
                else:
                    return {'response': []}, 200
            else:
                return {'response': "fail "}, 400

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.response(401, 'Resources access : Unexciting resource')
    @api.expect(token_argument)
    def post(self, user_id):
        data = token_argument.parse_args(request)
        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):

                # check if the post request has the file part
                if 'file' not in request.files:
                    return {'response': "No field file in payload "}, 401
                file = request.files['file']
                if file.filename == '':
                    return {'response': "Empty file in payload "}, 401
                if file:
                    filename = secure_filename(file.filename)
                    if not path.exists("./Resources/"+user_id):
                        os.mkdir("Resources/" + user_id)

                    if path.exists(os.path.join("./Resources/" + user_id, filename)):
                        name = filename.rsplit('.', 1)
                        cpt = 1
                        while path.exists(os.path.join("./Resources/" + user_id, name[0]+str(cpt)+"."+name[1])):
                            cpt += 1
                        file.save(os.path.join("./Resources/" + user_id, name[0]+str(cpt)+"."+name[1]))
                    else:
                        file.save(os.path.join("./Resources/" + user_id, filename))
                    return {'response': "File successfully uploaded"}, 200
                else:
                    return {'response': "Umpty file"}, 401
            else:
                return {'response': "fail "}, 400


@api.route("/rsc/<string:user_id>/<string:resource_name>")
class Resource(Resource):

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.response(401, 'Resources access : Unexciting resource')
    @api.expect(token_argument)
    def get(self, user_id, resource_name):

        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):
                filepath = "./Resources/" + user_id + "/" + resource_name
                if path.exists(filepath):
                    return send_file(filepath, as_attachment=True)
                else:
                    return {'response': "File doesn't exist"}, 401
            else:
                return {'response': "Token validation error"}, 400

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.response(401, 'Resources access : Unexciting resource')
    @api.expect(token_argument)
    def delete(self, user_id, resource_name):

        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):
                filepath = "./Resources/" + user_id + "/" + resource_name
                if path.exists(filepath):
                    os.remove(filepath)
                    return {'response': "File deleted"}, 200
                else:
                    return {'response': "File doesn't exist"}, 401
            else:
                return {'response': "Token validation error"}, 400


if __name__ == "__main__":
    app.run(host='0.0.0.0')
