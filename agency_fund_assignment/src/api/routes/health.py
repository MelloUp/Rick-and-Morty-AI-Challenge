"""Health check routes."""

from flask import Blueprint, jsonify


def create_health_blueprint(gemini_available: bool) -> Blueprint:
    """Create health check blueprint."""
    bp = Blueprint('health', __name__, url_prefix='/api')

    @bp.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'success': True,
            'status': 'healthy',
            'gemini_available': gemini_available
        })

    return bp
