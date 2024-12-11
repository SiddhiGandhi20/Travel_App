from flask import Blueprint, request, jsonify
from models.package_model import create_package, find_package_by_id, find_all_packages, filter_packages

# Create a Blueprint for package-related routes
package_blueprint = Blueprint("package", __name__)

# Route to fetch all packages (with optional filtering)
@package_blueprint.route("/packages", methods=["GET"])
def list_packages():
    # Extract query parameters for filtering (price, duration, availability, discount)
    filters = {
        "price": request.args.get("price"),
        "duration": request.args.get("duration"),
        "availability": request.args.get("availability"),
        "discount": request.args.get("discount")
    }

    # Fetch filtered packages from the model
    packages = filter_packages(filters)
    
    # Return the filtered list of packages as a JSON response
    return jsonify(packages), 200

# Route to fetch details of a specific package by its ID
@package_blueprint.route("/packages/<package_id>", methods=["GET"])
def package_details(package_id):
    # Fetch the package by ID
    package = find_package_by_id(package_id)
    
    if package:
        return jsonify(package), 200
    return jsonify({"error": "Package not found"}), 404

# Route to create a new package (Admin only)
@package_blueprint.route("/packages", methods=["POST"])
def add_package():
    # Get package details from the JSON body of the POST request
    data = request.json
    name = data.get("name")
    price = data.get("price")
    duration = data.get("duration")
    destinations = data.get("destinations")
    inclusions = data.get("inclusions")
    description = data.get("description")
    discount = data.get("discount")
    availability = data.get("availability")

    # Create the new package by calling the model's create_package function
    package = create_package(name, price, duration, destinations, inclusions, description, discount, availability)

    # Return a success message with the created package as a response
    return jsonify({"message": "Package created successfully", "package": package}), 201
