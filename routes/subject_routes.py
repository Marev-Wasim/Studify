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
@subject_bp.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    # قائمة لتخزين تقرير الخطوات
    debug_report = []
    debug_report.append(f"1. Start deleting Subject ID: {subject_id}")

    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Auth required', 'trace': debug_report}), 401
        
    subject = Subject.query.filter_by(id=subject_id, user_id=user_id).first()
    
    if not subject:
        debug_report.append("2. Subject not found or user not authorized.")
        return jsonify({'message': 'Not found', 'trace': debug_report}), 404

    debug_report.append(f"2. Found Subject: {subject.name}")

    try:
        # خطوة 1: StudyLog
        debug_report.append("3. Attempting to delete StudyLogs...")
        logs_count = StudyLog.query.filter_by(subject_id=subject_id).delete(synchronize_session=False)
        debug_report.append(f"   -> Deleted {logs_count} StudyLogs.")
        
        # خطوة 2: Tasks
        debug_report.append("4. Attempting to delete Tasks...")
        tasks_count = Task.query.filter_by(subject_id=subject_id).delete(synchronize_session=False)
        debug_report.append(f"   -> Deleted {tasks_count} Tasks.")
        
        # خطوة 3: Subject
        debug_report.append("5. Attempting to delete Subject...")
        db.session.delete(subject)
        debug_report.append("   -> Subject marked for deletion.")

        # خطوة 4: Commit
        debug_report.append("6. Committing to DB...")
        db.session.commit()
        debug_report.append("7. SUCCESS! Commit done.")
        
        # إرسال التقرير مع رسالة النجاح
        return jsonify({
            'message': 'Deleted successfully', 
            'trace': debug_report
        }), 200
        
    except Exception as e:
        db.session.rollback()
        debug_report.append(f"💥 ERROR HAPPENED: {str(e)}")
        # إرسال التقرير مع رسالة الخطأ 500
        return jsonify({
            'message': 'Server Error', 
            'error_details': str(e),
            'trace': debug_report 
        }), 500
        

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








