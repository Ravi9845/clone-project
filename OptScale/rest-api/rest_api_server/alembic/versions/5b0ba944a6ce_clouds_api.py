""""clouds_api"

Revision ID: 5b0ba944a6ce
Revises: 53cb39787ea5
Create Date: 2018-04-20 13:08:02.237249

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
from sqlalchemy.orm import Session

revision = '5b0ba944a6ce'
down_revision = '53cb39787ea5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cloud',
    sa.Column('deleted_at', sa.Integer(), nullable=False),
    sa.Column('id', sa.String(36), nullable=False),
    sa.Column('type', sa.Enum('OPENSTACK',), nullable=False),
    sa.Column('name', sa.String(256), nullable=False),
    sa.Column('endpoint', sa.String(256), nullable=False),
    sa.Column('username', sa.String(256), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('salt', sa.String(36), nullable=False),
    sa.Column('extra_args', sa.TEXT(), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    )
    bind = op.get_bind()
    session = Session(bind=bind)
    to_dynamic_stmt = "ALTER TABLE `cloud` ROW_FORMAT=DYNAMIC;"
    session.execute(to_dynamic_stmt)
    session.close()
    op.create_unique_constraint(
        'uc_cloud_name_del_at', 'cloud', ['name', 'deleted_at'])
    op.add_column('customer', sa.Column(
        'cloud_id', sa.String(length=36), nullable=True))
    op.create_foreign_key(
        'fk_customer_cloud_id', 'customer', 'cloud', ['cloud_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_customer_cloud_id', 'customer', type_='foreignkey')
    op.drop_constraint('uc_cloud_name_del_at', 'cloud', type_='unique')
    op.drop_column('customer', 'cloud_id')
    op.drop_table('cloud')
    # ### end Alembic commands ###
