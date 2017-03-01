"""empty message

Revision ID: 71d4067e4748
Revises: ca0abd6ca8ef
Create Date: 2017-01-24 22:02:39.393423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71d4067e4748'
down_revision = 'ca0abd6ca8ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stage', sa.Column('date_created', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('stage', 'date_created')
    # ### end Alembic commands ###
