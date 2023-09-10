from flask import render_template, redirect, session, request
from CMT.models import vehicle
from CMT import app


@app.route('/home')
def home_page():
    if "id" not in session:
        return redirect("/")
    else:
        user_vehicles = vehicle.Vehicle.get_user_vehicles({"id": session["id"]})
        loggged_user = session
        return render_template("vehicle_form.html", user = loggged_user, vehicles = user_vehicles)

@app.route('/add-vehicle', methods=['POST', 'GET'])
def add_vehicle():
    if "id" not in session:
        return redirect("/")
    if not vehicle.Vehicle.validate_vehicle(request.form):
        return redirect("/home")
    else:
        vehicle.Vehicle.create_vehicle(request.form)
        return redirect("/home")

@app.route('/<id>/edit-vehicle', methods=['POST', 'GET'])
def edit_vehicle_form(id):
    if "id" not in session:
        return redirect("/")
    else:
        loggged_user = session
        vehicle_update = vehicle.Vehicle.get_one_vehicle({"id": id})
        return render_template("vehicle_edit.html", user = loggged_user, vehicle_update = vehicle_update)

@app.route('/<id>/update-vehicle', methods=['POST'])
def update_vehicle_form(id):
    if "id" not in session:
        return redirect("/")
    elif not vehicle.Vehicle.validate_vehicle(request.form):
        return redirect(f"/{id}/edit-vehicle")
    else:
        vehicle.Vehicle.update_vehicle(request.form)
        return redirect("/home")
    

@app.route('/<id>/delete-vehicle')
def delete_vehicle_from_db(id):
    if "id" not in session:
        return redirect("/")
    else:
        vehicle.Vehicle.delete_vehicle({"id": id})
        return redirect("/home")