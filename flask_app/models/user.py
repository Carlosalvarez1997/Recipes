
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# The above is used when we do login registration, be sure to install flask-bcrypt: pipenv install flask-bcrypt


class User:
    db = "recipes" #which database are you using for this project
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        # What changes need to be made above for this project?
        #What needs to be added her for class association?



    # Create Users Models
    @classmethod
    def create_user(cls, data):
        if not cls.validate_user(data):
            return False
        data = cls.parsed_data(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        session['user_id'] = user_id
        session['first_name'] = data['first_name']
        session['user_name'] = f'{data["first_name"]} {data["last_name"]}'
        return user_id


    # Read Users Models
    @classmethod
    def get_user_by_email(cls, email):
        data = {'email': email}
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        if user_id:
            return cls(user_id[0])
        return False

    @classmethod
    def see_user_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        from users
        WHERE id = %(id)s
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        this_user = user_id[0]
        return this_user

    @classmethod
    def get_user_with_recipes(cls,id):
        data={'id' : id}
        query= """
        SELECT *
        FROM users
        JOIN recipes
        ON users.id = recipes.users_id
        WHERE users_id = %(id)s
        ;"""
        this_user = connectToMySQL(cls.db).query_db(query,data)
        all_recipes = []
        for row in this_user:
            one_recipe = cls(row)
            recipe_info = {
                'id' : row['id'],
                'name': row['name'],
                'decription' : row['decription'],
                'instructions': row['instructions'],
                'less_than_thirty' : row['less_than_thirty']
            }
            one_recipe.recipes.append(recipe_info)

        print(one_recipe.recipes)
        return one_recipe



    # Update Users Models



    # Delete Users Models


    #HELPER METHODS
    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2 :
            flash('First name has to be longer than 2 characters')
            is_valid = False
        if len(data['last_name']) <2 :
            flash('last Name has to be longer than 2 characters')
            is_valid = False
        if 'id' not in data:# this would mean that it's a new user
            if len(data['password']) <8:
                flash('Password has to be longer than 8 Characters')
                is_valid = False
            if data['password'] != data['confirm_password']:
                flash('Password do not match')
                is_valid= False
        if 'id' not in data or data['email'] != User.get_user_by_id(data['id']).email :
            if not EMAIL_REGEX.match(data['email']):
                flash("email address format incomplete")
                is_valid= False
            if User.get_user_by_email(data['email']):
                flash('Email Address is already Taken')
                is_valid= False
            return is_valid





    @staticmethod
    def parsed_data(data):
        parsed_data = {
        'email' : data['email'],
        'first_name' :data['first_name'],
        'last_name' : data['last_name'],
        'password' : bcrypt.generate_password_hash(data['password'])
    }
        return parsed_data

    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['first_name'] = this_user.first_name
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                return True
        flash('Email or Password is Incorrect')
        return False
