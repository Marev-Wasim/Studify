from flask import Blueprint, request, jsonify
from extensions import db
from models.friend import Friend
from models.user import User
from sqlalchemy import or_

friend_bp = Blueprint('friend', _name_, url_prefix='/friends')
    
# Send a Friend Request
@friend_bp.route('/request', methods=['POST'])
def send_request():
    data = request.get_json()
    user_id = data.get('user_id')    # The ID of the person sending the request
    friend_username = data.get('friend_username')

    if not user_id or not friend_username:
        return jsonify({'message': 'Missing data'}), 400

    # Find the friend
    friend_user = User.query.filter_by(username=friend_username).first()
    if not friend_user:
        return jsonify({'message': 'User not found'}), 404

    if friend_user.id == user_id:
        return jsonify({'message': 'You cannot add yourself'}), 400

    # Check if request already exists 
    existing_request = Friend.query.filter(
        or_(
            (Friend.user_id == user_id) & (Friend.friend_id == friend_user.id),
            (Friend.user_id == friend_user.id) & (Friend.friend_id == user_id)
        )
    ).first()

    if existing_request:
        return jsonify({'message': f'Friendship status is already {existing_request.status}'}), 400

    # Create new request
    new_friend = Friend(user_id=user_id, friend_id=friend_user.id, status='pending')
    db.session.add(new_friend)
    db.session.commit()

    return jsonify({'message': 'Friend request sent', 'status': 'pending'})

# Accept a Friend Request
@friend_bp.route('/accept/<int:request_id>', methods=['PUT'])
def accept_request(request_id):
    data = request.get_json() 
    current_user_id = data.get('user_id') 

    friend_request = Friend.query.get(request_id)

    if not friend_request:
        return jsonify({'message': 'Request not found'}), 404

    if friend_request.friend_id != current_user_id:
        return jsonify({'message': 'Error'}), 403

    friend_request.status = 'accepted'
    db.session.commit()

    return jsonify({'message': 'Friend request accepted', 'status': 'accepted'})

# List My Friends
@friend_bp.route('/<int:user_id>', methods=['GET'])
def get_friends(user_id):
    friends_query = Friend.query.filter(
        or_(Friend.user_id == user_id, Friend.friend_id == user_id),
        Friend.status == 'accepted'
    ).all()

    friends_list = []
    for f in friends_query:
        if f.user_id == user_id:
            friend_obj = f.receiver
        else:
            friend_obj = f.requester
        
        friends_list.append({
            'relationship_id': f.id,
            'friend_id': friend_obj.id,
            'username': friend_obj.username,
            'email': friend_obj.email,
            'status': f.status
        })

    return jsonify(friends_list)

#List Pending Requests 
@friend_bp.route('/pending/<int:user_id>', methods=['GET'])
def get_pending_requests(user_id):
    pending_query = Friend.query.filter_by(friend_id=user_id, status='pending').all()

    requests_list = []
    for r in pending_query:
        requests_list.append({
            'request_id': r.id,
            'sender_id': r.requester.id,
            'sender_username': r.requester.username,
            'sender_email': r.requester.email,
            'status': 'pending'
        })

    return jsonify(requests_list)

# Delete Friend or Reject Request
@friend_bp.route('/<int:request_id>', methods=['DELETE'])
def delete_friend(request_id):
    friend_request = Friend.query.get(request_id)
    if not friend_request:
        return jsonify({'message': 'Record not found'}), 404
        
    db.session.delete(friend_request)
    db.session.commit()

    return jsonify({'message': 'Friend/Request removed'})
