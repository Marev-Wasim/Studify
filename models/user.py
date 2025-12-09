from extensions import db # Changed import to include bcrypt if not already there
from extensions import bcrypt # Assuming bcrypt is initialized in extensions.py
from werkzeug.security import generate_password_hash, check_password_hash # Keep imports for type hints/backward compatibility

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    subjects = db.relationship('Subject', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)
    study_logs = db.relationship('StudyLog', backref='user', lazy=True)
    badges = db.relationship('Badge', backref='user', lazy=True)

    def set_password(self, password):
        # IMPORTANT: Use bcrypt from extensions to hash the password
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8') 

    def check_password(self, password):
        # IMPORTANT: Use bcrypt from extensions to check the password
        # You may need to handle cases where the hash is from werkzeug directly, 
        # but using bcrypt.check_password_hash is safer if you use Flask-Bcrypt
        return bcrypt.check_password_hash(self.password_hash, password)
    
    # You should add a to_dict method here if it doesn't exist to match user_routes.py expectations:
    # def to_dict(self):
    #     return { 'id': self.id, 'username': self.username, 'email': self.email, 'points': getattr(self, 'points', 0) }


