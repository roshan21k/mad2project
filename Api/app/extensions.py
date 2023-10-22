from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache
#creating instances
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
mail = Mail()
cache = Cache()