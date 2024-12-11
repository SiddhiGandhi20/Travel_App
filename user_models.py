from pymongo import MongoClient
from datetime import datetime
from bcrypt import hashpw, gensalt, checkpw
import uuid
from config import MONGO_URI

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client.get_database()
users_collection = db.users

def create_user(name, email, password):
    hashed_password = hashpw(password.encode('utf-8'), gensalt())
    user = {
        "user_id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password": hashed_password.decode('utf-8'),
        "created_at": datetime.utcnow()
    }
    users_collection.insert_one(user)
    return user

def find_user_by_email(email):
    return users_collection.find_one({"email": email})

def find_user_by_id(user_id):
    return users_collection.find_one({"user_id": user_id})
