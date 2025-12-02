from extensions import db

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    deadline = db.Column(db.DateTime)
    required_hours = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='to do')  # to do / in progress / done
    priority = db.Column(db.String(20), default='medium')  # low / medium / high
