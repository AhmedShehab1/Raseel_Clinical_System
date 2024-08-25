"""added last_seen column in patient

Revision ID: d850d5ff4e18
Revises: a4490feccc89
Create Date: 2024-08-25 15:10:52.535559

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd850d5ff4e18'
down_revision = 'a4490feccc89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_patients')
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('last_seen', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.drop_column('last_seen')

    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_column('last_seen')

    op.create_table('_alembic_tmp_patients',
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('contact_number', sa.VARCHAR(length=10), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(length=256), nullable=False),
    sa.Column('address', sa.VARCHAR(length=256), nullable=False),
    sa.Column('medical_history', sa.VARCHAR(length=400), nullable=False),
    sa.Column('current_medications', sa.VARCHAR(length=256), nullable=False),
    sa.Column('department_id', sa.VARCHAR(length=128), nullable=False),
    sa.Column('id', sa.VARCHAR(length=128), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.Column('updated_at', sa.DATETIME(), nullable=False),
    sa.Column('deleted_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
