from ducttapp.models import db
from .base import TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum


class Category(db.Model, TimestampMixin):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    users = relationship("UserCategoryAction", back_populates="category")

    def update_attr(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


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
