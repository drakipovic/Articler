from flask_restful import Resource

class Users(Resource):

    def get(self):
        return {'user': 'dino'}

    def post(self):
        return {'you POST': 'yeah'}