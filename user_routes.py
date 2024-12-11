from flask import Blueprint, request, jsonify
from models.user_models import create_user, find_user_by_email, find_user_by_id
from utils.auth import generate_token, decode_token
from bcrypt import checkpw

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if find_user_by_email(email):
        return jsonify({"error": "Email already exists"}), 400

    user = create_user(name, email, password)
    return jsonify({"message": "User registered successfully", "user_id": user["user_id"]}), 201

@user_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    user = find_user_by_email(email)
    if not user or not checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user["user_id"])
    return jsonify({"token": token}), 200

@user_blueprint.route("/profile", methods=["GET"])
def profile():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Token is required"}), 401

    decoded = decode_token(token)
    if not decoded:
        return jsonify({"error": "Invalid or expired token"}), 401

    user = find_user_by_id(decoded["user_id"])
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": {"name": user["name"], "email": user["email"]}}), 200
