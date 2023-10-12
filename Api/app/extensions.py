from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

#creating instances
db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()