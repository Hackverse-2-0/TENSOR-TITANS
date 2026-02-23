"""Shop management API routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Shop, User, UserRole, Stock, BiometricLog, DeliverySchedule
from api.auth import role_required, log_user_action
from sqlalchemy import desc
import logging

logger = logging.getLogger(__name__)

shop_bp = Blueprint('shop', __name__, url_prefix='/api/v1/shops')

@shop_bp.route('', methods=['POST'])
@role_required(UserRole.ADMIN.value)
def create_shop():
    """
    Create a new shop
    
    Request body:
    {
        "shop_code": "SHOP001",
        "shop_name": "Central Distribution Shop",
        "location": "Mumbai, MH",
        "latitude": 19.0760,
        "longitude": 72.8777
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['shop_code', 'shop_name', 'location']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Check if shop code already exists
        if Shop.query.filter_by(shop_code=data['shop_code']).first():
            return jsonify({'error': 'Shop code already exists'}), 400
        
        shop = Shop(
            shop_code=data['shop_code'],
            shop_name=data['shop_name'],
            location=data['location'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        
        db.session.add(shop)
        db.session.commit()
        
        log_user_action(
            user_id,
            'CREATE_SHOP',
            'shop',
            shop.id,
            {'shop_code': shop.shop_code, 'shop_name': shop.shop_name}
        )
        
        return jsonify({
            'success': True,
            'message': 'Shop created successfully',
            'shop': {
                'id': shop.id,
                'shop_code': shop.shop_code,
                'shop_name': shop.shop_name,
                'location': shop.location
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating shop: {e}")
        return jsonify({'error': str(e)}), 500

@shop_bp.route('', methods=['GET'])
@jwt_required()
def list_shops():
    """
    List all shops
    
    Query parameters:
    - limit: Number of shops to return (default: 50)
    - offset: Pagination offset (default: 0)
    """
    try:
        limit = min(int(request.args.get('limit', 50)), 500)
        offset = int(request.args.get('offset', 0))
        
        total = Shop.query.count()
        shops = Shop.query.order_by(
            desc(Shop.created_at)
        ).limit(limit).offset(offset).all()
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'shops': [{
                'id': s.id,
                'shop_code': s.shop_code,
                'shop_name': s.shop_name,
                'location': s.location,
                'latitude': s.latitude,
                'longitude': s.longitude,
                'created_at': s.created_at.isoformat()
            } for s in shops]
        }), 200
        
    except Exception as e:
        logger.error(f"Error listing shops: {e}")
        return jsonify({'error': str(e)}), 500

@shop_bp.route('/<int:shop_id>', methods=['GET'])
@jwt_required()
def get_shop(shop_id):
    """Get shop details"""
    try:
        shop = Shop.query.get(shop_id)
        
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404
        
        # Get statistics
        stock_records = Stock.query.filter_by(shop_id=shop_id).count()
        biometric_records = BiometricLog.query.filter_by(shop_id=shop_id).count()
        delivery_records = DeliverySchedule.query.filter_by(shop_id=shop_id).count()
        managers = User.query.filter_by(
            shop_id=shop_id,
            role=UserRole.SHOP_MANAGER.value
        ).count()
        
        return jsonify({
            'success': True,
            'shop': {
                'id': shop.id,
                'shop_code': shop.shop_code,
                'shop_name': shop.shop_name,
                'location': shop.location,
                'latitude': shop.latitude,
                'longitude': shop.longitude,
                'created_at': shop.created_at.isoformat(),
                'updated_at': shop.updated_at.isoformat()
            },
            'statistics': {
                'stock_records': stock_records,
                'biometric_records': biometric_records,
                'delivery_records': delivery_records,
                'shop_managers': managers
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching shop {shop_id}: {e}")
        return jsonify({'error': str(e)}), 500

@shop_bp.route('/<int:shop_id>', methods=['PUT'])
@role_required(UserRole.ADMIN.value)
def update_shop(shop_id):
    """Update shop details"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404
        
        # Update fields
        if 'shop_name' in data:
            shop.shop_name = data['shop_name']
        if 'location' in data:
            shop.location = data['location']
        if 'latitude' in data:
            shop.latitude = data['latitude']
        if 'longitude' in data:
            shop.longitude = data['longitude']
        
        db.session.commit()
        
        log_user_action(
            user_id,
            'UPDATE_SHOP',
            'shop',
            shop.id,
            data
        )
        
        return jsonify({
            'success': True,
            'message': 'Shop updated successfully',
            'shop': {
                'id': shop.id,
                'shop_code': shop.shop_code,
                'shop_name': shop.shop_name,
                'location': shop.location
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating shop {shop_id}: {e}")
        return jsonify({'error': str(e)}), 500

@shop_bp.route('/<int:shop_id>', methods=['DELETE'])
@role_required(UserRole.ADMIN.value)
def delete_shop(shop_id):
    """Delete a shop (admin only)"""
    try:
        user_id = get_jwt_identity()
        
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404
        
        shop_code = shop.shop_code
        
        db.session.delete(shop)
        db.session.commit()
        
        log_user_action(
            user_id,
            'DELETE_SHOP',
            'shop',
            shop_id,
            {'shop_code': shop_code}
        )
        
        return jsonify({
            'success': True,
            'message': f'Shop {shop_code} deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting shop {shop_id}: {e}")
        return jsonify({'error': str(e)}), 500

@shop_bp.route('/<int:shop_id>/stats', methods=['GET'])
@jwt_required()
def get_shop_stats(shop_id):
    """Get shop statistics and data summary"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Shop managers can only view their own shop stats
        if user.role == UserRole.SHOP_MANAGER.value and user.shop_id != shop_id:
            return jsonify({'error': 'Unauthorized access to this shop'}), 403
        
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404
        
        # Get latest data
        latest_stock = Stock.query.filter_by(shop_id=shop_id)\
            .order_by(desc(Stock.recorded_at)).first()
        
        latest_biometric = BiometricLog.query.filter_by(shop_id=shop_id)\
            .order_by(desc(BiometricLog.recorded_at)).first()
        
        latest_delivery = DeliverySchedule.query.filter_by(shop_id=shop_id)\
            .order_by(desc(DeliverySchedule.recorded_at)).first()
        
        return jsonify({
            'success': True,
            'shop_id': shop_id,
            'shop_name': shop.shop_name,
            'data_summary': {
                'total_stock_records': Stock.query.filter_by(shop_id=shop_id).count(),
                'total_biometric_records': BiometricLog.query.filter_by(shop_id=shop_id).count(),
                'total_delivery_records': DeliverySchedule.query.filter_by(shop_id=shop_id).count(),
                'last_stock_update': latest_stock.recorded_at.isoformat() if latest_stock else None,
                'last_biometric_update': latest_biometric.recorded_at.isoformat() if latest_biometric else None,
                'last_delivery_update': latest_delivery.recorded_at.isoformat() if latest_delivery else None
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching shop stats for {shop_id}: {e}")
        return jsonify({'error': str(e)}), 500
