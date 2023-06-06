"""add content to posts table

Revision ID: ac13e1a404fc
Revises: 1ed5f924f079
Create Date: 2023-06-06 16:31:49.212319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac13e1a404fc'
down_revision = '1ed5f924f079'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts',"content")
    pass
