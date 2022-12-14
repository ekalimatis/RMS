"""default value fix

Revision ID: 9771b612179c
Revises: 697e0a8c7e9a
Create Date: 2022-10-03 22:02:07.661638

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9771b612179c'
down_revision = '697e0a8c7e9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project', 'created_date',
               existing_type=postgresql.TIMESTAMP(),
               server_default=sa.text("(now() at time zone 'utc0')"),
               nullable=False)
    op.alter_column('requirement', 'created_date',
               existing_type=postgresql.TIMESTAMP(),
               server_default=sa.text("(now() at time zone 'utc0')"),
               nullable=False)
    op.alter_column('requirement', 'update_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('requirement', 'update_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('requirement', 'created_date',
               existing_type=postgresql.TIMESTAMP(),
               server_default=None,
               nullable=True)
    op.alter_column('project', 'created_date',
               existing_type=postgresql.TIMESTAMP(),
               server_default=None,
               nullable=True)
    # ### end Alembic commands ###
