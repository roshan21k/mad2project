from flask import Flask,jsonify
from datetime import timedelta
from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp
from .manager import manager_bp
from .extensions import db,jwt,cors
from .models import User,Product
from .initial import insert_default_data,create_admin

def create_app():
    app = Flask(__name__)
    app.config.from_prefixed_env()
    # app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) 
    
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()
        create_admin()
        insert_default_data()

    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(user_bp,url_prefix='/user')
    app.register_blueprint(manager_bp,url_prefix='/manager')
    
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
         user = User.query.filter_by(username=identity).first()
         return {"role":user.role}
    
    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_headers,jwt_data):
        identity = jwt_data['sub']

        return User.query.filter_by(username=identity).one_or_none()

    return app

