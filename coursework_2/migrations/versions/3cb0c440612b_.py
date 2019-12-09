"""empty message

Revision ID: 3cb0c440612b
Revises: f9e81ece060b
Create Date: 2019-12-08 23:45:51.708869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3cb0c440612b'
down_revision = 'f9e81ece060b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password_last_update', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password_last_update')
    # ### end Alembic commands ###
