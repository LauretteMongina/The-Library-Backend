from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import backref
from app.db_instance import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email  = db.Column(db.String(255),unique = True,nullable = False)
    secure_password = db.Column(db.String(255),nullable = False)
    bio = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_pic_path = db.Column(db.String())
    libraries= db.relationship('Library', backref='user', lazy='dynamic')
    upvote= db.relationship('Upvote', backref='user', lazy='dynamic')
    downvote=db.relationship('Downvote', backref='user', lazy='dynamic')
    lend=db.relationship('Lend', backref='user', lazy='dynamic')
    review=db.relationship('Review', backref='user', lazy='dynamic')
    

    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secure_password,password) 
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'User {self.username}'
class Lend(db.Model):

    __tablename__ = 'lender'

    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('libraries.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = 
    library = db.relationship('Library', backref='lend', lazy='dynamic')

    def __repr__(self):
        return f'Category {self.name}'
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    library_id = db.Column(db.Integer,db.ForeignKey('libraries.id'),nullable = False)

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_reviews(cls,library):
        reviews = Review.query.filter_by(library_id=library_id).all()

        return reviews

    
    def __repr__(self):
        return f'Review:{self.review}'

class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    library_id = db.Column(db.Integer,db.ForeignKey('libraries.id'))
    

    def save_upvote(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvote.query.filter_by(library_id=id).all()
        return upvote


    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'
class Downvote(db.Model):
    __tablename__ = 'downvotes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    library_id = db.Column(db.Integer,db.ForeignKey('libraries.id'))
    

    def save_downvote(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(library_id=id).all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.library_id}'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Library(db.Model):
    __tablename__ = 'libraries'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    post = db.Column(db.Text(), nullable = False)
    review = db.relationship('Review',backref='library',lazy='dynamic')
    upvote = db.relationship('Upvote',backref='library',lazy='dynamic')
    downvote = db.relationship('Downvote',backref='library',lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_pic = db.Column(db.String(255),nullable = False)
    lend = db.relationship('Lend',backref='library',lazy='dynamic')
    
    def save_library(self):
        db.session.add(self)
        db.session.commit()

        
    def __repr__(self):
        return f'Library {self.post}'