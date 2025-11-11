"""Image generation service for AI features."""

import requests
from typing import Optional
from urllib.parse import quote
import time


class ImageGenerationService:
    """Service for generating images using AI models."""

    def __init__(self):
        """Initialize image generation service."""
        # Using Pollinations AI - free, no API key required
        self.base_url = "https://image.pollinations.ai/prompt"

    def generate_image_url(
        self,
        prompt: str,
        width: int = 1024,
        height: int = 768,
        seed: Optional[int] = None,
        model: str = "flux"
    ) -> str:
        """
        Generate an image URL from a text prompt.

        Args:
            prompt: Text description of the image to generate
            width: Image width (default: 1024)
            height: Image height (default: 768)
            seed: Random seed for reproducibility (optional)
            model: Model to use (flux, turbo, or other supported models)

        Returns:
            URL of the generated image
        """
        # Encode the prompt for URL
        encoded_prompt = quote(prompt)

        # Build URL with parameters
        url = f"{self.base_url}/{encoded_prompt}"
        params = []

        if width:
            params.append(f"width={width}")
        if height:
            params.append(f"height={height}")
        if seed:
            params.append(f"seed={seed}")
        if model:
            params.append(f"model={model}")

        if params:
            url += "?" + "&".join(params)

        return url

    def generate_location_image_prompt(self, location_data: dict, summary: str) -> str:
        """
        Generate an image prompt for a location based on its data and summary.

        Args:
            location_data: Location information
            summary: Generated summary text

        Returns:
            Detailed image prompt for generation
        """
        name = location_data.get('name', 'Unknown Location')
        location_type = location_data.get('type', 'Unknown')
        dimension = location_data.get('dimension', 'Unknown')

        prompt = (
            f"Rick and Morty style sci-fi illustration of {name}, "
            f"a {location_type} in {dimension}. "
            f"Vibrant colors, cartoon style, science fiction elements, "
            f"portal green accents, cosmic background, detailed environment. "
            f"High quality digital art, animated series aesthetic."
        )

        return prompt

    def generate_dialogue_scene_prompt(
        self,
        char1_data: dict,
        char2_data: dict,
        dialogue: str
    ) -> str:
        """
        Generate an image prompt for a dialogue scene between characters.

        Args:
            char1_data: First character information
            char2_data: Second character information
            dialogue: Generated dialogue text

        Returns:
            Detailed image prompt for generation
        """
        char1_name = char1_data.get('name', 'Character 1')
        char2_name = char2_data.get('name', 'Character 2')

        prompt = (
            f"Rick and Morty animated style scene showing {char1_name} and {char2_name} "
            f"having a conversation. Both characters clearly visible, "
            f"vibrant colors, cartoon aesthetic, science fiction background, "
            f"expressive faces, high quality digital art matching the show's style. "
            f"Wide shot, detailed characters, portal green and space blue color scheme."
        )

        return prompt

    def verify_image_url(self, url: str, timeout: int = 10) -> bool:
        """
        Verify that an image URL is accessible.

        Args:
            url: Image URL to verify
            timeout: Request timeout in seconds

        Returns:
            True if image is accessible, False otherwise
        """
        try:
            response = requests.head(url, timeout=timeout, allow_redirects=True)
            return response.status_code == 200
        except Exception:
            return False

    def get_character_image_url(self, character_data: dict) -> Optional[str]:
        """
        Get character image URL from Rick and Morty API data.

        Args:
            character_data: Character information from API

        Returns:
            Character image URL or None
        """
        return character_data.get('image')
