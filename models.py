from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    preference = db.Column(db.Text)

    recipes = db.relationship('Recipes', backref='user', lazy=True)
    interactions = db.relationship('Interactions', backref='user', lazy=True)

class Recipes(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    ingredients = db.relationship('Ingredients', secondary='recipe_ingredients', back_populates='recipes')
    interactions = db.relationship('Interactions', backref='recipe', lazy=True)

class Ingredients(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255))
    nutritional_value = db.Column(db.Text)

    recipes = db.relationship('Recipes', secondary='recipe_ingredients', back_populates='ingredients')

recipe_ingredients = db.Table('recipe_ingredients',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.recipe_id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredients.ingredient_id'), primary_key=True)
)

class Interactions(db.Model):
    interaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'))
    rating = db.Column(db.Integer, db.CheckConstraint('rating BETWEEN 1 AND 5'))
    comment = db.Column(db.Text)
