"""empty message

Revision ID: ade594101812
Revises: 2678c0df4ea6
Create Date: 2019-12-03 21:13:27.985234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ade594101812'
down_revision = '2678c0df4ea6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('like', sa.Column('comment_id', sa.Integer(), nullable=True))
    op.alter_column('like', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'like', 'comment', ['comment_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'like', type_='foreignkey')
    op.alter_column('like', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('like', 'comment_id')
    # ### end Alembic commands ###