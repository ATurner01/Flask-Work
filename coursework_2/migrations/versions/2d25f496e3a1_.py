"""empty message

Revision ID: 2d25f496e3a1
Revises: 41f0262da3b8
Create Date: 2019-12-12 14:05:37.511809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d25f496e3a1'
down_revision = '41f0262da3b8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('image', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('book', 'image')
    # ### end Alembic commands ###
