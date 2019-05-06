import os
from base64 import b64encode
from hashlib import md5


def generate_hash(plaintext):
    text = f"plog{plaintext}golp"
    ret = md5(text.encode("utf-8"))
    return ret.hexdigest()


def generate_session_cookie():
    byte_array = os.urandom(64)
    byte_string = b64encode(byte_array).decode()
    return generate_hash(byte_string)
