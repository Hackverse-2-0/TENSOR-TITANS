"""Anomaly detection API routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Shop, AnomalyDetection, UserRole
from api.auth import role_required, log_user_action
from sqlalchemy import desc
import logging

logger = logging.getLogger(__name__)

anomaly_bp = Blueprint('anomaly', __name__, url_prefix='/api/v1/anomalies')

@anomaly_bp.route('/detect/<int:shop_id>', methods=['POST'])
@role_required(UserRole.ADMIN.value, UserRole.ANALYST.value, UserRole.DISTRIBUTION_CENTER.value)
def detect_anomalies(shop_id):
    """
    Run anomaly detection for a specific shop
    
    Returns detected anomalies across stock, attendance, and delivery
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Shop managers can only analyze their own shop
        if user.role == UserRole.SHOP_MANAGER.value and user.shop_id != shop_id:
            return jsonify({'error': 'Unauthorized access to this shop'}), 403
        
        # Verify shop exists
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404
        
        # Import the ML model lazily to avoid heavy ML dependency imports at app startup
        from ml_models.anomaly_detector import AnomalyDetectionModel

        detector = AnomalyDetectionModel()
        results = detector.run_full_detection(shop_id)
        
        log_user_action(
            user_id,
            'RUN_ANOMALY_DETECTION',
            'shop',
            shop_id,
            {
                'stock_discrepancies': len(results['stock_discrepancies']),
                'suspicious_attendance': len(results['suspicious_attendance']),
                'delivery_anomalies': len(results['delivery_anomalies'])
            }
        )
        
        total_anomalies = sum(len(v) for v in results.values())
        
        return jsonify({
            'success': True,
            'shop_id': shop_id,
            'total_anomalies': total_anomalies,
            'stock_discrepancies': results['stock_discrepancies'],
            'suspicious_attendance': results['suspicious_attendance'],
            'delivery_anomalies': results['delivery_anomalies']
        }), 200
        
    except Exception as e:
        logger.error(f"Error detecting anomalies for shop {shop_id}: {e}")
        return jsonify({'error': str(e)}), 500

@anomaly_bp.route('/<int:shop_id>', methods=['GET'])
@role_required(
    UserRole.ADMIN.value,
    UserRole.ANALYST.value,
    UserRole.SHOP_MANAGER.value,
    UserRole.DISTRIBUTION_CENTER.value
)
def get_anomalies(shop_id):
    """
    Get recent anomalies for a shop
    
    Query parameters:
    - severity: Filter by severity (low, medium, high, critical)
    - anomaly_type: Filter by type (stock_discrepancy, suspicious_activity, delivery_delay)
    - status: Filter by status (open, investigating, resolved)
    - limit: Number of records to return (default: 50)
    - offset: Pagination offset (default: 0)
    """
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        # Shop managers can only view their own shop
        if user.role == UserRole.SHOP_MANAGER.value and user.shop_id != shop_id:
            return jsonify({'error': 'Unauthorized access to this shop'}), 403
        
        # Verify shop exists
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404
        
        # Build query
        query = AnomalyDetection.query.filter_by(shop_id=shop_id)
        
        severity = request.args.get('severity')
        if severity:
            query = query.filter_by(severity=severity)
        
        anomaly_type = request.args.get('anomaly_type')
        if anomaly_type:
            query = query.filter_by(anomaly_type=anomaly_type)
        
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)
        
        limit = min(int(request.args.get('limit', 50)), 500)
        offset = int(request.args.get('offset', 0))
        
        total = query.count()
        anomalies = query.order_by(
            desc(AnomalyDetection.detected_at)
        ).limit(limit).offset(offset).all()
        
        return jsonify({
            'success': True,
            'shop_id': shop_id,
            'total': total,
            'limit': limit,
            'offset': offset,
            'anomalies': [{
                'id': a.id,
                'anomaly_type': a.anomaly_type,
                'anomaly_score': a.anomaly_score,
                'severity': a.severity,
                'description': a.description,
                'status': a.status,
                'detected_at': a.detected_at.isoformat(),
                'evidence': a.evidence
            } for a in anomalies]
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching anomalies for shop {shop_id}: {e}")
        return jsonify({'error': str(e)}), 500

@anomaly_bp.route('/<int:anomaly_id>/resolve', methods=['POST'])
@role_required(UserRole.ADMIN.value, UserRole.ANALYST.value)
def resolve_anomaly(anomaly_id):
    """
    Mark an anomaly as resolved
    
    Request body:
    {
        "status": "resolved",
        "resolution_notes": "Issue investigated and cleared"
    }
    """
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        anomaly = AnomalyDetection.query.get(anomaly_id)
        if not anomaly:
            return jsonify({'error': 'Anomaly not found'}), 404
        
        anomaly.status = data.get('status', 'resolved')
        anomaly.resolution_notes = data.get('resolution_notes', '')
        anomaly.resolved_at = db.func.now()
        
        db.session.commit()
        
        log_user_action(
            user_id,
            'RESOLVE_ANOMALY',
            'anomaly_detection',
            anomaly_id,
            {'new_status': anomaly.status}
        )
        
        return jsonify({
            'success': True,
            'message': 'Anomaly resolved',
            'anomaly': {
                'id': anomaly.id,
                'status': anomaly.status,
                'resolved_at': anomaly.resolved_at.isoformat() if anomaly.resolved_at else None
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error resolving anomaly {anomaly_id}: {e}")
        return jsonify({'error': str(e)}), 500

@anomaly_bp.route('/stats/<int:shop_id>', methods=['GET'])
@role_required(
    UserRole.ADMIN.value,
    UserRole.ANALYST.value,
    UserRole.SHOP_MANAGER.value
)
def get_anomaly_stats(shop_id):
    """Get anomaly statistics for a shop"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.role == UserRole.SHOP_MANAGER.value and user.shop_id != shop_id:
            return jsonify({'error': 'Unauthorized access to this shop'}), 403
        
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404
        
        # Count by severity
        severity_counts = {
            'critical': AnomalyDetection.query.filter_by(
                shop_id=shop_id, severity='critical'
            ).count(),
            'high': AnomalyDetection.query.filter_by(
                shop_id=shop_id, severity='high'
            ).count(),
            'medium': AnomalyDetection.query.filter_by(
                shop_id=shop_id, severity='medium'
            ).count(),
            'low': AnomalyDetection.query.filter_by(
                shop_id=shop_id, severity='low'
            ).count()
        }
        
        # Count by type
        type_counts = {
            'stock_discrepancy': AnomalyDetection.query.filter_by(
                shop_id=shop_id, anomaly_type='stock_discrepancy'
            ).count(),
            'suspicious_activity': AnomalyDetection.query.filter_by(
                shop_id=shop_id, anomaly_type='suspicious_activity'
            ).count(),
            'delivery_delay': AnomalyDetection.query.filter_by(
                shop_id=shop_id, anomaly_type='delivery_delay'
            ).count()
        }
        
        # Count by status
        status_counts = {
            'open': AnomalyDetection.query.filter_by(
                shop_id=shop_id, status='open'
            ).count(),
            'investigating': AnomalyDetection.query.filter_by(
                shop_id=shop_id, status='investigating'
            ).count(),
            'resolved': AnomalyDetection.query.filter_by(
                shop_id=shop_id, status='resolved'
            ).count()
        }
        
        return jsonify({
            'success': True,
            'shop_id': shop_id,
            'severity_distribution': severity_counts,
            'anomaly_type_distribution': type_counts,
            'status_distribution': status_counts,
            'total_anomalies': sum(severity_counts.values())
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching stats for shop {shop_id}: {e}")
        return jsonify({'error': str(e)}), 500
