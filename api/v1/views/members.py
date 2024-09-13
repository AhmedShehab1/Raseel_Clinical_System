from api.v1.errors import bad_request
from web_flask import db
from api.v1.views import bp, get_from_db
from models import Doctor, Admin, Department, Receptionist
from flask import request
from datetime import datetime
from functools import wraps
import sqlalchemy as sa


def save(model=None):
    if model:
        db.session.add(model)
    db.session.commit()

def validate_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.get_json()
        if not data:
            return bad_request('No input data provided')
        return f(data, *args, **kwargs)
    return decorated_function

def update_item(item, data):
    for k, v in data.items():
        if k in ['id', 'created_at', 'updated_at', 'deleted_at']:
            continue
        if v is not None:
            if k == 'password':
                item.set_password(v)
                continue
            setattr(item, k, v)
    save()

@bp.delete('/staff-members/<string:member_id>')
def delete_member(member_id):
    member = get_from_db(member_id, Doctor, Admin, Receptionist)
    member.deleted_at = datetime.utcnow()
    save()
    return {}, 200

@bp.get('/staff-members/<string:member_id>')
def get_member(member_id):
    member = get_from_db(member_id, Doctor, Admin, Receptionist)
    if member.__class__ == Doctor:
        dict_member = member.to_dict()
        dict_member['department'] = member.department.name
        return dict_member, 200
    return member.to_dict(), 200


def check_uniqueness(cls, field, val, error_msg):
    if val is not None:
        if db.session.scalar(sa.select(cls).where(
            getattr(cls, field) == val,
                )):
            return {'errors': {field: error_msg}}, 400
    return None

def validate_required_fields(data, required_fields):
    errors = {}
    if data.get('role', None) == 'Doctor':
        required_fields.extend(['department', 'certificates'])
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f'{field.title()} is required'
    return errors

def handle_department(data):
    if 'department' in data and data['department']:
        department = db.session.scalar(sa.select(Department).where(
                                                                Department.name == data['department'],
                                                                Department.deleted_at == None))
        if not department:
            return {'errors': {'department': 'Department doesnt exist'}}, 400
        return department.id


@bp.post('/staff-members/')
@validate_json
def add_member(data):
    required_fields = ['email', 'password', 'name', 'role']
    errors = validate_required_fields(data, required_fields)
    if errors:
        return {'errors': errors}, 400

    cls = globals().get(data['role'])
    if not cls:
        return bad_request('Invalid role specified')

    if data['role'] == 'Doctor':
        department_id = handle_department(data)
        if isinstance(department_id, tuple):
            return department_id
        data['department_id'] = department_id
        del data['department']

    if data['role'] != 'Doctor':
        for i in ['certificates', 'department']:
            del data[i]

    del data['role']

    uniqueness_checks = [
            check_uniqueness(cls, 'email', data['email'], 'Email already exists'),
            check_uniqueness(cls, 'phone', data['phone'], 'Phone number already exists')
        ]
    for check in uniqueness_checks:
        if check:
            return check
    new_member = cls(**data)
    save(new_member)
    return new_member.to_dict(), 201

@bp.put('/staff-members/<string:member_id>')
@validate_json
def manage_member(data, member_id):
    required_fields = ['email', 'name', 'role']

    errors = validate_required_fields(data, required_fields)
    if errors:
        return {'errors': errors}, 400

    cls = globals().get(data['role'])
    if not cls:
        return bad_request('Invalid role specified')

    if data['role'] == 'Doctor':
        department_id = handle_department(data)
        if isinstance(department_id, tuple):
            return department_id
        data['department_id'] = department_id
        del data['department']

    if data['role'] != 'Doctor':
        for i in ['certificates', 'department']:
            del data[i]

    del data['role']

    uniqueness_checks = []

    member = get_from_db(member_id, cls)
    if member.email != data['email']:
        uniqueness_checks.append(check_uniqueness(cls, 'email', data['email'], 'Email already exists'))
    if member.phone != data['phone']:
        uniqueness_checks.append(check_uniqueness(cls, 'phone', data['phone'], 'Phone Number already exists'))
    for check in uniqueness_checks:
        if check:
            return check
    update_item(member, data)
    return member.to_dict(), 200
