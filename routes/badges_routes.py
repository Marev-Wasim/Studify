from flask import Blueprint, jsonify, session, request
from extensions import db
from models.badge import Badge

badge_bp = Blueprint('badges', __name__, url_prefix='/badges')

def get_auth_user_id():
    """Retrieves the authenticated user's ID from the session."""
    return session.get('user_id')

@badge_bp.route('/', methods=['GET'])
def get_user_badges():
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    badges = Badge.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'description': b.description,
        'date_awarded': b.date_awarded.isoformat()
    } for b in badges])


@badge_bp.route('/', methods=['POST'])
def award_badge():

    data = request.get_json()
    user_id = data.get('user_id') # User ID to receive the badge
    name = data.get('name')
    description = data.get('description')

    if not user_id or not name:
        return jsonify({'message': 'Missing user_id or name'}), 400

    new_badge = Badge(
        user_id=user_id,
        name=name,
        description=description
    )
    db.session.add(new_badge)
    db.session.commit()

    return jsonify({'message': f'Badge "{name}" awarded to user {user_id}', 'badge_id': new_badge.id}), 201