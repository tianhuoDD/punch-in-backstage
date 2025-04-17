from flask import Blueprint, request, jsonify
from models import SVG,UserSvg  # 确保模型导入正确
from auth import token_required  # 令牌认证装饰器
from extensions import db
# 创建 Blueprint
svg_bp = Blueprint('svg', __name__)
# 获取所有svg
@svg_bp.route('/', methods=['GET'])
@token_required
def get_svgs(decoded):
    """
    获取所有 SVG 图标列表，返回扁平化的数组列表
    """
    try:
        # 获取所有 SVG 图标
        svgs = SVG.query.all()

        # 直接转换为扁平化的 JSON 数组
        svg_list = [{"id": svg.id, "svg_name": svg.svg_name, "category": svg.category} for svg in svgs]

        return jsonify({
            "success": True,
            "message": "获取SVG成功",
            "data": svg_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取SVG失败: {str(e)}",
            "data": []
        }), 500


# 获取用户的svg
@svg_bp.route('/user', methods=['GET'])
@token_required
def get_user_svgs(decoded):
    """
    获取用户 SVG 图标列表，仅返回用户自己的 SVG
    """
    try:
        user_id = decoded["user_id"]

        # 仅获取该用户的 SVG 图标
        user_svgs = UserSvg.query.filter_by(user_id=user_id).all()

        # 转换为扁平化的列表格式
        svg_list = [{"id": svg.id, "svg_name": svg.svg_name, "category": svg.category} for svg in user_svgs]


        return jsonify({
            "success": True,
            "message": "获取用户SVG成功",
            "data": svg_list
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"获取用户SVG失败: {str(e)}",
            "data": []
        }), 500



# 根据用户添加svg图标
@svg_bp.route('/user-svg', methods=['POST'])
@token_required
def add_svg(decoded):
    """
    允许用户添加新的 SVG 图标
    """
    try:
        user_id = decoded["user_id"]
        data = request.get_json()
        svg_name = data.get("svg_name")
        category = data.get("category")

        if not svg_name or not category:
            return jsonify({
                "success": False,
                "message": "svg_name 和 category 不能为空",
                "data": {}
            }), 400

        # 创建新的 SVG 记录
        new_svg = UserSvg(user_id=user_id, svg_name=svg_name, category=category)
        db.session.add(new_svg)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "SVG 添加成功",
            "data": {
                "id": new_svg.id,
                "svg_name": new_svg.svg_name,
                "category": new_svg.category
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"SVG 添加失败: {str(e)}",
            "data": {}
        }), 500


# 更新用户的 SVG
@svg_bp.route('/user-svg/<int:svg_id>', methods=['PUT'])
@token_required
def update_svg(decoded, svg_id):
    """
    允许用户更新自己的 SVG 图标
    """
    try:
        user_id = decoded["user_id"]
        data = request.get_json()
        svg_name = data.get("svg_name")
        category = data.get("category")

        if not svg_name or not category:
            return jsonify({
                "success": False,
                "message": "svg_name 和 category 不能为空",
                "data": {}
            }), 400

        # 查询用户的 SVG 记录
        user_svg = UserSvg.query.filter_by(id=svg_id, user_id=user_id).first()

        if not user_svg:
            return jsonify({
                "success": False,
                "message": "未找到对应的 SVG 或无权限修改",
                "data": {}
            }), 404

        # 更新 SVG 记录
        user_svg.svg_name = svg_name
        user_svg.category = category
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "SVG 更新成功",
            "data": {
                "id": user_svg.id,
                "svg_name": user_svg.svg_name,
                "category": user_svg.category
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"SVG 更新失败: {str(e)}",
            "data": {}
        }), 500
