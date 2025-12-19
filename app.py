from flask import Flask, jsonify, render_template, session, redirect, url_for, make_response
from flask_cors import CORS
from extensions import db, bcrypt  
from sqlalchemy import text

app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')

# Initialize db with app
db.init_app(app)
bcrypt.init_app(app)

# Test connection
with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1")).scalar()  # wrap in text()
        print("Connection successful! Result:", result)
    except Exception as e:
        print("Connection failed!")
        print(e)
@app.after_request # Added global handler to prevent back-button access after logout
def add_header(response): 
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate" # EDITED: Prevent caching
    response.headers["Pragma"] = "no-cache" 
    response.headers["Expires"] = "0" 
    return response 

# Import models AFTER db.init_app to avoid circular import
from models.user import User
from models.subject import Subject
from models.task import Task
from models.study_log import StudyLog
from models.badge import Badge
from models.friend import Friend

# Blueprints
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp
from routes.subject_routes import subject_bp
from routes.dashboard_routes import dashboard_bp
from routes.friend_routes import friend_bp
from routes.user_routes import user_bp
from routes.study_routes import study_bp

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
app.register_blueprint(subject_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(friend_bp)
app.register_blueprint(user_bp)
app.register_blueprint(study_bp)

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/signup")
def signup_page():
    return render_template("signup.html")
@app.route('/profile-page')
def profile_page():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    return render_template('profile.html')
@app.route('/dashboard-page')
def dashboard_page():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    return render_template('dashboard.html')
@app.route('/friends-page')
def friends_page():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    return render_template('friends.html')


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)


















