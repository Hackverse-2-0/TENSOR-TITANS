from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    ADMIN = "admin"
    SHOP_MANAGER = "shop_manager"
    DISTRIBUTION_CENTER = "distribution_center"
    ANALYST = "analyst"

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default=UserRole.SHOP_MANAGER.value)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Shop(db.Model):
    __tablename__ = 'shops'
    
    id = db.Column(db.Integer, primary_key=True)
    shop_code = db.Column(db.String(50), unique=True, nullable=False)
    shop_name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    stocks = db.relationship('Stock', backref='shop', lazy=True)
    biometric_logs = db.relationship('BiometricLog', backref='shop', lazy=True)
    
    def __repr__(self):
        return f'<Shop {self.shop_code}>'

class Stock(db.Model):
    __tablename__ = 'stocks'
    
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    item_code = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    quantity_received = db.Column(db.Float, nullable=False)
    quantity_sold = db.Column(db.Float, nullable=False)
    quantity_remaining = db.Column(db.Float, nullable=False)
    expected_quantity = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Stock {self.item_code}>'

class BiometricLog(db.Model):
    __tablename__ = 'biometric_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    employee_id = db.Column(db.String(50), nullable=False)
    employee_name = db.Column(db.String(120), nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=False)
    check_out_time = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='present')  # present, absent, late
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<BiometricLog {self.employee_id}>'

class DeliverySchedule(db.Model):
    __tablename__ = 'delivery_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    delivery_id = db.Column(db.String(50), unique=True, nullable=False)
    item_code = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    scheduled_quantity = db.Column(db.Float, nullable=False)
    delivered_quantity = db.Column(db.Float, nullable=True)
    scheduled_date = db.Column(db.DateTime, nullable=False)
    actual_delivery_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, delivered, delayed
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<DeliverySchedule {self.delivery_id}>'

class AnomalyDetection(db.Model):
    __tablename__ = 'anomaly_detections'
    
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    anomaly_type = db.Column(db.String(50), nullable=False)  # stock_discrepancy, suspicious_activity, delivery_delay
    anomaly_score = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    description = db.Column(db.Text, nullable=False)
    evidence = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(20), default='open')  # open, investigating, resolved
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    resolution_notes = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f'<AnomalyDetection {self.anomaly_type}>'

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)
    resource_id = db.Column(db.Integer, nullable=True)
    changes = db.Column(db.JSON, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action}>'
