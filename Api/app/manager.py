from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,current_user
from sqlalchemy import func
from .decorators import manager_required
from .models import User,Request,CategoryRequest,Category
from .extensions import db
from .schema import RequestSchema,CategoryRequestSchema


manager_bp = Blueprint('manager_bp',__name__)


@manager_bp.get('/requests')
@jwt_required()
@manager_required()
def get_requests():
    try:
        requests = CategoryRequest.query.filter_by(user_id = current_user.id).all()

        category_request_schema = CategoryRequestSchema(many=True)
        category_request_details = category_request_schema.dump(requests)

        return jsonify({'category_requests':category_request_details}),200
    except Exception as e:
       return jsonify({'error':'Something went wrong'}),500

@manager_bp.post('/add_category')
@jwt_required()
@manager_required()
def add_category():
    name = request.json.get('updated_name')
    try:
        name_exists = Category.query.filter(func.lower(Category.name).ilike(name)).first()
        category_request = CategoryRequest.query.filter_by(name=name,action='add',status='pending').first()
        if name_exists:
            return jsonify({'error':"The category with same name exists"}),400
        elif category_request:
            return jsonify({'error':"This category name is in pending list"}),400
        new_category_request = CategoryRequest(user_id = current_user.id,action='add',name=name)
        db.session.add(new_category_request)
        db.session.commit()
        return jsonify({'message':'Sent for approval'}),200
    except Exception as e:
       print(e)
       return jsonify({'error':'Something went wrong'}),500
    
@manager_bp.post('/delete_category/<int:id>')
@jwt_required()
@manager_required()
def delete_category(id):
    try:
        category_exists = Category.query.filter_by(id=id).first()
        if category_exists:
            category_request = CategoryRequest.query.filter_by(name=category_exists.name,action='delete',status='pending').first()
            if category_request:
                return jsonify({'error':"This category name is in pending list"}),400
            new_category_request = CategoryRequest(user_id = current_user.id,action='delete',name=category_exists.name)
            db.session.add(new_category_request)
            db.session.commit()
            return jsonify({'message':'Sent for approval'}),200
        else:
            return jsonify({'error':"This Category does not exists"}),400
        
    except Exception as e:
       print(e)
       return jsonify({'error':'Something went wrong'}),500

@manager_bp.post('/update_category/<int:id>')
@jwt_required()
@manager_required()
def update_category(id):
    name = request.json.get('updated_name')
    try:
        name_exists = Category.query.filter(func.lower(Category.name).ilike(name)).first()
        category_request = CategoryRequest.query.filter_by(name=name,action='update',status='pending').first()
        category_exists = Category.query.filter_by(id=id).first()
        if name_exists:
            return jsonify({'error':"The category with same name exists"}),400
        elif category_request:
            return jsonify({'error':"This category name is in pending list"}),400
        if category_exists:
            new_category_request = CategoryRequest(user_id = current_user.id,action='update',name=name,category_id = id,old_name=category_exists.name)
            db.session.add(new_category_request)
            db.session.commit()
            return jsonify({'message':'Sent for approval'}),200
        return jsonify({'error':"This category Does not exist"}),400
    except Exception as e:
       print(e)
       return jsonify({'error':'Something went wrong'}),500