from flask import Blueprint, jsonify, session
from extensions import db
from models.user import User
from models.friend import Friend
from sqlalchemy import or_

ranking_bp = Blueprint('ranking', __name__, url_prefix='/ranking')

def get_auth_user_id():
    """Retrieves the authenticated user's ID from the session."""
    return session.get('user_id')

@ranking_bp.route('/friends', methods=['GET'])
def friend_leaderboard():
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    #  Find all accepted friends' IDs
    friends_query = Friend.query.filter(
        or_(Friend.user_id == user_id, Friend.friend_id == user_id),
        Friend.status == 'accepted'
    ).all()

    friend_ids = {user_id} # Start with the current user's ID
    for f in friends_query:
        if f.user_id != user_id:
            friend_ids.add(f.user_id)
        if f.friend_id != user_id:
            friend_ids.add(f.friend_id)
            
    #  Query all users (including self) by their IDs and order by points
    leaderboard = User.query.filter(User.id.in_(friend_ids)).order_by(User.points.desc()).all()

    #  Format the ranking data
    ranking_data = []
    for rank, user in enumerate(leaderboard, 1):
        ranking_data.append({
            'rank': rank,
            'user_id': user.id,
            'username': user.username,
            'points': user.points,
            'is_me': user.id == user_id
        })
        
    return jsonify(ranking_data)