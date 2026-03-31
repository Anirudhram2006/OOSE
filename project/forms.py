"""Flask-WTF forms used by routes."""
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    role = SelectField(
        "Role",
        choices=[("user", "User"), ("medical_expert", "Medical Expert")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class UploadForm(FlaskForm):
    image = FileField("Skin Image", validators=[DataRequired(), FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Analyze Image")


class SymptomForm(FlaskForm):
    symptoms = TextAreaField("Symptoms", validators=[DataRequired(), Length(min=5, max=1000)])
    submit = SubmitField("Analyze Symptoms")


class ChatForm(FlaskForm):
    query = StringField("Ask chatbot", validators=[DataRequired(), Length(min=3, max=255)])
    submit = SubmitField("Ask")
