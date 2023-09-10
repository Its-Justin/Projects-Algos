from CMT.config.mysqlconnection import connectToMySQL
from CMT import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:

    db_schema = "cmt_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.username = data["username"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.vehicle = []

    @classmethod
    def create_user(cls, data):
        query = """
        INSERT INTO users(name, username, password)
        VALUES (%(name)s, %(username)s, %(password)s)
        """
        return connectToMySQL(cls.db_schema).query_db(query, data)

    @classmethod
    def get_user_by_username(cls,data): 
        query = """
        SELECT * FROM users
        WHERE username = %(username)s
        """
        user_results = connectToMySQL(cls.db_schema).query_db(query, data)
        if len(user_results) < 1:
            return False
        else:
            this_user = cls(user_results[0])
            return this_user

    @staticmethod
    def validate_user_register( user_form ):
        is_valid = True
        if len(user_form["name"]) == 0:
            if len(user_form["username"]) == 0:
                if len(user_form["password"]) == 0:
                    if len(user_form["confirm_password"]) == 0:
                        flash("All fields are required", "register")
                        return False
        if len(user_form["name"]) == 0:
            flash("Name is required", "register")
            is_valid = False
        elif len(user_form["name"]) < 2:
            flash("Name must be at least 2 characters long", "register")
            is_valid = False
        if len(user_form["username"]) == 0:
            flash("Username is required", "register")
            is_valid = False
        elif len(user_form["username"]) < 2:
            flash("Username must be at least 2 characters long", "register")
        elif User.get_user_by_username({"username": user_form["username"]}) != False:
            flash("This username already has an account", "register")
            is_valid = False
        if len(user_form["password"]) == 0:
            if len(user_form["confirm_password"]) == 0:
                flash("Password is required", "register")
                return False
        elif len(user_form["password"]) < 8:
            flash("Password must be at least 8 characters long", "register")
            is_valid = False
        if len(user_form["confirm_password"]) == 0:
            flash("Please confirm password", "register")
            is_valid = False
        elif user_form["password"] != user_form["confirm_password"]:
            flash("Password does not match confirmed password", "register")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_user_login(user_login):
        is_valid = True
        if len(user_login["username"]) == 0:
            if len(user_login["password"]) == 0:
                flash("Please enter Username/Password.", "sign_in")
                return False
        potential_user = User.get_user_by_username({"username": user_login["username"]})
        if len(user_login["username"]) == 0:
            flash("Username is required.", "sign_in")
            return False
        if not potential_user:
            flash("Invalid Username/Password", "sign_in")
            is_valid = False
        elif not bcrypt.check_password_hash(potential_user.password, user_login["password"]):
            flash("Invalid Username/Password", "sign_in")
            is_valid = False
        return is_valid

