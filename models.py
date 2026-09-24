from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default='Fresh Chicken')
    price_per_kg = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.Text, nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price_per_kg': self.price_per_kg,
            'description': self.description or '',
            'image_url': self.image_url or '/static/images/products/placeholder.svg',
            'is_available': self.is_available,
            'is_active': self.is_active
        }

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    order_type = db.Column(db.String(20), default='Pickup')  # Pickup
    status = db.Column(db.String(30), default='New')  # New, Accepted, Preparing, Ready for Pickup, Completed, Cancelled
    payment_method = db.Column(db.String(30), default='Cash / UPI')  # Cash, UPI, Online
    total_amount = db.Column(db.Float, nullable=False, default=0.0)
    cutting_preference = db.Column(db.String(100), default='Curry Cut')
    special_instructions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'order_type': self.order_type,
            'status': self.status,
            'payment_method': self.payment_method,
            'total_amount': self.total_amount,
            'cutting_preference': self.cutting_preference,
            'special_instructions': self.special_instructions or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity_kg = db.Column(db.Float, nullable=False)
    price_per_kg = db.Column(db.Float, nullable=False)
    item_total = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'quantity_kg': self.quantity_kg,
            'price_per_kg': self.price_per_kg,
            'item_total': self.item_total
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    review_text = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)  # Requires admin approval
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'rating': self.rating,
            'review_text': self.review_text,
            'is_approved': self.is_approved,
            'created_at': self.created_at.strftime('%b %d, %Y')
        }

class BulkEnquiry(db.Model):
    __tablename__ = 'bulk_enquiries'
    id = db.Column(db.Integer, primary_key=True)
    contact_name = db.Column(db.String(100), nullable=False)
    business_name = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=False)
    business_type = db.Column(db.String(50), default='Restaurant / Hotel')
    requirement_details = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='Pending')  # Pending, Contacted, In Discussion, Closed
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'contact_name': self.contact_name,
            'business_name': self.business_name or 'Individual Bulk',
            'phone': self.phone,
            'business_type': self.business_type,
            'requirement_details': self.requirement_details,
            'status': self.status,
            'notes': self.notes or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M')
        }

class RevenueTransaction(db.Model):
    __tablename__ = 'revenue_transactions'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(30), default='Cash')  # Cash, UPI, Card, Online
    order_type = db.Column(db.String(30), default='Retail Walk-in')  # Retail Walk-in, Website Order, Bulk Order
    description = db.Column(db.String(255), nullable=True)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'order_type': self.order_type,
            'description': self.description or '',
            'transaction_date': self.transaction_date.strftime('%Y-%m-%d %H:%M'),
            'order_id': self.order_id
        }

class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=True)
