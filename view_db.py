import sqlite3

conn = sqlite3.connect('recipe_management.db')
cursor = conn.cursor()

cursor.execute("""
               DELETE From Ingredients WHERE name = 'Potatoes'
                  """)
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
# from app import app, db 
# from models import Recipes, Ingredients, Interactions

# ingredient_list = [
#            ('Flour', 'Baking'),
#     ('Sugar', 'Baking'),
#     ('Salt', 'Seasoning'),
#     ('Olive oil', 'Oil'),
#     ('Chicken', 'Meat'),
#     ('Beef', 'Meat'),
#     ('Pork', 'Meat'),
#     ('Carrot', 'Vegetable'),
#     ('Tomato', 'Vegetable'),
#     ('Basil', 'Herb'),
#     ('Thyme', 'Herb'),
#     ('Garlic', 'Vegetable'),
#     ('Onion', 'Vegetable'),
#     ('Pasta', 'Grain'),
#     ('Rice', 'Grain'),
#     ('Beans', 'Legume'),
#     ('Peas', 'Legume')
# ]
# with app.app_context():
#     # Check if the table is empty and only then populate
#     if not Ingredients.query.first():
#         for name, category in ingredient_list:
#             ingredient = Ingredients(name=name, category=category)
#             db.session.add(ingredient)
#         db.session.commit()
#         print('Ingredients table has been populated.')
#     else:
#         print('Ingredients table already contains data.')