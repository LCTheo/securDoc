
from importlib.metadata import files

from flask import Flask, request, send_file, render_template
from flask_restx import Api, Resource, reqparse
import os
from os import path
from werkzeug.utils import secure_filename
from flask_cors import CORS
import tempfile
import pyAesCrypt
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
bufferSize = 64 * 1024
password = secret = os.getenv('DOC_PASS')


@api.route("/rsc/<string:user_id>")
class ResourcesList(Resource):

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.expect(token_argument)
    def get(self, user_id):
        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):
                if path.exists("./Resources/ " +user_id):
                    return {'response': os.listdir("./Resources/ " +user_id)}, 200
                else:
                    return {'response': []}, 200
            else:
                return {'response': "Token validation error "}, 400

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
                    if not path.exists("./Resources/ " +user_id):
                        os.mkdir("Resources/" + user_id)

                    file.save(os.path.join("/tmp/", filename))
                    name = filename.rsplit('.', 1)
                    cpt = 1
                    if path.exists(os.path.join("./Resources/" + user_id, filename)):

                        while path.exists(os.path.join("./Resources/" + user_id, name[0 ] +str(cpt ) +". " +name[1])):
                            cpt += 1
                        filepath = os.path.join("./Resources/" + user_id, name[0 ] +str(cpt ) +". " +name[1])
                    else:
                        filepath = os.path.join("./Resources/" + user_id, filename)

                    pyAesCrypt.encryptFile(os.path.join("/tmp/", filename), filepath, password, bufferSize)
                    os.remove(os.path.join("/tmp/", filename))
                    return {'response': "File successfully uploaded"}, 200
                else:
                    return {'response': "Empty file"}, 401
            else:
                return {'response': "fail "}, 400


@api.route("/rsc/<string:user_id>/<string:resource_name>")
class Resource(Resource):

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.response(401, 'Resources access : Unexciting resource')
    @api.response(402, 'Resources access : decryption error')
    @api.expect(token_argument)
    def get(self, user_id, resource_name):

        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):
                filepath = "./Resources/" + user_id + "/" + resource_name
                if path.exists(filepath):
                    fOut = tempfile.NamedTemporaryFile()
                    pyAesCrypt.decryptFile(filepath, fOut.name, password, bufferSize)
                    return send_file(fOut.name, as_attachment=True, attachment_filename=resource_name)
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
