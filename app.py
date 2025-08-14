from flask import Flask
from flask_cors import CORS
from routes.tool_routes import tool_bp

def create_app():
    """
    Create and configure the Flask application.

    :return: Configured Flask application instance.
    """
    app = Flask(__name__)
    
    # Enable CORS for all routes
    CORS(app, origins=["http://localhost:8080", "http://127.0.0.1:8080"])

    # Register the tool routes blueprint
    app.register_blueprint(tool_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)