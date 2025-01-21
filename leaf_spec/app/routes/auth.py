from flask import Blueprint, request, jsonify
from app.models.user import User
from bson.objectid import ObjectId

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/add_user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        
        if User.exists(data.get('email')):
            return jsonify({"error": "User Already exists"}), 409
        
        user = User(
            name=data.get('name'),
            email=data.get('email'),
            password=data.get('password')
        )
        user_id = user.save()
        return jsonify({"user_id": user_id}), 200
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500

@auth_bp.route('/sign_in', methods=['POST'])
def sign_in():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({"error": "Email and password are required"}), 400
        
        user = User.authenticate(data['email'], data['password'])
        
        if user:
            return jsonify({
                "message": "Login successful",
                "user_id": str(ObjectId(user['_id']))
            }), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500