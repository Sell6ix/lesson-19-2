from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from service.implemented import movie_service as service
from views.auth import auth_required, admin_required

movie_ns = Namespace("movies")


@movie_ns.route("/")
class MoviesView(Resource):
    @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }
        models = service.get_all(filters)
        res = MovieSchema(many=True).dump(models)
        return res, 200

    @admin_required
    def post(self):
        req_json = request.json
        model = service.create(req_json)
        return "", 201, {"location": f"/movies/{model.id}"}


@movie_ns.route("/<int:id>")
class MovieView(Resource):
    @auth_required
    def get(self, id: int):
        model = service.get_one(id)
        data = MovieSchema().dump(model)
        return data, 200

    @admin_required
    def put(self, id: int):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = id
        service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, id: int):
        service.delete(id)
        return "", 204