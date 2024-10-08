"""empty message

Revision ID: ceabcdc3c440
Revises: 49835bc90da3
Create Date: 2024-08-12 05:35:30.198085

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy_utils.types.ts_vector import TSVectorType

# revision identifiers, used by Alembic.
revision = 'ceabcdc3c440'
down_revision = '49835bc90da3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.add_column(sa.Column('application_tsv', TSVectorType(), sa.Computed('jsonb_to_tsvector(\'english\', "application_json", \'["string"]\')', persisted=True), nullable=True))
        batch_op.create_index('idx_application_tsv', ['application_tsv'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.drop_index('idx_application_tsv', postgresql_using='gin')
        batch_op.drop_column('application_tsv')
    # ### end Alembic commands ###
