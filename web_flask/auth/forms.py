from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
    DateField,
    SelectField,
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Regexp,
    EqualTo,
    ValidationError,
)
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
    contact_number = StringField(
        "Contact Number",
        validators=[
            DataRequired(),
            Length(10, message="Contact number must be 10 digits"),
            Regexp(
                r"^05[0-9]{8}$",
                message=(
                    "Ensure contact" " number in the following format: 05XXXXXXXX"
                ),
            ),
        ],
    )
    national_id = StringField(
        "National ID",
        validators=[
            DataRequired(),
            Length(10, message="National ID must be 10 digits"),
        ],
    )
    gender = SelectField(
        "Gender",
        choices=[(gender.value, gender.name) for gender in m.GenderType],
        validators=[DataRequired()],
    )

    birth_date = DateField("Birth Date", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])

    confirm_password = PasswordField(
        "Repeat Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
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
            sa.select(m.Patient).where(m.Patient.contact_number == contact_number.data)
        )
        if user is not None:
            raise ValidationError("Please use a different contact number.")

    def validate_national_id(self, national_id):
        user = db.session.scalar(
            sa.select(m.Patient).where(m.Patient.national_id == national_id.data)
        )
        if user is not None:
            raise ValidationError("Please use a different national ID.")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Request")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
