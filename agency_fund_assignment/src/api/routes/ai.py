"""AI feature routes."""

from flask import Blueprint, jsonify, request
from src.services import GeminiService, RickMortyService
from src.services.image_service import ImageGenerationService
from src.utils import ValidationError


def create_ai_blueprint(
    gemini_service: GeminiService,
    rick_morty_service: RickMortyService,
    image_service: ImageGenerationService = None
) -> Blueprint:
    """
    Create AI features blueprint.

    Args:
        gemini_service: Gemini service instance
        rick_morty_service: Rick & Morty service instance
        image_service: Image generation service instance (optional)

    Returns:
        Blueprint for AI routes
    """
    bp = Blueprint('ai', __name__, url_prefix='/api/ai')

    # Initialize image service if not provided
    if image_service is None:
        image_service = ImageGenerationService()

    @bp.route('/location-summary/<int:location_id>', methods=['GET'])
    def generate_location_summary(location_id: int):
        """Generate AI summary for a location."""
        location = rick_morty_service.get_location(location_id)
        summary = gemini_service.generate_location_summary(location)

        return jsonify({
            'success': True,
            'data': {
                'location': location.to_dict(include_residents=False),
                'summary': summary
            }
        })

    @bp.route('/character-dialogue', methods=['POST'])
    def generate_dialogue():
        """Generate dialogue between two characters."""
        data = request.get_json()

        required_fields = ['character1_id', 'character2_id']
        if not all(field in data for field in required_fields):
            raise ValidationError(
                f"Missing required fields: {', '.join(required_fields)}"
            )

        char1 = rick_morty_service.get_character(data['character1_id'])
        char2 = rick_morty_service.get_character(data['character2_id'])

        dialogue = gemini_service.generate_character_dialogue(char1, char2)

        # Get character images from API
        char1_dict = char1.to_dict()
        char2_dict = char2.to_dict()

        return jsonify({
            'success': True,
            'data': {
                'character1': char1_dict,
                'character2': char2_dict,
                'dialogue': dialogue,
                'character1_image': char1_dict.get('image'),
                'character2_image': char2_dict.get('image')
            }
        })

    @bp.route('/character-analysis/<int:character_id>', methods=['GET'])
    def generate_character_analysis(character_id: int):
        """Generate AI analysis of a character."""
        character = rick_morty_service.get_character(character_id)
        analysis = gemini_service.generate_character_analysis(character)

        return jsonify({
            'success': True,
            'data': {
                'character': character.to_dict(),
                'analysis': analysis
            }
        })

    # Evaluation endpoints
    @bp.route('/eval/factual-consistency', methods=['POST'])
    def evaluate_factual_consistency():
        """Evaluate factual consistency of generated text."""
        data = request.get_json()

        required_fields = ['generated_text', 'source_data']
        if not all(field in data for field in required_fields):
            raise ValidationError(
                f"Missing required fields: {', '.join(required_fields)}"
            )

        evaluation = gemini_service.evaluate_factual_consistency(
            data['generated_text'],
            data['source_data']
        )

        return jsonify({
            'success': True,
            'data': evaluation.to_dict()
        })

    @bp.route('/eval/creativity', methods=['POST'])
    def evaluate_creativity():
        """Evaluate creativity of generated text."""
        data = request.get_json()

        if 'generated_text' not in data:
            raise ValidationError("Missing required field: generated_text")

        evaluation = gemini_service.evaluate_creativity(data['generated_text'])

        return jsonify({
            'success': True,
            'data': evaluation.to_dict()
        })

    return bp
