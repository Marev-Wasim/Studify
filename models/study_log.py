from extensions import db
from datetime import datetime

class StudyLog(db.Model):
    __tablename__ = 'study_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    study_date = db.Column(db.Date, nullable=False)
    hours_studied = db.Column(db.Numeric(4, 2), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id'), nullable=True)
  

