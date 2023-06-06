"""add last few columns to posts table

Revision ID: 751ad500e206
Revises: 560ea4c18234
Create Date: 2023-06-06 17:15:57.814479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '751ad500e206'
down_revision = '560ea4c18234'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("published" , sa.Boolean(),nullable=False,
                                     server_default='TRUE'))
    op.add_column('posts' ,sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('NOW()'),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts',"created_at")
    pass
