from flask import Flask, jsonify, render_template
from flask_cors import CORS
from extensions import db  
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://marevwasim:soFt!waRe@studify-server.database.windows.net/Studify_db?"
    "driver=ODBC+Driver+18+for+SQL+Server"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)

# Test connection
with app.app_context():
    try:
        result = db.session.execute(text("SELECT 1")).scalar()  # wrap in text()
        print("Connection successful! Result:", result)
    except Exception as e:
        print("Connection failed!")
        print(e)

# Import models AFTER db.init_app to avoid circular import
from models.user import User
from models.subject import Subject
from models.task import Task
from models.activity_log import ActivityLog
from models.badge import Badge
from models.friend import Friend

# Blueprints
from routes.auth_routes import auth_bp
from routes.task_routes import task_bp
from routes.subject_routes import subject_bp
from routes.dashboard_routes import dashboard_bp
from routes.friend_routes import friend_bp
from routes.user_routes import user_bp

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)
app.register_blueprint(subject_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(friend_bp)
app.register_blueprint(user_bp)

@app.route("/")
def index():
    return render_template('index.html')
@app.route("/signup")
def signup_page():
    return render_template("signup.html")

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)

















