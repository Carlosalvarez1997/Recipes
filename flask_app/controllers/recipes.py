from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe# import entire file, rather than class, to avoid circular imports


@app.route('/recipes/create', methods = ['post'])
def create_recipe():
    if recipe.Recipe.create_recipe(request.form):
        return redirect('/users/recipe')
    return redirect('/recipes/user/create')

@app.route('/recipes/user/create')
def recipe_page():
    return render_template('recipes.html')

@app.route('/recipe/<int:id>/delete')
def delete(id):
    recipe.Recipe.delete_recipe(id)
    return redirect('/users/recipe')

@app.route('/recipes/update/<int:id>')
def update(id):
    this_recipe = recipe.Recipe.get_recipe_by_id(id)
    return render_template('update.html',this_recipe=this_recipe)

@app.route('/recipes/update', methods = ['post'])
def update_recipe():
    recipe.Recipe.update_recipe(request.form)
    return redirect('/users/recipe')


@app.route('/recipe/<int:id>/view')
def view_recipe(id):
    this_recipe = recipe.Recipe.get_one_recipe(id)
    return render_template('view_recipe.html', this_recipe= this_recipe)
