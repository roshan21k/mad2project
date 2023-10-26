from .extensions import db
from datetime import datetime
from sqlalchemy.orm import column_property
# import pytz

# IST = pytz.timezone('Asia/Kolkata')


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False,unique=True)
    email = db.Column(db.String(50),nullable=False,unique=True)
    password = db.Column(db.Text(128),nullable=False)
    role = db.Column(db.Text(20),nullable=False,default='user')
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    carts = db.relationship('Cart',backref='user')
    orders = db.relationship('Order',backref='user')
    requests = db.relationship('Request',backref='user')
    category_requests = db.relationship('CategoryRequest',backref='user')
    product_requests = db.relationship('ProductRequest',backref='user')
    def __repr__(self):
        return  f"<User {self.username}>"

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    quantity = db.Column(db.Integer,nullable=False,default=1)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'))
    product = db.relationship('Product',backref='cart',uselist=False)
    added_on = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    def __repr__(self):
        return f'<Cart:{self.id}>'
      
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),nullable=False)
    products = db.relationship('Product', backref='category',cascade='all, delete-orphan')
    product_requests = db.relationship('ProductRequest',backref='category')
    def __repr__(self):
        return f'<Category:{self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False,unique=True)
    price = db.Column(db.Float,nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id',ondelete='CASCADE'))
    stock = db.Column(db.Integer,default=5)
    ratings_sum = db.Column(db.Integer,default=0)
    ratings_count = db.Column(db.Integer,default = 0)
    uom = db.Column(db.String(),nullable=False)
    description = db.Column(db.String(256),nullable=True,default="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
    ratings_average = column_property(ratings_sum/ratings_count)
    product_requests = db.relationship('ProductRequest',backref='product')
    sales = db.relationship('Sale',backref='product')

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    stock_sold = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False)
    comment = db.Column(db.String(100),nullable=False)
    rating = db.Column(db.Float,nullable=False)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'),nullable = False)

class Request(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    role = db.Column(db.String(20),nullable=False)
    status = db.Column(db.String(20),nullable=False,default="pending")
    
class CategoryRequest(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    action = db.Column(db.String(20),nullable=False)
    name = db.Column(db.String(20),nullable=False)
    status = db.Column(db.String(20),nullable=False,default="pending")
    old_name = db.Column(db.String(20),nullable=True)
    category_id = db.Column(db.Integer,nullable=True)
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'))

class ProductRequest(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    action = db.Column(db.String(20),nullable=False)
    status = db.Column(db.String(20),nullable=False,default="pending")
    new_name = db.Column(db.String(20),nullable=True)
    new_desc = db.Column(db.String(250),nullable=True)
    new_price = db.Column(db.Integer,nullable=True)
    new_uom = db.Column(db.String(20),nullable= True)
    new_stock = db.Column(db.Integer,nullable=True)
    product_id = db.Column(db.Integer,db.ForeignKey('product.id'),nullable=True)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    total = db.Column(db.Float,nullable=False)
    order_details = db.relationship('OrderDetail',backref='order')
    ordered_on = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer,nullable=False)
    product_name = db.Column(db.String(50),nullable=False)
    product_price = db.Column(db.Float,nullable=False)
    product_uom = db.Column(db.String(20),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'))

    

    def __repr__(self):
        return f'<Product:{self.id}>'