from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe# import entire file, rather than class, to avoid circular imports

# Create Users Controller
@app.route('/users/create', methods = ['POST'])
def create_a_user():
    if user.User.create_user(request.form):
        return redirect('/users/recipe')
    return redirect ('/')


# Read Users Controller
@app.route('/users/recipe')
def main_page():
    if 'user_id' not in session : return redirect('/')
    all_recipes = recipe.Recipe.get_all_recipes_with_author()
    return render_template('main_page.html', all_recipes = all_recipes)

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/users/login' , methods = ['POST'])
def login():
    if user.User.login(request.form):
        return redirect('/users/recipe')
    return redirect('/')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/<int:id>/profile')
def view_profile(id):
    this_user = user.User.get_user_with_recipes(id)
    return render_template('profile.html', this_user=this_user)



# Update Users Controller



# Delete Users Controller


# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')
# def index(id):
#     user_info = user.User.get_user_by_id(id)
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.
