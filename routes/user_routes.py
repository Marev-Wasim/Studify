from flask import Blueprint, request, jsonify, session
from extensions import db, bcrypt
from models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/profile')

def get_auth_user_id():
    """Retrieves the authenticated user's ID from the session."""
    return session.get('user_id')

@user_bp.route('/', methods=['GET'])
def get_user_profile():
    """
    Retrieves the authenticated user's profile data (username, email, points).
    """
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    # Assuming User model has a 'points' attribute
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'points': getattr(user, 'points', 0) # Safely retrieve points
    }), 200


@user_bp.route('/', methods=['PUT', 'PATCH'])
def update_user_profile():
    """Allows authenticated user to update username, and/or password."""
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    data = request.get_json()
    
    new_username = data.get('username')
    if new_username and new_username != user.username:
        if User.query.filter(User.username == new_username).first():
            return jsonify({'error': 'Username already taken'}), 409
        user.username = new_username
    
    new_password = data.get('password')
    if new_password:
        user.set_password(new_password)
        
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user_id': user.id,
            'username': user.username 
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile due to database error'}), 500