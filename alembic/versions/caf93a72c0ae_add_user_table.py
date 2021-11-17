"""Add user table

Revision ID: caf93a72c0ae
Revises: a1d877e3825d
Create Date: 2021-11-17 21:32:39.050008

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null



# revision identifiers, used by Alembic.
revision = 'caf93a72c0ae'
down_revision = 'a1d877e3825d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id',sa.Integer(),nullable=False, primary_key=True),sa.Column('email',sa.String(),nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at',sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False), sa.PrimaryKeyConstraint('id'),sa.UniqueConstraint('email'))


def downgrade():
    op.drop_table('users')
    pass
