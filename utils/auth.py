# auth.py
import jwt
from flask import request, jsonify, current_app
from functools import wraps


# 验证 Token 的函数
def verify_token():
    token = None
    # 检查 Authorization 头部是否存在
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"success": False, "message": "Token不存在, 请重新登录!", "data": {"token":False}}), 403
    # 检查是否是 "Bearer <token>" 格式
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        return jsonify({"success": False, "message": "Token格式不正确", "data": {"token":False}}), 403
    token = parts[1]  # 获取 token
    try:
        # 解码 Token 并验证签名
        decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Token已过期, 请重新登录!", "data": {"token":False}}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "无效的Token, 请重新登录!", "data": {"token":False}}),401


# 装饰器：用来保护需要验证 Token 的路由
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        decoded = verify_token()  # 验证 Token
        if isinstance(decoded, tuple):  # 如果返回的是错误信息，则直接返回
            return decoded
        return f(decoded, *args, **kwargs)  # 如果验证通过，将解码后的数据传递给视图函数

    return decorated_function
