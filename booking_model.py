from pymongo import MongoClient
from bson import ObjectId
import uuid
from datetime import datetime

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")  # Update your database URI here
db = client.travel_app  # Use the appropriate database name
bookings_collection = db.bookings  # Collection for bookings

# Function to serialize ObjectId to string
def serialize_object_id(data):
    if isinstance(data, dict):
        return {key: serialize_object_id(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_object_id(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)  # Convert ObjectId to string
    else:
        return data  # Return the value as is if it's not an ObjectId

# Function to create a booking
def create_booking(user_id, package_id, travel_dates, total_price, status):
    booking = {
        "booking_id": str(uuid.uuid4()),  # Use UUID for booking ID
        "user_id": user_id,
        "package_id": package_id,
        "booking_date": datetime.utcnow(),
        "travel_dates": travel_dates,
        "total_price": total_price,
        "status": status
    }

    bookings_collection.insert_one(booking)
    return serialize_object_id(booking)  # Serialize before returning

# Function to find a booking by ID
def find_booking_by_id(booking_id):
    booking = bookings_collection.find_one({"booking_id": booking_id})
    if booking:
        return serialize_object_id(booking)  # Serialize before returning
    return None

# Function to find all bookings of a specific user
def find_bookings_by_user(user_id):
    bookings = list(bookings_collection.find({"user_id": user_id}))
    return [serialize_object_id(booking) for booking in bookings]  # Serialize each booking

# Function to cancel a booking
def cancel_booking(booking_id):
    result = bookings_collection.delete_one({"booking_id": booking_id})
    return result.deleted_count > 0  # Return True if booking was deleted
