from flask import Blueprint, request, jsonify
from flask_login import login_required
try:
    from models import db, Employee
except ImportError:
    from ..models import db, Employee

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/api/employees', methods=['GET'])
@login_required
def get_employees():
    employees = Employee.query.all()
    return jsonify([{
        'id': e.id,
        'name': e.name,
        'position': e.position,
        'department': e.department,
        'contact': e.contact
    } for e in employees])

@employees_bp.route('/api/employees', methods=['POST'])
@login_required
def add_employee():
    data = request.get_json()
    
    # Generate ID like EMPL-0001
    last_employee = Employee.query.order_by(Employee.id.desc()).first()
    if last_employee:
        last_num = int(last_employee.id.split('-')[1])
        new_id = f"EMPL-{last_num + 1:04d}"
    else:
        new_id = "EMPL-0001"
    
    employee = Employee(
        id=new_id,
        name=data['name'],
        position=data['position'],
        department=data['department'],
        contact=data['contact']
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify({'message': 'Employee added successfully', 'id': new_id}), 201

@employees_bp.route('/api/employees/<employee_id>', methods=['GET'])
@login_required
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify({
        'id': employee.id,
        'name': employee.name,
        'position': employee.position,
        'department': employee.department,
        'contact': employee.contact
    })

@employees_bp.route('/api/employees/<employee_id>', methods=['PUT'])
@login_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()
    
    employee.name = data['name']
    employee.position = data['position']
    employee.department = data['department']
    employee.contact = data['contact']
    
    db.session.commit()
    return jsonify({'message': 'Employee updated successfully'})

@employees_bp.route('/api/employees/<employee_id>', methods=['DELETE'])
@login_required
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return jsonify({'message': 'Employee deleted successfully'})