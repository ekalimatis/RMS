"""delete realese

Revision ID: c33eb337a31a
Revises: aeb2a5c3186c
Create Date: 2022-11-02 15:21:34.205897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c33eb337a31a'
down_revision = 'aeb2a5c3186c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('requirement', 'release')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requirement', sa.Column('release', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
