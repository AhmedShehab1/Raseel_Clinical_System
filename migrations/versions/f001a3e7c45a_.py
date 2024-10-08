"""empty message

Revision ID: f001a3e7c45a
Revises: f0c6347135e6
Create Date: 2024-09-06 15:19:17.316826

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "f001a3e7c45a"
down_revision = "f0c6347135e6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("admins", schema=None) as batch_op:
        batch_op.add_column(sa.Column("email", sa.String(length=120), nullable=False))
        batch_op.create_index(batch_op.f("ix_admins_email"), ["email"], unique=True)

    with op.batch_alter_table("appointments", schema=None) as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=mysql.VARCHAR(collation="utf8mb3_bin", length=256),
            nullable=True,
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("appointments", schema=None) as batch_op:
        batch_op.alter_column(
            "notes",
            existing_type=mysql.VARCHAR(collation="utf8mb3_bin", length=256),
            nullable=False,
        )

    with op.batch_alter_table("admins", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_admins_email"))
        batch_op.drop_column("email")

    # ### end Alembic commands ###
