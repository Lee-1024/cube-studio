"""empty message

Revision ID: c77d1dbba5d1
Revises: 1932452d5690
Create Date: 2023-04-05 15:28:54.410012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c77d1dbba5d1'
down_revision = '1932452d5690'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chat_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=400), nullable=False),
    sa.Column('chat_id', sa.Integer(), nullable=True),
    sa.Column('query', sa.String(length=5000), nullable=False),
    sa.Column('answer', sa.String(length=5000), nullable=False),
    sa.Column('manual_feedback', sa.String(length=400), nullable=False),
    sa.Column('answer_status', sa.String(length=400), nullable=False),
    sa.Column('answer_cost', sa.String(length=400), nullable=False),
    sa.Column('err_msg', sa.String(length=5000), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('changed_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('chat', sa.Column('knowledge', sa.Text(), nullable=True))
    op.add_column('chat', sa.Column('tips', sa.String(length=4000), nullable=True))
    op.create_unique_constraint(None, 'chat', ['name'])
    op.drop_column('chat', 'pre_question')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('pre_question', mysql.TEXT(), nullable=True))
    op.drop_constraint(None, 'chat', type_='unique')
    op.drop_column('chat', 'tips')
    op.drop_column('chat', 'knowledge')
    op.drop_table('chat_log')
    # ### end Alembic commands ###
