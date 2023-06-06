"""create post table

Revision ID: 1ed5f924f079
Revises: 
Create Date: 2023-06-06 16:19:20.377493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ed5f924f079'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts",sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("title",sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
