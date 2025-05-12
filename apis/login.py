import bcrypt
import jwt
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from models import User, UserDetails, UserSvg, DefaultSvg,EmailCode
import random
import string
from flask_mail import Message
from extensions import db, mail
from decrypt_key import rsa_decrypt_pkcs1v15

# 创建 Blueprint
login_bp = Blueprint('login', __name__)

# 登录
@login_bp.route('/login', methods=['POST'])
def login():
    try:
        username_or_email = request.json.get('username')
        password = request.json.get('password')

        if not username_or_email or not password:
            return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

        decrpty_password=rsa_decrypt_pkcs1v15(password)
        # 使用用户名或邮箱进行查找
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        if user and bcrypt.checkpw(decrpty_password.encode('utf-8'), user.password.encode('utf-8')):
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
# 注册
@login_bp.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')

        if not username or not password or not email:
            return jsonify({"success": False, "message": "用户名、密码、邮箱和验证码不能为空"}), 400

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

# 重置密码
@login_bp.route('/reset-password', methods=['POST'])
def forget_password():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        code=request.json.get('code')

        # 验证验证码是否成功
        verification_result = verify_email_code(email, code)
        # 如果验证码验证失败，直接返回错误信息
        if not verification_result['success']:
            return jsonify(verification_result), 400

        if not email or not password:
            return jsonify({"success": False, "message": "邮箱、密码不能为空"}), 400

        # 查询用户
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"success": False, "message": "该邮箱未注册"}), 404

        # 更新密码（加密）
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        return jsonify({"success": True, "message": "密码修改成功，请登录"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "密码修改失败，请重试", "error": str(e)}), 500

# 验证邮箱验证码
@login_bp.route('/verify-email-code', methods=['POST'])
def verify_code():
    email = request.json.get('email')
    code = request.json.get('code')
    return verify_email_code(email,code)

# 发送邮箱验证码
@login_bp.route('/send-email-code', methods=['POST'])
def send_email_code():
    try:
        email = request.json.get('email')
        repeatability = request.json.get('repeatability', True)  # 如果没有提供 repeatability，默认为 True

        if not email:
            return jsonify({"success": False, "message": "邮箱不能为空"}), 400

        # 验证邮箱是否已注册（可选逻辑）
        if User.query.filter_by(email=email).first() and repeatability:
            return jsonify({"success": False, "message": "该邮箱已注册,请重新输入"}), 400

        # 生成6位验证码
        code = ''.join(random.choices(string.digits, k=6))

        # 删除已有的验证码记录（如果有）
        EmailCode.query.filter_by(email=email).delete()

        # 每次都新增一条记录
        new_code = EmailCode(email=email, code=code, created_at=datetime.now())
        db.session.add(new_code)

        db.session.commit()

        # 发送邮件
        subject = "【PunchIn】您的验证码"
        body = f"尊敬的用户，您好！\n\n您的验证码是：{code}，有效期为10分钟。请在有效期内完成操作，避免验证码失效。\n\n请勿将验证码泄露给他人。\n\n—— PunchIn官方(romcere.top)"

        msg = Message(subject=subject, recipients=[email], body=body)
        mail.send(msg)

        return jsonify({"success": True, "message": "验证码已发送,请查看邮箱..."}), 200

    except Exception as e:
        db.session.rollback()
        # 判断错误信息中是否包含 '550'，代表邮箱不存在
        if '550' in str(e):
            return jsonify({"success": False, "message": "邮箱不存在，请检查邮箱", "error": str(e)}), 500
        else:
            return jsonify({"success": False, "message": "验证码发送失败，请重试", "error": str(e)}), 500


# 验证邮箱验证码
def verify_email_code(email,code):
    existing_code = EmailCode.query.filter_by(email=email).first()

    if not existing_code:
        return {
            "success": False,
            "message": "验证码无效或已过期",
            "data": {}
        }

    if existing_code.created_at + timedelta(minutes=10) < datetime.now():
        return {
            "success": False,
            "message": "验证码已过期，请重新获取",
            "data": {}
        }

    if existing_code.code != code:
        return {
            "success": False,
            "message": "验证码错误",
            "data": {}
        }

    return {
        "success": True,
        "message": "验证成功",
        "data": {}
    }
# 生成JWT Token
def generate_token(user_id, days=30):
    expiration_time = datetime.now() + timedelta(days=days)
    token = jwt.encode({
        'user_id': user_id,
        'exp': expiration_time
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

