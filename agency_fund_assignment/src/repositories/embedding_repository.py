"""Embedding repository for semantic search."""

import json
from typing import List, Dict, Any, Optional

from src.utils import DatabaseError
from .base import BaseRepository


class EmbeddingRepository(BaseRepository):
    """Repository for character embeddings."""

    def save(
        self,
        character_id: int,
        character_name: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Save character embedding.

        Args:
            character_id: Character ID
            character_name: Character name
            embedding: Embedding vector
            metadata: Optional metadata

        Raises:
            DatabaseError: If save fails
        """
        try:
            query = """
                INSERT OR REPLACE INTO character_embeddings
                (character_id, character_name, embedding, metadata)
                VALUES (?, ?, ?, ?)
            """
            self.db.execute(
                query,
                (
                    character_id,
                    character_name,
                    json.dumps(embedding),
                    json.dumps(metadata) if metadata else None
                )
            )
        except Exception as e:
            raise DatabaseError(f"Failed to save embedding: {str(e)}")

    def get(self, character_id: int) -> Optional[List[float]]:
        """
        Get embedding for a character.

        Args:
            character_id: Character ID

        Returns:
            Embedding vector if found, None otherwise
        """
        try:
            query = """
                SELECT embedding FROM character_embeddings
                WHERE character_id = ?
            """
            row = self.db.execute(query, (character_id,), fetch_one=True)

            if row:
                return json.loads(row['embedding'])
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch embedding: {str(e)}")

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Get all character embeddings.

        Returns:
            List of dictionaries with character ID, name, embedding, and metadata
        """
        try:
            query = """
                SELECT character_id, character_name, embedding, metadata
                FROM character_embeddings
            """
            rows = self.db.execute(query, fetch_all=True)

            return [
                {
                    'character_id': row['character_id'],
                    'character_name': row['character_name'],
                    'embedding': json.loads(row['embedding']),
                    'metadata': json.loads(row['metadata']) if row['metadata'] else None
                }
                for row in (rows or [])
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch all embeddings: {str(e)}")

    def exists(self, character_id: int) -> bool:
        """
        Check if embedding exists for a character.

        Args:
            character_id: Character ID

        Returns:
            True if exists, False otherwise
        """
        try:
            query = """
                SELECT 1 FROM character_embeddings
                WHERE character_id = ?
            """
            row = self.db.execute(query, (character_id,), fetch_one=True)
            return row is not None
        except Exception as e:
            raise DatabaseError(f"Failed to check embedding existence: {str(e)}")

    def delete(self, character_id: int) -> bool:
        """
        Delete embedding for a character.

        Args:
            character_id: Character ID

        Returns:
            True if deleted, False if not found
        """
        try:
            query = "DELETE FROM character_embeddings WHERE character_id = ?"
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (character_id,))
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseError(f"Failed to delete embedding: {str(e)}")

    def count(self) -> int:
        """
        Get count of indexed characters.

        Returns:
            Number of indexed characters
        """
        try:
            query = "SELECT COUNT(*) as count FROM character_embeddings"
            row = self.db.execute(query, fetch_one=True)
            return row['count'] if row else 0
        except Exception as e:
            raise DatabaseError(f"Failed to count embeddings: {str(e)}")
