from flask import Blueprint, request, jsonify
from extensions import db
from models.subject import Subject

subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')


@subject_bp.route('/', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        #'color': s.color
    } for s in subjects])


@subject_bp.route('/', methods=['POST'])
def create_subject():
    data = request.get_json()
    
    subject = Subject(
        name=data.get('name'),
        #color=data.get('color'),
        user_id=data.get('user_id')
    )
    db.session.add(subject)
    db.session.commit()

    return jsonify({'message': 'Subject created', 'subject_id': subject.id})


@subject_bp.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)

    if not subject:
        return jsonify({'error': 'Subject not found'}), 404

    db.session.delete(subject)
    db.session.commit()

    return jsonify({'message': 'Subject deleted successfully'})


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
