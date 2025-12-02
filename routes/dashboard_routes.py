from flask import Blueprint, jsonify
from models.task import Task
from models.activity_log import ActivityLog

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Simple dashboard: count tasks and total hours
@dashboard_bp.route('/summary', methods=['GET'])
def summary():
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(status='done').count()
    total_hours = sum([log.hours for log in ActivityLog.query.all()])

    return jsonify({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'total_hours': total_hours,
        'completion_percentage': (completed_tasks / total_tasks * 100) if total_tasks else 0
    })
