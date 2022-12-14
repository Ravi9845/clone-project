""""2.2 replace sub bu ids to budget ids in invite_assignment"

Revision ID: 24acd1baab5b
Revises: b21580a49268
Create Date: 2020-09-06 23:09:57.992221

"""
import json

from alembic import op
import sqlalchemy as sa
from sqlalchemy import table, column, update, select
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision = '24acd1baab5b'
down_revision = 'b21580a49268'
branch_labels = None
depends_on = None

old_name = "business_unit_id"
new_name = "scope_id"


def get_map_sub_bu_budget(session, reverse_map=False):
    table_ = table('partner',
                   column('id', sa.String(36)),
                   column('parent_id', sa.String(36)),
                   column('budget_id', sa.String(36)))
    select_stmt = select(
        [table_.c.id, table_.c.parent_id, table_.c.budget_id]
    ).where(
        table_.c.parent_id.isnot(None)
    )
    result = session.execute(select_stmt)
    if not reverse_map:
        sub_bu_budget_map = {bu_id: budget_id for bu_id, _, budget_id in result}
    else:
        sub_bu_budget_map = {budget_id: bu_id for bu_id, _, budget_id in result}
    return sub_bu_budget_map


def replace_bu_ids_to_budget_ids(session, target_map):
    invite_assignment_table = table(
        'invite_assignment',
        column('id', sa.String(36)),
        column('scope_id', sa.String(36)),
        column('scope_type', sa.String(20))
    )
    select_stmt = select(
        [invite_assignment_table.c.id, invite_assignment_table.c.scope_id]
    ).where(
        invite_assignment_table.c.scope_id.in_(target_map.keys())
    )
    result = session.execute(select_stmt)
    for id_, scope_id in result:
        target_scope_id = target_map.get(scope_id)
        update_stmt = update(
            invite_assignment_table
        ).values(
            scope_id=target_scope_id,
            scope_type='BUDGET'
        ).where(
            invite_assignment_table.c.id == id_
        )
        session.execute(update_stmt)


def _replace_all_keys_from_list(source_dict, sub_bu_budget_map):
    modified = False
    for old_key, _ in source_dict.copy().items():
        if old_key in sub_bu_budget_map.keys():
            modified = True
            new_key = sub_bu_budget_map[old_key]
            source_dict[new_key] = source_dict.pop(old_key)
    return modified


def replace_keys_in_meta(session, from_key, to_key, sub_bu_budget_map):
    invite_table = table(
        'invite',
        column('id', sa.String(36)),
        column('meta', sa.TEXT())
    )
    select_stmt = select(
        [invite_table.c.id, invite_table.c.meta]
    ).where(
        invite_table.c.meta.ilike('%%%s%%' % from_key)
    )
    result = session.execute(select_stmt)
    for id_, meta in result:
        meta = json.loads(meta)
        name_filed = meta.pop(from_key)
        _replace_all_keys_from_list(name_filed, sub_bu_budget_map)
        meta[to_key] = name_filed
        meta = json.dumps(meta)
        update_stmt = update(
            invite_table
        ).values(
            meta=meta
        ).where(
            invite_table.c.id == id_
        )
        session.execute(update_stmt)


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    rest_session = Session(bind=bind)
    op.drop_constraint('invite_assignment_ibfk_1', 'invite_assignment',
                       type_='foreignkey')
    op.drop_index(old_name, 'invite_assignment')
    op.alter_column('invite_assignment', old_name, existing_type=sa.String(36),
                    nullable=False, new_column_name=new_name)
    op.add_column(
        'invite_assignment',
        sa.Column('scope_type', sa.Enum('ORGANIZATION', 'BUDGET'),
                  nullable=False, server_default='ORGANIZATION'))
    sub_bu_budget_map = get_map_sub_bu_budget(rest_session)
    replace_bu_ids_to_budget_ids(rest_session, sub_bu_budget_map)
    replace_keys_in_meta(rest_session, 'business_units_names', 'scope_names',
                         sub_bu_budget_map)
    try:
        rest_session.commit()
    finally:
        rest_session.close()
    op.alter_column('invite_assignment', 'scope_type',
                    existing_type=sa.Enum('ORGANIZATION', 'BUDGET'),
                    nullable=False, server_default=None)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    bind = op.get_bind()
    rest_session = Session(bind=bind)
    sub_bu_budget_map = get_map_sub_bu_budget(rest_session, reverse_map=True)
    replace_bu_ids_to_budget_ids(rest_session, sub_bu_budget_map)
    replace_keys_in_meta(rest_session, 'scope_names', 'business_units_names',
                         sub_bu_budget_map)
    try:
        rest_session.commit()
    finally:
        rest_session.close()
    op.drop_column('invite_assignment', 'scope_type')
    op.alter_column('invite_assignment', new_name, existing_type=sa.String(36),
                    nullable=False, new_column_name=old_name)
    op.create_index(old_name, 'invite_assignment', [old_name])
    op.create_foreign_key('invite_assignment_ibfk_1',
                          'invite_assignment', 'partner',
                          ['business_unit_id'], ['id'])
    # ### end Alembic commands ###
