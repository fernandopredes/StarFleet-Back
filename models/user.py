from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    profile_pic = db.Column(db.String, nullable=True)


    # Relationship with PostModel
    posts = db.relationship("PostModel", back_populates="user", lazy=True, cascade="all,delete")
