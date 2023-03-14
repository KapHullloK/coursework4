from flask_restx import Resource, Namespace
from flask import request
from dao.model.movie import MovieSchema
from decorators import auth_required, admin_required
from implemented import movie_service

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class Movies_view(Resource):
    # @auth_required
    def get(self):
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        status = request.args.get("status")
        page = request.args.get('page')
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
            "status": status,
            "page": page
        }
        all_movies = movie_service.get_all(filters)
        return movies_schema.dump(all_movies), 200

    @admin_required
    def post(self):
        data = request.json
        movie_service.add(data)
        return "OK", 201


@movies_ns.route('/<int:mid>')
class Movie_view(Resource):
    @auth_required
    def get(self, mid):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie), 200

    @admin_required
    def put(self, mid):
        data = request.json
        movie_service.update(data, mid)
        return "OK", 201

    @admin_required
    def delete(self, mid):
        movie_service.delete(mid)
        return "OK", 204
