from flask import Blueprint, request, jsonify
from extensions import db
from models.friend import Friend
from models.user import User
from sqlalchemy import or_

friend_bp = Blueprint('friend', __name__, url_prefix='/friends')

# 🟢 دالة مساعدة لجلب ID المستخدم من الجلسة (للأمان)
def get_auth_user_id():
    return session.get('user_id')
    
# Send a Friend Request
@friend_bp.route('/requests', methods=['POST'])
def send_request():
    data = request.get_json()
    user_id = get_auth_user_id()    # The ID of the person sending the request
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
    
    # 🟢 1. التحقق من الهوية
    current_user_id = get_auth_user_id()
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401 

    friend_request = Friend.query.get(request_id)

    if not friend_request:
        return jsonify({'message': 'Request not found'}), 404

    # 🟢 2. التأكد من أن المستخدم الحالي هو "المستقبل" للطلب
    if friend_request.friend_id != current_user_id:
        return jsonify({'message': 'Unauthorized: You are not the receiver of this request'}), 403

    friend_request.status = 'accepted'
    db.session.commit()

    return jsonify({'message': 'Friend request accepted', 'status': 'accepted'})

# List My Friends
@friend_bp.route('/', methods=['GET'])
def get_friends():
    
    # 🟢 نستخدم الـ ID من الجلسة مباشرة
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
        
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
@friend_bp.route('/pending', methods=['GET'])
def get_pending_requests():
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
        
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
    current_user_id = get_auth_user_id()
    if not current_user_id:
        return jsonify({'error': 'Authentication required'}), 401
        
    friend_request = Friend.query.get(request_id)
    if not friend_request:
        return jsonify({'message': 'Record not found'}), 404
        
    if friend_request.user_id != current_user_id and friend_request.friend_id != current_user_id:
        return jsonify({'message': 'Unauthorized action'}), 403
        
    db.session.delete(friend_request)
    db.session.commit()

    return jsonify({'message': 'Friend/Request removed'})
   

# أضيفي هذا في نهاية ملف الباك إند الخاص بالأصدقاء
@friend_bp.route('/users/search', methods=['GET'])
def get_all_users_for_search():
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Auth required'}), 401
        
    # جلب كل المستخدمين ماعدا المستخدم الحالي
    users = User.query.filter(User.id != user_id).all()
    
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'points': u.total_coins # أو u.points حسب اسم العمود عندك
    } for u in users])


@app.route('/requests', methods=['GET'])
def get_requests():
    # 1. التأكد من تسجيل الدخول
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    current_user_id = session['user_id']
    
    try:
        # 2. البحث عن الطلبات المعلقة
        # الشرط: friend_id هو أنا (أنا المستقبل)، والحالة pending
        pending_requests = Friend.query.filter_by(
            friend_id=current_user_id, 
            status='pending'
        ).all()
        
        output = []
        for req in pending_requests:
            # هنا نستخدم العلاقة requester اللي موجودة في الـ Model
            # عشان نجيب بيانات الشخص اللي بعت الطلب بسهولة
            sender = req.requester 
            
            output.append({
                'request_id': req.id,            # ID الخاص بجدول الأصدقاء (مهم عشان القبول والرفض)
                'sender_id': sender.id,          # ID الشخص المرسل
                'name': sender.username,         # اسم المرسل (تأكدي أن العمود في User اسمه username)
                'profile_image': sender.profile_image if hasattr(sender, 'profile_image') else None # صورة المرسل
            })
            
        return jsonify(output)

    except Exception as e:
        print(f"Error in get_requests: {e}") # عشان يظهر في الـ Logs لو حصلت مشكلة
        return jsonify({'error': 'Internal Server Error'}), 500

