from flask import Flask, request, render_template, redirect, send_from_directory, send_file, jsonify, json, \
    make_response
from flask_restx import Api, Resource, reqparse
import os
from os import listdir, path
from os.path import isfile, join
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import Auth

app = Flask(__name__)
api = Api(app=app, version='0.1', title='Resources Doc API', validate=True)
token_argument = reqparse.RequestParser()
token_argument.add_argument('token', type=str, required=True)
data_argument = api.parser()
data_argument.add_argument('token', type=str, required=True)
data_argument.add_argument('Data', type=FileStorage, required=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/test/')
def upload_form():
    return render_template('test.html')


@api.route("/resources/<string:user_id>")
class ResourcesList(Resource):

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.expect(token_argument)
    def get(self, user_id):
        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):
                return {'response': "all file"}, 200
            else:
                return {'response': "fail "}, 400

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.response(401, 'Resources access : No file in payload')
    @api.expect(token_argument)
    def post(self, user_id):
        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):

                # check if the post request has the file part
                if 'file' not in request.files:
                    return {'response': "No file in payload "}, 401
                file = request.files['file']
                if file.filename == '':
                    return {'response': "No file in payload "}, 401
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    onlyDir = [d for d in listdir("./Resources") if not isfile(join("./Resources", d))]
                    if not (user_id in onlyDir):
                        os.mkdir("Resources/" + user_id)
                    file.save(os.path.join("./Resources/"+user_id, filename))
                    print('File successfully uploaded')
                    return redirect('/')
                else:
                    print('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                    return redirect(request.url)
            else:
                return {'response': "fail "}, 400



@api.route("/resources/<string:user_id>/<string:resource_name>")
class Resource(Resource):

    @api.response(200, 'Resources access : Success')
    @api.response(400, 'Resources access : Token validation error')
    @api.response(401, 'Resources access : unexciting resource')
    @api.expect(token_argument)
    def get(self, user_id, resource_name):

        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):
                filepath = "Resources\\"+user_id+"\\"+resource_name
                if path.exists(filepath):
                    return send_file(filepath, as_attachment=True)
                else:
                    return {'response': "unexciting resource "}, 401
            else:
                return {'response': "Token validation error "}, 400

    def delete(self, user_id, resource_name):

        data = token_argument.parse_args(request)

        if data.get('token'):
            if Auth.verifyToken(data.get('token'), user_id):
                if path.exists("./Resources/"+user_id+"/"+resource_name):

                    return {'response': "file found" }, 200
            else:
                return {'response': "fail "}, 400



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
