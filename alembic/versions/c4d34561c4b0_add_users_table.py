"""add users table

Revision ID: c4d34561c4b0
Revises: ac13e1a404fc
Create Date: 2023-06-06 16:38:57.929830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4d34561c4b0'
down_revision = 'ac13e1a404fc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table("users")
    pass
