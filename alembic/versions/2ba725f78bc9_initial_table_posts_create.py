"""Initial table - posts - create

Revision ID: 2ba725f78bc9
Revises: 
Create Date: 2021-11-17 21:11:46.755070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ba725f78bc9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False,primary_key=True), sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
