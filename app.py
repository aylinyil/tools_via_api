from flask import Flask
from routes.tool_routes import tool_bp

def create_app():
    """
    Create and configure the Flask application.

    :return: Configured Flask application instance.
    """
    app = Flask(__name__)

    # Register the tool routes blueprint
    app.register_blueprint(tool_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)