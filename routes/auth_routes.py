from flask import Blueprint, request, jsonify, render_template
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register a new user
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('signup.html')
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if password != confirm_password: 
        return jsonify({'message': 'Passwords do not match'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

# Login (simple placeholder, no JWT yet)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return jsonify({'message': 'Login successful', 'user_id': user.id})
    return jsonify({'message': 'Invalid credentials'}), 401






