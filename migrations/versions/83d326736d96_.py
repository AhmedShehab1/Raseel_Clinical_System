# flake8: noqa
"""empty message

Revision ID: 83d326736d96
Revises: 8463654b59f6
Create Date: 2024-08-24 14:10:06.305795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83d326736d96'
down_revision = '8463654b59f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('departments',
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('departments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_departments_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_departments_name'), ['name'], unique=False)

    op.create_table('doctors',
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('certificates', sa.String(length=256), nullable=False),
    sa.Column('phone', sa.String(length=10), nullable=True),
    sa.Column('department_id', sa.String(length=128), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_doctors_department_id'), ['department_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_doctors_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_doctors_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_doctors_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_doctors_phone'), ['phone'], unique=True)

    op.create_table('patients',
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('contact_number', sa.String(length=10), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=False),
    sa.Column('address', sa.String(length=256), nullable=False),
    sa.Column('medical_history', sa.String(length=400), nullable=False),
    sa.Column('current_medications', sa.String(length=256), nullable=False),
    sa.Column('department_id', sa.String(length=128), nullable=False),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_patients_contact_number'), ['contact_number'], unique=True)
        batch_op.create_index(batch_op.f('ix_patients_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_patients_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_patients_name'), ['name'], unique=False)

    op.create_table('appointments',
    sa.Column('patient_id', sa.String(length=128), nullable=False),
    sa.Column('doctor_id', sa.String(length=128), nullable=False),
    sa.Column('appointment_time', sa.DateTime(), nullable=False),
    sa.Column('status', sa.Enum('SCHEDULED', 'COMPLETED', 'CANCELLED', name='appointmentstatus'), nullable=False),
    sa.Column('reason', sa.String(length=256), nullable=False),
    sa.Column('notes', sa.String(length=256), nullable=False),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_appointments_appointment_time'), ['appointment_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_appointments_doctor_id'), ['doctor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_appointments_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_appointments_patient_id'), ['patient_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_appointments_status'), ['status'], unique=False)

    op.create_table('timeslots',
    sa.Column('doctor_id', sa.String(length=128), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('start_time', sa.Time(), nullable=False),
    sa.Column('end_time', sa.Time(), nullable=False),
    sa.Column('status', sa.Enum('AVAILABLE', 'BOOKED', name='timeslotstatus'), nullable=False),
    sa.Column('id', sa.String(length=128), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.CheckConstraint('end_time > start_time', name='check_time_validity'),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('doctor_id', 'date', 'start_time', name='doctor_date_startTime_uc')
    )
    with op.batch_alter_table('timeslots', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_timeslots_date'), ['date'], unique=False)
        batch_op.create_index(batch_op.f('ix_timeslots_doctor_id'), ['doctor_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_timeslots_end_time'), ['end_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_timeslots_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_timeslots_start_time'), ['start_time'], unique=False)
        batch_op.create_index(batch_op.f('ix_timeslots_status'), ['status'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('timeslots', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_timeslots_status'))
        batch_op.drop_index(batch_op.f('ix_timeslots_start_time'))
        batch_op.drop_index(batch_op.f('ix_timeslots_id'))
        batch_op.drop_index(batch_op.f('ix_timeslots_end_time'))
        batch_op.drop_index(batch_op.f('ix_timeslots_doctor_id'))
        batch_op.drop_index(batch_op.f('ix_timeslots_date'))

    op.drop_table('timeslots')
    with op.batch_alter_table('appointments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_appointments_status'))
        batch_op.drop_index(batch_op.f('ix_appointments_patient_id'))
        batch_op.drop_index(batch_op.f('ix_appointments_id'))
        batch_op.drop_index(batch_op.f('ix_appointments_doctor_id'))
        batch_op.drop_index(batch_op.f('ix_appointments_appointment_time'))

    op.drop_table('appointments')
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_patients_name'))
        batch_op.drop_index(batch_op.f('ix_patients_id'))
        batch_op.drop_index(batch_op.f('ix_patients_email'))
        batch_op.drop_index(batch_op.f('ix_patients_contact_number'))

    op.drop_table('patients')
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_doctors_phone'))
        batch_op.drop_index(batch_op.f('ix_doctors_name'))
        batch_op.drop_index(batch_op.f('ix_doctors_id'))
        batch_op.drop_index(batch_op.f('ix_doctors_email'))
        batch_op.drop_index(batch_op.f('ix_doctors_department_id'))

    op.drop_table('doctors')
    with op.batch_alter_table('departments', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_departments_name'))
        batch_op.drop_index(batch_op.f('ix_departments_id'))

    op.drop_table('departments')
    # ### end Alembic commands ###
