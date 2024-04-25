"""empty message

Revision ID: c18b5570ef4a
Revises: e3cbf35e14eb
Create Date: 2024-03-10 10:58:31.153949

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'c18b5570ef4a'
down_revision = 'e3cbf35e14eb'
branch_labels = None
depends_on = None


def upgrade():
    register_strategy = postgresql.ENUM('default', 'google', name='registerstrategy')
    register_strategy.create(op.get_bind())
    op.add_column('users', sa.Column('register_strategy', sa.Enum('default', 'google', name='registerstrategy'), nullable=False))


def downgrade():
    op.drop_column('users', 'register_strategy')
    register_strategy = postgresql.ENUM('default', 'google', name='registerstrategy')
    register_strategy.drop(op.get_bind())