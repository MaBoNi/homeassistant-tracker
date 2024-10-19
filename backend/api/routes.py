# backend/api/routes.py
from flask import request, jsonify
from . import api_bp
from .auth import token_required
from services.db_manager import get_gps_logs  # Absolute import

@api_bp.route('/gps-data', methods=['GET'])
@token_required
def get_gps_data():
    user = request.args.get('user')
    time_range = request.args.get('time_range', 'live')  # default to 'live'
    
    data = get_gps_logs(user, time_range)
    
    if not data:
        return jsonify({"message": "No data found!"}), 404

    return jsonify(data), 200
