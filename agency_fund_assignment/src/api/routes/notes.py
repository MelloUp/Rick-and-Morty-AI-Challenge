"""Note routes."""

from flask import Blueprint, jsonify, request
from src.repositories import NoteRepository
from src.utils import ValidationError


def create_notes_blueprint(note_repo: NoteRepository) -> Blueprint:
    """
    Create notes blueprint.

    Args:
        note_repo: Note repository instance

    Returns:
        Blueprint for note routes
    """
    bp = Blueprint('notes', __name__, url_prefix='/api/notes')

    @bp.route('', methods=['POST'])
    def add_note():
        """Add a note for a character."""
        data = request.get_json()

        required_fields = ['character_id', 'character_name', 'note']
        if not all(field in data for field in required_fields):
            raise ValidationError(
                f"Missing required fields: {', '.join(required_fields)}"
            )

        note_id = note_repo.create(
            data['character_id'],
            data['character_name'],
            data['note']
        )

        return jsonify({
            'success': True,
            'note_id': note_id
        }), 201

    @bp.route('/<int:character_id>', methods=['GET'])
    def get_notes(character_id: int):
        """Get all notes for a character."""
        notes = note_repo.get_by_character_id(character_id)

        return jsonify({
            'success': True,
            'count': len(notes),
            'data': [note.to_dict() for note in notes]
        })

    @bp.route('/<int:note_id>', methods=['PUT'])
    def update_note(note_id: int):
        """Update an existing note."""
        data = request.get_json()

        if 'note' not in data:
            raise ValidationError("Missing required field: note")

        success = note_repo.update(note_id, data['note'])

        if not success:
            from src.utils import NotFoundError
            raise NotFoundError("Note")

        return jsonify({'success': True})

    @bp.route('/<int:note_id>', methods=['DELETE'])
    def delete_note(note_id: int):
        """Delete a note."""
        success = note_repo.delete(note_id)

        if not success:
            from src.utils import NotFoundError
            raise NotFoundError("Note")

        return jsonify({'success': True})

    return bp
