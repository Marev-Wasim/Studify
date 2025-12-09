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
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='done').count()
    total_hours = sum([log.hours_studied for log in StudyLog.query.all()])

    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'total_hours': total_hours,
        'completion_percentage': (completed_tasks / total_tasks * 100) if total_tasks else 0
    })


