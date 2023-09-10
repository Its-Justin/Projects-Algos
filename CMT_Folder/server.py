from CMT import app

from CMT.controllers import user_controller, vehicle_controller, maintenance_controller

if __name__ == "__main__":
    app.run(debug=True)