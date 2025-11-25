from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
try:
    from models import db, Product
except ImportError:
    from ..models import db, Product

from datetime import datetime

products_bp = Blueprint('products', __name__)

@products_bp.route('/api/products', methods=['GET'])
@login_required
def get_products():
    try:
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'qty': p.qty,
            'price': p.price,
            'threshold': p.threshold,
            'date_added': p.date_added.isoformat()
        } for p in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@products_bp.route('/api/products', methods=['POST'])
@login_required
def add_product():
    try:
        data = request.get_json()
        
        # Generate ID like PROD-0001
        last_product = Product.query.order_by(Product.id.desc()).first()
        if last_product:
            last_num = int(last_product.id.split('-')[1])
            new_id = f"PROD-{last_num + 1:04d}"
        else:
            new_id = "PROD-0001"
        
        product = Product(
            id=new_id,
            name=data['name'],
            qty=data['qty'],
            price=data['price'],
            threshold=data.get('threshold', 10),
            date_added=datetime.strptime(data['date_added'], '%Y-%m-%d').date()
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'message': 'Product added successfully', 'id': new_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/api/products/<product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        
        product.name = data['name']
        product.qty = data['qty']
        product.price = data['price']
        product.threshold = data.get('threshold', product.threshold)
        product.date_added = datetime.strptime(data['date_added'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/api/products/<product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@products_bp.route('/api/products/<product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'qty': product.qty,
            'price': product.price,
            'threshold': product.threshold,
            'date_added': product.date_added.isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500