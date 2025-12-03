from extensions import db
from datetime import datetime

class Friend(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key=True)
    
    # The user who sent the request
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # The user who received the request
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Status: 'pending' or 'accepted'
    status = db.Column(db.String(20), default='pending', nullable=False)
    
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships to access user details easily
    requester = db.relationship('User', foreign_keys=[user_id], backref='sent_requests')
    receiver = db.relationship('User', foreign_keys=[friend_id], backref='received_requests')