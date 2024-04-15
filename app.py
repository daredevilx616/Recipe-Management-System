# app.py
from flask import Flask, render_template, url_for, redirect, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from models import db, Users, Recipes

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
    if 'username' in session:
        return redirect(url_for('home'))
    form = RegistrationForm()
    try:
        if form.validate_on_submit():
            user = Users(Username=form.username.data, Email=form.email.data, Password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            print(form.errors)
    except Exception as e:
        db.session.rollback()
        flash('Error creating user: ' + str(e), 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter((Users.Username == form.login_field.data) | (Users.Email == form.login_field.data)).first()
        if user and user.Password == form.password.data:  
            session['username'] = user.Username
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check login info and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('You have been logged out. Log back in to continue.', 'success')
    return redirect(url_for('home'))

@app.route("/recipes/search")
def search_recipes():
    query = request.args.get('query', '')
    recipes = Recipes.query.filter(Recipes.Title.like('%{}%'.format(query))).all()
    return render_template('recipes.html', recipes=recipes)

@app.route("/recipes")
def recipes():
    recipes = Recipes.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        flash('Please login to view this page.', 'warning')
        return redirect(url_for('login'))
    
    user = Users.query.filter_by(Username=session['username']).first()
    if request.method == 'POST':
        # Update user profile logic goes here
        # user.name = request.form['name'] 
        # db.session.commit()
        flash('Your profile has been updated.', 'success')
    
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
