"""auto vote

Revision ID: faf2221eb807
Revises: 751ad500e206
Create Date: 2023-06-06 17:28:52.691011

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faf2221eb807'
down_revision = '751ad500e206'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.add_column('users', sa.Column('first_name', sa.String(), nullable=False))
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.drop_table('votes')
    # ### end Alembic commands ###
