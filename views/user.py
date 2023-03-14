from flask import jsonify, request, abort
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from decorators import admin_required
from implemented import user_service

auth_ns = Namespace('auth')
user_ns = Namespace('user')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


@auth_ns.route('/register/')
class UserView(Resource):
    @admin_required
    def get(self):
        all_users = user_service.get_all()
        return users_schema.dump(all_users), 200

    def post(self):
        data = request.json
        user_service.add(data)
        return 'OK', 201


@auth_ns.route('/login/')
class Auth_view(Resource):
    def post(self):
        data = request.json
        if data is None:
            abort(401)
        tokens = user_service.post_tokens(data)
        return jsonify(tokens)

    def put(self):
        data = request.json
        if data is None:
            abort(401)
        tokens = user_service.put_tokens(data)
        print(tokens)
        return jsonify(tokens)


@user_ns.route('/')
class UserView(Resource):
    def get(selfm):
        return user_schema.dump(user_service.user_info())

    def patch(self):
        data = request.json
        user_service.patch(data)
        return 'OK', 201


@user_ns.route('/password/')
class UserView(Resource):
    def put(self):
        data = request.json
        user_service.passwords_user(data)
        return 'OK', 200
