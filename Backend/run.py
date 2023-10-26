from app import create_app
from app.extensions import db
from app.initial import insert_default_data,create_admin

app = create_app()
# with app.app_context():
#     # db.init_app(app)
#     # db.drop_all()
#     db.create_all()
#     create_admin()
#     insert_default_data()
    
if __name__ == '__main__':
    app.run()