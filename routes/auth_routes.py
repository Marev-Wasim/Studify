from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for, session
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Register a new user
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    # Input validation
    if not username or not email or not password or not confirm_password:
        flash('Missing required fields')
        return redirect(url_for('auth.signup'))
        
    if password != confirm_password:
        flash('Passwords do not match')
        return redirect(url_for('auth.signup'))
    
    if User.query.filter_by(email=email).first():
        flash('Email already exists')
        return redirect(url_for('auth.signup'))
    
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    # Log user in automatically after signup
    session['user_id'] = user.id
    flash('Account created successfully!')
    return redirect(url_for('dashboard.dashboard_page'))  # Changed to dashboard

# Login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        session['user_id'] = user.id

        if request.is_json:
            return jsonify({'success': True, 'message': 'Logged in'})
        return redirect(url_for('dashboard.dashboard_page'))  # Go to dashboard
    
    # The following lines are for handling failed login attempts
    if request.is_json:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
    flash('Invalid credentials')
    return redirect(url_for('auth.login'))

# Logout
@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out')
    return redirect(url_for('auth.login'))
