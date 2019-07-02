"""empty message

Revision ID: 54c363e4e76a
Revises: d7b0b3edaa40
Create Date: 2019-07-02 20:57:51.076613

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '54c363e4e76a'
down_revision = 'd7b0b3edaa40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_token', 'expired_time',
               existing_type=mysql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_token', 'expired_time',
               existing_type=mysql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
