""""optscale_models"

Revision ID: 57a4d893f531
Revises: b2b5f61c00be
Create Date: 2020-01-09 15:01:15.991885

"""
import datetime
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

revision = '57a4d893f531'
down_revision = '1cfd9a637d65'
branch_labels = None
depends_on = None


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'cloudcredentials',
        sa.Column('deleted_at', sa.Integer(), nullable=False),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('type', sa.Enum(
            'OPENSTACK', 'OPENSTACK_CNR', 'OPENSTACK_HUAWEI_CNR',
            'AWS_CNR', 'ALIBABA_CNR', 'VMWARE_CNR', 'AZURE_CNR',
            'FAKE'), nullable=False),
        sa.Column('cloud_credentials', sa.TEXT, nullable=False),
        sa.Column('business_unit_id', sa.String(length=36), nullable=False),
        sa.ForeignKeyConstraint(['business_unit_id'], ['partner.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'budget',
        sa.Column('deleted_at', sa.Integer(), nullable=False),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('budget', sa.BIGINT(), nullable=False),
        sa.Column('parent_id', sa.String(length=36), nullable=True),
        sa.Column('type', sa.Enum('PROJECT', 'BUSINESS_UNIT', 'EMPLOYEE'),
                  nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['budget.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'employee',
        sa.Column('deleted_at', sa.Integer(), nullable=False),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('tags', sa.TEXT(), nullable=False),
        sa.Column('business_unit_id', sa.String(length=36), nullable=False),
        sa.Column('budget_id', sa.String(length=36), nullable=False),
        sa.Column('auth_user_id', sa.String(length=36), nullable=True),
        sa.ForeignKeyConstraint(['budget_id'], ['budget.id'], ),
        sa.ForeignKeyConstraint(['business_unit_id'], ['partner.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'project',
        sa.Column('deleted_at', sa.Integer(), nullable=False),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('tags', sa.TEXT(), nullable=False),
        sa.Column('business_unit_id', sa.String(length=36), nullable=False),
        sa.Column('budget_id', sa.String(length=36), nullable=False),
        sa.Column('starting_date', sa.Integer(), nullable=False),
        sa.Column('completion_date', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['budget_id'], ['budget.id'], ),
        sa.ForeignKeyConstraint(['business_unit_id'], ['partner.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'projectemployee',
        sa.Column('project_id', sa.String(length=36), nullable=False),
        sa.Column('employee_id', sa.String(length=36), nullable=False),
        sa.Column('project_role', sa.Enum('MEMBER', 'ADMIN', 'OWNER'),
                  nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], ),
        sa.PrimaryKeyConstraint('project_id', 'employee_id')
    )
    op.create_table(
        'resource',
        sa.Column('deleted_at', sa.Integer(), nullable=False),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('cloud_resource_id', sa.String(length=256), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('employee_id', sa.String(length=36), nullable=True),
        sa.Column('cloud_credentials_id', sa.String(length=36), nullable=False),
        sa.Column('budget_id', sa.String(length=36), nullable=True),
        sa.Column('resource_type', sa.String(length=256), nullable=False),
        sa.ForeignKeyConstraint(['budget_id'], ['budget.id'], ),
        sa.ForeignKeyConstraint(['cloud_credentials_id'], ['cloudcredentials.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('partner', sa.Column('budget_id', sa.String(length=36),
                                       nullable=False))
    op.add_column('partner', sa.Column('created_at', sa.TIMESTAMP(),
                                       nullable=False))
    op.add_column('partner', sa.Column('parent_id', sa.String(length=36),
                                       nullable=True))
    op.add_column('partner', sa.Column('tags', sa.TEXT(), nullable=True))

    budget_table = sa.table(
        'budget',
        sa.column('deleted_at', sa.Integer()),
        sa.column('id', sa.String(36)),
        sa.column('created_at', sa.Integer()),
        sa.column('budget', sa.BIGINT()),
        sa.column('parent_id', sa.String(36)),
        sa.column('type', sa.Enum('PROJECT', 'BUSINESS_UNIT', 'EMPLOYEE')),
    )

    partners_table = sa.table(
        'partner',
        sa.column('id', sa.String(36)),
        sa.column('budget_id', sa.String(36)),
    )

    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        budgets = []
        updates = {}
        for row in session.execute(partners_table.select()):
            budget_dict = {
                'deleted_at': 0,
                'id': str(uuid.uuid4()),
                'created_at': int(datetime.datetime.utcnow().timestamp()),
                'budget': 0,
                'parent_id': None,
                'type': 'BUSINESS_UNIT'
            }
            budgets.append(budget_dict)
            updates[row['id']] = budget_dict['id']

        op.bulk_insert(budget_table, budgets)

        for partner_id, budget_id in updates.items():
            session.execute(sa.update(partners_table).values(
                budget_id=budget_id).where(partners_table.c.id == partner_id))
        session.commit()
    finally:
        session.close()

    op.create_foreign_key('partner_budget_fk', 'partner', 'budget',
                          ['budget_id'], ['id'])
    op.create_foreign_key('partner_partner_fk', 'partner', 'partner',
                          ['parent_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('partner_budget_fk', 'partner', type_='foreignkey')
    op.drop_constraint('partner_partner_fk', 'partner', type_='foreignkey')
    op.drop_column('partner', 'tags')
    op.drop_column('partner', 'parent_id')
    op.drop_column('partner', 'created_at')
    op.drop_column('partner', 'budget_id')
    op.drop_table('resource')
    op.drop_table('projectemployee')
    op.drop_table('project')
    op.drop_table('employee')
    op.drop_table('cloudcredentials')
    op.drop_table('budget')
    # ### end Alembic commands ###
