"""Character routes."""

from flask import Blueprint, jsonify, request
from src.services import RickMortyService
from src.repositories import NoteRepository
from src.utils import ValidationError


def create_characters_blueprint(
    rick_morty_service: RickMortyService,
    note_repo: NoteRepository
) -> Blueprint:
    """
    Create characters blueprint.

    Args:
        rick_morty_service: Rick & Morty service instance
        note_repo: Note repository instance

    Returns:
        Blueprint for character routes
    """
    bp = Blueprint('characters', __name__, url_prefix='/api/characters')

    @bp.route('/<int:character_id>', methods=['GET'])
    def get_character(character_id: int):
        """Get character details with notes."""
        character = rick_morty_service.get_character(character_id)
        notes = note_repo.get_by_character_id(character_id)

        return jsonify({
            'success': True,
            'data': {
                'character': character.to_dict(),
                'notes': [note.to_dict() for note in notes]
            }
        })

    @bp.route('/search', methods=['GET'])
    def search_characters():
        """Search characters by name."""
        name = request.args.get('name', '')

        if not name:
            raise ValidationError("Name parameter is required")

        characters = rick_morty_service.search_characters(name)

        return jsonify({
            'success': True,
            'count': len(characters),
            'data': [char.to_dict() for char in characters]
        })

    return bp
