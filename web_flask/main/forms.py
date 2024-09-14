from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SubmitField,
    BooleanField,
    TextAreaField,
    DateField,
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Regexp,
    ValidationError,
)
from web_flask import db
import sqlalchemy as sa
import models as m
from flask import request


class EditProfileInfo(FlaskForm):
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
                    "Ensure contact number in " "the following format: 05XXXXXXXX"
                ),
            ),
        ],
    )
    birth_date = DateField("Birth Date", validators=[DataRequired()])
    address = TextAreaField("Address", validators=[Length(min=0, max=256)])
    medical_history = TextAreaField(
        "Medical History", validators=[Length(min=0, max=400)]
    )
    current_medications = TextAreaField(
        "Current Medication", validators=[Length(min=0, max=256)]
    )
    submit = SubmitField("Update")

    def __init__(self, original_email, original_contact_number, *args, **kwargs):
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
                    m.Patient.contact_number == contact_number.data
                )
            )
            if user is not None:
                raise ValidationError("Please use a different contact number.")


class VisitorForm(FlaskForm):
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
                    "Ensure contact number in the" " following format: 05XXXXXXXX"
                ),
            ),
        ],
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(),
            Length(
                min=30,
                max=100,
                message=("Message must be between" " 30 and 100 characters"),
            ),
        ],
    )
    statement = BooleanField(
        "I allow this website to store my submission so they can respond to my inquiry.",
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    q = StringField("Search", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if "formdata" not in kwargs:
            kwargs["formdata"] = request.args
        if "meta" not in kwargs:
            kwargs["meta"] = {"csrf": False}
        super(SearchForm, self).__init__(*args, **kwargs)
