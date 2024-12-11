from flask import Flask
from routes.booking_routes import booking_blueprint  # Import your booking routes

app = Flask(__name__)

# Register blueprints
app.register_blueprint(booking_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
