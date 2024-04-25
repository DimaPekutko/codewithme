"""empty message

Revision ID: 64dae6b2af13
Revises: b4c1a8528291
Create Date: 2024-04-08 21:26:11.406385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64dae6b2af13'
down_revision = 'b4c1a8528291'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_blocked', sa.Boolean(), server_default=sa.text('false'), nullable=False))
    op.add_column('users', sa.Column('rating', sa.Float(), server_default=sa.text('500'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'rating')
    op.drop_column('users', 'is_blocked')
    # ### end Alembic commands ###