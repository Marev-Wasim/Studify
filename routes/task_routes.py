from flask import Blueprint, request, jsonify
from extensions import db
from models.task import Task

task_bp = Blueprint('task', __name__, url_prefix='/tasks')

@task_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'status': t.status,
    } for t in tasks])


@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    
    task = Task(
        title=data.get('title'),
        subject_id=data.get('subject_id'),
        user_id=data.get('user_id'),
        deadline=data.get('deadline'),
        required_minutes=data.get('required_minutes', 0),
        status=data.get('status', 'to do'),
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({'message': 'Task created', 'task_id': task.id})

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'})


@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'subject_id' in data:
        task.subject_id = data['subject_id']
   # if 'user_id' in data:
       # task.user_id = data['user_id']
    if 'deadline' in data:
        task.deadline = data['deadline']
    if 'required_minutes' in data:
        task.required_minutes = data['required_minutes']
    if 'status' in data:
        task.status = data['status']

    db.session.commit()

    return jsonify({'message': 'Task updated successfully'})
