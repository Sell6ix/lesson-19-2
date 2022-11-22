from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from service.implemented import user_service as service

user_ns = Namespace("users")


@user_ns.route("/")
class UsersView(Resource):
    def get(self):
        models = service.get_all()
        res = UserSchema(many=True).dump(models)
        return res, 200

    def post(self):
        req_json = request.json
        model = service.create(req_json)
        return "", 201, {"location": f"/users/{model.id}"}


@user_ns.route("/<int:id>")
class UserView(Resource):
    def get(self, id: int):
        model = service.get_one(id)
        res = UserSchema().dump(model)
        return res, 200

    def put(self, id: int):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = id
        service.update(req_json)
        return "", 204

    def delete(self, id):
        movie_service.delete(id)
        return "", 204