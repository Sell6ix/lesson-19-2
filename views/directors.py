from flask_restx import Resource, Namespace
from flask import request

from dao.model.director import DirectorSchema
from service.implemented import director_service as service
from views.auth import auth_required, admin_required

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        models = service.get_all()
        res = DirectorSchema(many=True).dump(models)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        model = service.create(req_json)
        return "", 201, {"location": f"/directors/{model.id}"}

@director_ns.route('/<int:id>')
class DirectorView(Resource):
    @auth_required
    def get(self, id):
        model = service.get_one(id)
        data = DirectorSchema().dump(model)
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