from flask import render_template, request, redirect, url_for, flash, current_app
from app import db
from app.forms import RecipeForm, SearchForm
from app.models import Recipe, User
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import stripe


stripe.api_key = 'sk_test_51PdiTb2MsyJaOcXOk2N8p2ZESZte2yZIlJM10mwaLSGJI7d6r3nRNlHj3mFMNEkVxObznAlfD44UUCwZDuXlbuZN00AgzxOuhD'  # Replace with your actual secret key


def init_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def home():
        search_form = SearchForm()
        if search_form.validate_on_submit():
            return redirect(url_for('search', query=search_form.query.data))
        
        recipes = Recipe.query.all()
        return render_template('index.html', recipes=recipes)

    @app.route('/recipe/<int:id>')
    def recipe_details(id):
        recipe = Recipe.query.get_or_404(id)
        return render_template('recipe_details.html', recipe=recipe)

    @app.route('/add_recipe', methods=['GET', 'POST'])
    def add_recipe():
        # Check if the user is logged in
        if 'username' not in session:
            flash('Please log in to add a recipe.', 'danger')
            return redirect(url_for('login'))

        form = RecipeForm()
        if form.validate_on_submit():
            new_recipe = Recipe(
                name=form.name.data,
                ingredients=form.ingredients.data,
                instructions=form.instructions.data,
                cuisine=form.cuisine.data,
                dietary_info=form.dietary_info.data,
                username=session['username']  # Retrieve username from session
            )
            db.session.add(new_recipe)
            db.session.commit()
            flash('Recipe added successfully!', 'success')
            return redirect(url_for('home'))
        return render_template('add_recipe.html', form=form)


    @app.route('/search')
    def search():
        query = request.args.get('query')
        if query:
            search_conditions = [
                Recipe.name.ilike(f'%{query}%'),
                Recipe.ingredients.ilike(f'%{query}%'),
                Recipe.instructions.ilike(f'%{query}%'),
                Recipe.cuisine.ilike(f'%{query}%'),
                Recipe.dietary_info.ilike(f'%{query}%')
            ]
            results = Recipe.query.filter(or_(*search_conditions)).all()
        else:
            results = []
        return render_template('search.html', results=results, query=query)
    
    @app.route('/edit_recipe/<int:id>', methods=['GET', 'POST'])
    def edit_recipe(id):
        # Check if the user is logged in
        if 'username' not in session:
            flash('Please log in to edit a recipe.', 'danger')
            return redirect(url_for('login'))

        recipe = Recipe.query.get_or_404(id)
        form = RecipeForm(obj=recipe)
        if form.validate_on_submit():
            form.populate_obj(recipe)
            db.session.commit()
            flash('Recipe updated successfully!', 'success')
            return redirect(url_for('recipe_details', id=recipe.id))
        return render_template('edit_recipe.html', form=form, recipe=recipe)

    

    # Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                flash('Login successful!', 'success')
                session['username'] = username  # Store username in session
                return jsonify({'success': True, 'username': username}), 200
            else:
                flash('Invalid credentials. Please try again.', 'danger')
                return jsonify({'success': False}), 401
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('username', None)  # Remove username from session
        flash('You have been logged out.', 'success')
        return redirect(url_for('home'))
    

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            if password == confirm_password:
                hashed_password = generate_password_hash(password)
                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Passwords do not match. Please try again.', 'danger')
        return render_template('register.html')



    @app.route('/payments')
    def payments():
        return render_template('payment.html')
    

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')
    











    @app.route('/payment', methods=['GET', 'POST'])
    def payment():
        if request.method == 'POST':
            token = request.form['stripeToken']
            amount = int(request.form['amount']) * 100  # Amount in cents

            try:
                charge = stripe.Charge.create(
                    amount=amount,
                    currency='usd',
                    source=token,
                    description='Donation'
                )
                flash('Payment successful!', 'success')
                return redirect(url_for('success'))
            except stripe.error.StripeError as e:
                flash(f'Payment error: {e}', 'danger')
                return redirect(url_for('payment'))

        return render_template('payment.html')

    @app.route('/success')
    def success():
        return 'Payment succeeded!'





 
    @app.route('/cancel')
    def cancel():
        return 'Payment canceled.'























    
    @app.route('/terms')
    def terms():
        return render_template('terms.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error_message="Page not found"), 404



    @app.route('/error')
    def error():
        return render_template('error.html', error_message="An error occurred")
    






















