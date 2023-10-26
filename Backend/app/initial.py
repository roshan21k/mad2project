from .extensions import db
from .models import Category, Product,User
from werkzeug.security import generate_password_hash
import os

# Create Admin when Database is Created
def create_admin():
    user_name = os.getenv("USER_NAME")
    user_email = os.getenv("USER_EMAIL")
    user_password = os.getenv("USER_PASSWORD")

    user_exists = User.query.filter_by(username=user_name).first()
    if not user_exists:
        new_user = User(username=user_name,email=user_email,password=generate_password_hash(user_password),role="admin")
        db.session.add(new_user)
        db.session.commit()


# Insert Some default data to work with
def insert_default_data():

    if Category.query.all():
        return
    fruits = Category(name='Fruits')
    vegetables = Category(name='Vegetables')
    dairy = Category(name='Dairy and Eggs')
    bakery = Category(name='Bakery')


    apple = Product(name='Apples', price=120.0, category=fruits, uom='kg')
    banana = Product(name='Bananas', price=50.0, category=fruits, uom='kg',ratings_sum=92,ratings_count=20)
    orange = Product(name='Oranges', price=80.0, category=fruits, uom='kg',ratings_sum=78,ratings_count=20)
    grapes = Product(name='Grapes', price=150.0, category=fruits, uom='kg')
    strawberries = Product(name='Strawberries', price=200.0, category=fruits, uom='pack')

    tomatoes = Product(name='Tomatoes', price=100.0, category=vegetables, uom='kg',ratings_sum=63,ratings_count=20)
    cucumbers = Product(name='Cucumbers', price=50.0, category=vegetables, uom='kg',ratings_sum=69,ratings_count=20)
    carrots = Product(name='Carrots', price=40.0, category=vegetables, uom='kg',ratings_sum=72,ratings_count=20)
    spinach = Product(name='Spinach', price=120.0, category=vegetables, uom='pack',ratings_sum=88,ratings_count=20)
    bell_peppers = Product(name='Bell Peppers', price=160.0, category=vegetables, uom='kg',ratings_sum=95,ratings_count=20)


    milk = Product(name='Milk', price=80.0, category=dairy, uom='liter')
    eggs = Product(name='Eggs', price=100.0, category=dairy, uom='dozen')
    cheese = Product(name='Cheese', price=160.0, category=dairy, uom='pack',ratings_sum=85,ratings_count=20)
    yogurt = Product(name='Yogurt', price=50.0, category=dairy, uom='pack')
    butter = Product(name='Butter', price=120.0, category=dairy, uom='pack',ratings_sum=98,ratings_count=20)


    bread = Product(name='Bread', price=150.0, category=bakery, uom='loaf',ratings_sum=66,ratings_count=20)
    bagels = Product(name='Bagels', price=240.0, category=bakery, uom='pack',ratings_sum=65,ratings_count=20)
    croissants = Product(name='Croissants', price=120.0, category=bakery, uom='pack',ratings_sum=88,ratings_count=20)
    muffins = Product(name='Muffins', price=140.0, category=bakery, uom='pack',ratings_sum=66,ratings_count=20)
    donuts = Product(name='Donuts', price=60.0, category=bakery, uom='each',ratings_sum=88,ratings_count=20)


    db.session.add_all([
        fruits, vegetables, dairy, bakery,
        apple, banana, orange, grapes, strawberries,
        tomatoes, cucumbers, carrots, spinach, bell_peppers,
        milk, eggs, cheese, yogurt, butter,
        bread, bagels, croissants, muffins, donuts,
    ])

    # Commit the changes to the database
    db.session.commit()
