from extensions import db
from datetime import datetime

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    hours = db.Column(db.Float, nullable=False)
