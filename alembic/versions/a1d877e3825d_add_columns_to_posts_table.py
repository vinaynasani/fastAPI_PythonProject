"""add columns to posts table

Revision ID: a1d877e3825d
Revises: 2ba725f78bc9
Create Date: 2021-11-17 21:22:42.069088

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = 'a1d877e3825d'
down_revision = '2ba725f78bc9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','title')
    pass
