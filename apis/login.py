import bcrypt
import jwt
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from models import User, UserDetails, UserSvg, DefaultSvg,EmailCode
import random
import string
from flask_mail import Message
from extensions import db, mail


# 创建 Blueprint
login_bp = Blueprint('login', __name__)


# 注册用户
@login_bp.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')
        code = request.json.get('code')  # 获取前端提交的验证码

        if not username or not password or not email or not code:
            return jsonify({"success": False, "message": "用户名、密码、邮箱和验证码不能为空"}), 400

        # 检查验证码是否正确
        existing_code = EmailCode.query.filter_by(email=email).first()

        if not existing_code:
            return jsonify({"success": False, "message": "验证码无效或已过期"}), 400

        # 验证验证码是否过期（假设有效期为10分钟）
        if existing_code.created_at + timedelta(minutes=10) < datetime.now():
            return jsonify({"success": False, "message": "验证码已过期，请重新获取"}), 400

        if existing_code.code != code:
            return jsonify({"success": False, "message": "验证码错误"}), 400

        # 检查用户名或邮箱是否已存在
        if User.query.filter((User.username == username) | (User.email == email)).first():
            return jsonify({"success": False, "message": "用户名或邮箱已存在"}), 400

        # 加密密码
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 创建新用户
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.flush()  # 获取用户 ID

        # 创建用户详情
        new_user_details = UserDetails(user_id=new_user.id, nickname=username)
        db.session.add(new_user_details)

        # 赋予默认 SVG
        default_svgs = DefaultSvg.query.all()
        user_svgs = [UserSvg(user_id=new_user.id, svg_name=svg.svg_name, category=svg.category) for svg in default_svgs]
        db.session.bulk_save_objects(user_svgs)

        db.session.commit()  # 提交事务
        return jsonify({"success": True, "message": "注册成功，请登录"}), 201

    except Exception as e:
        db.session.rollback()  # 发生错误时回滚事务
        return jsonify({"success": False, "message": "注册失败，请重试", "error": str(e)}), 500

# 发送邮箱验证码
@login_bp.route('/send-email-code', methods=['POST'])
def send_email_code():
    try:
        email = request.json.get('email')

        if not email:
            return jsonify({"success": False, "message": "邮箱不能为空"}), 400

        # 验证邮箱是否已注册（可选逻辑）
        if User.query.filter_by(email=email).first():
            return jsonify({"success": False, "message": "该邮箱已注册,请重新输入"}), 400

        # 生成6位验证码
        code = ''.join(random.choices(string.digits, k=6))

        # 创建或更新验证码记录
        existing_code = EmailCode.query.filter_by(email=email).first()
        if existing_code:
            existing_code.code = code
            existing_code.created_at = datetime.now()
        else:
            new_code = EmailCode(email=email, code=code, created_at=datetime.now())
            db.session.add(new_code)

        db.session.commit()

        # 发送邮件
        subject = "您的验证码"
        body = f"您的验证码是：{code}，有效期为10分钟。请勿泄露。"

        msg = Message(subject=subject, recipients=[email], body=body)
        mail.send(msg)

        return jsonify({"success": True, "message": "验证码已发送,请查看邮箱..."}), 200

    except Exception as e:
        db.session.rollback()
        # 判断错误信息中是否包含 '550'，代表邮箱不存在
        if '550' in str(e):
            return jsonify({"success": False, "message": "邮箱不存在，请检查邮箱", "error": str(e)}), 500
        else:
            return jsonify({"success": False, "message": "验证码发送失败", "error": str(e)}), 500


# 登录接口
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

        # 查找用户
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # 生成JWT Token
            token = generate_token(user.id)

            # 获取用户详情
            user_details = UserDetails.query.filter_by(user_id=user.id).first()

            return jsonify({
                "success": True,
                "message": "登录成功",
                "data": {
                    "token": token,
                    "user_info": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "nickname": user_details.nickname if user_details else None,
                        "avatar": user_details.avatar if user_details else None,
                        "created_at": user_details.created_at if user_details else None
                    }
                }
            }), 200
        else:
            return jsonify({"success": False, "message": "用户名或密码错误"}), 401

    except Exception as e:
        return jsonify({"success": False, "message": "登录失败", "error": str(e)}), 500


# 生成JWT Token
def generate_token(user_id, days=30):
    expiration_time = datetime.now() + timedelta(days=days)
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration_time
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token
