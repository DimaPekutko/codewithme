"""empty message

Revision ID: 102ce12cbb98
Revises: 8fef0d94a47b
Create Date: 2024-03-24 16:35:37.278269

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '102ce12cbb98'
down_revision = '8fef0d94a47b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('code_assertions_lang_problem_id_fkey', 'code_assertions', type_='foreignkey')
    op.create_foreign_key(None, 'code_assertions', 'lang_problems', ['lang_problem_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('lang_problems_problem_id_fkey', 'lang_problems', type_='foreignkey')
    op.create_foreign_key(None, 'lang_problems', 'problems', ['problem_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'lang_problems', type_='foreignkey')
    op.create_foreign_key('lang_problems_problem_id_fkey', 'lang_problems', 'problems', ['problem_id'], ['id'])
    op.drop_constraint(None, 'code_assertions', type_='foreignkey')
    op.create_foreign_key('code_assertions_lang_problem_id_fkey', 'code_assertions', 'lang_problems', ['lang_problem_id'], ['id'])
    # ### end Alembic commands ###
