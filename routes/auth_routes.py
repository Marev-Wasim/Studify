from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register a new user
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    # data = request.get_json()
    # username = data.get('username')
    # email = data.get('email')
    # password = data.get('password')
    # confirm_password = data.get('confirm_password')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    # if password != confirm_password: 
    #     return jsonify({'message': 'Passwords do not match'}), 400

    # if User.query.filter_by(email=email).first():
    #     return jsonify({'message': 'Email already exists'}), 400
    #############################marev here
    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('auth.register'))
    
    if User.query.filter_by(email=email).first():
        flash('Email already exists')
        return redirect(url_for('auth.register'))

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    #return jsonify({'message': 'User registered successfully'}), 201
    flash('Account created successfully! Please login.')
    return redirect(url_for('login'))

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








