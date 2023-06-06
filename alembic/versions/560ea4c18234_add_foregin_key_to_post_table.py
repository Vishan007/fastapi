"""add foregin key to post table

Revision ID: 560ea4c18234
Revises: c4d34561c4b0
Create Date: 2023-06-06 16:49:43.541859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '560ea4c18234'
down_revision = 'c4d34561c4b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts',"owner_id")
    pass
