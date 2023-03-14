from dao.model.movie import Movie


class MovieDAO:

    def __init__(self, session):
        self.ses = session

    def get_all(self):
        return self.ses.query(Movie)

    def get_by_director_id(self, director_id):
        return self.ses.query(Movie).filter(Movie.director_id == director_id)

    def get_by_genre_id(self, genre_id):
        return self.ses.query(Movie).filter(Movie.genre_id == genre_id)

    def get_by_year(self, year):
        return self.ses.query(Movie).filter(Movie.year == year)

    def class_(self):
        return Movie

    def get_one(self, mid):
        return self.ses.query(Movie).get(mid)

    def add(self, data):
        new_movie = Movie(**data)
        self.ses.add(new_movie)
        self.ses.commit()

    def update(self, data):
        self.ses.add(data)
        self.ses.commit()
        return data

    def delete(self, mid):
        get_movie = self.get_one(mid)
        self.ses.delete(get_movie)
        self.ses.commit()
