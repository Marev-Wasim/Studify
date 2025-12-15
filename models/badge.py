from extensions import db
from datetime import datetime
from sqlalchemy import func

class Badge(db.Model):
    __tablename__ = 'badges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_name = db.Column(db.String(100), nullable=False)
    earned_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    #description = db.Column(db.String(200))
