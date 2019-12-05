"""empty message

Revision ID: 2678c0df4ea6
Revises: 9c76b54ba329
Create Date: 2019-12-03 16:32:36.805950

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2678c0df4ea6'
down_revision = '9c76b54ba329'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'like', 'users', ['user_id'], ['id'])
    op.create_foreign_key(None, 'post', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_constraint(None, 'like', type_='foreignkey')
    # ### end Alembic commands ###