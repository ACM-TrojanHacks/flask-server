import os
from flask import Flask, flash, request, redirect, url_for
import werkzeug
from flask_restful import reqparse, Api, Resource

from .clarifai import detect
from .db import insertIntoCollection, getSummary 

UPLOAD_FOLDER = "../uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
api = Api(app)

class UploadImage(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location='files')
        args = self.parser.parse_args()
        image = args.get("file")
        filename = os.path.join(app.root_path, UPLOAD_FOLDER, image.filename)
        image.save(filename)
        items = detect(filename)
        x = insertIntoCollection(items)
        print(x)
        return { "msg" : x }, 201

class GetSummary(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def get(self):
        y = getSummary()
        return { "msg": y }, 201

api.add_resource(UploadImage, '/upload_image')

api.add_resource(GetSummary, '/get_summary')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0", ssl_context='adhoc')