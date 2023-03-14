from dao.movie_dao import MovieDAO
from sqlalchemy import desc


class MovieService:

    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_all(self, filters):
        if filters.get("director_id") is not None:
            movies = self.dao.get_by_director_id(filters.get("director_id"))
        elif filters.get("genre_id") is not None:
            movies = self.dao.get_by_genre_id(filters.get("genre_id"))
        elif filters.get("year") is not None:
            movies = self.dao.get_by_year(filters.get("year"))
        else:
            movies = self.dao.get_all()

        if filters.get("status") is not None and filters.get("status") == "new":
            movies = movies.order_by(desc(self.dao.class_().year))
        if filters.get("page") is not None:
            movies = movies.limit(12).offset((int(filters.get('page')) - 1) * 12)
        return movies

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def add(self, data):
        return self.dao.add(data)

    def update(self, data, mid):
        get_movie = self.get_one(mid)

        get_movie.title = data.get("title")
        get_movie.description = data.get("description")
        get_movie.trailer = data.get("trailer")
        get_movie.year = data.get("year")
        get_movie.rating = data.get("rating")

        self.dao.update(get_movie)

    def patch(self, data):
        mid = data.get("id")
        get_movie = self.get_one(mid)

        if "title" in data:
            get_movie.title = data.get("title")
        if "description" in data:
            get_movie.description = data.get("description")
        if "trailer" in data:
            get_movie.trailer = data.get("trailer")
        if "year" in data:
            get_movie.year = data.get("year")
        if "rating" in data:
            get_movie.rating = data.get("rating")

        self.dao.update(get_movie)

    def delete(self, mid):
        self.dao.delete(mid)
