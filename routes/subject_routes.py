from flask import Blueprint, request, jsonify
from extensions import db
from models.subject import Subject

subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')

# Get all subjects
@subject_bp.route('/', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'color': s.color
    } for s in subjects])

# Create a new subject
@subject_bp.route('/', methods=['POST'])
def create_subject():
    data = request.get_json()
    subject = Subject(
        name=data.get('name'),
        color=data.get('color'),
        user_id=data.get('user_id')
    )
    db.session.add(subject)
    db.session.commit()
    return jsonify({'message': 'Subject created', 'subject_id': subject.id})
