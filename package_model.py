from pymongo import MongoClient
import uuid
from datetime import datetime
from bson import ObjectId

# MongoDB connection
try:
    client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB URI
    db = client.travel_app  # Use 'travel_app' database
    print("MongoDB connection successful.")
except Exception as e:
    print(f"Error while connecting to MongoDB: {e}")
    raise  # Raise the exception if MongoDB connection fails

# Packages collection
packages_collection = db.packages

# Function to serialize MongoDB's ObjectId to string
def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def create_package(name, price, duration, destinations, inclusions, description, discount, availability):
    # Generate a unique package ID and create a new package document
    package = {
        "_id": str(ObjectId()),  # Use ObjectId as the MongoDB document ID
        "name": name,
        "price": price,
        "duration": duration,
        "destinations": destinations,
        "inclusions": inclusions,
        "description": description,
        "discount": discount,
        "availability": availability,
        "created_at": datetime.utcnow()
    }
    packages_collection.insert_one(package)
    return package

def find_package_by_id(package_id):
    # Fetch a package by its unique package_id
    package = packages_collection.find_one({"_id": ObjectId(package_id)})
    if package:
        package["_id"] = str(package["_id"])  # Convert ObjectId to string
    return package

def find_all_packages():
    # Fetch all packages from the database and serialize ObjectId
    packages = list(packages_collection.find())
    for package in packages:
        package["_id"] = str(package["_id"])  # Convert ObjectId to string
    return packages

def filter_packages(filters):
    # Build the MongoDB query based on provided filters
    query = {}

    if filters.get("price"):
        query["price"] = float(filters["price"])  # Ensure price is a float
    if filters.get("duration"):
        query["duration"] = filters["duration"]
    if filters.get("availability"):
        query["availability"] = filters["availability"]
    if filters.get("discount"):
        query["discount"] = int(filters["discount"])

    # Fetch filtered packages from the database
    packages = list(packages_collection.find(query))
    for package in packages:
        package["_id"] = str(package["_id"])  # Convert ObjectId to string
    return packages
