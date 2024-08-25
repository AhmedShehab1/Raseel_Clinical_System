from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, \
    BooleanField, TextAreaField

from wtforms.validators import DataRequired, Email, Length, Regexp, \
    EqualTo, ValidationError
from web_flask import db
import sqlalchemy as sa
import models as m


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    contact_number = StringField("Contact Number", validators=[
        DataRequired(),
        Length(10, message="Contact number must be 10 digits"),
        Regexp(r'^05[0-9]{8}$',
               message=(
                   "Ensure contact"
                   " number in the following format: 05XXXXXXXX"
                )
               )
        ])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Repeat Password", validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
        ])
    submit = SubmitField("Register")

    # Will be called by WTForms

    def validate_email(self, email):
        user = db.session.scalar(
            sa.select(m.Patient).where(m.Patient.email == email.data)
        )
        if user is not None:
            raise ValidationError("Please use a different email address.")

    def validate_contact_number(self, contact_number):
        user = db.session.scalar(
            sa.select(m.Patient).where(
                m.Patient.contact_number == contact_number.data)
        )
        if user is not None:
            raise ValidationError("Please use a different contact number.")


class EditProfileInfo(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    contact_number = StringField("Contact Number", validators=[
        DataRequired(),
        Length(10, message="Contact number must be 10 digits"),
        Regexp(r'^05[0-9]{8}$',
               message=(
                    "Ensure contact number in "
                    "the following format: 05XXXXXXXX"
                   )
               )
        ])
    address = TextAreaField('Address', validators=[Length(min=0, max=256)])
    medical_history = TextAreaField('Medical History',
                                    validators=[Length(min=0, max=400)])
    current_medications = TextAreaField('Current Medication',
                                        validators=[Length(min=0, max=256)])
    submit = SubmitField("Update")

    def __init__(self, original_email, original_contact_number,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_email = original_email
        self.original_contact_number = original_contact_number

    def validate_email(self, email):
        if self.original_email != email.data:
            user = db.session.scalar(
                sa.select(m.Patient).where(m.Patient.email == email.data)
            )
            if user is not None:
                raise ValidationError("Please use a different email address.")

    def validate_contact_number(self, contact_number):
        if self.original_contact_number != contact_number.data:
            user = db.session.scalar(
                sa.select(m.Patient).where(
                    m.Patient.contact_number == contact_number.data)
            )
            if user is not None:
                raise ValidationError("Please use a different contact number.")
