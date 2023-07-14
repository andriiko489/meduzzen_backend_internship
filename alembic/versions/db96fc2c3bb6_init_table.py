"""init table

Revision ID: db96fc2c3bb6
Revises: 
Create Date: 2023-07-14 11:17:28.015954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db96fc2c3bb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.String(60), nullable=False),
        sa.Column('is_active', sa.Boolean),
    )


def downgrade() -> None:
    op.drop_table('users')
