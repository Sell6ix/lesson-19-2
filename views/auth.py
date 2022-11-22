from flask_restx import Resource, Namespace
from flask import request, abort

from dao.model.genre import GenreSchema
from service.implemented import auth_service as service

auth_ns = Namespace("auth")


def auth_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            return {"error": "Not authorize request"}, 401
        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        try:
            service.validate_token(token)
        except Exception as e:
            print(f"Traceback: {e}")
            return {"error": "Not authorize request"}, 401
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):
        if "Authorization" not in request.headers:
            return {"error": "Not authorize request"}, 401
        data = request.headers["Authorization"]
        token = data.split("Bearer ")[-1]
        is_admin = False
        is_admin = service.validate_admin_token(token)
        if is_admin:
            return func(*args, **kwargs)
        else:
            return {"error": "User is not admin"}, 401

    return wrapper


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        data = request.json
        return service.auth(data)

    def put(self):
        req_json = request.json
        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            return {"error": "Bad request"}, 400
        return (service.refresh_token(refresh_token),)