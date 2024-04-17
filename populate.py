from flask_sqlalchemy import SQLAlchemy
from app import app, db 
from models import Recipes, Ingredients, RecipeIngredients, Interactions

# Create an application context
app.app_context().push()

# Populate Ingredients
ingredients_data = [
    {"Name": "Tomato", "Category": "Vegetable", "Nutritional_Value": "Rich in Vitamin C and antioxidants"},
    {"Name": "Chicken", "Category": "Meat", "Nutritional_Value": "High in protein"},
    {"Name": "Rice", "Category": "Grain", "Nutritional_Value": "Good source of carbohydrates"},
    # Add more ingredients as needed
]

for data in ingredients_data:
    ingredient = Ingredients(**data)
    db.session.add(ingredient)

# Commit the changes to Ingredients table
db.session.commit()

# Populate Recipes
recipes_data = [
    {"Title": "Tomato Soup", "Instructions": "1. Boil tomatoes. 2. Blend. 3. Season to taste."},
    {"Title": "Grilled Chicken", "Instructions": "1. Marinate chicken. 2. Grill until cooked."},
    {"Title": "Rice Pilaf", "Instructions": "1. Cook rice. 2. Add vegetables and spices."},
    # Add more recipes as needed
]

for data in recipes_data:
    recipe = Recipes(**data)
    db.session.add(recipe)

# Commit the changes to Recipes table
db.session.commit()

# Populate RecipeIngredients
recipe_ingredients_data = [
    {"RecipeID": 1, "IngredientID": 1},  # Tomato Soup contains Tomato
    {"RecipeID": 2, "IngredientID": 2},  # Grilled Chicken contains Chicken
    {"RecipeID": 3, "IngredientID": 3},  # Rice Pilaf contains Rice
    # Add more recipe-ingredient relationships as needed
]

for data in recipe_ingredients_data:
    recipe_ingredient = RecipeIngredients(**data)
    db.session.add(recipe_ingredient)

# Commit the changes to RecipeIngredients table
db.session.commit()

# Populate Interactions
interactions_data = [
    {"UserID": 1, "RecipeID": 1, "Rating": 4, "Comment": "Delicious!"},
    {"UserID": 2, "RecipeID": 2, "Rating": 5, "Comment": "Perfectly grilled!"},
    {"UserID": 3, "RecipeID": 3, "Rating": 3, "Comment": "Could use more seasoning."},
    # Add more interactions as needed
]

for data in interactions_data:
    interaction = Interactions(**data)
    db.session.add(interaction)

# Commit the changes to Interactions table
db.session.commit()
