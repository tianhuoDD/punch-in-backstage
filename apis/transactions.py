from flask import Blueprint, request, jsonify
from utils.models import  Transaction
from utils.auth import token_required  # 保护 API 需要登录
from utils.extensions import db
from utils.logger import logger  # 新增引入日志模块

# 创建 Blueprint
transaction_bp = Blueprint('transactions', __name__)

# 获取当前用户的所有交易记录
@transaction_bp.route('/', methods=['GET'])
@token_required
def get_transactions(decoded):
    try:
        user_id = decoded["user_id"]
        transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.id.desc()).all()
        logger.info(f"获取用户 {user_id} 的所有交易记录成功")
        return jsonify({
            "success": True,
            "message": "获取交易记录成功",
            "data": [t.to_dict() for t in transactions]
        })
    except Exception as e:
        logger.error(f"获取用户 {user_id} 的所有交易记录失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取交易记录失败: {str(e)}",
            "data": []
        }), 500

# 获取当前用户的单个交易记录
@transaction_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_transaction(decoded, id):
    try:
        user_id = decoded["user_id"]
        transaction = Transaction.query.filter_by(id=id, user_id=user_id).first()

        if not transaction:
            logger.warning(f"获取用户 {user_id} 的单个交易记录失败: 交易记录不存在或无权限访问, 交易ID: {id}")
            return jsonify({
                "success": False,
                "message": "交易记录不存在或无权限访问",
                "data": {}
            }), 404

        logger.info(f"获取用户 {user_id} 的单个交易记录成功, 交易ID: {id}")
        return jsonify({
            "success": True,
            "message": "获取交易记录成功",
            "data": transaction.to_dict()
        })
    except Exception as e:
        logger.error(f"获取用户 {user_id} 的单个交易记录失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取交易记录失败: {str(e)}",
            "data": {}
        }), 500

# 创建新交易记录
@transaction_bp.route('/', methods=['POST'])
@token_required
def create_transaction(decoded):
    try:
        data = request.get_json()
        user_id = decoded["user_id"]  # 获取当前用户的 user_id
        data["user_id"] = user_id  # 绑定交易到当前用户

        transaction = Transaction(**data)
        db.session.add(transaction)
        db.session.commit()
        logger.info(f"用户 {user_id} 创建新交易记录成功, 交易ID: {transaction.id}")
        return jsonify({
            "success": True,
            "message": "交易记录创建成功",
            "data": transaction.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"用户 {user_id} 创建新交易记录失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"交易记录创建失败: {str(e)}",
            "data": {}
        }), 500

# 更新当前用户的交易记录
@transaction_bp.route('/<int:id>', methods=['PUT'])
@token_required
def update_transaction(decoded, id):
    try:
        user_id = decoded["user_id"]
        transaction = Transaction.query.filter_by(id=id, user_id=user_id).first()

        if not transaction:
            logger.warning(f"更新用户 {user_id} 的交易记录失败: 交易记录不存在或无权限访问, 交易ID: {id}")
            return jsonify({
                "success": False,
                "message": "交易记录不存在或无权限访问",
                "data": {}
            }), 404

        data = request.get_json()
        for key, value in data.items():
            setattr(transaction, key, value)

        db.session.commit()
        logger.info(f"用户 {user_id} 更新交易记录成功, 交易ID: {id}")
        return jsonify({
            "success": True,
            "message": "交易记录更新成功",
            "data": transaction.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"用户 {user_id} 更新交易记录失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"交易记录更新失败: {str(e)}",
            "data": {}
        }), 500

# 删除当前用户的交易记录
@transaction_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def delete_transaction(decoded, id):
    try:
        user_id = decoded["user_id"]
        transaction = Transaction.query.filter_by(id=id, user_id=user_id).first()

        if not transaction:
            logger.warning(f"删除用户 {user_id} 的交易记录失败: 交易记录不存在或无权限访问, 交易ID: {id}")
            return jsonify({
                "success": False,
                "message": "交易记录不存在或无权限访问",
                "data": {}
            }), 404

        db.session.delete(transaction)
        db.session.commit()
        logger.info(f"用户 {user_id} 删除交易记录成功, 交易ID: {id}")
        return jsonify({
            "success": True,
            "message": "交易记录删除成功",
            "data": {}
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"删除用户 {user_id} 的交易记录失败: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"交易记录删除失败: {str(e)}",
            "data": {}
        }), 500