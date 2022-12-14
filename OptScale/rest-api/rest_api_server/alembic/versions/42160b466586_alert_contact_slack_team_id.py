""""alert_contact_slack_team_id"

Revision ID: 42160b466586
Revises: da0145def701
Create Date: 2021-04-23 11:28:42.646682

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.sql import table
from sqlalchemy import String, select, Column, delete


# revision identifiers, used by Alembic.
revision = '42160b466586'
down_revision = 'da0145def701'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    session = Session(bind=bind)
    try:
        alert_contact_table = table(
            'alert_contact',
            Column('budget_alert_id', String(36)),
            Column('employee_id', String(36)),
            Column('slack_channel_id', String(36))
        )
        budget_alert_table = table(
            'budget_alert',
            Column('id', String(36))
        )
        del_stmt = delete(alert_contact_table).where(
            alert_contact_table.c.slack_channel_id.isnot(None))
        session.execute(del_stmt)
        email_contacts = session.execute(select([alert_contact_table]))
        alert_ids = list(map(
            lambda x: x.budget_alert_id, email_contacts))
        del_stmt = delete(budget_alert_table).where(
            budget_alert_table.c.id.notin_(alert_ids))
        session.execute(del_stmt)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    op.add_column('alert_contact', sa.Column(
        'slack_team_id', sa.String(length=36), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('alert_contact', 'slack_team_id')
    # ### end Alembic commands ###
