"""Location routes."""

from flask import Blueprint, jsonify, request
from src.services import RickMortyService


def create_locations_blueprint(rick_morty_service: RickMortyService) -> Blueprint:
    """
    Create locations blueprint.

    Args:
        rick_morty_service: Rick & Morty service instance

    Returns:
        Blueprint for location routes
    """
    bp = Blueprint('locations', __name__, url_prefix='/api/locations')

    @bp.route('', methods=['GET'])
    def get_locations():
        """Get all locations with optional resident details."""
        include_residents = request.args.get('include_residents', 'false').lower() == 'true'

        if include_residents:
            locations = rick_morty_service.get_all_locations_with_residents()
        else:
            locations = rick_morty_service.get_all_locations()

        return jsonify({
            'success': True,
            'count': len(locations),
            'data': [loc.to_dict(include_residents) for loc in locations]
        })

    @bp.route('/<int:location_id>', methods=['GET'])
    def get_location(location_id: int):
        """Get specific location with resident details."""
        location = rick_morty_service.get_location_with_residents(location_id)

        return jsonify({
            'success': True,
            'data': location.to_dict(include_residents=True)
        })

    return bp
