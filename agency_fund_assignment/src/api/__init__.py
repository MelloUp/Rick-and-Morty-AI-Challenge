"""API routes package."""

from flask import Flask
from .routes import register_blueprints


def create_app(config=None) -> Flask:
    """
    Create and configure Flask application.

    Args:
        config: Optional configuration object

    Returns:
        Configured Flask application
    """
    from src.config import get_config
    from src.database import get_db_connection, init_database

    app = Flask(__name__, static_folder='../../')

    # Load configuration
    app_config = config or get_config()
    app.config.from_object(app_config.flask)

    # Initialize database
    db = get_db_connection()
    init_database(db)

    # Register blueprints
    register_blueprints(app)

    # Register error handlers
    _register_error_handlers(app)

    return app


def _register_error_handlers(app: Flask) -> None:
    """Register global error handlers."""
    from src.utils import AppException

    @app.errorhandler(AppException)
    def handle_app_exception(error: AppException):
        """Handle application exceptions."""
        return error.to_dict(), error.status_code

    @app.errorhandler(404)
    def handle_404(error):
        """Handle 404 errors."""
        return {"success": False, "error": "Resource not found"}, 404

    @app.errorhandler(500)
    def handle_500(error):
        """Handle 500 errors."""
        return {"success": False, "error": "Internal server error"}, 500


__all__ = ["create_app"]
