from flask import Blueprint, request, jsonify, session
from extensions import db
from models.task import Task
from models.study_log import StudyLog
from models.user import User
from models.subject import Subject # Needed to check user ownership via subject
from datetime import datetime
from sqlalchemy.exc import IntegrityError

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

def get_auth_user_id():
    """Retrieves the authenticated user's ID from the session."""
    return session.get('user_id')

@task_bp.route('/', methods=['GET'])
def get_tasks():
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    # Query tasks that belong to a subject owned by the current user
    tasks = db.session.query(Task).join(Subject).filter(Subject.user_id == user_id).all()
    
    return jsonify([{
        'id': t.task_id,
        'title': t.name,
        'subject_id': t.subject_id,
        'time': t.est_min,
        'due_date': t.due_date.isoformat() if t.due_date else None,
        'is_complete': t.completed,
    } for t in tasks])


@task_bp.route('/', methods=['POST'])
def create_task():
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
        
    data = request.get_json()
    
    name = data.get('name')
    subject_id = data.get('subject_id')
    est_min = data.get('time')
    due_date = data.get('date') # Matches dashboard HTML input 'taskDate'

    if not all([name, subject_id, est_min, due_date]):
        return jsonify({'message': 'Missing required fields (name, subject_id, time, date)'}), 400

    try:
        # Check if the subject belongs to the user
        if not Subject.query.filter_by(id=subject_id, user_id=user_id).first():
            return jsonify({'message': 'Invalid Subject ID or unauthorized'}), 403
            
        task_date = datetime.strptime(due_date, '%Y-%m-%d').date()

        task = Task(
            name=name,
            subject_id=subject_id,
            due_date=task_date,
            est_min=int(est_min),
            completed=False
        )
        db.session.add(task)
        
        db.session.commit()
        return jsonify({'message': 'Task created', 'task_id': task.task_id}), 201
    except ValueError:
        return jsonify({'message': 'Invalid format for time or date (YYYY-MM-DD)'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred during task creation', 'details': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    # Find the task and ensure it belongs to a subject owned by the user
    task = db.session.query(Task).join(Subject).filter(
        Task.task_id == task_id,
        Subject.user_id == user_id
    ).first()

    if not task:
        return jsonify({'error': 'Task not found or unauthorized'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


# PUT: Mark a task as complete (matches client-side window.completeTask)
@task_bp.route('/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    task = db.session.query(Task).join(Subject).filter(
        Task.task_id == task_id,
        Subject.user_id == user_id
    ).first()
    
    if not task:
        return jsonify({'error': 'Task not found or unauthorized'}), 404
        
   # if task.completed:
   #     return jsonify({'message': 'Task is already completed'}), 200

    try:
        # 🟢 المنطق الجديد: التبديل بين True و False
        if not task.completed:
            # 1. تحويلها لمكتملة
            task.completed = True
            task.completed_at = datetime.utcnow()
            
            # تسجيل الساعات في StudyLog (زي ما كودك كان بيعمل)
            minutes_studied = task.est_min
            if minutes_studied and minutes_studied > 0:
                hours_logged = round(minutes_studied / 60.0, 2)
                if float(current_total) + hours_logged >= 200:
                    StudyLog.query.filter_by(user_id=user_id).delete()
                    db.session.flush()
                study_log = StudyLog(
                    user_id=user_id,
                    subject_id=task.subject_id,
                    study_date=datetime.utcnow().date(),
                    hours_studied=hours_logged,
                    task_id=task.task_id 
                )
                db.session.add(study_log)
        else:
            # 2. إعادتها لحالة "غير مكتملة"
            task.completed = False
            task.completed_at = None
            
            # ❗ خطوة اختيارية ومهمة: مسح الساعات اللي اتسجلت عشان التوتال يرجع مظبوط
            StudyLog.query.filter_by(task_id=task_id).delete()

        db.session.commit()
        return jsonify({
            'message': 'Task status updated', 
            'is_complete': task.completed, 
            'id': task.task_id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred', 'details': str(e)}), 500


@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    # Find the task and ensure it belongs to a subject owned by the user
    task = db.session.query(Task).join(Subject).filter(
        Task.task_id == task_id,
        Subject.user_id == user_id
    ).first()

    if not task:
        return jsonify({'error': 'Task not found or unauthorized'}), 404

    data = request.get_json()

    if 'name' in data:
        task.name = data['name']
    if 'subject_id' in data:
        # Ensure new subject also belongs to the user (optional but safer)
        if not Subject.query.filter_by(id=data['subject_id'], user_id=user_id).first():
            return jsonify({'message': 'New Subject ID is invalid or unauthorized'}), 403
        task.subject_id = data['subject_id']

    if 'date' in data:
        try:
            task.due_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid date format (YYYY-MM-DD)'}), 400
            
    if 'time' in data:
        try:
            task.est_min = int(data['time'])
        except ValueError:
            return jsonify({'message': 'Time must be an integer'}), 400
            
    if 'completed' in data and isinstance(data['completed'], bool):
        task.completed = data['completed']
        if data['completed']:
            task.completed_at = datetime.utcnow()
        else:
            task.completed_at = None

    db.session.commit()
    return jsonify({'message': 'Task updated successfully'}), 200


















