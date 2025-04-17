from flask import Blueprint, request, jsonify
from models import  Transaction
from auth import token_required  # 保护 API 需要登录
from extensions import db
# 创建 Blueprint
transaction_bp = Blueprint('transactions', __name__)

# 获取当前用户的所有交易记录
@transaction_bp.route('/', methods=['GET'])
@token_required
def get_transactions(decoded):
    user_id = decoded["user_id"]
    transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.id.desc()).all()
    return jsonify({
        "success": True,
        "message": "获取交易记录成功",
        "data": [t.to_dict() for t in transactions]
    })


# 获取当前用户的单个交易记录
@transaction_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_transaction(decoded, id):
    user_id = decoded["user_id"]
    transaction = Transaction.query.filter_by(id=id, user_id=user_id).first()

    if not transaction:
        return jsonify({
            "success": False,
            "message": "交易记录不存在或无权限访问",
            "data": {}
        }), 404

    return jsonify({
        "success": True,
        "message": "获取交易记录成功",
        "data": transaction.to_dict()
    })

# 创建新交易记录
@transaction_bp.route('/', methods=['POST'])
@token_required
def create_transaction(decoded):
    data = request.get_json()
    user_id = decoded["user_id"]  # 获取当前用户的 user_id
    data["user_id"] = user_id  # 绑定交易到当前用户

    transaction = Transaction(**data)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "交易记录创建成功",
        "data": transaction.to_dict()
    }), 201

# 更新当前用户的交易记录
@transaction_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_transaction(decoded, id):
    user_id = decoded["user_id"]
    transaction = Transaction.query.filter_by(id=id, user_id=user_id).first()

    if not transaction:
        return jsonify({
            "success": False,
            "message": "交易记录不存在或无权限访问",
            "data": {}
        }), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(transaction, key, value)

    db.session.commit()
    return jsonify({
        "success": True,
        "message": "交易记录更新成功",
        "data": transaction.to_dict()
    })

# 删除当前用户的交易记录
@transaction_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_transaction(decoded, id):
    user_id = decoded["user_id"]
    transaction = Transaction.query.filter_by(id=id, user_id=user_id).first()

    if not transaction:
        return jsonify({
            "success": False,
            "message": "交易记录不存在或无权限访问",
            "data": {}
        }), 404

    db.session.delete(transaction)
    db.session.commit()
    return jsonify({
        "success": True,
        "message": "交易记录删除成功",
        "data": {}
    })
