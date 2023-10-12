from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required,current_user
from .decorators import admin_required
from .models import User,Request,CategoryRequest,Category
from .extensions import db
from .schema import RequestSchema,CategoryRequestSchema


admin_bp = Blueprint('admin_bp',__name__)


@admin_bp.get('/roles')
@jwt_required()
@admin_required()
def get_roles():
    try:
        requests = Request.query.filter_by(status="pending").all()
        role_schema = RequestSchema(many=True)
        role_details = role_schema.dump(requests)
        return jsonify({'role_details' : role_details}),200
    except Exception as e:
        return jsonify({'error':'Something went wrong'}),500

@admin_bp.patch('/approve/<int:id>')
@jwt_required()
@admin_required()
def approve_roles(id):
    try:
        request_exists = Request.query.filter_by(id=id).first()
        if request_exists:
            request_exists.status = "approved"
            request_exists.user.role = "manager"
            db.session.commit()
            return jsonify({'message' : "Approved Successfully"}),200
        return jsonify({'error':'No Request Found'}),404

    except Exception as e:
        return jsonify({'error':'Something went wrong'}),500
    
@admin_bp.patch('/reject/<int:id>')
@jwt_required()
@admin_required()
def reject_roles(id):
    try:
        request_exists = Request.query.filter_by(id=id).first()
        if request_exists:
            request_exists.status = "rejected"
            db.session.commit()
            return jsonify({'message' : "Rejected Successfully"}),200
        return jsonify({'error':'No Request Found'}),404

    except Exception as e:
        return jsonify({'error':'Something went wrong'}),500
    

@admin_bp.get('/category_requests')
@jwt_required()
@admin_required()
def get_category_requests():
    try:
        requests = CategoryRequest.query.filter_by(status='pending').all()
        category_request_schema = CategoryRequestSchema(many=True)
        category_request_details = category_request_schema.dump(requests)
        return jsonify({'category_requests':category_request_details}),200

    except Exception as e:
       return jsonify({'error':'Something went wrong'}),500
    
@admin_bp.post('/approve/category/<int:id>')
@jwt_required()
@admin_required()
def approve_category_add(id):
    try:
        category_request = CategoryRequest.query.filter_by(id=id).first()
        if category_request:
            if category_request.action == 'add':
                category = Category.query.filter_by(name=category_request.name).first()
                if category:
                    return jsonify({'error':'Category already exists'}),400
                new_category = Category(name=category_request.name)
                db.session.add(new_category)
                category_request.status = "approved"
                db.session.commit()
                return jsonify({'message' : "Approved successfully"}),200
            elif category_request.action == 'delete':
                category = Category.query.filter_by(name=category_request.name).first()
                if category:
                    db.session.delete(category)
                    category_request.status = "approved"
                    db.session.commit()
                    return jsonify({'message' : "Approved successfully"}),200
                return jsonify({'error':'No Category found'}),404
            else:
                category = Category.query.filter_by(id=category_request.category_id).first()
                if category:
                    category.name = category_request.name
                    category_request.status = "approved"
                    db.session.commit()
                    return jsonify({'message' : "Approved successfully"}),200
                return jsonify({'error':'No Category found'}),404
        return jsonify({'error':'No Request Found'}),404

    except Exception as e:
        return jsonify({'error':'Something went wrong'}),500

@admin_bp.patch('/reject/category/<int:id>')
@jwt_required()
@admin_required()
def reject_category_add(id):
    try:
        category_request = CategoryRequest.query.filter_by(id=id).first()
        if category_request:
            if category_request.status == 'pending':
                category_request.status = "rejected"
                db.session.commit()
                return jsonify({'message' : "Rejected Successfully"}),200
            else:
                return jsonify({'error':'This Request have already been reviewed'}),400
        return jsonify({'error':'No Request Found'}),404

    except Exception as e:
        print(e)
        return jsonify({'error':'Something went wrong'}),500
    
@admin_bp.get('/updated_category_requests')
@jwt_required()
@admin_required()
def updated_category_requests():
    try:
        requests = CategoryRequest.query.filter(CategoryRequest.status.in_(['approved', 'rejected'])).all()
        category_request_schema = CategoryRequestSchema(many=True)
        category_request_details = category_request_schema.dump(requests)
        return jsonify({'category_requests':category_request_details}),200
    except Exception as e:
       return jsonify({'error':'Something went wrong'}),500