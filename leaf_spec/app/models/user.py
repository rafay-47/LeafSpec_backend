from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password
        self.db = mongo['LeafSpec']

    @staticmethod
    def exists(email):
        user = mongo['LeafSpec'].users.find_one({"email": email})
        return user is not None

    def save(self):
        if not self.name or not self.email or not self.password:
            raise ValueError("Name, email and password are required")
        
        hashed_password = generate_password_hash(self.password)
        user_id = self.db.users.insert_one({
            "name": self.name,
            "email": self.email,
            "password": hashed_password
        }).inserted_id
        return str(user_id)

    @staticmethod
    def authenticate(email, password):
        user = mongo['LeafSpec'].users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            return user
        return None