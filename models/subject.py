from extensions import db

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    tasks = db.relationship('Task', backref='subject', lazy=True)
