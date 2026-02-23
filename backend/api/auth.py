"""Authentication and authorization"""
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, UserRole, AuditLog
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash a password"""
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(password, password_hash):
    """Verify a password"""
    return check_password_hash(password_hash, password)

def role_required(*allowed_roles):
    """Decorator for role-based access control"""
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user or not user.is_active:
                return jsonify({'error': 'User not found or inactive'}), 401
            
            if user.role not in allowed_roles:
                log_access_denial(user_id, request.path, 'UNAUTHORIZED_ROLE')
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def log_access_denial(user_id, path, reason):
    """Log unauthorized access attempts"""
    try:
        log = AuditLog(
            user_id=user_id,
            action='ACCESS_DENIED',
            resource_type='api_endpoint',
            ip_address=request.remote_addr,
            changes={'reason': reason, 'path': path}
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error logging access denial: {e}")

def log_user_action(user_id, action, resource_type, resource_id=None, changes=None):
    """Log user actions for audit trail"""
    try:
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=request.remote_addr,
            changes=changes
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        logger.error(f"Error logging user action: {e}")

class AuthService:
    """Authentication service"""
    
    @staticmethod
    def register_user(username, email, password, role=UserRole.SHOP_MANAGER, shop_id=None):
        """Register a new user"""
        try:
            if User.query.filter_by(username=username).first():
                return {'success': False, 'error': 'Username already exists'}, 400
            
            if User.query.filter_by(email=email).first():
                return {'success': False, 'error': 'Email already exists'}, 400
            
            user = User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                role=role if isinstance(role, str) else role.value,
                shop_id=shop_id
            )
            
            db.session.add(user)
            db.session.commit()

            return {
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'shop_id': user.shop_id,
                    'is_active': user.is_active,
                    'created_at': user.created_at.isoformat()
                },
                'message': 'User registered successfully'
            }, 201
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error registering user: {e}")
            return {'success': False, 'error': str(e)}, 500
    
    @staticmethod
    def login(username, password):
        """Authenticate user and return JWT token"""
        try:
            user = User.query.filter_by(username=username).first()
            
            if not user or not verify_password(password, user.password_hash):
                return {'success': False, 'error': 'Invalid credentials'}, 401
            
            if not user.is_active:
                return {'success': False, 'error': 'User account is inactive'}, 403
            
            # Ensure identity is a string to satisfy JWT subject requirements
            access_token = create_access_token(identity=str(user.id))
            
            log_user_action(user.id, 'LOGIN', 'authentication')
            
            return {
                'success': True,
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'shop_id': user.shop_id
                }
            }, 200
            
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return {'success': False, 'error': str(e)}, 500
