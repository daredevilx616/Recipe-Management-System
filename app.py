# app.py
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from models import db, Users, Recipes  # Ensure models.py is correctly referenced

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a8a38fdf63a53366e21a1c5576d55929'  # Needed for CSRF protection in forms
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with Flask app
db.init_app(app)

# IMPORTANT: This step ensures that your Flask app is able to create/use database tables appropriately
# Especially relevant when running the app for the first time or if there are model changes
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    # return "Welcome to the Recipe Management System!"
    return render_template("base.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = form.password.data  # Implement password hashing here
        user = Users(Username=form.username.data, Email=form.email.data, Password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Placeholder for login logic, ensure to check user credentials against the database
        flash('You have been logged in!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

@app.route("/recipes")
def recipes():
    recipes = Recipes.query.all()  # Fetches all recipes for demonstration
    return render_template('recipes.html', recipes=recipes)

if __name__ == '__main__':
    app.run(debug=True)
