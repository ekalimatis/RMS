"""add accept_table

Revision ID: fb525c3ebafb
Revises: 9b6cd2d5545c
Create Date: 2022-10-12 09:18:30.700290

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb525c3ebafb'
down_revision = '9b6cd2d5545c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accept_requirement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requirement_id', sa.Integer(), nullable=False),
    sa.Column('accept_user', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['accept_user'], ['user.id'], ),
    sa.ForeignKeyConstraint(['requirement_id'], ['requirement.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('requirement', sa.Column('requirement_node_id', sa.Integer(), nullable=True))
    op.drop_constraint('requirement_requirement_id_fkey', 'requirement', type_='foreignkey')
    op.create_foreign_key(None, 'requirement', 'requirement_tree', ['requirement_node_id'], ['id'])
    op.drop_column('requirement', 'requirement_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('requirement', sa.Column('requirement_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'requirement', type_='foreignkey')
    op.create_foreign_key('requirement_requirement_id_fkey', 'requirement', 'requirement_tree', ['requirement_id'], ['id'])
    op.drop_column('requirement', 'requirement_node_id')
    op.drop_table('accept_requirement')
    # ### end Alembic commands ###
