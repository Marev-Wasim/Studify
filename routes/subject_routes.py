from flask import Blueprint, request, jsonify, session
from extensions import db
from models.subject import Subject
from models.study_log import StudyLog
from models.task import Task

subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')

# 🟢 1. تعريف دالة المصادقة (كانت مفقودة وتسبب الانهيار)
def get_auth_user_id():
    return session.get('user_id')

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
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
        
    subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
    
    if not subject:
        return jsonify({'message': 'Subject not found or unauthorized'}), 404

    try:
        # 1. حذف سجلات الدراسة المرتبطة (StudyLogs)
        # هام: نستخدم synchronize_session=False لتجنب مشاكل الذاكرة
        # StudyLog.query.filter_by(subject_id=subject_id).delete(synchronize_session=False)
        # 1. Instead of deleting, we NULLIFY the subject_id and task_id
        # This keeps the 'hours_studied' records in the database for total history.
        StudyLog.query.filter_by(subject_id=subject_id).update(
            {
                StudyLog.subject_id: None,
                StudyLog.task_id: None
            }, 
            synchronize_session=False
        )
        
        # 2. Delete the Tasks (Since you want the task to disappear, but the logs above are now safe)
        Task.query.filter_by(subject_id=subject_id).delete(synchronize_session=False)
        
        # 3. Delete the Subject
        db.session.delete(subject)
        
        # 4. Save changes
        db.session.commit()
        return jsonify({'message': 'Subject and tasks deleted successfully, study hours preserved in history'}), 200
        
    except Exception as e:
        db.session.rollback()
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
