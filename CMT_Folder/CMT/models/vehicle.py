from CMT.config.mysqlconnection import connectToMySQL
from CMT.models import user
from CMT import app
from flask import flash


class Vehicle:

    db_schema = "cmt_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.year = data["year"]
        self.make = data["make"]
        self.model = data["model"]
        self.trim = data["trim"]
        self.nickname = data["nickname"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.maintenance = []

    @classmethod
    def create_vehicle(cls, data):
        query = """
        INSERT INTO vehicles(year, make, model, trim, nickname, user_id)
        VALUES (%(year)s, %(make)s, %(model)s, %(trim)s, %(nickname)s, %(user_id)s);
        """
        return connectToMySQL(cls.db_schema).query_db(query, data)

    @classmethod
    def get_one_vehicle(cls, data):
        query = """
        SELECT * FROM vehicles
        WHERE vehicles.id = %(id)s;
        """
        vehicle = connectToMySQL(cls.db_schema).query_db(query, data)
        return vehicle[0]

    @classmethod
    def get_user_vehicles(cls, data):
        query = """
        SELECT * FROM vehicles
        WHERE vehicles.user_id = %(id)s;
        """
        vehicle_results = connectToMySQL(cls.db_schema).query_db(query, data)
        if len(vehicle_results) == 0:
            return []
        else:
            vehicle_list = []
            for vehicle in vehicle_results:
                every_vehicle = cls(vehicle)
                vehicle_list.append(every_vehicle)
            return vehicle_list

    @classmethod
    def update_vehicle(cls, data):
        query = """
        UPDATE vehicles 
        SET year = %(year)s, make = %(make)s, model = %(model)s, trim = %(trim)s, nickname = %(nickname)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_schema).query_db(query, data)

    @classmethod
    def delete_vehicle(cls, data):
        query = """
        DELETE FROM vehicles
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_schema).query_db(query, data)

    @staticmethod
    def validate_vehicle(vehicle_form):
        is_valid = True
        if len(vehicle_form["year"]) == 0:
            if len(vehicle_form["make"]) == 0:
                if len(vehicle_form["model"]) == 0:
                    if len(vehicle_form["trim"]) == 0:
                        if len(vehicle_form["nickname"]) == 0:
                            flash("All fields are required", "vehicle")
                            return False
        if len(vehicle_form["year"]) == 0:
            flash("Year is required", "vehicle")
            is_valid = False
        elif int(vehicle_form["year"]) < 1886:
            flash("Cars did not exist before 1886 silly goose. Please enter a valid year", "vehicle")
            is_valid = False
        elif int(vehicle_form["year"]) > 2023:
            flash("Unless you time traveled from the future Marty McFly. Please enter a valid year.", "vehicle")
            is_valid = False
        if len(vehicle_form["make"]) == 0:
            flash("Make is required", "vehicle")
            is_valid = False
        elif len(vehicle_form["make"]) < 2:
            flash("Make must be at least 2 characters long", "vehicle")
            is_valid = False
        elif len(vehicle_form["make"]) > 50:
            flash("Make must be less than 50 characters long", "vehicle")
            is_valid = False
        if len(vehicle_form["model"]) == 0:
            flash("Model is required", "vehicle")
            is_valid = False
        elif len(vehicle_form["model"]) < 2:
            flash("Model must be at least 2 characters long", "vehicle")
            is_valid = False
        elif len(vehicle_form["model"]) > 50:
            flash("Model must be less than 50 characters long", "vehicle")
            is_valid = False
        if len(vehicle_form["trim"]) == 0:
            flash("Trim is required", "vehicle")
            is_valid = False
        elif len(vehicle_form["trim"]) > 50:
            flash("Trim must be less than 50 characters long", "vehicle")
            is_valid = False
        if len(vehicle_form["nickname"]) == 0:
            flash("Nickname is required", "vehicle")
            is_valid = False
        elif len(vehicle_form["nickname"]) < 2:
            flash("Nickname must be at least 3 characters long", "vehicle")
            is_valid = False
        elif len(vehicle_form["nickname"]) > 50:
            flash("Nickname must be less than 50 characters long", "vehicle")
            is_valid = False
        return is_valid