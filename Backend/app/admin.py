from flask import Blueprint,jsonify
from flask_jwt_extended import jwt_required
from .decorators import admin_required
from .models import Request,CategoryRequest,Category,ProductRequest,Product
from .extensions import db,cache
from .schema import RequestSchema,CategoryRequestSchema,ProductRequestSchema


admin_bp = Blueprint('admin_bp',__name__)

# Roles sent for Approval
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
    
# Updated Roles (Rejected/Approved)
@admin_bp.get('/updated_roles')
@jwt_required()
@admin_required()
def get_updated_roles():
    try:
        requests = Request.query.filter(Request.status.in_(['approved', 'rejected'])).all()
        print(requests)
        role_schema = RequestSchema(many=True)
        role_details = role_schema.dump(requests)
        return jsonify({'updated_role_details' : role_details}),200
    except Exception as e:
        return jsonify({'error':'Something went wrong'}),500

# Approve Manager Request
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

# Reject Manager Request
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
    
# All Category Request
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
    
# Approve Category Request
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
                cache.delete('filter')
                # cache.delete('category_requests')
                return jsonify({'message' : "Approved successfully"}),200
            elif category_request.action == 'delete':
                category = Category.query.filter_by(name=category_request.name).first()
                if category:
                    db.session.delete(category)
                    category_request.status = "approved"
                    db.session.commit()
                    cache.delete('filter')
                    # cache.delete('category_requests')
                    return jsonify({'message' : "Approved successfully"}),200
                return jsonify({'error':'No Category found'}),404
            else:
                category = Category.query.filter_by(id=category_request.category_id).first()
                if category:
                    category.name = category_request.name
                    category_request.status = "approved"
                    db.session.commit()
                    cache.delete('filter')
                    # cache.delete('category_requests')
                    return jsonify({'message' : "Approved successfully"}),200
                return jsonify({'error':'No Category found'}),404
        return jsonify({'error':'No Request Found'}),404

    except Exception as e:
        return jsonify({'error':'Something went wrong'}),500

# Reject Category Request
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
                # cache.delete('category_requests')
                return jsonify({'message' : "Rejected Successfully"}),200
            else:
                return jsonify({'error':'This Request have already been reviewed'}),400
        return jsonify({'error':'No Request Found'}),404

    except Exception as e:
        print(e)
        return jsonify({'error':'Something went wrong'}),500

# Updated Category Requests
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
    
# All Product Requests
@admin_bp.get('/product_requests')
@jwt_required()
@admin_required()
def get_product_requests():
    try:
        requests = ProductRequest.query.filter_by(status = "pending").all()
        product_request_schema = ProductRequestSchema(many=True)
        product_request_details = product_request_schema.dump(requests)

        return jsonify({'product_requests':product_request_details}),200
    except Exception as e:
       return jsonify({'error':'Something went wrong'}),500
    
# Approve Product Request
@admin_bp.post('/approve/product/<int:id>')
@jwt_required()
@admin_required()
def approve_product(id):
    try:
        product_request = ProductRequest.query.filter_by(id=id).first()
        if product_request:
            if product_request.action == 'add':
                product = Product.query.filter_by(name=product_request.new_name).first()
                if product:
                    return jsonify({'error':'Product already exists'}),400
                new_product = Product(name=product_request.new_name,price=product_request.new_price,category_id = product_request.category_id,stock=product_request.new_stock,uom=product_request.new_uom,description=product_request.new_desc)
                db.session.add(new_product)
                product_request.status = "approved"
                db.session.commit()
                # cache.delete('product_requests')
                return jsonify({'message' : "Approved successfully"}),200
            elif product_request.action == 'delete':
                product = Product.query.filter_by(id=product_request.product_id).first()
                if product:
                    db.session.delete(product)
                    product_request.status = "approved"
                    db.session.commit()
                    # cache.delete('product_requests')
                    return jsonify({'message' : "Approved successfully"}),200
                return jsonify({'error':'No Product found'}),404
            else:
                product = Product.query.filter_by(id=product_request.product_id).first()
                if product:
                    product.name = product_request.new_name
                    product.price = product_request.new_price
                    product.stock += product_request.new_stock
                    product.uom = product_request.new_uom
                    product.description = product_request.new_desc
                    product_request.status = "approved"
                    db.session.commit()
                    # cache.delete('product_requests')
                    return jsonify({'message' : "Approved successfully"}),200
                return jsonify({'error':'No Product found'}),404
        return jsonify({'error':'No Request Found'}),404

    except Exception as e:
        print(e)
        return jsonify({'error':'Something went wrong'}),500

# Reject Product Request
@admin_bp.patch('/reject/product/<int:id>')
@jwt_required()
@admin_required()
def reject_product(id):
    try:
        product_request = ProductRequest.query.filter_by(id=id).first()
        if product_request:
            if product_request.status == 'pending':
                product_request.status = "rejected"
                db.session.commit()
                # cache.delete('product_requests')
                return jsonify({'message' : "Rejected Successfully"}),200
            else:
                return jsonify({'error':'This Request have already been reviewed'}),400
        return jsonify({'error':'No Request Found'}),404

    except Exception as e:
        print(e)
        return jsonify({'error':'Something went wrong'}),500

# Updated Product Requests 
@admin_bp.get('/updated_product_requests')
@jwt_required()
@admin_required()
def updated_product_requests():
    try:
        requests = ProductRequest.query.filter(ProductRequest.status.in_(['approved', 'rejected'])).all()
        product_request_schema = ProductRequestSchema(many=True)
        product_request_details = product_request_schema.dump(requests)
        return jsonify({'product_requests':product_request_details}),200
    except Exception as e:
       return jsonify({'error':'Something went wrong'}),500