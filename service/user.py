import jwt
from flask import abort, request
import calendar
import datetime
from dao.user import UserDAO
import hashlib
from config import Config


class UserService:

    def __init__(self, dao: UserDAO):
        self.dao = dao
        self.secret = Config.SECRET_HERE
        self.algo = Config.ALGO

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, email):
        return self.dao.get_one(email)

    def add(self, data):
        data['password'] = self.get_hash(data['password'])
        return self.dao.add(data)

    def get_hash(self, password):
        print(bool)
        bytes = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode("utf-8"),
            salt=Config.PWD_HASH_SALT,
            iterations=Config.PWD_HASH_ITERATIONS
        ).hex()

        return bytes

    def post_tokens(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if None in [email, password]:
            abort(401)

        user = self.get_one(email)

        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        if self.get_hash(password) != user.password:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "email": user.email,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, self.secret, algorithm=self.algo)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, self.secret, algorithm=self.algo)

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens, 201

    def put_tokens(self, data):
        global user_info
        refresh_token = data.get("refresh_token")
        if refresh_token is None:
            abort(400)

        try:
            user_info = jwt.decode(jwt=refresh_token, key=self.secret, algorithms=[self.algo])
        except Exception as e:
            abort(400)

        email = user_info.get("email")

        user = self.get_one(email)

        data = {
            "email": user.email,
            "role": user.role
        }
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, self.secret, algorithm=self.algo)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, self.secret, algorithm=self.algo)

        tokens = {"access_token": access_token, "refresh_token": refresh_token}
        return tokens, 201

    def patch(self, data):
        get_user = self.user_info()

        if "username" in data:
            get_user.username = data.get("username")
        if "favorite_genre" in data:
            get_user.favorite_genre = data.get("favorite_genre")

        return self.dao.update(get_user)

    def user_info(self):
        token = request.headers['Authorization'].split("Bearer ")[-1]
        user = None
        try:
            user = jwt.decode(token, Config.SECRET_HERE, algorithms=[Config.ALGO])

        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)

        return self.get_one(user.get('email'))

    def passwords_user(self, passwords):
        get_user = self.user_info()

        if self.get_hash(passwords.get('password_1')) == get_user.password:
            get_user.password = self.get_hash(passwords.get('password_2'))
        else:
            return {"error": "Неверные учётные данные"}, 401

        return self.dao.update(get_user)
