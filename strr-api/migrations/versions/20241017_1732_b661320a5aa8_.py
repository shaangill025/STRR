"""empty message

Revision ID: b661320a5aa8
Revises: a6abe20bd998
Create Date: 2024-10-17 17:32:27.050843

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b661320a5aa8'
down_revision = 'a6abe20bd998'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('property_manager',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('business_legal_name', sa.String(length=250), nullable=True),
    sa.Column('business_number', sa.String(length=100), nullable=True),
    sa.Column('business_mailing_address_id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['business_mailing_address_id'], ['addresses.id'], name=op.f('fk_property_manager_business_mailing_address_id_addresses')),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], name=op.f('fk_property_manager_contact_id_contacts')),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], name=op.f('fk_property_manager_created_by_id_users')),
    sa.ForeignKeyConstraint(['modified_by_id'], ['users.id'], name=op.f('fk_property_manager_modified_by_id_users')),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    op.create_table('property_manager_history',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('business_legal_name', sa.String(length=250), autoincrement=False, nullable=True),
    sa.Column('business_number', sa.String(length=100), autoincrement=False, nullable=True),
    sa.Column('business_mailing_address_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('contact_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('created', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('modified', sa.DateTime(), autoincrement=False, nullable=True),
    sa.Column('created_by_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('modified_by_id', sa.Integer(), autoincrement=False, nullable=True),
    sa.Column('version', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('changed', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['business_mailing_address_id'], ['addresses.id'], name=op.f('fk_property_manager_business_mailing_address_id_addresses')),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], name=op.f('fk_property_manager_contact_id_contacts')),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], name=op.f('fk_property_manager_created_by_id_users')),
    sa.ForeignKeyConstraint(['modified_by_id'], ['users.id'], name=op.f('fk_property_manager_modified_by_id_users')),
    sa.PrimaryKeyConstraint('id', 'version'),
    sqlite_autoincrement=True
    )

    with op.batch_alter_table('rental_properties', schema=None) as batch_op:
        batch_op.add_column(sa.Column('property_manager_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_rental_properties_property_manager_id_property_manager'), 'property_manager', ['property_manager_id'], ['id'])

    with op.batch_alter_table('rental_properties_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('property_manager_id', sa.Integer(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_rental_properties_property_manager_id_property_manager'), 'property_manager', ['property_manager_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    with op.batch_alter_table('rental_properties_history', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_rental_properties_property_manager_id_property_manager'), type_='foreignkey')
        batch_op.drop_column('property_manager_id')

    with op.batch_alter_table('rental_properties', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_rental_properties_property_manager_id_property_manager'), type_='foreignkey')
        batch_op.drop_column('property_manager_id')

    op.drop_table('property_manager_history')
    op.drop_table('property_manager')
    # ### end Alembic commands ###