from flask import Flask, render_template, url_for, redirect, flash, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from forms import *
from models import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a8a38fdf63a53366e21a1c5576d55929'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = Users(username=form.username.data, email=form.email.data, password=hashed_password, preference=form.preferences.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter((Users.username == form.login_field.data) | (Users.email == form.login_field.data)).first()
        if user and check_password_hash(user.password, form.password.data):  
            session['username'] = user.username
            session['user_id'] = user.user_id
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check login info and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash('You have been logged out. Log back in to continue.', 'success')
    return redirect(url_for('home'))

@app.route('/recipes')
def recipes():
    user_id = session.get('user_id')
    if user_id:
        user_recipes = Recipes.query.filter_by(user_id=user_id).all()
        return render_template('recipes.html', recipes=user_recipes)
    return 'You must be logged in to view recipes', 401

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if 'user_id' not in session:
        flash('Please log in to add recipes.', 'warning')
        return redirect(url_for('login'))
    
    form = RecipeForm()
    if form.validate_on_submit():
        new_recipe = Recipes(
            title=form.title.data,
            instructions=form.instructions.data,
            user_id=session['user_id']
        )
        for ingredient_id in form.ingredients.data:
            ingredient = Ingredients.query.get(int(ingredient_id))
            new_recipe.ingredients.append(ingredient)
        
        db.session.add(new_recipe)
        db.session.commit()
        flash('Recipe added successfully!', 'success')
        return redirect(url_for('recipes'))
    
    return render_template('add_recipe.html', form=form)

@app.route('/delete_recipe/<int:recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = Recipes.query.get_or_404(recipe_id)
    if 'user_id' in session and recipe.user_id == session['user_id']:
        db.session.delete(recipe)
        db.session.commit()
        flash('Recipe deleted successfully!')
    else:
        flash('Unauthorized attempt to delete a recipe.', 'danger')
    return redirect(url_for('recipes'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You must be logged in to view this page', 'warning')
        return redirect(url_for('login'))

    user = Users.query.get(user_id)
    form = ProfileForm(obj=user)  
    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data: 
            user.password = generate_password_hash(form.password.data)
        user.preference = form.preference.data  
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    form.password.data = user.password

    return render_template('profile.html', form=form, user=user)

@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    data = request.get_json()
    name = data.get('name')
    category = data.get('category')

    # Validatidation needed

    new_ingredient = Ingredients(name=name, category=category)
    db.session.add(new_ingredient)
    db.session.commit()

    return jsonify({
        'id': new_ingredient.id,
        'name': new_ingredient.name,
        'category': new_ingredient.category
    }), 201

@app.route('/delete_ingredient', methods=['POST'])
def delete_ingredient():
    data = request.get_json()
    ingredient_id = data.get('id')

    ingredient = Ingredients.query.get(ingredient_id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        return jsonify({'message': 'Ingredient deleted'}), 200
    else:
        return jsonify({'message': 'Ingredient not found'}), 404

@app.route('/update_recipe/<int:recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipe = Recipes.query.get(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404

    data = request.get_json()
    if 'title' in data:
        recipe.title = data['title']
    if 'instructions' in data:
        recipe.instructions = data['instructions']
    if 'ingredients' in data:
        # Clear existing ingredients and add new ones
        # This is simplistic; you might want to implement more nuanced ingredient handling
        recipe.ingredients.clear()
        for ingredient_name in data['ingredients']:
            ingredient = Ingredients.query.filter_by(name=ingredient_name).first()
            if ingredient:
                recipe.ingredients.append(ingredient)
            else:
                # Create a new ingredient if it does not exist
                new_ingredient = Ingredients(name=ingredient_name)
                db.session.add(new_ingredient)
                recipe.ingredients.append(new_ingredient)

    db.session.commit()
    return jsonify({'message': 'Recipe updated successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True)
