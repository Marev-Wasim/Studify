from flask import Blueprint, request, jsonify, session
from extensions import db, bcrypt
from models.user import User
from models.subject import Subject
from models.task import Task
from models.study_log import StudyLog 
from models.badge import Badge       
from sqlalchemy import func

user_bp = Blueprint('user', __name__, url_prefix='/profile')

def get_auth_user_id():
    """Retrieves the authenticated user's ID from the session."""
    return session.get('user_id')

@user_bp.route('/', methods=['GET'])
def get_user_profile():
    """
    Retrieves the authenticated user's comprehensive profile data, 
    including aggregated stats (hours, badges, points).
    """
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    
    # 1. Calculate Total Study Hours
    total_hours_query = db.session.query(func.sum(StudyLog.hours_studied)).filter(StudyLog.user_id == user_id)
    total_hours_studied = total_hours_query.scalar() or 0.0
    
    # 2. Count Total Badges
    badge_count = Badge.query.filter_by(user_id=user_id).count()
    
   # Get all subjects for this user
    user_subjects = Subject.query.filter_by(user_id=user_id).all()
    subject_ids = [subject.id for subject in user_subjects]

    #subjects_data = [{'id': s.id, 'name': s.name} for s in user_subjects]
    
    # Get tasks for user's subjects
    total_tasks = Task.query.filter(Task.subject_id.in_(subject_ids)).count() if subject_ids else 0
    completed_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids),
        Task.completed == True
    ).count() if subject_ids else 0
       
    # Calculate percentage (avoid division by zero)
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks else 0
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'points':user.total_coins,
        
        # New Consolidated Stats
        'total_hours_studied': float(total_hours_studied),
        'badge_count': badge_count,
        'subjects': subjects_list
    }), 200


@user_bp.route('/', methods=['PUT', 'PATCH'])
def update_user_profile():
    """Allows authenticated user to update username, and/or password."""
    user_id = get_auth_user_id()
    if not user_id:
        return jsonify({'error': 'Authentication required'}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    data = request.get_json()
    
    new_username = data.get('username')
    if new_username and new_username != user.username:
        if User.query.filter(User.username == new_username).first():
            return jsonify({'error': 'Username already taken'}), 409
        user.username = new_username
    
    new_password = data.get('password')
    if new_password:
        user.set_password(new_password)
        
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user_id': user.id,
            'username': user.username 
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile due to database error'}), 500
        






