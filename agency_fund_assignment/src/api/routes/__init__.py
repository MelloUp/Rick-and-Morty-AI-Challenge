"""API routes blueprints."""

from flask import Flask
from flask_cors import CORS

from .locations import create_locations_blueprint
from .characters import create_characters_blueprint
from .notes import create_notes_blueprint
from .ai import create_ai_blueprint
from .search import create_search_blueprint
from .health import create_health_blueprint


def register_blueprints(app: Flask) -> None:
    """
    Register all API blueprints.

    Args:
        app: Flask application instance
    """
    # Enable CORS
    CORS(app)

    # Initialize services (dependency injection)
    from src.config import get_config
    from src.database import get_db_connection
    from src.repositories import (
        NoteRepository,
        CacheRepository,
        EmbeddingRepository
    )
    from src.services import (
        RickMortyService,
        GeminiService,
        SearchService
    )

    config = get_config()
    db = get_db_connection()

    # Repositories
    note_repo = NoteRepository(db)
    cache_repo = CacheRepository(db)
    embedding_repo = EmbeddingRepository(db)

    # Services
    rick_morty_service = RickMortyService(cache_repo, config.api)

    try:
        gemini_service = GeminiService(config.gemini)
        search_service = SearchService(
            embedding_repo,
            gemini_service,
            rick_morty_service
        )
        gemini_available = True
    except Exception as e:
        print(f"Warning: Gemini service not available: {e}")
        gemini_service = None
        search_service = None
        gemini_available = False

    # Register blueprints with dependencies
    app.register_blueprint(create_health_blueprint(gemini_available))
    app.register_blueprint(create_locations_blueprint(rick_morty_service))
    app.register_blueprint(create_characters_blueprint(rick_morty_service, note_repo))
    app.register_blueprint(create_notes_blueprint(note_repo))

    if gemini_available:
        app.register_blueprint(create_ai_blueprint(gemini_service, rick_morty_service))
        app.register_blueprint(create_search_blueprint(search_service))

    # Serve frontend
    @app.route('/')
    def index():
        """Serve main HTML page."""
        from flask import send_from_directory
        return send_from_directory('../..', 'index.html')


__all__ = ["register_blueprints"]
