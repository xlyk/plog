import datetime
import uuid

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
        user_obj = mongo.db.users.find_one(
            {
                "username": self.document["username"],
                "password": self.document["password"],
            }
        )
        if not user_obj:
            raise ValueError("login failed")
        # TODO: salt and md5 this session_key
        session_key = str(uuid.uuid4())
        mongo.db.users.find_one_and_update(
            {"_id": user_obj["_id"]}, {"$set": {"session": session_key}}
        )
        self.document.update(user_obj)


class Post:
    @staticmethod
    def get_recent(limit):
        cursor = mongo.db.posts.find().limit(limit)
        posts = [x for x in cursor]
        return posts

    def create(self, title=None, content=None, image=None, slug=None, tags=[]):
        post = {
            "title": title,
            "content": content,
            "image": image,
            "slug": slug,
            "tags": tags,
            "created": datetime.datetime.utcnow(),
        }
        mongo.db.posts.insert_one(post)
