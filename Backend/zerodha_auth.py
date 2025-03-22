from flask import Blueprint, request, jsonify
from ..config import kite, supabase
import os

zerodha_auth_bp = Blueprint("zerodha_auth", __name__)

@zerodha_auth_bp.route("/generate_token", methods=["POST"])
def generate_token():
    data = request.json
    request_token = data.get("request_token")

    try:
        session_data = kite.generate_session(request_token, api_secret=os.getenv("ZERODHA_API_SECRET"))
        access_token = session_data["access_token"]

        supabase.table("api_tokens").upsert({"platform": "zerodha", "access_token": access_token}).execute()

        return jsonify({"message": "Token generated", "access_token": access_token})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
