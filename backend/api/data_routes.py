"""Data ingestion API routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, UserRole
from pipelines.data_pipeline import StockPipeline, BiometricPipeline, DeliveryPipeline
from api.auth import role_required, log_user_action
import logging

logger = logging.getLogger(__name__)

data_bp = Blueprint('data', __name__, url_prefix='/api/v1/data')

@data_bp.route('/ingest/stock', methods=['POST'])
@role_required(UserRole.ADMIN.value, UserRole.DISTRIBUTION_CENTER.value)
def ingest_stock_data():
    """
    Ingest shop-wise stock data
    
    Request body:
    {
        "shop_id": 1,
        "stocks": [
            {
                "item_code": "RICE001",
                "item_name": "Rice 10kg",
                "quantity_received": 100,
                "quantity_sold": 45,
                "quantity_remaining": 55,
                "expected_quantity": 60
            }
        ]
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        shop_id = data.get('shop_id')
        stocks = data.get('stocks', [])
        
        if not shop_id or not stocks:
            return jsonify({'error': 'Missing shop_id or stocks'}), 400
        
        success, failed, errors = StockPipeline.ingest_stock_data(shop_id, stocks)
        
        log_user_action(
            user_id,
            'INGEST_STOCK_DATA',
            'stock',
            changes={'shop_id': shop_id, 'records': success}
        )
        
        return jsonify({
            'success': True,
            'message': f'Ingested {success} stock records',
            'success_count': success,
            'failed_count': failed,
            'errors': errors[:10]  # Return first 10 errors
        }), 200
        
    except Exception as e:
        logger.error(f"Error ingesting stock data: {e}")
        return jsonify({'error': str(e)}), 500

@data_bp.route('/ingest/biometric', methods=['POST'])
@role_required(UserRole.ADMIN.value, UserRole.SHOP_MANAGER.value)
def ingest_biometric_logs():
    """
    Ingest biometric attendance logs
    
    Request body:
    {
        "shop_id": 1,
        "biometric_logs": [
            {
                "employee_id": "EMP001",
                "employee_name": "John Doe",
                "check_in_time": "2026-02-17T08:30:00",
                "check_out_time": "2026-02-17T16:30:00",
                "status": "present"
            }
        ]
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        shop_id = data.get('shop_id')
        logs = data.get('biometric_logs', [])
        
        if not shop_id or not logs:
            return jsonify({'error': 'Missing shop_id or biometric_logs'}), 400
        
        success, failed, errors = BiometricPipeline.ingest_biometric_logs(shop_id, logs)
        
        log_user_action(
            user_id,
            'INGEST_BIOMETRIC_LOGS',
            'biometric_log',
            changes={'shop_id': shop_id, 'records': success}
        )
        
        return jsonify({
            'success': True,
            'message': f'Ingested {success} biometric records',
            'success_count': success,
            'failed_count': failed,
            'errors': errors[:10]
        }), 200
        
    except Exception as e:
        logger.error(f"Error ingesting biometric logs: {e}")
        return jsonify({'error': str(e)}), 500

@data_bp.route('/ingest/delivery', methods=['POST'])
@role_required(UserRole.ADMIN.value, UserRole.DISTRIBUTION_CENTER.value)
def ingest_delivery_schedules():
    """
    Ingest delivery schedule data
    
    Request body:
    {
        "shop_id": 1,
        "deliveries": [
            {
                "delivery_id": "DEL001",
                "item_code": "RICE001",
                "item_name": "Rice 10kg",
                "scheduled_quantity": 100,
                "scheduled_date": "2026-02-17T09:00:00",
                "delivered_quantity": 100,
                "actual_delivery_date": "2026-02-17T09:30:00",
                "status": "delivered"
            }
        ]
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        shop_id = data.get('shop_id')
        deliveries = data.get('deliveries', [])
        
        if not shop_id or not deliveries:
            return jsonify({'error': 'Missing shop_id or deliveries'}), 400
        
        success, failed, errors = DeliveryPipeline.ingest_delivery_schedules(shop_id, deliveries)
        
        log_user_action(
            user_id,
            'INGEST_DELIVERY_SCHEDULES',
            'delivery_schedule',
            changes={'shop_id': shop_id, 'records': success}
        )
        
        return jsonify({
            'success': True,
            'message': f'Ingested {success} delivery records',
            'success_count': success,
            'failed_count': failed,
            'errors': errors[:10]
        }), 200
        
    except Exception as e:
        logger.error(f"Error ingesting delivery schedules: {e}")
        return jsonify({'error': str(e)}), 500
@data_bp.route('/recent', methods=['GET'])
@jwt_required()
def get_recent_ingestions():
    """
    Get recent ingestions (last 10 of each type)
    """
    try:
        from models import Stock, BiometricLog, DeliverySchedule
        
        # Get recent stock data
        stocks = Stock.query.order_by(Stock.recorded_at.desc()).limit(10).all()
        stock_data = [{
            'id': s.id,
            'shop_id': s.shop_id,
            'item_code': s.item_code,
            'item_name': s.item_name,
            'quantity_received': s.quantity_received,
            'quantity_sold': s.quantity_sold,
            'quantity_remaining': s.quantity_remaining,
            'expected_quantity': s.expected_quantity,
            'recorded_at': s.recorded_at.isoformat()
        } for s in stocks]
        
        # Get recent biometric logs
        biometric = BiometricLog.query.order_by(BiometricLog.recorded_at.desc()).limit(10).all()
        biometric_data = [{
            'id': b.id,
            'shop_id': b.shop_id,
            'employee_id': b.employee_id,
            'employee_name': b.employee_name,
            'check_in_time': b.check_in_time.isoformat(),
            'check_out_time': b.check_out_time.isoformat() if b.check_out_time else None,
            'status': b.status,
            'recorded_at': b.recorded_at.isoformat()
        } for b in biometric]
        
        # Get recent delivery schedules
        deliveries = DeliverySchedule.query.order_by(DeliverySchedule.recorded_at.desc()).limit(10).all()
        delivery_data = [{
            'id': d.id,
            'shop_id': d.shop_id,
            'delivery_id': d.delivery_id,
            'item_code': d.item_code,
            'item_name': d.item_name,
            'scheduled_quantity': d.scheduled_quantity,
            'delivered_quantity': d.delivered_quantity,
            'scheduled_date': d.scheduled_date.isoformat(),
            'actual_delivery_date': d.actual_delivery_date.isoformat() if d.actual_delivery_date else None,
            'status': d.status,
            'recorded_at': d.recorded_at.isoformat()
        } for d in deliveries]
        
        return jsonify({
            'success': True,
            'stocks': stock_data,
            'biometric_logs': biometric_data,
            'deliveries': delivery_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching recent ingestions: {e}")
        return jsonify({'error': str(e)}), 500