"""
Comprehensive API tests for clean architecture.
Tests all endpoints with valid inputs and edge cases.
"""
import pytest
import os
from src.api import create_app
from src.config import get_config


@pytest.fixture
def app():
    """Create test application."""
    config = get_config()
    test_app = create_app(config)
    test_app.config['TESTING'] = True
    return test_app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns success."""
        response = client.get('/api/health')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert data['status'] == 'healthy'
        assert 'gemini_available' in data


class TestLocationEndpoints:
    """Test location-related endpoints."""

    def test_get_all_locations(self, client):
        """Test fetching all locations."""
        response = client.get('/api/locations')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'count' in data
        assert isinstance(data['data'], list)
        assert data['count'] > 0

    def test_get_locations_with_residents(self, client):
        """Test fetching locations with resident details."""
        response = client.get('/api/locations?include_residents=true')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert isinstance(data['data'], list)

        if len(data['data']) > 0:
            first_location = data['data'][0]
            assert 'residents_details' in first_location

    def test_get_specific_location(self, client):
        """Test fetching a specific location by ID."""
        response = client.get('/api/locations/1')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert data['data']['id'] == 1
        assert 'name' in data['data']
        assert 'type' in data['data']
        assert 'residents_details' in data['data']

    def test_get_invalid_location(self, client):
        """Test fetching a non-existent location."""
        response = client.get('/api/locations/99999')
        assert response.status_code == 404

        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data


class TestCharacterEndpoints:
    """Test character-related endpoints."""

    def test_get_character_by_id(self, client):
        """Test fetching a specific character."""
        response = client.get('/api/characters/1')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert 'character' in data['data']
        assert 'notes' in data['data']
        assert data['data']['character']['id'] == 1

    def test_get_invalid_character(self, client):
        """Test fetching a non-existent character."""
        response = client.get('/api/characters/99999')
        assert response.status_code == 404

        data = response.get_json()
        assert data['success'] is False

    def test_search_characters_by_name(self, client):
        """Test searching characters by name."""
        response = client.get('/api/characters/search?name=Rick')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert data['count'] > 0

        for char in data['data']:
            assert 'rick' in char['name'].lower()

    def test_search_characters_no_query(self, client):
        """Test search with empty query."""
        response = client.get('/api/characters/search')
        assert response.status_code == 400

        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data

    def test_search_characters_no_results(self, client):
        """Test search with no matching results."""
        response = client.get('/api/characters/search?name=XYZNonexistentName123')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert data['count'] == 0
        assert len(data['data']) == 0


class TestNotesEndpoints:
    """Test notes CRUD operations."""

    def test_add_note(self, client):
        """Test adding a note for a character."""
        note_data = {
            'character_id': 1,
            'character_name': 'Rick Sanchez',
            'note': 'Genius scientist with alcohol problems'
        }

        response = client.post(
            '/api/notes',
            json=note_data
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'note_id' in data
        assert isinstance(data['note_id'], int)

    def test_add_note_missing_fields(self, client):
        """Test adding note with missing required fields."""
        note_data = {
            'character_id': 1,
            'note': 'Some note'
        }

        response = client.post('/api/notes', json=note_data)

        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data

    def test_get_notes_for_character(self, client):
        """Test retrieving notes for a character."""
        # First add a note
        note_data = {
            'character_id': 2,
            'character_name': 'Morty Smith',
            'note': 'Often reluctant sidekick'
        }
        client.post('/api/notes', json=note_data)

        # Then retrieve notes
        response = client.get('/api/notes/2')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert data['count'] > 0


class TestEdgeCases:
    """Test edge cases and corner scenarios."""

    def test_negative_character_id(self, client):
        """Test negative character ID."""
        response = client.get('/api/characters/-1')
        assert response.status_code == 404

    def test_very_large_character_id(self, client):
        """Test extremely large character ID."""
        response = client.get('/api/characters/999999999')
        assert response.status_code == 404

    def test_special_characters_in_search(self, client):
        """Test search with special characters."""
        response = client.get('/api/characters/search?name=@#$%')
        assert response.status_code == 200

        data = response.get_json()
        assert data['success'] is True
        assert data['count'] == 0

    def test_empty_note_content(self, client):
        """Test adding an empty note."""
        note_data = {
            'character_id': 1,
            'character_name': 'Rick Sanchez',
            'note': ''
        }

        response = client.post('/api/notes', json=note_data)
        assert response.status_code == 201

    def test_unicode_in_notes(self, client):
        """Test Unicode characters in notes."""
        note_data = {
            'character_id': 1,
            'character_name': 'Rick Sanchez',
            'note': 'Testing Unicode: 你好 🚀 café'
        }

        response = client.post('/api/notes', json=note_data)
        assert response.status_code == 201


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
