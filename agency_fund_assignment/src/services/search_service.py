"""Semantic search service."""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from src.repositories import EmbeddingRepository
from .gemini_service import GeminiService
from .rick_morty_service import RickMortyService
from src.models import Character


@dataclass
class SearchResult:
    """Search result with similarity score."""

    character: Character
    similarity: float
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "character_id": self.character.id,
            "character_name": self.character.name,
            "similarity": self.similarity,
            "metadata": self.metadata,
            "character": self.character.to_dict()
        }


class SearchService:
    """Service for semantic search operations."""

    def __init__(
        self,
        embedding_repo: EmbeddingRepository,
        gemini_service: GeminiService,
        rick_morty_service: RickMortyService
    ):
        """
        Initialize search service.

        Args:
            embedding_repo: Repository for embeddings
            gemini_service: Gemini service for embedding generation
            rick_morty_service: Rick & Morty service for character data
        """
        self.embedding_repo = embedding_repo
        self.gemini_service = gemini_service
        self.rick_morty_service = rick_morty_service

    def index_character(self, character_id: int) -> bool:
        """
        Index a single character for semantic search.

        Args:
            character_id: Character ID to index

        Returns:
            True if successful, False otherwise
        """
        try:
            character = self.rick_morty_service.get_character(character_id)

            # Generate embedding
            text = character.get_description()
            embedding = self.gemini_service.generate_embedding(text)

            # Save to repository
            metadata = {
                "species": character.species,
                "status": character.status,
                "gender": character.gender
            }

            self.embedding_repo.save(
                character.id,
                character.name,
                embedding,
                metadata
            )

            return True
        except Exception as e:
            print(f"Failed to index character {character_id}: {e}")
            return False

    def index_characters(
        self,
        character_ids: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Index multiple characters for semantic search.

        Args:
            character_ids: List of character IDs to index (default: 1-50)

        Returns:
            Dictionary with indexed_count and errors
        """
        if character_ids is None:
            character_ids = list(range(1, 51))  # Default to first 50

        indexed_count = 0
        errors = []

        for char_id in character_ids:
            if self.index_character(char_id):
                indexed_count += 1
            else:
                errors.append({
                    "character_id": char_id,
                    "error": "Failed to index"
                })

        return {
            "indexed_count": indexed_count,
            "errors": errors
        }

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> List[SearchResult]:
        """
        Perform semantic search.

        Args:
            query: Natural language query
            top_k: Number of results to return

        Returns:
            List of SearchResult objects ranked by similarity

        Raises:
            ValueError: If no embeddings are indexed
        """
        # Get all embeddings
        all_embeddings = self.embedding_repo.get_all()

        if not all_embeddings:
            raise ValueError("No character embeddings found. Please index characters first.")

        # Generate query embedding
        query_embedding = self.gemini_service.generate_query_embedding(query)

        # Calculate similarities
        results = []
        for item in all_embeddings:
            similarity = self.gemini_service.cosine_similarity(
                query_embedding,
                item['embedding']
            )

            # Fetch full character details
            character = self.rick_morty_service.get_character(
                item['character_id']
            )

            results.append(
                SearchResult(
                    character=character,
                    similarity=similarity,
                    metadata=item['metadata'] or {}
                )
            )

        # Sort by similarity (highest first) and return top-k
        results.sort(key=lambda x: x.similarity, reverse=True)
        return results[:top_k]

    def get_indexed_count(self) -> int:
        """
        Get number of indexed characters.

        Returns:
            Count of indexed characters
        """
        return self.embedding_repo.count()

    def is_character_indexed(self, character_id: int) -> bool:
        """
        Check if a character is indexed.

        Args:
            character_id: Character ID

        Returns:
            True if indexed, False otherwise
        """
        return self.embedding_repo.exists(character_id)

    def reindex_character(self, character_id: int) -> bool:
        """
        Reindex a character (delete and recreate embedding).

        Args:
            character_id: Character ID

        Returns:
            True if successful
        """
        self.embedding_repo.delete(character_id)
        return self.index_character(character_id)
