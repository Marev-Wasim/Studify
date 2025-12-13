from flask import Blueprint, jsonify, render_template, session, redirect, url_for
from models.task import Task
from models.study_log import StudyLog

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
# HTML Dashboard page (users see this after login)
@dashboard_bp.route('/')
def dashboard_page():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html')
    
# Simple dashboard: count tasks and total hours
@dashboard_bp.route('/summary', methods=['GET'])
def summary():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    # 1. Get all subjects for this user
    user_subjects = Subject.query.filter_by(user_id=user_id).all()
    subject_ids = [subject.id for subject in user_subjects]
    
    # 2. Get tasks for user's subjects
    total_tasks = Task.query.filter(Task.subject_id.in_(subject_ids)).count() if subject_ids else 0
    completed_tasks = Task.query.filter(
        Task.subject_id.in_(subject_ids),
        Task.completed == True
    ).count() if subject_ids else 0
    
    # 3. Get user's study logs (already has user_id)
    user_study_logs = StudyLog.query.filter_by(user_id=user_id).all()
    total_hours = sum([log.hours_studied for log in user_study_logs])
    
    # 4. Calculate percentage (avoid division by zero)
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks else 0
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'total_hours': round(total_hours, 2),  # Round to 2 decimal places
        'completion_percentage': round(completion_percentage, 1)  # Round to 1 decimal
    })





