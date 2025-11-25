
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user

try:
    from models import db, Product,User
    from auth import authenticate_user
except ImportError:
    from ..models import db, Product,User
    from ..auth import authenticate_user


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])  # Remove /api prefix since it's added in app.py
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
            
        user = authenticate_user(data['username'], data['password'])
        
        if user:
            login_user(user, remember=True)
            return jsonify({
                'message': 'Login successful', 
                'user': {
                    'user': user.to_dict()
                }
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        logout_user()
        return jsonify({'message': 'Logout successful'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/check-auth', methods=['GET'])
@login_required
def check_auth():
    try:
        return jsonify({'authenticated': True, 'user': current_user.username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500