from ducttapp.models import db
from flask_restplus import fields
from sqlalchemy.orm import relationship

user_role_table = db.Table(
    'user_role',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))
)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(256, collation='utf8mb4_general_ci', convert_unicode=True), nullable=True)
    users = relationship(
        "User",
        secondary=user_role_table,
        back_populates="roles")


class RoleSchema:
    role_res_schema = {
        'id': fields.Integer(),
        'role_name': fields.String()
    }
