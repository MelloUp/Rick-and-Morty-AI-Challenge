"""
Rick & Morty AI Challenge - Main Application Entry Point.

Clean, modular architecture with:
- Dependency injection
- Repository pattern
- Service layer
- Flask blueprints
- Proper error handling
"""

from src.api import create_app
from src.config import get_config


def main():
    """Run the Flask application."""
    config = get_config()
    app = create_app(config)

    print("=" * 60)
    print("Rick & Morty AI Challenge - Clean Architecture")
    print("=" * 60)
    print(f"\nServer starting at http://{config.flask.host}:{config.flask.port}")
    print(f"Gemini AI: {'Enabled' if config.gemini.is_available else 'Disabled'}")
    print("\nPress Ctrl+C to stop\n")

    app.run(
        host=config.flask.host,
        port=config.flask.port,
        debug=config.flask.debug
    )


if __name__ == '__main__':
    main()
