
from flask import Blueprint, request, jsonify, session
from extensions import db
from models.study_log import StudyLog 
from models.subject import Subject
from models.user import User
from datetime import datetime
from sqlalchemy.exc import IntegrityError # <-- FIX: Ensure IntegrityError is imported
from sqlalchemy import func

study_bp = Blueprint('study', __name__, url_prefix='/study')

def get_auth_user_id():
    """Retrieves the authenticated user's ID from the session."""
    return session.get('user_id')


def calculate_points(hours_logged):
    """Calculates points based on study hours."""
    try:
        # Convert Numeric type (from DB) or incoming data to float
        hours_float = float(hours_logged)
        # Rule: 6 points per hour (1 point per 10 minutes)
        return int(hours_float * 6)
    except (ValueError, TypeError):
        return 0

@study_bp.route('/', methods=['POST'])
def log_study():
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    subject_id = data.get('subject_id')
    hours_studied = data.get('hours_studied')
    task_id = data.get('task_id')
    study_date_str = data.get('study_date')

    # Basic input validation
    if not subject_id or not hours_studied:
        return jsonify({'message': 'Missing subject ID or hours_studied'}), 400
    
    try:
        hours_float = float(hours_studied)
        if hours_float <= 0:
            return jsonify({'message': 'Study duration must be positive'}), 400
            
        # Parse date, default to today's date if not provided
        study_date = datetime.strptime(study_date_str, '%Y-%m-%d').date() if study_date_str else datetime.utcnow().date()
        
    except ValueError:
        return jsonify({'message': 'Invalid format for hours_studied or study_date'}), 400
    
    try:
        if float(current_total) + hours_float >= 200:
            # OPTION A: Delete old logs to reset to 0 (Fresh Start)
            StudyLog.query.filter_by(user_id=user_id).delete()
            # If resetting, the new log becomes the start of the new cycle
            log_to_save = hours_float 
            message = "Congratulations!🥳 You've reached 200 study hours!"
        else:
            log_to_save = hours_float
            message = "Study time logged"
        # Create the study log record
        log = StudyLog(
            user_id=user_id,
            subject_id=subject_id,
            hours_studied=hours_float,
            task_id=task_id,
            study_date=study_date
        )
        db.session.add(log)
        
        # Update user points
        points_earned = calculate_points(hours_float)
        user = User.query.get(user_id)
        if user:
            user.points += points_earned
        
        db.session.commit()

        return jsonify({
            'message': 'Study time logged and points awarded', 
            'points_earned': points_earned,
            'new_total_points': user.points if user else 0
        }), 201
        
    except IntegrityError as e:
        db.session.rollback()
        # This catches errors like invalid subject_id or task_id (Foreign Key violation)
        return jsonify({'message': 'Database error: Invalid subject or task ID', 'details': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An unexpected error occurred', 'details': str(e)}), 500


@study_bp.route('/', methods=['GET'])
def get_study_logs():
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401
        
    # Optional filtering by subject ID
    subject_id = request.args.get('subject_id')
    query = StudyLog.query.filter_by(user_id=user_id)
    
    if subject_id:
        query = query.filter_by(subject_id=subject_id)
        
    logs = query.order_by(StudyLog.study_date.desc()).all()
    
    total_hours_query = db.session.query(func.sum(StudyLog.hours_studied)).filter(StudyLog.user_id == user_id)
    total_hours_studied = total_hours_query.scalar() or 0.0
    
    formatted_logs = [{
        'id': log.id,
        'task_id': log.task_id,
        'subject_id': log.subject_id,
        'study_date': log.study_date.isoformat(),
        'hours_studied': str(float(log.hours_studied)), 
        'points_earned': calculate_points(log.hours_studied)
    } for log in logs]
    
    # Return both logs and the total summary
    return jsonify({
        'logs': formatted_logs,
        'total_hours_studied': float(total_hours_studied)
    })



