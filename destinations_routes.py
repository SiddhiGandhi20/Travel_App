# routes/destinations_routes.py
from flask import Blueprint, jsonify, request
from models.destinations_model import get_all_destinations, get_destination_by_id, add_new_destination

destinations_blueprint = Blueprint("destination", __name__)

# Route to fetch all destinations with filters
@destinations_blueprint.route("/destinations", methods=["GET"])
def list_destinations():
    filters = request.args.to_dict()  # Get query parameters as filters
    destinations = get_all_destinations(filters)
    return jsonify(destinations), 200

# Route to fetch a single destination by ID
@destinations_blueprint.route("/destinations/<destination_id>", methods=["GET"])
def single_destination(destination_id):
    destination = get_destination_by_id(destination_id)
    if destination:
        return jsonify(destination), 200
    return jsonify({"error": "Destination not found"}), 404

# Route to create a new destination
@destinations_blueprint.route("/destinations", methods=["POST"])
def create_destination():
    data = request.json
    
    # Validation for required fields
    required_fields = ["name", "region", "type", "description", "images", "highlights", "best_time_to_visit"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Call the model function to add the new destination
    new_destination = add_new_destination(data)
    
    return jsonify({"message": "Destination created successfully", "destination": new_destination}), 201
