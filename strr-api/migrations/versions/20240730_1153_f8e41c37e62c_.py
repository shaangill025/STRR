"""empty message

Revision ID: f8e41c37e62c
Revises: 0be766af65ea
Create Date: 2024-07-30 11:53:07.590949

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f8e41c37e62c'
down_revision = '0be766af65ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registrations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expiry_date', sa.DateTime(), nullable=True))
        batch_op.drop_column('end_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('registrations', schema=None) as batch_op:
        batch_op.drop_column('expiry_date')
    # ### end Alembic commands ###
