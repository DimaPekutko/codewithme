"""empty message

Revision ID: bf8938aeebb1
Revises: 64dae6b2af13
Create Date: 2024-04-14 15:41:24.653756

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bf8938aeebb1"
down_revision = "64dae6b2af13"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "games",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user1_id", sa.Integer(), nullable=False),
        sa.Column("user2_id", sa.Integer(), nullable=False),
        sa.Column("winner_id", sa.Integer(), nullable=False),
        sa.Column("lang_problem_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.Enum("active", "finished", name="gamestatus"), nullable=False),
        sa.ForeignKeyConstraint(["lang_problem_id"], ["lang_problems.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user1_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user2_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["winner_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "runtimes",
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("lang_problem_id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=True),
        sa.Column("seconds_passed", sa.Integer(), nullable=True),
        sa.Column("status", sa.Enum("processing", "completed", "failed", name="runtimestatus"), nullable=False),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["lang_problem_id"], ["lang_problems.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("runtimes")
    op.drop_table("games")
    # ### end Alembic commands ###
