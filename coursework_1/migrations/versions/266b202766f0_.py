"""empty message

Revision ID: 266b202766f0
Revises: a157eda96822
Create Date: 2019-10-14 23:59:10.386064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '266b202766f0'
down_revision = 'a157eda96822'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('dateCompleted', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('task', 'dateCompleted')
    # ### end Alembic commands ###
