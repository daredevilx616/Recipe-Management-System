# forms.py
from flask_wtf import FlaskForm
from wtforms import * 
from wtforms.validators import DataRequired, Email, Length
from models import Ingredients

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    preferences = SelectField('Food Preferences', choices=[('no Preference', 'No Preference'), ('halal', 'Halal'), ('kosher', 'Kosher'), ('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('pescatarian', 'Pescatarian')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    login_field = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RecipeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    ingredients = SelectMultipleField('Ingredients', choices=[], coerce=int)
    submit = SubmitField('Add Recipe')
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.ingredients.choices = [
            (ingredient.ingredient_id, f"{ingredient.name} ({ingredient.category})") 
            for ingredient in Ingredients.query.all()
        ]

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    preference = SelectField('Food Preferences', choices=[('no Preference', 'No Preference'), ('halal', 'Halal'), ('kosher', 'Kosher'), ('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('pescatarian', 'Pescatarian')], validators=[DataRequired()])
    submit = SubmitField('Update')