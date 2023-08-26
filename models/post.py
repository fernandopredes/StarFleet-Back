from db import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    abstract = db.Column(db.String(300), nullable=False)
    text = db.Column(db.String(2200), nullable=False)
    image_one = db.Column(db.String, nullable=True)
    image_two = db.Column(db.String, nullable=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with UserModel
    user = db.relationship("UserModel", back_populates="posts")
