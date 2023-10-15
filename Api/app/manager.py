from flask import Blueprint,jsonify,request
from flask_jwt_extended import jwt_required,current_user
from sqlalchemy import func
from .decorators import manager_required
from .models import User,Request,CategoryRequest,Category,ProductRequest,Product
from .extensions import db
from .schema import RequestSchema,CategoryRequestSchema,ProductRequestSchema,CategorySchema


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
       return jsonify({'error':'Something went wrong'}),500

@manager_bp.post('/add_product')
@jwt_required()
@manager_required()
def add_product():
    new_name = request.json.get('new_name')
    new_desc = request.json.get('new_desc')
    new_uom = request.json.get('new_uom')
    new_price = request.json.get('new_price')
    new_stock = request.json.get('new_stock')
    category_id = request.json.get('category_id')
    user_id = current_user.id
   
    try:
        product_exists = Product.query.filter(func.lower(Product.name).ilike(new_name)).first()
        name_exists = ProductRequest.query.filter_by(new_name=new_name ,action='add',status="pending").first()
        category_exists = Category.query.filter_by(id=category_id).first()
        if product_exists:
            return jsonify({'error':"The Product with same name exists"}),400
        elif name_exists:
            return jsonify({'error':"This Product is in pending list"}),400
        elif not category_exists:
            return jsonify({'error':"The Category does not exists"}),400
        new_product_request = ProductRequest(action='add',new_name=new_name,new_desc=new_desc,new_uom=new_uom,new_price=new_price,new_stock=new_stock,category_id=category_id,user_id=user_id)
        db.session.add(new_product_request)
        db.session.commit()
        return jsonify({'message':'Sent for approval'}),200
    except Exception as e:
       print(e)
       return jsonify({'error':'Something went wrong'}),500
    
@manager_bp.get('/product_requests')
@jwt_required()
@manager_required()
def get_product_requests():
    try:
        requests = ProductRequest.query.filter_by(user_id = current_user.id).all()
        product_request_schema = ProductRequestSchema(many=True)
        product_request_details = product_request_schema.dump(requests)

        return jsonify({'product_requests':product_request_details}),200
    except Exception as e:
       return jsonify({'error':'Something went wrong'}),500

@manager_bp.get('/all_details')
@jwt_required()
@manager_required()
def get_all_details():
    try:
        all_detail = Category.query.all()
        all_details_schema = CategorySchema(many=True)
        all_details = all_details_schema.dump(all_detail)

        return jsonify({'all_details':all_details}),200
    except Exception as e:
       return jsonify({'error':'Something went wrong'}),500
    
@manager_bp.post('/delete_product/<int:pid>/<int:cid>')
@jwt_required()
@manager_required()
def delete_product(pid,cid):
    try:
        category_exists = Category.query.filter_by(id=cid).first()
        product_exists = Product.query.filter_by(id=pid).first()
        if category_exists:
            if product_exists:
                product_request = ProductRequest.query.filter_by(product_id=pid,action='delete',status='pending').first()
                if product_request:
                    return jsonify({'error':"This Product is in pending list"}),400
                new_product_request = ProductRequest(user_id = current_user.id,action='delete',product_id=pid,category_id = cid,new_name = product_exists.name,new_desc = product_exists.description,new_uom = product_exists.uom,new_stock = product_exists.stock,new_price = product_exists.price )
                db.session.add(new_product_request)
                db.session.commit()
                return jsonify({'message':'Sent for approval'}),200
            else:
                return jsonify({'error':"This Product does not exists"}),400
        else:
            return jsonify({'error':"This Category does not exists"}),400
        
    except Exception as e:
       print(e)
       return jsonify({'error':'Something went wrong'}),500

@manager_bp.post('/update_product')
@jwt_required()
@manager_required()
def update_product():
    new_name = request.json.get('new_name')
    new_desc = request.json.get('new_desc')
    new_uom = request.json.get('new_uom')
    new_price = request.json.get('new_price')
    new_stock = request.json.get('new_stock')
    category_id = request.json.get('category_id')
    product_id = request.json.get('product_id')
    user_id = current_user.id
   
    try:
        product_exists = Product.query.filter_by(id=product_id).first()
        product_request_exist = ProductRequest.query.filter_by(new_name=new_name ,action='update',status="pending").first()
        category_exists = Category.query.filter_by(id=category_id).first()
        if not product_exists:
            return jsonify({'error':"The Product does Not exists"}),400
        elif product_request_exist:
            return jsonify({'error':"This Product is in pending list"}),400
        elif not category_exists:
            return jsonify({'error':"The Category does not exists"}),400
        new_product_request = ProductRequest(action='update',new_name=new_name,new_desc=new_desc,new_uom=new_uom,new_price=new_price,new_stock=new_stock,category_id=category_id,user_id=user_id,product_id=product_id)
        db.session.add(new_product_request)
        db.session.commit()
        return jsonify({'message':'Sent for approval'}),200
    except Exception as e:
       print(e)
       return jsonify({'error':'Something went wrong'}),500