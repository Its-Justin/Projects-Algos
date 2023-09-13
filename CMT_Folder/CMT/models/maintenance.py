from CMT.config.mysqlconnection import connectToMySQL
from CMT import app
from flask import flash
from CMT.models import vehicle

class Maintenance:

    db_schema = "cmt_schema"

    def __init__(self, data):
        self.id = data["id"]
        self.date = data["date"]
        self.type = data["type"]
        self.mileage = data["mileage"]
        self.comments = data["comments"]
        self.vehicle_id = data["vehicle_id"]
        self.vehicle_user_id = data["vehicle_user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.vehicle = None

    @classmethod
    def create_maintenance(cls, data):
        query = """
        INSERT INTO maintenances(date, type, mileage, comments, vehicle_id, vehicle_user_id)
        VALUES (%(date)s, %(type)s, %(mileage)s, %(comments)s, %(vehicle_id)s, %(vehicle_user_id)s);
        """
        return connectToMySQL(cls.db_schema).query_db(query, data)

    @classmethod
    def vehicle_maintenances(cls, data):
        query = """
        SELECT * FROM maintenances
        WHERE vehicle_id = %(id)s
        """
        maintenances_result = connectToMySQL(cls.db_schema).query_db(query, data)
        if len(maintenances_result) == 0:
            return []
        else:
            maintenance_list = []
            for maintenance in maintenances_result:
                every_maintenance = cls(maintenance)
                maintenance_list.append(every_maintenance)
            return maintenance_list

    @classmethod
    
    def select_maintenance(cls, data):
        query ="""
        SELECT * FROM maintenances
        LEFT JOIN vehicles
        ON vehicles.id = maintenances.vehicle_id
        WHERE maintenances.id = %(id)s
        """
        maintenance_result = connectToMySQL(cls.db_schema).query_db(query, data)
        if len(maintenance_result) == 0:
            return []
        else:
            maintenance_list = []
            for maintenance in maintenance_result:
                this_maintenance = cls(maintenance)
                vehicle_dict = {
                    "id": maintenance["vehicles.id"],
                    "year": maintenance["year"],
                    "make": maintenance["make"],
                    "model": maintenance["model"],
                    "trim": maintenance["trim"],
                    "nickname": maintenance["nickname"],
                    "user_id": maintenance["user_id"],
                    "created_at": maintenance["vehicles.created_at"],
                    "updated_at": maintenance["vehicles.updated_at"]
                }
                vehicle_object = vehicle.Vehicle(vehicle_dict)
                this_maintenance.vehicle = vehicle_object
                maintenance_list.append(this_maintenance)
                return this_maintenance

    @classmethod
    def update_maintenance(cls, data):
        query = """
        UPDATE maintenances
        SET date = %(date)s, type = %(type)s, mileage = %(mileage)s, comments = %(comments)s
        WHERE id = %(id)s
        """
        return connectToMySQL(cls.db_schema).query_db(query, data)

    @classmethod
    def delete_maintenance(cls, data):
        query = """
        DELETE FROM maintenances
        WHERE id = %(id)s
        """
        return connectToMySQL(cls.db_schema).query_db(query, data)

    @staticmethod
    def validate_maintenance(maintenance_form):
        is_valid = True
        if len(maintenance_form["vehicle_id"]) == 0:
            if len(maintenance_form["date"]) == 0:
                if len(maintenance_form["type"]) == 0:
                    if len(maintenance_form["mileage"]) == 0:
                        flash("All fields required", "maintenance")
                        return False
        if len(maintenance_form["vehicle_id"]) == 0:
            flash("Please select a vehicle.", "maintenance")
            is_valid = False
        if len(maintenance_form["date"]) == 0:
            flash("Date is required", "maintenance")
            is_valid = False
        if len(maintenance_form["type"]) == 0:
            flash("Miantenance Type is required", "maintenance")
            is_valid = False
        elif len(maintenance_form["type"]) < 3:
            flash("Maintenance type must be at least 3 characters long.", "maintenance")
            is_valid = False
        elif len(maintenance_form["type"]) > 100:
            flash("Maintenance type must be less than 100 characters long.", "maintenance")
            is_valid = False
        for number in maintenance_form["mileage"]:
            if number == ".":
                flash("Mileage can only have numbers.", "maintenance")
                return False
        if len(maintenance_form["mileage"]) == 0:
            flash("Mileage is required.", "maintenance")
            is_valid = False
        elif int(maintenance_form["mileage"]) < 1:
            flash("Mileage must be greater than 0.", "maintenance")
            is_valid = False
        elif int(maintenance_form["mileage"]) > 999999:
            flash("Mileage must be less than 1,000,000.", "maintenance")
            is_valid = False
        return is_valid
