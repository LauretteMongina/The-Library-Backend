from . import main
from .. import db
from flask_login import current_user
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, abort,make_response
from werkzeug.wrappers import response
from app.main.models import User,Library,Review,Lend
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt)
import datetime
from functools import wraps
from . import main




@main.route('/user', methods=['GET'])
def get_all_users():


    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['bio'] = user.bio
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})
@main.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}

    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    user_data['bio'] = user.bio
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})



@main.route('/user', methods=['POST'])
def create_user():

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'],email=data['email'],bio=data['bio'] ,password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@main.route('/user/<public_id>', methods=['PUT'])
def promote_user(public_id):
    

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})
@main.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

@main.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    if check_password_hash(user.password, auth.password):
        
        return{
                    "message": "logged in"}, 200
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
@main.route('/library', methods=['GET'])
def get_all_libraries():
    libraries = Library.query.all()

    output = []

    for library in libraries:
        library_data = {}
        library_data['id'] = library.id
        library_data['title'] = library.title
        library_data['name'] = library.name
        output.append(library_data)

    return jsonify({'libraries' : output})

@main.route('/library/<library_id>', methods=['GET'])
def get_one_library(library_id):
    library = Library.query.filter_by(id=library_id).first()

    if not library:
        return jsonify({'message' : 'No book found!'})

    library_data = {}
    library_data['id'] = library_id
    library_data['title'] = library.title
    library_data['name'] = library.name

    return jsonify(library_data)

@main.route('/library', methods=['POST'])
def create_library():
    data = request.get_json()


    new_library = Library(title=data['title'],name=data['name'],book_pic=data['book_pic'], lend=False)
    db.session.add(new_library)
    db.session.commit()

    return jsonify({'message' : "Book  created!"})
@main.route('/library/<library_id>', methods=['PUT'])
def lend_library(library_id):
    library = Library.query.filter_by(id=library_id).first()

    if not library:
        return jsonify({'message' : 'No book found!'})

    library.lend = True
    db.session.commit()

    return jsonify({'message' : 'Book item has been lended!'})

@main.route('/library/<library_id>', methods=['DELETE'])
def delete_library(library_id):
    library = Library.query.filter_by(id=library_id).first()

    if not library:
        return jsonify({'message' : 'No book found!'})

    db.session.delete(library)
    db.session.commit()

    return jsonify({'message' : 'Book item deleted!'})
@main.route('/lend', methods=['GET'])
def get_all_lends():
    lends = Lend.query.all()

    output = []

    for lend in lends:
        lend_data = {}
        lend_data['id'] = lend.id
        lend_data['price'] = lend.price
        output.append(lend_data)

    return jsonify({'lends' : output})

@main.route('/lend/<lend_id>', methods=['GET'])
def get_one_lend(current_user, lend_id):
    lend = Lend.query.filter_by(id=lend_id, user_id=current_user.id).first()

    if not lend:
        return jsonify({'message' : 'No lend found!'})

    lend_data = {}
    lend_data['id'] = lend.id
    lend_data['price'] = lend.price

    return jsonify(lend_data)

@main.route('/lend', methods=['POST'])
def create_lend():
    data = request.get_json()

    new_lend = Lend(price=data['price'])
    db.session.add(new_lend)
    db.session.commit()

    return jsonify({'message' : "Lend created!"})


@main.route('/lend/<lend_id>', methods=['DELETE'])
def delete_lend(lend_id):
    lend = Lend.query.filter_by(id=lend_id).first()

    if not lend:
        return jsonify({'message' : 'No lend found!'})

    db.session.delete(lend)
    db.session.commit()

    return jsonify({'message' : 'lend item deleted!'})
