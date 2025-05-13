import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify, current_app
from utils.models import User, UserDetails
from utils.auth import token_required  # 确保用户已登录
from utils.extensions import db
from utils.logger import logger  # 新增引入日志模块

# 创建用户蓝图
user_bp = Blueprint('user', __name__)

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# 判断文件是否是允许的类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 用户头像上传 API
@user_bp.route('/upload_avatar', methods=['POST'])
@token_required
def upload_avatar(decoded_data):
    user_id = decoded_data['user_id']  # 获取用户 ID
    if 'avatar' not in request.files:
        logger.warning(f"用户 {user_id} 上传头像失败: 未找到文件")
        return jsonify({"success": False, "message": "未找到文件", "data": {}}), 400

    file = request.files['avatar']
    if file.filename == '':
        logger.warning(f"用户 {user_id} 上传头像失败: 未选择文件")
        return jsonify({"success": False, "message": "未选择文件", "data": {}}), 400

    if file and allowed_file(file.filename):
        # 生成安全的文件名
        filename = secure_filename(f"user_{user_id}_{file.filename}")

        # 设置文件存储路径
        upload_folder = os.path.join(current_app.root_path, 'static/uploads/avatars')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)  # 如果文件夹不存在则创建

        # 保存文件
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # 存储相对路径
        avatar_path = f"static/uploads/avatars/{filename}"

        # 更新数据库
        user_details = UserDetails.query.filter_by(user_id=user_id).first()
        if not user_details:
            logger.warning(f"用户 {user_id} 上传头像失败: 用户详情不存在")
            return jsonify({"success": False, "message": "用户详情不存在", "data": {}}), 404

        user_details.avatar = avatar_path
        db.session.commit()

        logger.info(f"用户 {user_id} 上传头像成功: {avatar_path}")
        return jsonify({
            "success": True,
            "message": "头像上传成功",
            "data": {"avatar_url": avatar_path}
        }), 200
    else:
        logger.warning(f"用户 {user_id} 上传头像失败: 文件类型不允许")
        return jsonify({"success": False, "message": "文件类型不允许，仅支持 png, jpg, jpeg, gif", "data": {}}), 400


# 修改昵称
@user_bp.route('/update_nickname', methods=['POST'])
@token_required
def update_nickname(decoded_data):
    user_id = decoded_data['user_id']  # 从 JWT token 获取 user_id
    new_nickname = request.json.get('nickname')

    if not new_nickname:
        logger.warning(f"用户 {user_id} 修改昵称失败: 新昵称不能为空")
        return jsonify({"success": False, "message": "新昵称不能为空", "data": {}}), 400

    # 查找用户详情并更新
    user_details = UserDetails.query.filter_by(user_id=user_id).first()
    if user_details:
        user_details.nickname = new_nickname
    else:
        logger.warning(f"用户 {user_id} 修改昵称失败: 用户详情不存在")
        return jsonify({"success": False, "message": "用户详情不存在", "data": {}}), 404

    db.session.commit()
    logger.info(f"用户 {user_id} 修改昵称成功: {new_nickname}")
    return jsonify({"success": True, "message": "昵称修改成功", "data": {"nickname": new_nickname}}), 200


# 修改邮箱
@user_bp.route('/update_email', methods=['POST'])
@token_required
def update_email(decoded_data):
    user_id = decoded_data['user_id']  # 从 JWT token 获取 user_id
    new_email = request.json.get('email')

    if not new_email:
        logger.warning(f"用户 {user_id} 修改邮箱失败: 新邮箱不能为空")
        return jsonify({"success": False, "message": "新邮箱不能为空", "data": {}}), 400

    # 检查邮箱是否已存在
    existing_user = User.query.filter_by(email=new_email).first()
    if existing_user:
        logger.warning(f"用户 {user_id} 修改邮箱失败: 该邮箱已被使用")
        return jsonify({"success": False, "message": "该邮箱已被使用", "data": {}}), 400

    # 查找用户并更新邮箱
    user = User.query.get(user_id)
    if user:
        user.email = new_email
    else:
        logger.warning(f"用户 {user_id} 修改邮箱失败: 用户不存在")
        return jsonify({"success": False, "message": "用户不存在", "data": {}}), 404

    db.session.commit()
    logger.info(f"用户 {user_id} 修改邮箱成功: {new_email}")
    return jsonify({"success": True, "message": "邮箱修改成功", "data": {"email": new_email}}), 200