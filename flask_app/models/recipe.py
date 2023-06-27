
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt

class Recipe:
    db = "recipes"
    def __init__(self, data):
        self. id = data['id']
        self.name = data['name']
        self.decription = data['decription']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.less_than_thirty = data['less_than_thirty']
        self.users_id = data['users_id']
        self.author = None

    @classmethod
    def create_recipe(cls, data):
        if not cls.validate_recipe(data):
            return False
        query = """
        INSERT INTO recipes (name, decription, instructions, less_than_thirty, users_id, created_at)
        VALUES (%(name)s, %(decription)s, %(instructions)s,%(less_than_thirty)s, %(users_id)s, %(created_at)s)
        ;"""
        this_recipe = connectToMySQL(cls.db).query_db(query,data)
        return this_recipe



    @classmethod
    def get_all_recipes(cls):
        query = """
        SELECT *
        FROM recipes
        ;"""
        all_recipes = connectToMySQL(cls.db).query_db(query)
        recipe_list = []
        for a_recipe in all_recipes:
            recipe_list.append(cls(a_recipe))
        return recipe_list

    @classmethod
    def get_recipe_by_id(cls,id):
        data={'id': id}
        query = """
        SELECT *
        FROM recipes
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        this_recipe = results[0]
        return this_recipe

    @classmethod
    def get_all_recipes_with_author(cls):
        query = """
        SELECT *
        FROM recipes
        JOIN users
        ON users.id = recipes.users_id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            one_recipe_author = {
                'id': row ['users_id'],
                'first_name' : row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            author = user.User(one_recipe_author)
            one_recipe.author = author
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_one_recipe(cls,id):
        data = {'id':id}
        query = """
        SELECT *
        FROM recipes
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])


    @classmethod
    def delete_recipe(cls, id):
        data = {'id': id}
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return

    @classmethod
    def update_recipe(cls, data):
        query = """
        UPDATE recipes
        SET name = %(name)s, decription = %(decription)s, instructions = %(instructions)s
        WHERE id = %(id)s
        ;"""
        updated_recipe = connectToMySQL(cls.db).query_db(query,data)
        print (updated_recipe)
        return


    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['decription']) <1 :
            flash('Description Cannot be blank')
            is_valid =False
        if len(data['instructions']) <1:
            flash('Instructions Cannot be blank')
            is_valid = False
        if not data['created_at']:
            flash('You need to add the date this recepie was created')
            is_valid= False
        return is_valid
