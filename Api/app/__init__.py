from flask import Flask
from datetime import timedelta
import redis
from .auth import auth_bp
from .admin import admin_bp
from .user import user_bp
from .mail import mail_bp
from .manager import manager_bp
from .extensions import db,jwt,cors,mail,cache
from .models import User
from .initial import insert_default_data,create_admin
from .workers import celery_init_app
import os
from .config import Config

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            result_backend="redis://localhost:6379/0",
            task_ignore_result=True,
        ),
    )
    jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
    )
    app.config.from_object(Config)
    db.init_app(app)
    celery_init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    cache.init_app(app)


    with app.app_context():
        # db.drop_all()
        db.create_all()
        create_admin()
        insert_default_data()

    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(user_bp,url_prefix='/user')
    app.register_blueprint(manager_bp,url_prefix='/manager')
    app.register_blueprint(mail_bp,url_prefix='/')
    
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
         user = User.query.filter_by(username=identity).first()
         return {"role":user.role}
    
    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_headers,jwt_data):
        identity = jwt_data['sub']
        return User.query.filter_by(username=identity).one_or_none()
    
    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
        jti = jwt_payload["jti"]
        token_in_redis = jwt_redis_blocklist.get(jti)
        return token_in_redis is not None
    return app
