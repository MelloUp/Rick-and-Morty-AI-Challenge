"""Rick and Morty API service with clean architecture."""

import requests
from typing import List, Dict, Any, Optional
from functools import lru_cache

from src.models import Character, Location
from src.repositories import CacheRepository
from src.config import APIConfig
from src.utils import ExternalAPIError, NotFoundError


class RickMortyService:
    """
    Service for interacting with Rick and Morty API.

    Uses REST API for:
    - Simpler implementation and debugging
    - Better HTTP caching support
    - Well-documented and stable endpoints
    """

    def __init__(
        self,
        cache_repo: CacheRepository,
        config: APIConfig
    ):
        """
        Initialize Rick and Morty service.

        Args:
            cache_repo: Cache repository for storing API responses
            config: API configuration
        """
        self.cache_repo = cache_repo
        self.config = config
        self.base_url = config.rick_morty_base_url
        self._session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create configured requests session."""
        session = requests.Session()
        session.headers.update({'Content-Type': 'application/json'})
        return session

    def _build_cache_key(self, endpoint: str, params: Optional[Dict] = None) -> str:
        """Build cache key from endpoint and params."""
        params_str = str(sorted(params.items())) if params else ""
        return f"rick_morty:{endpoint}:{params_str}"

    def _fetch(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Fetch data from API with caching support.

        Args:
            endpoint: API endpoint
            params: Query parameters
            use_cache: Whether to use cache

        Returns:
            API response data

        Raises:
            ExternalAPIError: If API request fails
            NotFoundError: If resource not found
        """
        cache_key = self._build_cache_key(endpoint, params)

        # Try cache first
        if use_cache:
            cached_data = self.cache_repo.get(cache_key)
            if cached_data:
                return cached_data

        # Fetch from API
        url = f"{self.base_url}/{endpoint}"
        try:
            response = self._session.get(
                url,
                params=params,
                timeout=self.config.request_timeout
            )
            response.raise_for_status()
            data = response.json()

            # Cache successful response
            if use_cache:
                self.cache_repo.set(
                    cache_key,
                    data,
                    ttl_minutes=self.config.cache_ttl_minutes
                )

            return data

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise NotFoundError(resource=endpoint.split('/')[0].title())
            raise ExternalAPIError(f"Rick and Morty API error: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise ExternalAPIError(f"Network error: {str(e)}")

    def get_all_locations(self) -> List[Location]:
        """
        Fetch all locations with pagination.

        Returns:
            List of all locations

        Raises:
            ExternalAPIError: If API request fails
        """
        locations = []
        page = 1

        while True:
            data = self._fetch("location", params={"page": page})
            page_locations = [
                Location.from_dict(loc_data)
                for loc_data in data['results']
            ]
            locations.extend(page_locations)

            if not data['info'].get('next'):
                break
            page += 1

        return locations

    def get_location(self, location_id: int) -> Location:
        """
        Get a specific location by ID.

        Args:
            location_id: Location ID

        Returns:
            Location instance

        Raises:
            NotFoundError: If location not found
            ExternalAPIError: If API request fails
        """
        data = self._fetch(f"location/{location_id}")
        return Location.from_dict(data)

    def get_location_with_residents(self, location_id: int) -> Location:
        """
        Get location with full resident details.

        Args:
            location_id: Location ID

        Returns:
            Location with resident details populated

        Raises:
            NotFoundError: If location not found
            ExternalAPIError: If API request fails
        """
        location_data = self._fetch(f"location/{location_id}")

        if not location_data['residents']:
            return Location.from_dict(location_data, residents_details=[])

        # Extract resident IDs and batch fetch
        resident_ids = [
            url.split('/')[-1]
            for url in location_data['residents']
        ]

        residents = self._fetch_characters_batch(resident_ids)

        return Location.from_dict(
            location_data,
            residents_details=residents
        )

    def get_all_locations_with_residents(self) -> List[Location]:
        """
        Get all locations with full resident details (optimized).

        Returns:
            List of locations with resident details

        Raises:
            ExternalAPIError: If API request fails
        """
        locations = self.get_all_locations()

        # Collect all unique character IDs
        all_character_ids = set()
        for location in locations:
            for resident_url in location.residents:
                char_id = resident_url.split('/')[-1]
                all_character_ids.add(char_id)

        # Batch fetch all characters
        characters_map = self._fetch_all_characters_map(list(all_character_ids))

        # Attach resident details to each location
        result = []
        for location in locations:
            resident_details = []
            for resident_url in location.residents:
                char_id = int(resident_url.split('/')[-1])
                if char_id in characters_map:
                    resident_details.append(characters_map[char_id])

            result.append(
                Location.from_dict(
                    location.to_dict(include_residents=False),
                    residents_details=resident_details
                )
            )

        return result

    def get_character(self, character_id: int) -> Character:
        """
        Get a specific character by ID.

        Args:
            character_id: Character ID

        Returns:
            Character instance

        Raises:
            NotFoundError: If character not found
            ExternalAPIError: If API request fails
        """
        data = self._fetch(f"character/{character_id}")
        return Character.from_dict(data)

    def search_characters(self, name: str) -> List[Character]:
        """
        Search characters by name.

        Args:
            name: Character name to search

        Returns:
            List of matching characters

        Raises:
            ExternalAPIError: If API request fails
        """
        try:
            data = self._fetch(
                "character",
                params={"name": name},
                use_cache=False
            )
            return [
                Character.from_dict(char_data)
                for char_data in data['results']
            ]
        except NotFoundError:
            return []

    def _fetch_characters_batch(self, character_ids: List[str]) -> List[Character]:
        """
        Fetch multiple characters in a single request.

        Args:
            character_ids: List of character IDs

        Returns:
            List of Character instances
        """
        if not character_ids:
            return []

        if len(character_ids) == 1:
            char = self.get_character(int(character_ids[0]))
            return [char]

        endpoint = f"character/{','.join(character_ids)}"
        data = self._fetch(endpoint)

        # API returns single object for one ID, array for multiple
        if isinstance(data, dict):
            return [Character.from_dict(data)]

        return [Character.from_dict(char_data) for char_data in data]

    def _fetch_all_characters_map(
        self,
        character_ids: List[str]
    ) -> Dict[int, Character]:
        """
        Fetch all characters and return as a map.

        Args:
            character_ids: List of character IDs

        Returns:
            Dictionary mapping character ID to Character instance
        """
        characters_map = {}

        # Batch requests in groups of 100 (API limit)
        batch_size = 100
        for i in range(0, len(character_ids), batch_size):
            batch = character_ids[i:i + batch_size]
            try:
                characters = self._fetch_characters_batch(batch)
                for char in characters:
                    characters_map[char.id] = char
            except (ExternalAPIError, NotFoundError):
                # Skip failed batches
                continue

        return characters_map
