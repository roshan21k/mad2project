from flask_jwt_extended import get_jwt,verify_jwt_in_request
from functools import wraps
from flask import jsonify

# custom decorator for ADMIN
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == 'admin':
                return fn(*args, **kwargs)
            else:
                return jsonify({"Message":"Only Admins Have access"}), 403

        return decorator

    return wrapper

# custom decorator for Manager
def manager_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] == 'manager':
                return fn(*args, **kwargs)
            else:
                return jsonify({"Message":"Only Manager Have access"}), 403

        return decorator

    return wrapper