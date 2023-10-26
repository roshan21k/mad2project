from celery import shared_task
from flask import request,render_template,jsonify,make_response
from flask_mail import Message
from io import StringIO
import csv
from datetime import datetime,timedelta,time
from .extensions import mail
from .models import Order,OrderDetail,User,Product
import pdfkit

# ---------------Some Message Templates for email---------------

product_csv_message = """
Dear Manager,

Attached is your CSV file containing product details for your reference.

Please let us know if you need any further assistance or have any questions regarding the data.

Thank you for using our service.

Best regards,
Grocery Store
"""
user_monthly_report_message = """
Dear {username},

Attached is your monthly report for the month of {current_month} {current_year}. This email serves as a notification that your report is ready.

For the detailed report, please open the attached PDF file. It contains comprehensive information about your orders for the past month.

If you have any questions or need further assistance, feel free to reach out to us. We're here to help.

Thank you for your continued partnership.

Best regards,
Grocery Store
"""
user_remainder_message = """
Hey, 

It looks like your cart is empty Or you havent placed any order yet . 

We have some great products waiting for you. Visit our website and start shopping!"""

#---------------Some Message Templates for email---------------

# CELERY WORKER AND BEAT TASKS

# send order details email (celery worker)
@shared_task()
def send_order_email_task(order_id,user_id,recipient):
    subject = 'Order Details!'
    try:
        is_user_order = Order.query.filter_by(id=order_id,user_id = user_id).first()
        if is_user_order:
            order_details = OrderDetail.query.filter_by(order_id = order_id).all()
            
            html_content = render_template("user_order.html",order_details = order_details)
            # pdf = pdfkit.from_string(html_content, False,configuration=pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf'))
            msg = Message(subject, sender='k.roshan21k@gmail.com',recipients=[recipient])
            msg.html = html_content
            # msg.attach('Order Details.pdf','application/pdf',pdf)
            mail.send(msg)
            return jsonify({"Message":"Email sent successfully!"}),202
        else:
            return jsonify({"error":"You dont Have access!"}),400
    except Exception as e:
        return f"An error occurred: {str(e)}",500

# send monthly report (celery Beat)
@shared_task()
def send_user_monthly_report_task():
    try:
        current_date = datetime.utcnow()
        first_day_of_current_month = current_date.replace(day=1)
        end_of_previous_month = first_day_of_current_month - timedelta(days=1)
        

        start_date = end_of_previous_month.replace(day=1)
        end_date = end_of_previous_month

        users = User.query.filter((User.role=="user") | (User.role=="manager")).all()
        for user in users:
            previous_month_orders = Order.query.filter(
                Order.user_id == user.id,
                Order.ordered_on >= start_date,
                Order.ordered_on <= end_date
            ).all()

            if previous_month_orders:
                subject = "Your Monthly Order Report"
                msg = Message(
                    subject,sender='k.roshan21k@gmail.com',
                    recipients=[user.email]
                )

                current_month = start_date.strftime('%B')
                current_year = start_date.year
                html_content = render_template("user_report.html", orders=previous_month_orders, user=user,
                                               current_month=current_month, current_year=current_year)
                pdf = pdfkit.from_string(html_content, False,configuration=pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf'))
                msg.attach('Monthly report.pdf','application/pdf',pdf)
                msg.body = user_monthly_report_message.format(username=user.username,current_month=current_month,current_year = current_year)
                mail.send(msg)

        return jsonify({'Message':'Email Sent Successfully'}),202
    
    except Exception as e:
        print(f"Error sending email: {str(e)}"),500

# User triggered Asynchronous Task (Celery Worker)
@shared_task
def manager_product_report_task(email):
    try:
        output = StringIO()
        csv_writer = csv.DictWriter(output, fieldnames=['Product Name', 'Remaining Stock', 'Sold Stock','Description', 'Price'])
        csv_writer.writeheader()
        products = Product.query.all()
        if products:
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

            msg = Message('Product Export Report',sender='k.roshan21k@gmail.com',  recipients=[email])
            msg.body = product_csv_message
            
            msg.attach('products.csv', 'text/csv', csv_data)

            mail.send(msg)
            return 'Email sent with the CSV file attached.'
    except Exception as e:
        return jsonify({'error':'Something went wrong'}),500
    
# Send notification if user didnt buy anything or no items in cart for 24 hours
@shared_task()
def send_visit_email_task():
    users = User.query.filter_by(role="user").all()
    previous_day = datetime.now() - timedelta(days=1)
    subject = "Your Cart Deserves Some Love ❤️"
    if users:
        recipients = [user.email for user in users if not user.carts and not Order.query.filter_by(user_id=user.id).filter(Order.ordered_on > previous_day).first()]
        if recipients:
            msg = Message(subject, sender='k.roshan21k@gmail.com', recipients=recipients)
            msg.body = user_remainder_message
            mail.send(msg)
            return "Mail sent Successfully"
        return "No one to send"
    return "No users Found"