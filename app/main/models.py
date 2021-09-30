from .. import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email  = db.Column(db.String(255),unique = True,nullable = False)
    password = db.Column(db.String(255),nullable = False)
    bio = db.Column(db.String(255))
    admin = db.Column(db.Boolean)
       
    def __repr__(self):
        return f'User {self.username}'
class Lend(db.Model):

    __tablename__ = 'lender'

    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('libraries.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    price = db.Column(db.Integer)

    def __repr__(self):
        return f'Lend {self.name}'
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.Text(),nullable = False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    library_id = db.Column(db.Integer,db.ForeignKey('libraries.id'),nullable = False) 
    def __repr__(self):
        return f'Review:{self.review}'
    



class Library(db.Model):
    __tablename__ = 'libraries'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    name = db.Column(db.Text(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    book_pic = db.Column(db.String(255),nullable = False)
    lend = db.Column(db.Boolean)

        
    def __repr__(self):
        return f'Library {self.post}'