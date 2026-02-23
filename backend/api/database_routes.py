"""Database management and data retrieval routes"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import (db, User, Shop, Stock, BiometricLog, DeliverySchedule, 
                   AnomalyDetection, AuditLog, UserRole)
from api.auth import role_required
from datetime import datetime, timedelta
from sqlalchemy import func, and_, or_
import json
import logging

logger = logging.getLogger(__name__)

db_bp = Blueprint('database', __name__, url_prefix='/api/v1/database')

# ==================== STOCK DATA ====================

@db_bp.route('/stocks', methods=['GET'])
@jwt_required()
def get_stocks():
    """
    Get stock data with optional filtering
    Query params:
    - shop_id: Filter by shop
    - item_code: Filter by item code
    - limit: Number of records (default 50)
    - offset: Pagination offset (default 0)
    - start_date: ISO format date
    - end_date: ISO format date
    """
    try:
        shop_id = request.args.get('shop_id', type=int)
        item_code = request.args.get('item_code')
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = Stock.query

        if shop_id:
            query = query.filter_by(shop_id=shop_id)
        if item_code:
            query = query.filter_by(item_code=item_code)
        if start_date:
            start = datetime.fromisoformat(start_date)
            query = query.filter(Stock.recorded_at >= start)
        if end_date:
            end = datetime.fromisoformat(end_date)
            query = query.filter(Stock.recorded_at <= end)

        total = query.count()
        stocks = query.order_by(Stock.recorded_at.desc()).limit(limit).offset(offset).all()

        data = [{
            'id': s.id,
            'shop_id': s.shop_id,
            'shop_name': s.shop.shop_name if s.shop else None,
            'item_code': s.item_code,
            'item_name': s.item_name,
            'quantity_received': s.quantity_received,
            'quantity_sold': s.quantity_sold,
            'quantity_remaining': s.quantity_remaining,
            'expected_quantity': s.expected_quantity,
            'discrepancy': abs(s.quantity_remaining - s.expected_quantity),
            'recorded_at': s.recorded_at.isoformat()
        } for s in stocks]

        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': data
        }), 200

    except Exception as e:
        logger.error(f"Error fetching stocks: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== BIOMETRIC DATA ====================

@db_bp.route('/biometric-logs', methods=['GET'])
@jwt_required()
def get_biometric_logs():
    """
    Get biometric logs with optional filtering
    Query params:
    - shop_id: Filter by shop
    - employee_id: Filter by employee
    - status: Filter by status
    - limit: Number of records
    - offset: Pagination offset
    - start_date: ISO format date
    - end_date: ISO format date
    """
    try:
        shop_id = request.args.get('shop_id', type=int)
        employee_id = request.args.get('employee_id')
        status = request.args.get('status')
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = BiometricLog.query

        if shop_id:
            query = query.filter_by(shop_id=shop_id)
        if employee_id:
            query = query.filter_by(employee_id=employee_id)
        if status:
            query = query.filter_by(status=status)
        if start_date:
            start = datetime.fromisoformat(start_date)
            query = query.filter(BiometricLog.recorded_at >= start)
        if end_date:
            end = datetime.fromisoformat(end_date)
            query = query.filter(BiometricLog.recorded_at <= end)

        total = query.count()
        logs = query.order_by(BiometricLog.recorded_at.desc()).limit(limit).offset(offset).all()

        data = [{
            'id': l.id,
            'shop_id': l.shop_id,
            'shop_name': l.shop.shop_name if l.shop else None,
            'employee_id': l.employee_id,
            'employee_name': l.employee_name,
            'check_in_time': l.check_in_time.isoformat(),
            'check_out_time': l.check_out_time.isoformat() if l.check_out_time else None,
            'duration_hours': round((l.check_out_time - l.check_in_time).total_seconds() / 3600, 2) if l.check_out_time else None,
            'status': l.status,
            'recorded_at': l.recorded_at.isoformat()
        } for l in logs]

        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': data
        }), 200

    except Exception as e:
        logger.error(f"Error fetching biometric logs: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== DELIVERY DATA ====================

@db_bp.route('/deliveries', methods=['GET'])
@jwt_required()
def get_deliveries():
    """
    Get delivery schedules with optional filtering
    Query params:
    - shop_id: Filter by shop
    - status: Filter by status
    - item_code: Filter by item
    - limit: Number of records
    - offset: Pagination offset
    - start_date: ISO format date
    - end_date: ISO format date
    """
    try:
        shop_id = request.args.get('shop_id', type=int)
        status = request.args.get('status')
        item_code = request.args.get('item_code')
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query = DeliverySchedule.query

        if shop_id:
            query = query.filter_by(shop_id=shop_id)
        if status:
            query = query.filter_by(status=status)
        if item_code:
            query = query.filter_by(item_code=item_code)
        if start_date:
            start = datetime.fromisoformat(start_date)
            query = query.filter(DeliverySchedule.scheduled_date >= start)
        if end_date:
            end = datetime.fromisoformat(end_date)
            query = query.filter(DeliverySchedule.scheduled_date <= end)

        total = query.count()
        deliveries = query.order_by(DeliverySchedule.scheduled_date.desc()).limit(limit).offset(offset).all()

        data = [{
            'id': d.id,
            'shop_id': d.shop_id,
            'shop_name': d.shop.shop_name if d.shop else None,
            'delivery_id': d.delivery_id,
            'item_code': d.item_code,
            'item_name': d.item_name,
            'scheduled_quantity': d.scheduled_quantity,
            'delivered_quantity': d.delivered_quantity,
            'quantity_variance': round(((d.delivered_quantity or 0) - d.scheduled_quantity) / d.scheduled_quantity * 100, 2) if d.scheduled_quantity > 0 else 0,
            'scheduled_date': d.scheduled_date.isoformat(),
            'actual_delivery_date': d.actual_delivery_date.isoformat() if d.actual_delivery_date else None,
            'days_delayed': (d.actual_delivery_date - d.scheduled_date).days if d.actual_delivery_date else None,
            'status': d.status,
            'recorded_at': d.recorded_at.isoformat()
        } for d in deliveries]

        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': data
        }), 200

    except Exception as e:
        logger.error(f"Error fetching deliveries: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== ANOMALIES ====================

@db_bp.route('/anomalies', methods=['GET'])
@jwt_required()
def get_all_anomalies():
    """
    Get all anomalies with optional filtering
    Query params:
    - shop_id: Filter by shop
    - anomaly_type: Filter by type
    - severity: Filter by severity
    - status: Filter by status
    - limit: Number of records
    - offset: Pagination offset
    """
    try:
        shop_id = request.args.get('shop_id', type=int)
        anomaly_type = request.args.get('anomaly_type')
        severity = request.args.get('severity')
        status = request.args.get('status')
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)

        query = AnomalyDetection.query

        if shop_id:
            query = query.filter_by(shop_id=shop_id)
        if anomaly_type:
            query = query.filter_by(anomaly_type=anomaly_type)
        if severity:
            query = query.filter_by(severity=severity)
        if status:
            query = query.filter_by(status=status)

        total = query.count()
        anomalies = query.order_by(AnomalyDetection.detected_at.desc()).limit(limit).offset(offset).all()

        data = [{
            'id': a.id,
            'shop_id': a.shop_id,
            'shop_name': a.shop.shop_name if a.shop else None,
            'anomaly_type': a.anomaly_type,
            'anomaly_score': round(a.anomaly_score, 3),
            'severity': a.severity,
            'description': a.description,
            'evidence': a.evidence,
            'status': a.status,
            'detected_at': a.detected_at.isoformat(),
            'resolved_at': a.resolved_at.isoformat() if a.resolved_at else None,
            'resolution_notes': a.resolution_notes
        } for a in anomalies]

        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': data
        }), 200

    except Exception as e:
        logger.error(f"Error fetching anomalies: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== DASHBOARD STATS ====================

@db_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_database_stats():
    """
    Get overall database statistics
    """
    try:
        shop_id = request.args.get('shop_id', type=int)
        
        # Total counts
        total_stocks = Stock.query.filter_by(shop_id=shop_id).count() if shop_id else Stock.query.count()
        total_biometric = BiometricLog.query.filter_by(shop_id=shop_id).count() if shop_id else BiometricLog.query.count()
        total_deliveries = DeliverySchedule.query.filter_by(shop_id=shop_id).count() if shop_id else DeliverySchedule.query.count()
        total_anomalies = AnomalyDetection.query.filter_by(shop_id=shop_id).count() if shop_id else AnomalyDetection.query.count()
        
        # Anomaly breakdown
        query_anom = AnomalyDetection.query
        if shop_id:
            query_anom = query_anom.filter_by(shop_id=shop_id)
        
        severity_stats = db.session.query(
            AnomalyDetection.severity,
            func.count(AnomalyDetection.id)
        ).filter_by(shop_id=shop_id) if shop_id else db.session.query(
            AnomalyDetection.severity,
            func.count(AnomalyDetection.id)
        )
        severity_stats = severity_stats.group_by(AnomalyDetection.severity).all()
        
        type_stats = db.session.query(
            AnomalyDetection.anomaly_type,
            func.count(AnomalyDetection.id)
        ).filter_by(shop_id=shop_id) if shop_id else db.session.query(
            AnomalyDetection.anomaly_type,
            func.count(AnomalyDetection.id)
        )
        type_stats = type_stats.group_by(AnomalyDetection.anomaly_type).all()
        
        # Total shops
        total_shops = Shop.query.count()
        
        # Last 7 days data
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_stocks = Stock.query.filter(Stock.recorded_at >= week_ago)
        week_deliveries = DeliverySchedule.query.filter(DeliverySchedule.recorded_at >= week_ago)
        
        if shop_id:
            week_stocks = week_stocks.filter_by(shop_id=shop_id)
            week_deliveries = week_deliveries.filter_by(shop_id=shop_id)
        
        stats = {
            'total_stocks': total_stocks,
            'total_biometric_logs': total_biometric,
            'total_deliveries': total_deliveries,
            'total_anomalies': total_anomalies,
            'total_shops': total_shops,
            'anomalies_by_severity': {
                'critical': next((count for sev, count in severity_stats if sev == 'critical'), 0),
                'high': next((count for sev, count in severity_stats if sev == 'high'), 0),
                'medium': next((count for sev, count in severity_stats if sev == 'medium'), 0),
                'low': next((count for sev, count in severity_stats if sev == 'low'), 0)
            },
            'anomalies_by_type': {
                anom_type: count for anom_type, count in type_stats
            },
            'recent_7_days': {
                'stocks': week_stocks.count(),
                'deliveries': week_deliveries.count()
            }
        }

        return jsonify({
            'success': True,
            'stats': stats
        }), 200

    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({'error': str(e)}), 500


# ==================== DATA EXPORT ====================

@db_bp.route('/export/stocks', methods=['GET'])
@jwt_required()
def export_stocks():
    """Export stock data as JSON"""
    try:
        shop_id = request.args.get('shop_id', type=int)
        
        query = Stock.query
        if shop_id:
            query = query.filter_by(shop_id=shop_id)
        
        stocks = query.order_by(Stock.recorded_at.desc()).all()
        
        data = [{
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
        
        return jsonify({
            'success': True,
            'export_date': datetime.utcnow().isoformat(),
            'total_records': len(data),
            'data': data
        }), 200

    except Exception as e:
        logger.error(f"Error exporting stocks: {e}")
        return jsonify({'error': str(e)}), 500


@db_bp.route('/export/biometric', methods=['GET'])
@jwt_required()
def export_biometric():
    """Export biometric data as JSON"""
    try:
        shop_id = request.args.get('shop_id', type=int)
        
        query = BiometricLog.query
        if shop_id:
            query = query.filter_by(shop_id=shop_id)
        
        logs = query.order_by(BiometricLog.recorded_at.desc()).all()
        
        data = [{
            'id': l.id,
            'shop_id': l.shop_id,
            'employee_id': l.employee_id,
            'employee_name': l.employee_name,
            'check_in_time': l.check_in_time.isoformat(),
            'check_out_time': l.check_out_time.isoformat() if l.check_out_time else None,
            'status': l.status,
            'recorded_at': l.recorded_at.isoformat()
        } for l in logs]
        
        return jsonify({
            'success': True,
            'export_date': datetime.utcnow().isoformat(),
            'total_records': len(data),
            'data': data
        }), 200

    except Exception as e:
        logger.error(f"Error exporting biometric: {e}")
        return jsonify({'error': str(e)}), 500


@db_bp.route('/export/deliveries', methods=['GET'])
@jwt_required()
def export_deliveries():
    """Export delivery data as JSON"""
    try:
        shop_id = request.args.get('shop_id', type=int)
        
        query = DeliverySchedule.query
        if shop_id:
            query = query.filter_by(shop_id=shop_id)
        
        deliveries = query.order_by(DeliverySchedule.scheduled_date.desc()).all()
        
        data = [{
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
            'export_date': datetime.utcnow().isoformat(),
            'total_records': len(data),
            'data': data
        }), 200

    except Exception as e:
        logger.error(f"Error exporting deliveries: {e}")
        return jsonify({'error': str(e)}), 500
