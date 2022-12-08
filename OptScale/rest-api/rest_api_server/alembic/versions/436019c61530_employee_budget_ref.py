""""employee_budget_ref"

Revision ID: 436019c61530
Revises: 57a4d893f531
Create Date: 2020-02-19 08:04:08.313417

"""
from alembic import op
import sqlalchemy as sa
import uuid
import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql import table, column
from sqlalchemy import (update, String, select, Integer, LargeBinary, insert,
                        func)
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '436019c61530'
down_revision = '57a4d893f531'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('employee_ibfk_1', 'employee', type_='foreignkey')
    op.drop_column('employee', 'budget_id')
    op.add_column('budget', sa.Column(
        'employee_id', sa.String(length=36), nullable=True))
    op.create_foreign_key(
        'employee_budget_fk', 'budget', 'employee', ['employee_id'], ['id'])
    op.alter_column('partner', 'tags', existing_type=sa.TEXT(), nullable=False)
    bind = op.get_bind()
    session = Session(bind=bind)
    dt = datetime.datetime.utcnow().timestamp()
    budged_table = table('budget',
                         column('type', String(36)),
                         column('id', String(36)),
                         column('deleted_at', Integer))
    try:
        upd_stmt = update(budged_table).values(
            deleted_at=dt).where(
            budged_table.c.type.in_(['EMPLOYEE']))
        session.execute(upd_stmt)
        session.commit()
    finally:
        session.close()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('employee_budget_fk', 'budget', type_='foreignkey')
    op.drop_column('budget', 'employee_id')
    op.add_column('employee', sa.Column(
        'budget_id', sa.String(length=36), nullable=False))
    budget_id = str(uuid.uuid4())
    budget_table = table('budget',
                         column('deleted_at', Integer),
                         column('id', String(36)),
                         column('created_at', Integer),
                         column('budget', Integer))
    dt = datetime.datetime.utcnow().timestamp()
    ins_stmt = insert(budget_table).values(
        deleted_at=dt,
        id=budget_id,
        created_at=dt,
        budget=0
    )
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(ins_stmt)
    employee_table = table('employee',
                           column('id', String(36)),
                           column('budget_id', String(36))
                           )
    try:
        upd_stmt = update(employee_table).values(budget_id=budget_id)
        session.execute(upd_stmt)
        session.commit()
    finally:
        session.close()
    op.create_foreign_key(
        'employee_ibfk_1', 'employee', 'budget', ['budget_id'], ['id'])
    op.alter_column('partner', 'tags', existing_type=sa.TEXT(), nullable=True)
    # ### end Alembic commands ###