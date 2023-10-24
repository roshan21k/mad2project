from flask import Blueprint,request,jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,current_user,get_jwt_identity,get_jwt
from .extensions import db
from .models import User
import redis
from datetime import timedelta


auth_bp = Blueprint('auth',__name__)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)
ACCESS_EXPIRES = timedelta(hours=1)

@auth_bp.post('/register')
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    

    if username is None or email is None or password is None:
        return jsonify({'error':'Invalid credentials'}),409
    
    username_exists=User.query.filter_by(username=username).first()
    email_exists = User.query.filter_by(email=email).first()

    if username_exists:
        return jsonify({'error':'Username taken already'}),409
    elif email_exists:
        return jsonify({'error':'An account with this email already exists'}),409
    elif password is None:
        return jsonify({'error':'Password cannot be Empty'}),409
    
    new_user = User(username=username,email=email,password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'user created Successfully',"tokens":{

    'access':create_access_token(identity=new_user.username),"refresh":create_refresh_token(identity=new_user.username)}}),201


@auth_bp.post('/login')
def login():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

    if email is not None and username is None:
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                return jsonify({"message":"Logged in successfully","tokens":{
            'access':create_access_token(identity=user.username),
            'refresh':create_refresh_token(identity=user.username)
        }}),200
            else:
                return jsonify({'error':'Invalid credentials'}),400
        else:
            return jsonify({"error":"User does not exists"}),409
    elif email is None and username is not None:   
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password,password):
                return jsonify({"message":"Logged in successfully","tokens":{
            'access':create_access_token(identity=user.username),
            'refresh':create_refresh_token(identity=user.username)
        },"role":user.role}),200
            else:
                return jsonify({'error':'Invalid credentials'}),400
        else:
            return jsonify({"error":"User does not exists"}),409
    
    return jsonify({'error':'Invalid credentials'}),400

@auth_bp.get('/refresh')
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access":new_access_token})

@auth_bp.delete('/logout')
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")