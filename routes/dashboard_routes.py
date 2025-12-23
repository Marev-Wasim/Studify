from flask import Blueprint, jsonify, render_template, session, redirect, url_for
from sqlalchemy import func
from models.task import Task
from models.study_log import StudyLog
from models.subject import Subject

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
    # user_subjects = Subject.query.filter_by(user_id=user_id).all()
    # subject_ids = [subject.id for subject in user_subjects]
    # 1.Get Subject IDs (Uses index on user_id if exists)
    subject_ids = [s.id for s in Subject.query.filter_by(user_id=user_id).all()]
    if not subject_ids:
        return jsonify({'total_tasks': 0, 'completed_tasks': 0, 'total_hours': 0, 'completion_percentage': 0})

    ####subjects_data = [{'id': s.id, 'name': s.name} for s in user_subjects]
    
    # 2. Get tasks for user's subjects
    # total_tasks = Task.query.filter(Task.subject_id.in_(subject_ids)).count() if subject_ids else 0
    # completed_tasks = Task.query.filter(
    #     Task.subject_id.in_(subject_ids),
    #     Task.completed == True
    # ).count() if subject_ids else 0
    # 2.Get Task Counts (Uses idx_tasks_subject_id)
    # We do this in one query to be efficient
    task_stats = db.session.query(
        func.count(Task.task_id),
        func.sum(db.case((Task.completed == True, 1), else_=0))
    ).filter(Task.subject_id.in_(subject_ids)).first()

    total_tasks = task_stats[0] or 0
    completed_tasks = task_stats[1] or 0
    
    # 3. Get user's study logs (already has user_id)
    # user_study_logs = StudyLog.query.filter_by(user_id=user_id).all()
    # total_hours = sum([log.hours_studied for log in user_study_logs])
    # 3. Get total hours (Uses idx_study_logs_user_date)
    # This is MUCH faster because it stays in the database
    total_hours = db.session.query(func.sum(StudyLog.hours_studied)).filter(
        StudyLog.user_id == user_id
    ).scalar() or 0
    
    # 4. Calculate percentage (avoid division by zero)
    # completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks else 0
    # 4. Calculate percentage
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks else 0
    
    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        #'total_hours': round(total_hours, 2),  # Round to 2 decimal places
        'total_hours': round(float(total_hours), 2),
        'completion_percentage': round(completion_percentage, 1)  # Round to 1 decimal
    })
