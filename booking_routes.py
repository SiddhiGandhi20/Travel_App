from flask import Blueprint, request, jsonify
from models.booking_model import create_booking, find_booking_by_id, find_bookings_by_user, cancel_booking

booking_blueprint = Blueprint("booking", __name__)

# Create a new booking
@booking_blueprint.route("/", methods=["POST"])
def create_new_booking():
    data = request.get_json()
    user_id = data.get("user_id")
    package_id = data.get("package_id")
    travel_dates = data.get("travel_dates")
    total_price = data.get("total_price")
    status = data.get("status")
    
    booking = create_booking(user_id, package_id, travel_dates, total_price, status)
    return jsonify(booking), 201

# Get booking details by booking_id
@booking_blueprint.route("/<booking_id>", methods=["GET"])
def get_booking(booking_id):
    booking = find_booking_by_id(booking_id)
    if booking:
        return jsonify(booking), 200
    return jsonify({"error": "Booking not found"}), 404

# Get all bookings by a user
@booking_blueprint.route("/user/<user_id>", methods=["GET"])
def get_user_bookings(user_id):
    bookings = find_bookings_by_user(user_id)
    if bookings:
        return jsonify(bookings), 200
    return jsonify({"error": "No bookings found for this user"}), 404

# Cancel a booking
@booking_blueprint.route("/<booking_id>", methods=["DELETE"])
def cancel_booking_route(booking_id):
    success = cancel_booking(booking_id)
    if success:
        return jsonify({"message": "Booking cancelled successfully"}), 200
    return jsonify({"error": "Booking not found"}), 404
