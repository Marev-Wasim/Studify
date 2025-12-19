from flask import Blueprint, request, jsonify, session
from extensions import db
from models.friend import Friend
from models.user import User
from sqlalchemy import or_

friend_bp = Blueprint('friend', __name__, url_prefix='/friends')
    
# Send a Friend Request
@friend_bp.route('/request', methods=['POST'])
def send_request():
    data = request.get_json()
    #user_id = session.get('user_id')
    my_id = session.get('user_id')        # The ID of the person sending the request
    friend_username = data.get('friend_username')

    if not my_id or not friend_username:
        return jsonify({'message': 'Missing data'}), 400

    # Find the friend
    #friend_user = User.query.get(friend_id)
    friend_user = User.query.filter_by(username=friend_username).first()
    
    if not friend_user:
        return jsonify({'message': 'User not found'}), 404

    if friend_user.id == my_id:
        return jsonify({'message': 'You cannot add yourself'}), 400

    # MUST handle the user_id1 < user_id2 constraint
    id1, id2 = sorted([my_id, friend_user.id])

    # Check if request already exists
    existing_request = Friend.query.filter_by(user_id1=id1, user_id2=id2).first()
    # existing_request = Friend.query.filter(
    #     or_(
    #         (Friend.user_id == user_id) & (Friend.friend_id == friend_user.id),
    #         (Friend.user_id == friend_user.id) & (Friend.friend_id == user_id)
    #     )
    # ).first()

    if existing_request:
        return jsonify({'message': f'Friendship status is already {existing_request.status}'}), 400

    # Create new request using the sorted IDs
    #new_friend = Friend(user_id=user_id, friend_id=friend_user.id, status='pending')
    new_friend = Friend(
        user_id1=id1, 
        user_id2=id2, 
        status='pending',
        sent_by_id=my_id     # Track who actually sent it
    )
    db.session.add(new_friend)
    db.session.commit()

    return jsonify({'message': 'Friend request sent', 'status': 'pending'})

# Accept a Friend Request
#@friend_bp.route('/accept/<int:request_id>', methods=['PUT'])
@friend_bp.route('/accept', methods=['PUT'])
def accept_request():
    data = request.get_json() 
    my_id = session.get('user_id')
    sender_id = data.get('sender_id') # The person who sent me the request
    #friend_request = Friend.query.get(request_id)

    id1, id2 = sorted([my_id, sender_id])
    friend_request = Friend.query.filter_by(user_id1=id1, user_id2=id2, status='pending').first()
    
    if not friend_request:
        return jsonify({'message': 'Request not found'}), 404

    # if friend_request.friend_id != current_user_id:
    #     return jsonify({'message': 'Error'}), 403

    # Security: Only the receiver can accept
    if friend_request.sent_by_id == my_id:
        return jsonify({'message': 'You cannot accept your own request'}), 403

    friend_request.status = 'accepted'
    db.session.commit()

    return jsonify({'message': 'Friend request accepted', 'status': 'accepted'})

# Search For A Friend
@friend_bp.route('/users/search', methods=['GET'])
def search_users():
    query = request.args.get('q', '')
    my_id = session.get('user_id')
    if not query or not my_id:
        return jsonify([])
    
    # Find users whose username contains the query string (excluding yourself)
    users = User.query.filter(
        User.username.contains(query),
        User.id != my_id
    ).limit(10).all()
    
    #return jsonify([{'id': u.id, 'username': u.username} for u in users])
    results = []
    for user in users:
        # Check relationship status using your id1 < id2 logic
        id1, id2 = sorted([my_id, user.id])
        rel = Friend.query.filter_by(user_id1=id1, user_id2=id2).first()
        
        status = "none" # Stranger, no row for this pair 
        if rel:
            if rel.status == 'accepted':
                status = "friends"
            elif rel.status == 'pending':
                # Identify if I sent it or they sent it
                status = "sent_by_me" if rel.sent_by_id == my_id else "sent_to_me"

        results.append({
            'id': user.id,
            'username': user.username,
            'status': status
        })
    
    return jsonify(results)

# List My Friends
@friend_bp.route('/', methods=['GET'])
def get_friends():
    my_id = session.get('user_id')
    if not my_id:
        return jsonify({'message': 'Unauthorized'}), 401
        
    # friends_query = Friend.query.filter(
    #     or_(Friend.user_id == user_id, Friend.friend_id == user_id),
    #     Friend.status == 'accepted'
    # ).all()

    friends_query = Friend.query.filter(
        ((Friend.user_id1 == my_id) | (Friend.user_id2 == my_id)),
        Friend.status == 'accepted'
    ).all()
    
    friends_list = []
    for f in friends_query:
        # if f.user_id == user_id:
        #     friend_obj = f.receiver
        # else:
        #     friend_obj = f.requester
        
        # Determine which column holds the other user
        friend_id = f.user_id2 if f.user_id1 == my_id else f.user_id1
        other_user = User.query.get(friend_id) # Fetch user details
        #other_user = f.user2 if f.user_id1 == my_id else f.user1
        
        # friends_list.append({
        #     'relationship_id': f.id,
        #     'friend_id': friend_obj.id,
        #     'username': friend_obj.username,
        #     'email': friend_obj.email,
        #     'status': f.status
        # })
        friends_list.append({
            'username': other_user.username,
            'email': other_user.email
        })

    return jsonify(friends_list)

#List Pending Requests 
@friend_bp.route('/pending', methods=['GET'])
def get_pending_requests():
    my_id = session.get('user_id')
    if not my_id:
        return jsonify({'message': 'Unauthorized'}), 401
        
    #pending_query = Friend.query.filter_by(friend_id=user_id, status='pending').all()
    
    # Logic: Status is pending && was NOT sent by me
    pending_query = Friend.query.filter(
        ((Friend.user_id1 == my_id) | (Friend.user_id2 == my_id)),
        Friend.status == 'pending',
        Friend.sent_by_id != my_id
    ).all()
    
    requests_list = []
    for r in pending_query:
        sender = r.user2 if r.user_id1 == my_id else r.user1
        requests_list.append({
            'sender_id': sender.id,
            'sender_username': sender.username,
            'requested_at': r.requested_at
        })

    return jsonify(requests_list)

# Delete Friend or Reject Request
#@friend_bp.route('/<int:request_id>', methods=['DELETE'])
@friend_bp.route('/<int:other_user_id>', methods=['DELETE'])
def delete_friend(other_user_id):
    my_id = session.get('user_id')
    
    if not my_id:
        return jsonify({'message': 'Unauthorized'}), 401
        
    id1, id2 = sorted([my_id, other_user_id])
        
    #friend_request = Friend.query.get(request_id)
    friend = Friend.query.filter_by(user_id1=id1, user_id2=id2).first()
    if not friend:
        return jsonify({'message': 'Record not found'}), 404
        
    # 🟢 حماية: التأكد أن المستخدم الحالي هو طرف في العلاقة قبل الحذف
    # if current_user_id not in [friend_request.user_id, friend_request.friend_id]:
    #      return jsonify({'message': 'Permission denied'}), 403
         
    db.session.delete(friend)
    db.session.commit()

    return jsonify({'message': 'Friend/Request removed'})


