from extensions import db

class Task(db.Model):
    __tablename__ = 'tasks'
    task_id = db.Column('task_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(150), nullable=False)
    #description = db.Column(db.Text)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    due_date = db.Column('due_date', db.Date, nullable=True)
    est_min = db.Column('est_min', db.Integer, nullable=True)
    # status = db.Column(db.String(20), default='to do')  # to do / in progress / done
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column('created_at', db.DateTime, default=db.func.now())
    subject_id = db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    #priority = db.Column(db.String(20), default='medium')  # low / medium / high
