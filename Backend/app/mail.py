from flask import Flask, request, render_template,Blueprint,jsonify,make_response
from flask_mail import Message
from .extensions import mail,db
from .models import Order,OrderDetail,Product,User
from flask_jwt_extended import jwt_required,current_user
from .task import *
import csv
from io import StringIO
from datetime import datetime,timedelta,time


mail_bp = Blueprint('mail_bp',__name__)


@mail_bp.get('/send_orders/<int:id>')
@jwt_required()
def send_order_email(id):

    recipient = current_user.email
    order_id = id
    user_id = current_user.id
    result = send_order_email_task.delay(order_id,user_id,recipient)
    return jsonify({"message": "Email will be sent asynchronously!", "task_id": result.id}), 202


@mail_bp.get('/report')
def get_report():
    output = StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=['Product Name', 'Remaining Stock', 'Sold Stock','Description', 'Price'])
    csv_writer.writeheader()
    products = Product.query.all()
    for product in products:
        csv_writer.writerow({
        'Product Name': product.name,
        'Remaining Stock': product.stock,
        'Sold Stock':sum(sale.stock_sold for sale in product.sales) if product.sales else 0,
        'Description': product.description,
        'Price': product.price,
    })
    csv_data = output.getvalue()
    output.close()

    response = make_response(csv_data)
    response.headers["Content-Disposition"] = "attachment; filename=products.csv"
    response.headers["Content-Type"] = "text/csv"


    response.status_code = 200

    return response


