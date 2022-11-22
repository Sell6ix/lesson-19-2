from flask_restx import Resource, Namespace
from flask import request

from dao.model.genre import GenreSchema
from service.implemented import genre_service as service
from views.auth import auth_required, admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        model = service.create(req_json)
        return "", 201, {"location": f"/genres/{model.id}"}

@genre_ns.route('/<int:id>')
class GenreView(Resource):
    @auth_required
    def get(self, id):
        model = service.get_one(id)
        data = GenreSchema().dump(model)
        return data, 200

    @admin_required
    def put(self, id):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = id
        service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, id):
        service.delete(id)
        return "", 204
