"""Gemini AI service for generative features and embeddings."""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import numpy as np
from dataclasses import dataclass

from src.config import GeminiConfig
from src.models import Character, Location
from src.utils import GeminiNotConfiguredError


@dataclass
class EvaluationResult:
    """Result from LLM evaluation."""

    score: int
    raw_response: str
    reasoning: str
    details: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "score": self.score,
            "raw_response": self.raw_response,
            "reasoning": self.reasoning,
            "details": self.details
        }


class GeminiService:
    """Service for Gemini AI operations."""

    def __init__(self, config: GeminiConfig):
        """
        Initialize Gemini service.

        Args:
            config: Gemini configuration

        Raises:
            GeminiNotConfiguredError: If API key not configured
        """
        if not config.is_available:
            raise GeminiNotConfiguredError()

        self.config = config
        genai.configure(api_key=config.api_key)
        self.model = genai.GenerativeModel(config.model_name)
        self.embedding_model = config.embedding_model

    def generate_location_summary(self, location: Location) -> str:
        """
        Generate Rick & Morty style narration for a location.

        Args:
            location: Location instance

        Returns:
            Generated summary text
        """
        context = location.get_summary_context()
        prompt = self._build_location_summary_prompt(context)

        response = self.model.generate_content(prompt)
        return response.text

    def generate_location_image_prompt(self, location: Location, summary: str) -> str:
        """
        Generate a detailed image prompt for a location.

        Args:
            location: Location instance
            summary: Generated summary text

        Returns:
            Image generation prompt
        """
        prompt = f"""
        Based on this Rick and Morty location and its summary, create a detailed image generation prompt
        that would produce a high-quality visual representation.

        Location: {location.name}
        Type: {location.type}
        Dimension: {location.dimension}
        Summary: {summary}

        Generate a single detailed prompt (2-3 sentences) for an AI image generator that captures:
        - The sci-fi, cartoon aesthetic of Rick and Morty
        - Key visual elements of this specific location
        - Vibrant colors and the show's art style

        Return ONLY the image prompt, nothing else.
        """

        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_character_dialogue(
        self,
        character1: Character,
        character2: Character
    ) -> str:
        """
        Generate a conversation between two characters.

        Args:
            character1: First character
            character2: Second character

        Returns:
            Generated dialogue text
        """
        prompt = self._build_dialogue_prompt(character1, character2)
        response = self.model.generate_content(prompt)
        return response.text

    def generate_dialogue_image_prompt(
        self,
        character1: Character,
        character2: Character,
        dialogue: str
    ) -> str:
        """
        Generate a detailed image prompt for a dialogue scene.

        Args:
            character1: First character
            character2: Second character
            dialogue: Generated dialogue text

        Returns:
            Image generation prompt
        """
        prompt = f"""
        Based on this Rick and Morty dialogue between two characters, create a detailed image generation prompt
        for a scene showing them in conversation.

        Character 1: {character1.name} ({character1.species})
        Character 2: {character2.name} ({character2.species})

        Dialogue excerpt:
        {dialogue[:200]}...

        Generate a single detailed prompt (2-3 sentences) for an AI image generator that:
        - Shows both characters in the Rick and Morty animated art style
        - Captures the mood and setting of their conversation
        - Uses vibrant colors and the show's signature sci-fi aesthetic
        - Shows the characters clearly with expressive poses

        Return ONLY the image prompt, nothing else.
        """

        response = self.model.generate_content(prompt)
        return response.text.strip()

    def generate_character_analysis(self, character: Character) -> str:
        """
        Generate analysis of a character.

        Args:
            character: Character instance

        Returns:
            Generated analysis text
        """
        prompt = self._build_analysis_prompt(character)
        response = self.model.generate_content(prompt)
        return response.text

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for semantic search.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        result = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']

    def generate_query_embedding(self, query: str) -> List[float]:
        """
        Generate embedding for search query.

        Args:
            query: Search query

        Returns:
            Query embedding vector
        """
        result = genai.embed_content(
            model=self.embedding_model,
            content=query,
            task_type="retrieval_query"
        )
        return result['embedding']

    def evaluate_factual_consistency(
        self,
        generated_text: str,
        source_data: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate factual consistency of generated text.

        Args:
            generated_text: Text to evaluate
            source_data: Source data to compare against

        Returns:
            EvaluationResult with score and details
        """
        prompt = self._build_factual_consistency_prompt(
            generated_text,
            source_data
        )

        response = self.model.generate_content(prompt)
        return self._parse_evaluation_response(response.text)

    def evaluate_creativity(self, generated_text: str) -> EvaluationResult:
        """
        Evaluate creativity of generated text.

        Args:
            generated_text: Text to evaluate

        Returns:
            EvaluationResult with score and details
        """
        prompt = self._build_creativity_prompt(generated_text)
        response = self.model.generate_content(prompt)
        return self._parse_evaluation_response(response.text)

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity score (0 to 1)
        """
        arr1 = np.array(vec1)
        arr2 = np.array(vec2)

        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    # Private helper methods for building prompts

    @staticmethod
    def _build_location_summary_prompt(context: Dict[str, Any]) -> str:
        """Build prompt for location summary generation."""
        return f"""
        You are the narrator from Rick and Morty. Generate a short, witty summary (2-3 sentences)
        about this location in the distinctive cynical and absurdist tone of the show.

        Location Details:
        - Name: {context['name']}
        - Type: {context['type']}
        - Dimension: {context['dimension']}
        - Number of Residents: {context['resident_count']}

        Make it funny, slightly dark, and remember to include some existential dread or sci-fi absurdity.
        """

    @staticmethod
    def _build_dialogue_prompt(char1: Character, char2: Character) -> str:
        """Build prompt for character dialogue generation."""
        return f"""
        Generate a short dialogue (4-6 lines) between these two Rick and Morty characters.
        Make it authentic to the show's humor and the characters' personalities.

        Character 1:
        - Name: {char1.name}
        - Species: {char1.species}
        - Status: {char1.status}
        - Location: {char1.location.name}

        Character 2:
        - Name: {char2.name}
        - Species: {char2.species}
        - Status: {char2.status}
        - Location: {char2.location.name}

        Format the dialogue as:
        {char1.name}: [their line]
        {char2.name}: [their line]
        (continue for 4-6 exchanges)
        """

    @staticmethod
    def _build_analysis_prompt(character: Character) -> str:
        """Build prompt for character analysis."""
        return f"""
        Provide a brief character analysis (2-3 sentences) for this Rick and Morty character.
        Focus on their significance, relationships, or interesting facts.

        Character:
        - Name: {character.name}
        - Species: {character.species}
        - Status: {character.status}
        - Gender: {character.gender}
        - Origin: {character.origin.name}
        - Current Location: {character.location.name}
        - Episodes Appeared: {len(character.episode)}

        Be informative but keep the Rick and Morty vibe.
        """

    @staticmethod
    def _build_factual_consistency_prompt(
        generated_text: str,
        source_data: Dict[str, Any]
    ) -> str:
        """Build prompt for factual consistency evaluation."""
        return f"""
        Evaluate if the following generated text is factually consistent with the source data.
        Rate on a scale of 1-10 and explain your reasoning.

        Source Data:
        {source_data}

        Generated Text:
        {generated_text}

        Respond in this format:
        Score: [1-10]
        Reasoning: [Your explanation]
        Issues: [List any factual inconsistencies, or "None" if consistent]
        """

    @staticmethod
    def _build_creativity_prompt(generated_text: str) -> str:
        """Build prompt for creativity evaluation."""
        return f"""
        Evaluate the creativity and entertainment value of this Rick and Morty themed text.
        Consider humor, originality, and how well it captures the show's tone.
        Rate on a scale of 1-10.

        Generated Text:
        {generated_text}

        Respond in this format:
        Score: [1-10]
        Reasoning: [Your explanation]
        Strengths: [What works well]
        Improvements: [What could be better]
        """

    @staticmethod
    def _parse_evaluation_response(response_text: str) -> EvaluationResult:
        """
        Parse evaluation response into structured format.

        Args:
            response_text: Raw response text from model

        Returns:
            EvaluationResult instance
        """
        lines = response_text.strip().split('\n')
        score = 0
        reasoning = ""
        details = {}

        for line in lines:
            if line.startswith('Score:'):
                try:
                    score_str = line.replace('Score:', '').strip()
                    # Extract just the number
                    score_str = ''.join(filter(str.isdigit, score_str))
                    score = int(score_str) if score_str else 0
                    score = min(max(score, 0), 10)  # Clamp to 0-10
                except ValueError:
                    score = 0
            elif line.startswith('Reasoning:'):
                reasoning = line.replace('Reasoning:', '').strip()
            elif ':' in line:
                key, value = line.split(':', 1)
                details[key.strip()] = value.strip()

        return EvaluationResult(
            score=score,
            raw_response=response_text,
            reasoning=reasoning,
            details=details
        )
