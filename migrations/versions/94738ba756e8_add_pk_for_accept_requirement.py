"""add PK for accept_requirement

Revision ID: 94738ba756e8
Revises: e73c8ac63d20
Create Date: 2022-10-13 21:01:56.154649

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94738ba756e8'
down_revision = 'e73c8ac63d20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'accept_requirement', ['requirement_id', 'accept_user'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'accept_requirement', type_='unique')
    # ### end Alembic commands ###
