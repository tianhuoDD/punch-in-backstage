from extensions import db, mail
from datetime import datetime

# 用户表
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
# 用户详情表
class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)  # 外键
    nickname = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(255), nullable=True) # 存储头像的相对路径
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
# 账单表
class Transaction(db.Model):
    __tablename__ = 'transactions'  # 避免SQL关键字冲突

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    svg = db.Column(db.String(50))
    account = db.Column(db.String(50), nullable=False)
    income = db.Column(db.Float)
    expense = db.Column(db.Float)
    remark = db.Column(db.String(255))

    # 添加 user_id 字段
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 外键关联到 users 表
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))  # 关系映射

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "svg": self.svg,
            "account": self.account,
            "income": self.income,
            "expense": self.expense,
            "remark": self.remark,
            "user_id": self.user_id
        }
# SVG表
class SVG(db.Model):
    __tablename__ = 'svgs'  # 数据库表名

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='SVG 图标 ID')
    svg_name = db.Column(db.String(255), unique=True, nullable=False, comment='图标名称')
    category = db.Column(db.String(255), nullable=False, comment='分类名称')

    def to_dict(self):
        """
        转换为字典格式，便于 JSON 序列化
        """
        return {
            "id": self.id,
            "svg_name": self.svg_name,
            "category": self.category
        }

    def __repr__(self):
        return f'<SVG {self.svg_name} ({self.category})>'
# 默认 SVG 表
class DefaultSvg(db.Model):
    __tablename__ = 'default_svgs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="-- 默认SVG表")
    svg_name = db.Column(db.String(255), nullable=False, unique=True, comment="SVG 名称")
    category = db.Column(db.String(255), nullable=False, comment="分类名称")

    def __repr__(self):
        return f"<DefaultSvg(id={self.id}, svg_name={self.svg_name}, category={self.category})>"

# 用户 SVG 表
class UserSvg(db.Model):
    __tablename__ = 'user_svgs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="-- 用户的SVG配置")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False, comment="用户 ID")
    svg_name = db.Column(db.String(255), nullable=False, comment="SVG 名称")
    category = db.Column(db.String(255), nullable=False, comment="分类名称")

    user = db.relationship('User', backref=db.backref('user_svgs', cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<UserSvg(id={self.id}, user_id={self.user_id}, svg_name={self.svg_name}, category={self.category})>"

class EmailCode(db.Model):
    __tablename__ = 'email_codes'  # 数据库中的表名

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)