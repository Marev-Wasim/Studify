from flask import Blueprint, request, jsonify, session
from extensions import db
from models.subject import Subject
from models.study_log import StudyLog
from models.task import Task

subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')


@subject_bp.route('/', methods=['POST'])
def create_subject():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    data = request.get_json()
    name=data.get('name')
    
    subject = Subject(
        name=name,
        #color=data.get('color'),
        user_id=user_id
    )
    db.session.add(subject)
    db.session.commit()

    return jsonify({'message': 'Subject created', 'subject_id': subject.id})


@subject_bp.route('/', methods=['GET'])
def get_subjects():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    subjects = Subject.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        #'color': s.color
    } for s in subjects])


@subject_bp.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    print(f"\n🚀 Starting deletion for Subject ID: {subject_id}") # بداية التتبع

    user_id = get_auth_user_id()
    print(f"👤 User ID: {user_id}")
    
    if not user_id:
        print("❌ Error: No user ID found in session")
        return jsonify({'error': 'Authentication required'}), 401
        
    subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
    
    if not subject:
        print("❌ Error: Subject not found or unauthorized")
        return jsonify({'message': 'Subject not found or unauthorized'}), 404
    
    print(f"✅ Subject found: {subject.name} (ID: {subject.id})")

    try:
        # 1. اختبار حذف StudyLog
        print("⏳ Attempting to delete StudyLogs...")
        deleted_logs = StudyLog.query.filter_by(subject_id=subject_id).delete(synchronize_session=False)
        print(f"✅ StudyLogs deleted. Count: {deleted_logs}")
        
        # 2. اختبار حذف Tasks
        print("⏳ Attempting to delete Tasks...")
        deleted_tasks = Task.query.filter_by(subject_id=subject_id).delete(synchronize_session=False)
        print(f"✅ Tasks deleted. Count: {deleted_tasks}")
        
        # 3. اختبار حذف Subject
        print("⏳ Attempting to delete Subject...")
        db.session.delete(subject)
        print("✅ Subject marked for deletion.")

        # 4. تنفيذ الحذف الفعلي (Commit)
        print("⏳ Committing changes to database...")
        db.session.commit()
        print("🎉 SUCCESS: Database commit successful.")
        
        return jsonify({'message': 'Subject and associated records deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"\n💥 CRITICAL ERROR at step: {e}") # سيطبع الخطأ هنا
        import traceback
        traceback.print_exc() # سيطبع تفاصيل الخطأ كاملة ومكانه في الملف
        return jsonify({'message': 'An error occurred during deletion', 'details': str(e)}), 500
        

@subject_bp.route('/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    subject = Subject.query.get(subject_id)

    if not subject:
        return jsonify({'error': 'Subject not found'}), 404

    data = request.get_json()

    if 'name' in data:
        subject.name = data['name']
    #if 'color' in data:
        #subject.color = data['color']
    #if 'user_id' in data:
       # subject.user_id = data['user_id']

    db.session.commit()

    return jsonify({'message': 'Subject updated successfully'})







