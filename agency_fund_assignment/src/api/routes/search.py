"""Semantic search routes."""

from flask import Blueprint, jsonify, request
from src.services import SearchService
from src.utils import ValidationError


def create_search_blueprint(search_service: SearchService) -> Blueprint:
    """
    Create semantic search blueprint.

    Args:
        search_service: Search service instance

    Returns:
        Blueprint for search routes
    """
    bp = Blueprint('search', __name__, url_prefix='/api/search')

    @bp.route('/index-characters', methods=['POST'])
    def index_characters():
        """Index characters for semantic search."""
        data = request.get_json() or {}
        character_ids = data.get('character_ids')

        result = search_service.index_characters(character_ids)

        return jsonify({
            'success': True,
            **result
        })

    @bp.route('/semantic', methods=['POST'])
    def semantic_search():
        """Perform semantic search across characters."""
        data = request.get_json()

        if 'query' not in data:
            raise ValidationError("Missing required field: query")

        query = data['query']
        top_k = data.get('top_k', 5)

        try:
            results = search_service.search(query, top_k)

            return jsonify({
                'success': True,
                'query': query,
                'count': len(results),
                'data': [result.to_dict() for result in results]
            })
        except ValueError as e:
            raise ValidationError(str(e))

    return bp
