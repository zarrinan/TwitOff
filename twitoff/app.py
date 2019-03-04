# main app and routing logic
from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    @app.route('/')
    def root():
        return 'Welcome to TwitOff!'

    return app
