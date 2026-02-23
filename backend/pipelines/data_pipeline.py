"""Data pipeline orchestrator"""
import logging
from datetime import datetime
from models import (
    db, Stock, BiometricLog, DeliverySchedule, Shop
)

logger = logging.getLogger(__name__)

class DataPipeline:
    """Base data pipeline class"""
    
    @staticmethod
    def validate_data(data, required_fields):
        """Validate required fields in data"""
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        return True
    
    @staticmethod
    def log_ingestion(source_type, records_processed, status='success', error=None):
        """Log data ingestion event"""
        log_entry = {
            'source_type': source_type,
            'records_processed': records_processed,
            'status': status,
            'timestamp': datetime.utcnow().isoformat(),
            'error': error
        }
        logger.info(f"Data Ingestion: {log_entry}")
        return log_entry

class StockPipeline(DataPipeline):
    """Pipeline for shop-wise stock data"""
    
    @staticmethod
    def ingest_stock_data(shop_id, stock_records):
        """
        Ingest stock data for a shop
        
        Args:
            shop_id: ID of the shop
            stock_records: List of stock dictionaries with fields:
                - item_code: Item code (required)
                - item_name: Item name (required)
                - quantity_received: Quantity received (required)
                - quantity_sold: Quantity sold (required)
                - quantity_remaining: Quantity remaining (required)
                - expected_quantity: Expected quantity (required)
        
        Returns:
            Tuple of (success_count, failed_count, errors)
        """
        success_count = 0
        failed_count = 0
        errors = []
        
        required_fields = [
            'item_code', 'item_name', 'quantity_received',
            'quantity_sold', 'quantity_remaining', 'expected_quantity'
        ]
        
        # Verify shop exists
        shop = Shop.query.get(shop_id)
        if not shop:
            raise ValueError(f"Shop with ID {shop_id} not found")
        
        for record in stock_records:
            try:
                DataPipeline.validate_data(record, required_fields)
                
                # Check if stock entry exists for today
                existing = Stock.query.filter_by(
                    shop_id=shop_id,
                    item_code=record['item_code']
                ).order_by(Stock.recorded_at.desc()).first()
                
                stock = Stock(
                    shop_id=shop_id,
                    item_code=record['item_code'],
                    item_name=record['item_name'],
                    quantity_received=float(record['quantity_received']),
                    quantity_sold=float(record['quantity_sold']),
                    quantity_remaining=float(record['quantity_remaining']),
                    expected_quantity=float(record['expected_quantity'])
                )
                
                db.session.add(stock)
                success_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append({
                    'record': record,
                    'error': str(e)
                })
                logger.error(f"Error processing stock record: {e}")
        
        try:
            db.session.commit()
            DataPipeline.log_ingestion('stock', success_count, 'success')
        except Exception as e:
            db.session.rollback()
            DataPipeline.log_ingestion('stock', success_count, 'error', str(e))
            raise
        
        return success_count, failed_count, errors

class BiometricPipeline(DataPipeline):
    """Pipeline for biometric logs"""
    
    @staticmethod
    def ingest_biometric_logs(shop_id, biometric_records):
        """
        Ingest biometric attendance data
        
        Args:
            shop_id: ID of the shop
            biometric_records: List of biometric dictionaries with fields:
                - employee_id: Employee ID (required)
                - employee_name: Employee name (required)
                - check_in_time: Check-in timestamp (required)
                - check_out_time: Check-out timestamp (optional)
                - status: Status (present/absent/late, optional)
        
        Returns:
            Tuple of (success_count, failed_count, errors)
        """
        success_count = 0
        failed_count = 0
        errors = []
        
        required_fields = ['employee_id', 'employee_name', 'check_in_time']
        
        shop = Shop.query.get(shop_id)
        if not shop:
            raise ValueError(f"Shop with ID {shop_id} not found")
        
        for record in biometric_records:
            try:
                DataPipeline.validate_data(record, required_fields)
                
                from datetime import datetime as dt
                check_in = dt.fromisoformat(record['check_in_time'])
                check_out = None
                if record.get('check_out_time'):
                    check_out = dt.fromisoformat(record['check_out_time'])
                
                log = BiometricLog(
                    shop_id=shop_id,
                    employee_id=record['employee_id'],
                    employee_name=record['employee_name'],
                    check_in_time=check_in,
                    check_out_time=check_out,
                    status=record.get('status', 'present')
                )
                
                db.session.add(log)
                success_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append({
                    'record': record,
                    'error': str(e)
                })
                logger.error(f"Error processing biometric record: {e}")
        
        try:
            db.session.commit()
            DataPipeline.log_ingestion('biometric', success_count, 'success')
        except Exception as e:
            db.session.rollback()
            DataPipeline.log_ingestion('biometric', success_count, 'error', str(e))
            raise
        
        return success_count, failed_count, errors

class DeliveryPipeline(DataPipeline):
    """Pipeline for delivery schedules"""
    
    @staticmethod
    def ingest_delivery_schedules(shop_id, delivery_records):
        """
        Ingest delivery schedule data
        
        Args:
            shop_id: ID of the shop
            delivery_records: List of delivery dictionaries with fields:
                - delivery_id: Unique delivery ID (required)
                - item_code: Item code (required)
                - item_name: Item name (required)
                - scheduled_quantity: Scheduled quantity (required)
                - scheduled_date: Scheduled delivery date (required)
                - delivered_quantity: Actual delivered quantity (optional)
                - actual_delivery_date: Actual delivery date (optional)
                - status: Status (optional)
        
        Returns:
            Tuple of (success_count, failed_count, errors)
        """
        success_count = 0
        failed_count = 0
        errors = []
        
        required_fields = [
            'delivery_id', 'item_code', 'item_name',
            'scheduled_quantity', 'scheduled_date'
        ]
        
        shop = Shop.query.get(shop_id)
        if not shop:
            raise ValueError(f"Shop with ID {shop_id} not found")
        
        for record in delivery_records:
            try:
                DataPipeline.validate_data(record, required_fields)
                
                from datetime import datetime as dt
                scheduled_date = dt.fromisoformat(record['scheduled_date'])
                actual_delivery_date = None
                if record.get('actual_delivery_date'):
                    actual_delivery_date = dt.fromisoformat(record['actual_delivery_date'])
                
                delivery = DeliverySchedule(
                    shop_id=shop_id,
                    delivery_id=record['delivery_id'],
                    item_code=record['item_code'],
                    item_name=record['item_name'],
                    scheduled_quantity=float(record['scheduled_quantity']),
                    delivered_quantity=float(record.get('delivered_quantity', 0)) if record.get('delivered_quantity') else None,
                    scheduled_date=scheduled_date,
                    actual_delivery_date=actual_delivery_date,
                    status=record.get('status', 'pending')
                )
                
                db.session.add(delivery)
                success_count += 1
                
            except Exception as e:
                failed_count += 1
                errors.append({
                    'record': record,
                    'error': str(e)
                })
                logger.error(f"Error processing delivery record: {e}")
        
        try:
            db.session.commit()
            DataPipeline.log_ingestion('delivery', success_count, 'success')
        except Exception as e:
            db.session.rollback()
            DataPipeline.log_ingestion('delivery', success_count, 'error', str(e))
            raise
        
        return success_count, failed_count, errors
