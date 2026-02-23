"""Machine Learning models for anomaly detection"""
import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import xgboost as xgb
from datetime import datetime, timedelta
from models import db, Stock, BiometricLog, DeliverySchedule, AnomalyDetection, Shop

logger = logging.getLogger(__name__)

class AnomalyDetectionModel:
    """Base anomaly detection class"""
    
    def __init__(self):
        self.isolation_forest = None
        self.xgb_model = None
        self.scaler = StandardScaler()
    
    def detect_stock_discrepancies(self, shop_id, threshold=0.7):
        """
        Detect stock discrepancies using Isolation Forest
        
        Args:
            shop_id: Shop ID to analyze
            threshold: Anomaly score threshold (0-1)
        
        Returns:
            List of detected anomalies
        """
        try:
            # Fetch recent stock data
            stocks = Stock.query.filter_by(shop_id=shop_id)\
                .order_by(Stock.recorded_at.desc()).limit(100).all()
            
            if len(stocks) < 10:
                logger.warning(f"Insufficient stock data for shop {shop_id}")
                return []
            
            # Prepare features
            features = []
            for stock in stocks:
                discrepancy = abs(stock.quantity_remaining - stock.expected_quantity)
                discrepancy_ratio = discrepancy / max(stock.expected_quantity, 1)
                
                features.append({
                    'id': stock.id,
                    'discrepancy': discrepancy,
                    'discrepancy_ratio': discrepancy_ratio,
                    'quantity_remaining': stock.quantity_remaining,
                    'expected_quantity': stock.expected_quantity,
                    'quantity_sold': stock.quantity_sold
                })
            
            df = pd.DataFrame(features)
            X = df[['discrepancy', 'discrepancy_ratio', 'quantity_remaining']].values
            X_scaled = self.scaler.fit_transform(X)
            
            # Isolation Forest
            iso_forest = IsolationForest(
                contamination=0.1,
                random_state=42,
                n_estimators=100
            )
            anomaly_labels = iso_forest.fit_predict(X_scaled)
            anomaly_scores = 1 - (iso_forest.score_samples(X_scaled) + 0.5)  # Normalize to [0, 1]
            
            # Identify anomalies
            anomalies = []
            for idx, (label, score) in enumerate(zip(anomaly_labels, anomaly_scores)):
                if score >= threshold:
                    feature = features[idx]
                    severity = self._calculate_severity(score)
                    
                    anomalies.append({
                        'stock_id': feature['id'],
                        'anomaly_score': float(score),
                        'severity': severity,
                        'discrepancy': feature['discrepancy'],
                        'discrepancy_ratio': feature['discrepancy_ratio'],
                        'description': f"Stock discrepancy detected: Expected {feature['expected_quantity']}, Found {feature['quantity_remaining']}"
                    })
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting stock discrepancies for shop {shop_id}: {e}")
            return []
    
    def detect_suspicious_attendance(self, shop_id, threshold=0.7):
        """
        Detect suspicious biometric patterns using Isolation Forest
        
        Args:
            shop_id: Shop ID to analyze
            threshold: Anomaly score threshold
        
        Returns:
            List of detected anomalies
        """
        try:
            # Fetch recent biometric data
            logs = BiometricLog.query.filter_by(shop_id=shop_id)\
                .order_by(BiometricLog.check_in_time.desc()).limit(200).all()
            
            if len(logs) < 20:
                logger.warning(f"Insufficient biometric data for shop {shop_id}")
                return []
            
            # Group by employee and extract features
            employee_features = {}
            for log in logs:
                emp_id = log.employee_id
                if emp_id not in employee_features:
                    employee_features[emp_id] = []
                
                duration = 0
                if log.check_out_time:
                    duration = (log.check_out_time - log.check_in_time).total_seconds() / 3600
                
                employee_features[emp_id].append({
                    'log_id': log.id,
                    'duration_hours': duration,
                    'status': log.status,
                    'check_in_hour': log.check_in_time.hour
                })
            
            anomalies = []
            for emp_id, emp_logs in employee_features.items():
                if len(emp_logs) < 5:
                    continue
                
                durations = [log['duration_hours'] for log in emp_logs]
                hours = [log['check_in_hour'] for log in emp_logs]
                
                features = np.array([
                    [d, h] for d, h in zip(durations, hours)
                ])
                
                if len(features) < 5:
                    continue
                
                X_scaled = self.scaler.fit_transform(features)
                iso_forest = IsolationForest(contamination=0.1, random_state=42)
                scores = 1 - (iso_forest.fit_predict(X_scaled) + 0.5)
                
                for idx, score in enumerate(scores):
                    if score >= threshold:
                        anomalies.append({
                            'employee_id': emp_id,
                            'log_id': emp_logs[idx]['log_id'],
                            'anomaly_score': float(score),
                            'severity': self._calculate_severity(score),
                            'description': f"Unusual attendance pattern detected for employee {emp_id}"
                        })
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting suspicious attendance for shop {shop_id}: {e}")
            return []
    
    def detect_delivery_anomalies(self, shop_id, threshold=0.7):
        """
        Detect delivery anomalies using XGBoost
        
        Args:
            shop_id: Shop ID to analyze
            threshold: Anomaly score threshold
        
        Returns:
            List of detected anomalies
        """
        try:
            # Fetch delivery data
            deliveries = DeliverySchedule.query.filter_by(shop_id=shop_id)\
                .order_by(DeliverySchedule.scheduled_date.desc()).limit(100).all()
            
            if len(deliveries) < 10:
                logger.warning(f"Insufficient delivery data for shop {shop_id}")
                return []
            
            # Extract features
            features = []
            for delivery in deliveries:
                days_delayed = 0
                if delivery.actual_delivery_date and delivery.scheduled_date:
                    days_delayed = (delivery.actual_delivery_date - delivery.scheduled_date).days
                
                quantity_variance = 0
                if delivery.delivered_quantity and delivery.scheduled_quantity:
                    quantity_variance = (delivery.delivered_quantity - delivery.scheduled_quantity) / delivery.scheduled_quantity
                
                features.append({
                    'id': delivery.id,
                    'days_delayed': max(0, days_delayed),
                    'quantity_variance': abs(quantity_variance) if quantity_variance else 0,
                    'scheduled_qty': delivery.scheduled_quantity,
                    'delivered_qty': delivery.delivered_quantity or 0,
                    'is_delayed': 1 if delivery.status == 'delayed' else 0
                })
            
            df = pd.DataFrame(features)
            X = df[['days_delayed', 'quantity_variance', 'scheduled_qty', 'delivered_qty']].values
            X_scaled = self.scaler.fit_transform(X)
            
            # Isolation Forest for delivery anomalies
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            scores = 1 - (iso_forest.fit_predict(X_scaled) + 0.5)
            
            anomalies = []
            for idx, score in enumerate(scores):
                if score >= threshold:
                    feature = features[idx]
                    anomalies.append({
                        'delivery_id': feature['id'],
                        'anomaly_score': float(score),
                        'severity': self._calculate_severity(score),
                        'days_delayed': feature['days_delayed'],
                        'quantity_variance': feature['quantity_variance'],
                        'description': f"Delivery anomaly: {feature['days_delayed']} days delayed, {abs(feature['quantity_variance']*100):.1f}% quantity variance"
                    })
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting delivery anomalies for shop {shop_id}: {e}")
            return []
    
    @staticmethod
    def _calculate_severity(score):
        """Calculate severity level based on anomaly score"""
        if score >= 0.9:
            return 'critical'
        elif score >= 0.75:
            return 'high'
        elif score >= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def save_anomalies(self, shop_id, anomalies_list):
        """Save detected anomalies to database"""
        for anomaly_type, anomalies in anomalies_list.items():
            for anomaly in anomalies:
                try:
                    db_anomaly = AnomalyDetection(
                        shop_id=shop_id,
                        anomaly_type=anomaly_type,
                        anomaly_score=anomaly['anomaly_score'],
                        severity=anomaly['severity'],
                        description=anomaly['description'],
                        evidence=anomaly
                    )
                    db.session.add(db_anomaly)
                except Exception as e:
                    logger.error(f"Error saving anomaly: {e}")
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error committing anomalies: {e}")
    
    def run_full_detection(self, shop_id):
        """Run all anomaly detection methods for a shop"""
        results = {
            'stock_discrepancies': self.detect_stock_discrepancies(shop_id),
            'suspicious_attendance': self.detect_suspicious_attendance(shop_id),
            'delivery_anomalies': self.detect_delivery_anomalies(shop_id)
        }
        
        # Save to database
        self.save_anomalies(shop_id, results)
        
        return results
