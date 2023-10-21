from flask import Blueprint,jsonify,request
from sqlalchemy import func
from flask_jwt_extended import jwt_required,current_user
from .models import Category,Product,Cart,Order,OrderDetail,Review,Request,Sale
from .extensions import db
from .schema import CategorySchema,ProductSchema,CartSchema,OrderSchema,OrderDetailsSchema,ReviewSchema,RequestSchema,UserSchema
from .task import *
user_bp = Blueprint('user',__name__)

@user_bp.get('/')
@jwt_required()
def user_home():

    categories = Category.query.all()
    category_schema = CategorySchema(many=True)

    category_data = category_schema.dump(categories)

    return jsonify({'categories': category_data}),200

@user_bp.post('/cart/<int:id>')
@jwt_required()
def user_cart(id):
    try:
        item_exists = Cart.query.filter_by(user_id=current_user.id,product_id=id).first()

        if item_exists:
            item_exists.quantity += 1
        else:
            new_item = Cart(user_id=current_user.id,product_id=id)
            db.session.add(new_item)
        db.session.commit()
        return jsonify({'message':f'Added to the cart successfully'}),200
    except Exception:
        db.session.rollback() 
        return jsonify({'error': ' error occurred'}), 500
    
@user_bp.get('/product/<int:id>')
@jwt_required()
def product(id):
    try:
        product_exists = Product.query.filter_by(id=id).first()

        if product_exists:
            product_schema = ProductSchema()
            product_details = product_schema.dump(product_exists)
            return jsonify({"product_details":product_details,"category":product_exists.category.name}),200
        else:
            return jsonify({'error':"No such Product exists"}),404
    except Exception as e:
        print(e)
        db.session.rollback() 
        return jsonify({'error': ' error occurred'}), 500

@user_bp.get('/filter')
@jwt_required()
def filter_options():
    try:
        categories = Category.query.all()
        category_schema = CategorySchema(many=True,only=('id','name'))
        result = category_schema.dump(categories)
        max_price = Product.query.order_by(Product.price.desc()).first()
        min_price = Product.query.order_by(Product.price.asc()).first()
        return jsonify({'categories':result,'max_price':max_price.price,"min_price":min_price.price})
        
    except Exception as e:
        print(e)
        db.session.rollback() 
        return jsonify({'error': 'An error occurred while fetching information'}), 500
    
@user_bp.get('/cart')
@jwt_required()
def cart():
    try:
        cart = Cart.query.filter_by(user_id=current_user.id).all()
        cart_schema = CartSchema(many=True)
        cart_data = cart_schema.dump(cart)
        return jsonify({'cart_details':cart_data}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'something went wrong'}),500

@user_bp.patch('/cart/<int:id>/increment')
@jwt_required()
def cart_increment(id):
    try:
        cart = Cart.query.filter_by(id=id).first()
        if cart:
            cart.quantity+=1
            db.session.commit()
            return jsonify({'cart_count':cart.quantity}),200
        else:
            return jsonify({'error':'this item not in cart'}),404

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'something went wrong'}),500

@user_bp.patch('/cart/<int:id>/decrement')
@jwt_required()
def cart_decrement(id):
    try:
        cart = Cart.query.filter_by(id=id).first()
        if cart:
            if cart.quantity == 1:
                return jsonify({'error':"Invalid Operation"}),400
            cart.quantity-=1
            db.session.commit()
            return jsonify({'cart_count':cart.quantity}),200
        else:
            return jsonify({'error':'this item not in cart'}),404

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'something went wrong'}),500

@user_bp.delete('/cart/<int:id>/remove')
@jwt_required()
def cart_remove(id):
    try:
        cart = Cart.query.filter_by(id=id).first()
        if cart:
            db.session.delete(cart)
            db.session.commit()
            return jsonify({'message':"Successfully deleted"}),200
        else:
            return jsonify({'error':'this item not in cart'}),404

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'something went wrong'}),500
    
@user_bp.post('/place_order')
@jwt_required()
def place_order():
    try:
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()
        insufficient_stock = []
        for item in cart_items:
            available_stock = item.product.stock
            if item.quantity > available_stock:
                insufficient_stock.append({
                    'product_name':item.product.name,
                    'requested':item.quantity,
                    'available':available_stock
                })
        if insufficient_stock:
            return jsonify({'error':'Insufficient stock for some items','items':insufficient_stock}),400
        
        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order(user_id=current_user.id, total=total)
        db.session.add(order)

        for item in cart_items:
            order_detail = OrderDetail(
                product_id=item.product_id,
                product_name=item.product.name,
                product_price=item.product.price,
                quantity=item.quantity,
                order=order,
                product_uom = item.product.uom
            )
            item.product.stock -= item.quantity
            sale = Sale(product_id=item.product_id,stock_sold =item.quantity)
            db.session.add(order_detail)
            db.session.add(sale)
        for cart in current_user.carts:
            db.session.delete(cart)
        db.session.commit()
        result = send_order_email_task.delay(order.id,current_user.id,current_user.email)

        return jsonify({'message':'Order Placed Successfully','result':result.id}),200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({'error':'something went wrong'}),500
    
@user_bp.get('/orders')
@jwt_required()
def order():
    try:
        orders = Order.query.filter_by(user_id=current_user.id).all()
        order_schema = OrderSchema(many=True)
        cart_data = order_schema.dump(orders)
        return jsonify({'order_details':cart_data}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'something went wrong'}),500
    
@user_bp.get('/order/<int:id>')
@jwt_required()
def order_details(id):
    try:
        order_details = OrderDetail.query.filter_by(order_id = id).all()
        if order_details:
            order_details_schema = OrderDetailsSchema(many=True)
            order_details_data = order_details_schema.dump(order_details)
            return jsonify({'order_details':order_details_data}),200
        return jsonify({'error':"No Order details found"}),400
    except Exception as e:
        return jsonify({'error':'something went wrong'}),500
    
@user_bp.post('/product/<int:id>/comment')
@jwt_required()
def product_comment(id):
    try:
        product_exists = Product.query.filter_by(id= id).first()
        review_exists = Review.query.filter_by(username = current_user.username ,product_id=id).first()
        if product_exists and not(review_exists):
            comment = request.json.get('comment')
            rating = request.json.get('rating')
            review = Review(username=current_user.username,comment=comment,rating=rating,product_id = id)
            db.session.add(review)
            product_exists.ratings_count+=1
            product_exists.ratings_sum+=rating
            db.session.commit()
            return jsonify({'message':"added successfully"}),200
        return jsonify({'error':"Review already exists"}),400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'something went wrong'}),500
    
@user_bp.get('/product/<int:id>/reviews')
@jwt_required()
def product_reviews(id):
    try:
        review_exists = Review.query.filter_by(product_id=id).order_by(Review.rating.desc()).all()
        review_schema = ReviewSchema(many=True)
        review_details = review_schema.dump(review_exists)

        return jsonify({'review_details':review_details}),200
    except Exception as e:
        print(e)
        return jsonify({'error':'something went wrong'}),500
    
@user_bp.post('/apply')
@jwt_required()
def apply_post():
    try:
        request_exist = Request.query.filter_by(user_id = current_user.id).first()
        if request_exist and current_user.role == 'user':
            return jsonify({'error':"Request Already there"}),400
        elif request_exist and current_user.role == 'manager':
            return jsonify({'error':"You are Manager! Can't Request again "}),400
        new_request = Request(user_id = current_user.id,role="manager")
        db.session.add(new_request)
        db.session.commit()
        return jsonify({'message':"Request sent successfully"}),200

    except:
        db.session.rollback()
        return jsonify({'error':'something went wrong'}),500
@user_bp.get('/requests')
@jwt_required()
def get_requests():
    try:
       request_exist= current_user.requests
       request_schema = RequestSchema(many=True)
       request_details = request_schema.dump(request_exist)
       return jsonify({'request_details':request_details}),200

    except Exception as e:
        print(e)
        return jsonify({'error':'something went wrong'}),500
    
@user_bp.get('/about_me')
@jwt_required()
def about_me():
    try:
        about = current_user
        user_schema = UserSchema()
        user_details = user_schema.dump(about)
        return jsonify({"about":user_details})
    except Exception as e:
        print(e)
        return jsonify({'error':'something went wrong'}),500