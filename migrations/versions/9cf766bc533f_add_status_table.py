"""add status table

Revision ID: 9cf766bc533f
Revises: 9771b612179c
Create Date: 2022-10-05 00:26:01.501216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cf766bc533f'
down_revision = '9771b612179c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('requirement_statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requirement_statuses')
    # ### end Alembic commands ###
