'''from flask import Blueprint, request, jsonify
from extensions import db
from models.friend import Friend
from models.user import User
from sqlalchemy import or_

friend_bp = Blueprint('friend', __name__, url_prefix='/friends')

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
    '''

  from flask import Blueprint, request, jsonify
from extensions import db
from models.friend import Friend
from models.user import User
from sqlalchemy import or_

friend_bp = Blueprint('friend', name, url_prefix='/friends')

# --- 1. إرسال طلب صداقة (POST /friends/request) ---
@friend_bp.route('/request', methods=['POST'])
def send_request():
    data = request.get_json()
    user_id = data.get('user_id')
    friend_username = data.get('friend_username')

    if not user_id or not friend_username:
        return jsonify({'message': 'Missing user_id or friend_username'}), 400

    friend_user = User.query.filter_by(username=friend_username).first()

    if not friend_user:
        return jsonify({'message': f'User {friend_username} not found'}), 404
        
    friend_id = friend_user.id
    
    if user_id == friend_id:
        return jsonify({'message': 'Cannot send a request to yourself'}), 400

    # التحقق من وجود علاقة سابقة (مقبولة أو معلّقة)
    existing_friendship = Friend.query.filter(
        or_(
            (Friend.user_id == user_id) & (Friend.friend_id == friend_id),
            (Friend.user_id == friend_id) & (Friend.friend_id == user_id)
        )
    ).first()

    if existing_friendship:
        if existing_friendship.status == 'accepted':
            return jsonify({'message': 'Already friends'}), 400
        elif existing_friendship.status == 'pending':
            if existing_friendship.user_id == user_id:
                 return jsonify({'message': 'Request already sent and pending'}), 400
            else:
                 return jsonify({'message': 'User already sent you a request (pending acceptance)'}), 400

    # إنشاء طلب الصداقة (يرسلها user_id إلى friend_id)
    new_request = Friend(user_id=user_id, friend_id=friend_id, status='pending')
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Friend request sent', 'status': 'pending'}), 201


# --- 2. جلب الأصدقاء المقبولين (GET /friends/<int:user_id>) 🚨 تم تعديل هذه الدالة 🚨 ---
@friend_bp.route('/<int:user_id>', methods=['GET'])
def get_user_friends(user_id):
    # جلب جميع الصفوف التي فيها المستخدم هو إما user_id أو friend_id والحالة 'accepted'
    accepted_friends = Friend.query.filter(
        (Friend.status == 'accepted') &
        (or_(Friend.user_id == user_id, Friend.friend_id == user_id))
    ).all()
    
    friends_list = []
    for friendship in accepted_friends:
        
        # تحديد الصديق الآخر (الذي ليس المستخدم الحالي)
        if friendship.user_id == user_id:
            friend_obj = friendship.receiver # الصديق هو المستقبل
            friend_id = friendship.friend_id
        else: # friendship.friend_id == user_id
            friend_obj = friendship.requester # الصديق هو المرسل
            friend_id = friendship.user_id
            
        friends_list.append({
            'relationship_id': friendship.id, # ⬅️ ضروري لعملية الحذف في Frontend
            'friend_id': friend_id,
            'username': friend_obj.username,
            'points': getattr(friend_obj, 'points', 0)
        })
        
    return jsonify(friends_list)


# --- 3. جلب طلبات الصداقة المعلقة الواردة (GET /friends/pending/<int:user_id>) ---
@friend_bp.route('/pending/<int:user_id>', methods=['GET'])
def get_pending_requests(user_id):
    # جلب الطلبات المرسلة إلى user_id وحالتها 'pending'
    pending_requests = Friend.query.filter_by(friend_id=user_id, status='pending').all()
    
    requests_list = []
    for req in pending_requests:
        requests_list.append({
            'request_id': req.id,
            'sender_id': req.user_id,
            'sender_username': req.requester.username 
        })
        
    return jsonify(requests_list)


# --- 4. قبول طلب صداقة (PUT /friends/accept/<int:request_id>) ---
@friend_bp.route('/accept/<int:request_id>', methods=['PUT'])
def accept_request(request_id):
    data = request.get_json()
    user_id = data.get('user_id') # المستخدم الذي يقوم بالقبول (يجب أن يكون هو المستقبل)
    
    friendship = Friend.query.get(request_id)
    
    if not friendship:
        return jsonify({'message': 'Request not found'}), 404

    if friendship.friend_id != user_id:
        return jsonify({'message': 'Unauthorized action: You are not the receiver of this request'}), 403

    if friendship.status == 'accepted':
        return jsonify({'message': 'Request already accepted'}), 400

    friendship.status = 'accepted'
    db.session.commit()
    
    return jsonify({'message': 'Friend request accepted', 'status': 'accepted'}), 200

# --- 5. حذف طلب صداقة معلّق أو علاقة صداقة قائمة (DELETE /friends/<int:relationship_id>) 🚨 تم إضافة هذه الدالة 🚨 ---
# يمكن استخدامها لرفض طلب (إذا كان status='pending') أو لحذف صديق (إذا كان status='accepted')
@friend_bp.route('/<int:relationship_id>', methods=['DELETE'])
def delete_friendship_or_request(relationship_id):
    friendship = Friend.query.get(relationship_id)
    
    if not friendship:
        return jsonify({'message': 'Friendship or request not found'}), 404
        
    # هنا قد تحتاج لإضافة تحقق أمني: هل المستخدم الحالي هو أحد أطراف العلاقة؟
    # if friendship.user_id != CURRENT_USER_ID and friendship.friend_id != CURRENT_USER_ID:
    #     return jsonify({'message': 'Unauthorized action'}), 403
        
    db.session.delete(friendship)
    db.session.commit()
    
    return jsonify({'message': 'Friendship or request deleted successfully'}), 200


# --- 6. جلب جميع المستخدمين للبحث (GET /friends/users) ---
@friend_bp.route('/users/<int:current_user_id>', methods=['GET'])
def get_all_users_for_search(current_user_id):
    
    # استثناء المستخدم الحالي من نتائج البحث
    users_query = User.query.filter(User.id != current_user_id).all()
    
    users_list = []
    for user in users_query:
        points = getattr(user, 'points', 0) 
        
        users_list.append({
            'id': user.id,
            'username': user.username,
            'points': points
        })
        
    return jsonify(users_list)
