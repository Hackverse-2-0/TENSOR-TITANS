"""Authentication API routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, UserRole
from api.auth import AuthService, role_required, log_user_action
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request body:
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "securepassword",
        "role": "shop_manager",
        "shop_id": 1
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', UserRole.SHOP_MANAGER.value)
        shop_id = data.get('shop_id')
        
        # Validate role
        valid_roles = [r.value for r in UserRole]
        if role not in valid_roles:
            return jsonify({'error': f'Invalid role. Must be one of: {valid_roles}'}), 400
        
        result, status_code = AuthService.register_user(
            username=username,
            email=email,
            password=password,
            role=role,
            shop_id=shop_id
        )
        
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and get JWT token
    
    Request body:
    {
        "username": "john_doe",
        "password": "securepassword"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
        
        result, status_code = AuthService.login(username, password)
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user and invalidate JWT token
    """
    try:
        user_id = get_jwt_identity()
        log_user_action(user_id, 'logout', 'User logged out')
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user information"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'shop_id': user.shop_id,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching current user: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users/<int:user_id>', methods=['GET'])
@role_required(UserRole.ADMIN.value)
def get_user(user_id):
    """Get user details (admin only)"""
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'shop_id': user.shop_id,
                'is_active': user.is_active,
                'created_at': user.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users', methods=['GET'])
@role_required(UserRole.ADMIN.value)
def list_users():
    """List all users (admin only)
    
    Query parameters:
    - limit: Number of users to return (default: 50)
    - offset: Pagination offset (default: 0)
    - role: Filter by role
    """
    try:
        query = User.query
        
        role = request.args.get('role')
        if role:
            query = query.filter_by(role=role)
        
        limit = min(int(request.args.get('limit', 50)), 500)
        offset = int(request.args.get('offset', 0))
        
        total = query.count()
        users = query.limit(limit).offset(offset).all()
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'users': [{
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'role': u.role,
                'shop_id': u.shop_id,
                'is_active': u.is_active,
                'created_at': u.created_at.isoformat()
            } for u in users]
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users/<int:user_id>/deactivate', methods=['POST'])
@role_required(UserRole.ADMIN.value)
def deactivate_user(user_id):
    """Deactivate a user account (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        
        if current_user_id == user_id:
            return jsonify({'error': 'Cannot deactivate your own account'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        user.is_active = False
        db.session.commit()
        
        log_user_action(
            current_user_id,
            'DEACTIVATE_USER',
            'user',
            user_id
        )
        
        return jsonify({
            'success': True,
            'message': f'User {user.username} deactivated'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deactivating user: {e}")
        return jsonify({'error': str(e)}), 500
