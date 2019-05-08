import datetime
from bson.objectid import ObjectId

from . import utils

mongo = None


class Document:
    def __init__(self):
        self.keys = []
        self.document = {}

    def to_json(self):
        return self.document

    def __getitem__(self, key):
        return self.document.get(key)

    def __setitem__(self, key, value):
        self.document[key] = value


class User(Document):
    def __init__(self, **kwargs):
        self.keys = ["username", "password", "session"]
        self.document = {k: kwargs.get(k) for k in self.keys}

    def login(self):
        """authenticate user to admin dashboard"""

        # lookup user document matching username and hashed password
        user_obj = mongo.db.users.find_one(
            {
                "username": self["username"],
                "password": utils.generate_hash(self["password"]),
            }
        )

        # check if lookup was successful
        if not user_obj:
            raise ValueError("login failed")

        # create session_key
        session_key = utils.generate_session_cookie()

        # save a session cookie to user document
        mongo.db.users.find_one_and_update(
            {"_id": user_obj["_id"]}, {"$set": {"session": session_key}}
        )

        # update our document
        user_obj["session"] = session_key
        self.document.update(user_obj)

        return self

    @staticmethod
    def get_by_session(session):
        """lookup user by session"""

        return mongo.db.users.find_one({"session": session})


class Post(Document):
    def __init__(self, **kwargs):
        self.keys = ["title", "content", "image"]
        self.document = {k: kwargs.get(k) for k in self.keys}

    @staticmethod
    def get_by_id(post_id):
        """get post by id"""
        return mongo.db.posts.find_one({"_id": ObjectId(post_id)})

    @staticmethod
    def get_all():
        """get all posts"""
        return [x for x in mongo.db.posts.find().sort("created", -1)]

    @staticmethod
    def get_recent(limit):
        """get recent posts with limit"""
        return [x for x in mongo.db.posts.find().sort("created", -1).limit(limit)]

    @staticmethod
    def update(post_id, title, content, image=""):
        """update an existing post document"""
        mongo.db.posts.find_one_and_update(
            {"_id": ObjectId(post_id)},
            {"$set": {"title": title, "content": content, "image": image}},
        )

    @staticmethod
    def create(title, content, image=""):
        """create a new post document"""
        post = {
            "title": title,
            "content": content,
            "image": image,
            "created": datetime.datetime.utcnow(),
        }
        mongo.db.posts.insert_one(post)
