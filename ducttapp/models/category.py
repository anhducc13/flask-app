from ducttapp.models import db
from .base import TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum
from datetime import datetime


class Category(db.Model, TimestampMixin):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(collation='utf8mb4_general_ci', convert_unicode=True), nullable=False)
    description = db.Column(db.Text(collation='utf8mb4_general_ci', convert_unicode=True), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    users = relationship("UserCategoryAction", back_populates="category", cascade="all, delete-orphan")

    def update_attr(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.updated_at = datetime.now()

    def to_dict(self):
        from ducttapp.models import User, UserCategoryAction
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'user_created': db.session.query(
                User
            ).filter(
                self.id == UserCategoryAction.category_id
            ).filter(
                UserCategoryAction.log_name == CategoryAction.CREATED
            ).filter(
                User.id == UserCategoryAction.user_id
            ).first().username or ""
        }


class CategoryAction(enum.Enum):
    CREATED = 'CREATED'
    UPDATED = 'UPDATED'


class UserCategoryAction(db.Model):
    __tablename__ = 'category_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'))
    log_name = db.Column(db.Enum(CategoryAction), nullable=False, default=CategoryAction.UPDATED)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now(), default=func.now(), nullable=False)
    category = relationship("Category", back_populates="users")
    user = relationship("User", back_populates="categories")

    def to_dict(self):
        from ducttapp.models import User
        return {
            'id': self.id,
            'log_name': self.log_name.value,
            'created_at': self.created_at,
            'username': db.session.query(
                User
            ).filter(
                self.user_id == User.id
            ).first().username or ""
        }
