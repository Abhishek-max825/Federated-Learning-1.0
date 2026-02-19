from functools import wraps
from flask import abort
from flask_login import current_user
from app.models import Role

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'Admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'Doctor':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def hospital_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name != 'Hospital Node':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
