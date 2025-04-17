import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
# 导入并注册蓝图
from apis.login import login_bp
from apis.user import user_bp
from apis.transactions import transaction_bp
from apis.svg import svg_bp
from extensions import db, mail

# 加载 .env 配置
load_dotenv()
# 初始化 Flask 应用
app = Flask(__name__)

# 启用 CORS 允许跨域请求
CORS(app, supports_credentials=True)

# ====================
# 数据库配置
# ====================
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用对象修改追踪
# ====================
# 邮件配置（从 .env 读取）
# ====================
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'false').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# 设置JWT密钥
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')

# 绑定SQLAlchemy实例
db.init_app(app)
# 初始化Mail
mail.init_app(app)

# 注册 Blueprint（只注册一次）
app.register_blueprint(login_bp, url_prefix="/")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(transaction_bp, url_prefix="/transaction")
app.register_blueprint(svg_bp, url_prefix="/svg")

if __name__ == '__main__':
    app.run(host=os.getenv('APP_HOST'), port=int(os.getenv('APP_PORT')), debug=os.getenv('FLASK_DEBUG') == 'True')
