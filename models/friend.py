from extensions import db
from datetime import datetime
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy import func

class Friend(db.Model):
    __tablename__ = 'friends'
    #id = db.Column(db.Integer, primary_key=True)
    
    # The user who sent the request
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # The user who received the request
    #friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user_id1 = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    user_id2 = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # Status: 'pending' or 'accepted'
    status = db.Column(db.String(20), default='pending', nullable=False)
    
    #date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    requested_at = db.Column(db.DateTime, server_default=func.now())

    # Check Constraint to ensure id1 < id2
    __table_args__ = (
        CheckConstraint('user_id1 < user_id2', name='check_user_order'),
    )

    # Relationships to access user details easily
    #requester = db.relationship('User', foreign_keys=[user_id], backref='sent_requests')

    #receiver = db.relationship('User', foreign_keys=[friend_id], backref='received_requests')
