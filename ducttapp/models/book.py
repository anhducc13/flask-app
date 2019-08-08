from ducttapp.models import db, LogAction, category_book_table
from .base import TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy import func
from datetime import datetime


class Book(db.Model, TimestampMixin):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255, convert_unicode=True), nullable=False, unique=True)
    author = db.Column(db.Text(convert_unicode=True), nullable=True)
    description = db.Column(db.Text(convert_unicode=True), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    star = db.Column(db.SmallInteger, default=5)
    price = db.Column(db.Float, nullable=False)
    quantity_in_stock = db.Column(db.Integer, nullable=False)
    quantity_sold = db.Column(db.Integer, default=0)
    users = relationship("UserBookAction", back_populates="book")
    categories = relationship(
        "Category",
        secondary=category_book_table,
        back_populates="books")

    def update_attr(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'quantity_in_stock': self.quantity_in_stock,
            'price': self.price,
        }


class UserBookAction(db.Model):
    __tablename__ = 'book_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'))
    log_name = db.Column(db.Enum(LogAction), nullable=False, default=LogAction.UPDATED)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now(), default=func.now(), nullable=False)
    book = relationship("Book", back_populates="users")
    user = relationship("User", back_populates="books")
