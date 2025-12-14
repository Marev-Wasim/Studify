from extensions import db
from sqlalchemy import func
from sqlalchemy import CheckConstraint

class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    
    due_date = db.Column(db.Date, nullable=True)
    est_min = db.Column(db.Integer, nullable=True)
    __table_args__ = (CheckConstraint(est_min > 0, name='est_min_positive_check'))

    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    #description = db.Column(db.Text)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #status = db.Column(db.String(20), default='to do')  # to do / in progress / done
    #priority = db.Column(db.String(20), default='medium')  # low / medium / high


