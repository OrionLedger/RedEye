from flask import Blueprint, jsonify

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.route("/", methods=["GET"])
def get_users():
    return jsonify([])