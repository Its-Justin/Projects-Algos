from flask import render_template, redirect, session, request
from CMT.models import maintenance, vehicle
from CMT import app


@app.route('/<id>/maintenance-history')
def maintenances_view(id):
    if "id" not in session:
        return redirect("/")
    else:
        car_maintenances = maintenance.Maintenance.vehicle_maintenances({"id": id})
        main_vehicle = vehicle.Vehicle.get_one_vehicle({"id": id})
        return render_template("maintenance_view.html", main_vehicle = main_vehicle, car_maintenances = car_maintenances)

@app.route('/new-maintenance')
def maintenance_form():
    if "id" not in session:
        return redirect("/")
    else:
        all_vehicles = vehicle.Vehicle.get_user_vehicles({"id": session["id"]})
        user = session
        return render_template("maintenance_form.html", all_vehicles = all_vehicles, user = user)

@app.route('/create-maintenance', methods=['POST'])
def new_maintenance():
    if "id" not in session:
        return redirect("/")
    if not maintenance.Maintenance.validate_maintenance(request.form):
            return redirect("/new-maintenance")
    else:
        maintenance.Maintenance.create_maintenance(request.form)
        return redirect("/home")

@app.route('/<id>/edit-maintenance')
def edit_maintenance(id):
    if "id" not in session:
        return redirect("/")
    else:
        this_maintenance = maintenance.Maintenance.select_maintenance({"id": id})
        return render_template("maintenance_edit.html", maintenance = this_maintenance)

@app.route('/<id>/update-maintenance', methods=['POST'])
def updating_maintenance(id):
    if "id" not in session:
        return redirect("/")
    if not maintenance.Maintenance.validate_maintenance(request.form):
        return redirect("/")
    else:
        maintenance.Maintenance.update_maintenance(request.form)
        return redirect("/home")

@app.route("/<id>/delete-maintenance")
def deleting_maintenance(id):
    if "id" not in session:
        return redirect("/")
    else:
        maintenance.Maintenance.delete_maintenance({"id": id})
        return redirect("/home")