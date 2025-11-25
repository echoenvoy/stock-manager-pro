from flask import Blueprint, request, jsonify
from flask_login import login_required
try:
    from models import db, Delivery, Product, Employee
except ImportError:
    from ..models import db, Delivery, Product, Employee
from datetime import datetime

deliveries_bp = Blueprint('deliveries', __name__)

@deliveries_bp.route('/api/deliveries', methods=['GET'])
@login_required
def get_deliveries():
    try:
        deliveries = Delivery.query.join(Employee).join(Product).all()
        return jsonify([{
            'id': d.id,
            'employee_name': d.employee.name,
            'employee_id': d.employee_id,
            'product_name': d.product.name,
            'quantity': d.quantity,
            'date_order': d.date_order.isoformat(),
            'date_received': d.date_received.isoformat(),
            'status': d.status
        } for d in deliveries])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@deliveries_bp.route('/api/deliveries', methods=['POST'])
@login_required
def add_delivery():
    try:
        data = request.get_json()
        
        # Check stock availability
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 400
        if product.qty < data['quantity']:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Generate ID like DELV-0001
        last_delivery = Delivery.query.order_by(Delivery.id.desc()).first()
        if last_delivery:
            last_num = int(last_delivery.id.split('-')[1])
            new_id = f"DELV-{last_num + 1:04d}"
        else:
            new_id = "DELV-0001"
        
        # Update stock
        product.qty -= data['quantity']
        
        delivery = Delivery(
            id=new_id,
            employee_id=data['employee_id'],
            product_id=data['product_id'],
            quantity=data['quantity'],
            date_order=datetime.strptime(data['date_order'], '%Y-%m-%d').date(),
            date_received=datetime.strptime(data['date_received'], '%Y-%m-%d').date(),
            status='pending'
        )
        
        db.session.add(delivery)
        db.session.commit()
        
        return jsonify({'message': 'Delivery added successfully', 'id': new_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@deliveries_bp.route('/api/deliveries/<delivery_id>', methods=['GET'])
@login_required
def get_delivery(delivery_id):
    try:
        delivery = Delivery.query.get_or_404(delivery_id)
        return jsonify({
            'id': delivery.id,
            'employee_name': delivery.employee.name,
            'employee_id': delivery.employee_id,
            'product_name': delivery.product.name,
            'product_id': delivery.product_id,
            'quantity': delivery.quantity,
            'date_order': delivery.date_order.isoformat(),
            'date_received': delivery.date_received.isoformat(),
            'status': delivery.status
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@deliveries_bp.route('/api/deliveries/<delivery_id>', methods=['PUT'])
@login_required
def update_delivery(delivery_id):
    try:
        delivery = Delivery.query.get_or_404(delivery_id)
        data = request.get_json()
        
        delivery.employee_id = data['employee_id']
        delivery.product_id = data['product_id']
        delivery.quantity = data['quantity']
        delivery.date_order = datetime.strptime(data['date_order'], '%Y-%m-%d').date()
        delivery.date_received = datetime.strptime(data['date_received'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'message': 'Delivery updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@deliveries_bp.route('/api/deliveries/<delivery_id>', methods=['DELETE'])
@login_required
def delete_delivery(delivery_id):
    try:
        delivery = Delivery.query.get_or_404(delivery_id)
        db.session.delete(delivery)
        db.session.commit()
        return jsonify({'message': 'Delivery deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500