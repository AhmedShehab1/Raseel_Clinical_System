from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
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
               message="Contact number must contain only digits")
        ])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Repeat Password", validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
        ])
    submit = SubmitField("Register")

    # Will be called by WTForms

    def validate_name(self, name):
        user = db.session.scalar(
            sa.select(m.Patient).where(m.Patient.name == name.data)
        )
        if user is not None:
            raise ValidationError("Please use a different name.")

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
