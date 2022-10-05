"""add requirement, tree and project table

Revision ID: 9bf193d8079a
Revises: fd74e478c9a0
Create Date: 2022-10-01 21:24:40.487156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bf193d8079a'
down_revision = 'fd74e478c9a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requirement',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=240), nullable=True),
    sa.Column('requirement', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('update_date', sa.DateTime(), nullable=True),
    sa.Column('approve', sa.Boolean(), nullable=True),
    sa.Column('verify_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Enum('new', 'on_review', 'active', 'old', 'changed', name='requirement_status'), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('tags', sa.String(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('test_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('priorty_id', sa.Integer(), nullable=True),
    sa.Column('history_log', sa.Integer(), nullable=True),
    sa.Column('version', sa.String(length=20), nullable=True),
    sa.Column('type_id', sa.Integer(), nullable=True),
    sa.Column('release', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requirement_tree',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('requirement_id', sa.Integer(), nullable=True),
    sa.Column('lft', sa.Integer(), nullable=False),
    sa.Column('rgt', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('tree_id', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['requirement_tree.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('requirement_tree_level_idx', 'requirement_tree', ['level'], unique=False)
    op.create_index('requirement_tree_lft_idx', 'requirement_tree', ['lft'], unique=False)
    op.create_index('requirement_tree_rgt_idx', 'requirement_tree', ['rgt'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('requirement_tree_rgt_idx', table_name='requirement_tree')
    op.drop_index('requirement_tree_lft_idx', table_name='requirement_tree')
    op.drop_index('requirement_tree_level_idx', table_name='requirement_tree')
    op.drop_table('requirement_tree')
    op.drop_table('requirement')
    op.drop_table('project')
    # ### end Alembic commands ###