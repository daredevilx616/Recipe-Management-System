from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Preferences = db.Column(db.Text)

class Recipes(db.Model):
    RecipeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(255), nullable=False)
    Instructions = db.Column(db.Text, nullable=False)
    Rating = db.Column(db.Numeric(2,1))  
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))

    user = db.relationship('Users', backref=db.backref('recipes', lazy=True))

class Ingredients(db.Model):
    IngredientID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(255))
    Nutritional_Value = db.Column(db.Text)

class RecipeIngredients(db.Model):
    RecipeID = db.Column(db.Integer, db.ForeignKey('recipes.RecipeID'), primary_key=True)
    IngredientID = db.Column(db.Integer, db.ForeignKey('ingredients.IngredientID'), primary_key=True)

    recipe = db.relationship('Recipes', backref=db.backref('recipe_ingredients', lazy=True))
    ingredient = db.relationship('Ingredients', backref=db.backref('recipe_ingredients', lazy=True))

class Interactions(db.Model):
    InteractionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'))
    RecipeID = db.Column(db.Integer, db.ForeignKey('recipes.RecipeID'))
    Rating = db.Column(db.Integer) 
    Comment = db.Column(db.Text)
    __table_args__ = (
        db.CheckConstraint('Rating BETWEEN 1 AND 5', name='rating_range_check'),
    )
    user = db.relationship('Users', backref=db.backref('interactions', lazy=True))
    recipe = db.relationship('Recipes', backref=db.backref('interactions', lazy=True))
