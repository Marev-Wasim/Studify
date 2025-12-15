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
    '''from flask import Blueprint, request, jsonify
from extensions import db
from models.friend import Friend
from models.user import User  # تأكد أنك تستورد نموذج المستخدم
from sqlalchemy import or_

# تأكد أنك تُمرر اسم الوحدة النمطية الصحيح هنا، عادةً يكون 'friend' أو 'name'
friend_bp = Blueprint('friend', name, url_prefix='/friends')

# --- المتغيرات التي تحتاج لتعريفها (مثال: نموذج المستخدم) ---
#  ملاحظة: هذه مجرد هياكل افتراضية للعمل 
# يجب أن تكون نماذجك (Models) موجودة في ملف extensions.py أو models.py
#class User(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    username = db.Column(db.String(80), unique=True, nullable=False)
#    email = db.Column(db.String(120), unique=True, nullable=False)
#    # ... أضف أي حقول أخرى مثل points أو avatar

# --- 1. إرسال طلب صداقة (POST /friends/request) ---
@friend_bp.route('/request', methods=['POST'])
def send_request():
    data = request.get_json()
    # يتم استقبال: user_id (المرسل) و friend_username (اسم مستقبل الطلب)
    user_id = data.get('user_id')
    friend_username = data.get('friend_username')

    if not user_id or not friend_username:
        return jsonify({'message': 'Missing data (user_id or friend_username)'}), 400

    # البحث عن المستخدم المستقبل
    friend_user = User.query.filter_by(username=friend_username).first()
    if not friend_user:
        return jsonify({'message': 'User not found'}), 404

    if friend_user.id == user_id:
        return jsonify({'message': 'You cannot add yourself'}), 400

    # التحقق من وجود علاقة سابقة (في كلا الاتجاهين)
    existing_request = Friend.query.filter(
        or_(
            (Friend.user_id == user_id) & (Friend.friend_id == friend_user.id),
            (Friend.user_id == friend_user.id) & (Friend.friend_id == user_id)
        )
    ).first()

    if existing_request:
        if existing_request.status == 'pending':
            # تحديد ما إذا كان الطلب مُرسلًا منه أم إليه
            if existing_request.user_id == user_id:
                return jsonify({'message': 'Request already sent by you'}), 400
            else:
                return jsonify({'message': 'You have a pending request from this user'}), 400
        
        # إذا كانت الحالة 'accepted'
        return jsonify({'message': 'You are already friends'}), 400

    # إنشاء طلب جديد
    new_friend = Friend(user_id=user_id, friend_id=friend_user.id, status='pending')
    db.session.add(new_friend)
    db.session.commit()

    return jsonify({'message': 'Friend request sent', 'status': 'pending'})

# --- 2. قبول طلب صداقة (PUT /friends/accept/<request_id>) ---
@friend_bp.route('/accept/<int:request_id>', methods=['PUT'])
def accept_request(request_id):
    # نستقبل user_id للتحقق من أن المستخدم الحالي هو مستقبل الطلب
    data = request.get_json() 
    current_user_id = data.get('user_id') 

    friend_request = Friend.query.get(request_id)

    if not friend_request:
        return jsonify({'message': 'Request not found'}), 404

    # التحقق من أن المستخدم الحالي هو المستقبل (friend_id)
    if friend_request.friend_id != current_user_id:
        return jsonify({'message': 'Permission denied: This request is not addressed to you'}), 403

    friend_request.status = 'accepted'
    db.session.commit()

    return jsonify({'message': 'Friend request accepted', 'status': 'accepted'})

# --- 3. حذف صديق أو رفض طلب (DELETE /friends/<request_id>) ---
@friend_bp.route('/<int:request_id>', methods=['DELETE'])
def delete_friend(request_id):
    # يجب أن يتم تمرير request_id (لرفض طلب) أو relationship_id (لحذف صديق)
    friend_request = Friend.query.get(request_id)
    if not friend_request:
        return jsonify({'message': 'Record (Friend/Request) not found'}), 404
        
    db.session.delete(friend_request)
    db.session.commit()
    return jsonify({'message': 'Friend/Request removed'})
    
@friend_bp.route('/<int:user_id>', methods=['GET'])
def get_friends(user_id):
    # جلب جميع العلاقات المقبولة التي يكون المستخدم طرفاً فيها
    friends_query = Friend.query.filter(
        or_(Friend.user_id == user_id, Friend.friend_id == user_id),
        Friend.status == 'accepted'
    ).all()

    friends_list = []
    for f in friends_query:
        # تحديد من هو الصديق الفعلي (الطرف الآخر في العلاقة)
        if f.user_id == user_id:
            friend_obj = f.receiver # افتراض أن لديك خاصية receiver في نموذج Friend
        else:
            friend_obj = f.requester # افتراض أن لديك خاصية requester في نموذج Friend
        
        friends_list.append({
            'relationship_id': f.id, # ID العلاقة، يستخدم للحذف
            'friend_id': friend_obj.id,
            'username': friend_obj.username,
            # النقاط غير متوفرة في النموذج، نضعها صفر مؤقتاً
            'points': 0 
        })

    return jsonify(friends_list)

# --- 5. جلب طلبات الصداقة المعلقة (GET /friends/pending/<user_id>) ---
@friend_bp.route('/pending/<int:user_id>', methods=['GET'])
def get_pending_requests(user_id):
    # جلب الطلبات المرسلة إلى المستخدم (حيث يكون هو friend_id)
    pending_query = Friend.query.filter_by(friend_id=user_id, status='pending').all()

    requests_list = []
    for r in pending_query:
        requests_list.append({
            'request_id': r.id, # ID الطلب، يستخدم للقبول والرفض
            'sender_id': r.requester.id,
            'sender_username': r.requester.username,
        })

    return jsonify(requests_list)

# --- 6. جلب جميع المستخدمين (لعمل البحث) (GET /friends/users) ---
@friend_bp.route('/users', methods=['GET'])
def get_all_users_for_search():
    # هذا المسار يستخدم في الواجهة الأمامية لقائمة البحث
    users_query = User.query.all()
    
    users_list = []
    for user in users_query:
        users_list.append({
            'id': user.id,
            'username': user.username,
            'points': 0 # نقاط افتراضية
        })
        
    return jsonify(users_list)
