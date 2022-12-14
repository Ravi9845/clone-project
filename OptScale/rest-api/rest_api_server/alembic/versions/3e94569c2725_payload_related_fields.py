""""payload_related_fields"

Revision ID: 3e94569c2725
Revises: 78f19da81b1e
Create Date: 2017-07-02 22:44:02.943428

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3e94569c2725'
down_revision = '78f19da81b1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('drive', sa.Column('payload_connection_info', sa.TEXT(), nullable=True))
    op.add_column('drive', sa.Column('payload_volume_id', sa.String(length=36), nullable=True))
    op.add_column('drive', sa.Column('payload_volume_size', sa.Integer(), nullable=True))
    op.add_column('drive', sa.Column('project_id', sa.String(length=36), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('drive', 'project_id')
    op.drop_column('drive', 'payload_volume_size')
    op.drop_column('drive', 'payload_volume_id')
    op.drop_column('drive', 'payload_connection_info')
    # ### end Alembic commands ###
