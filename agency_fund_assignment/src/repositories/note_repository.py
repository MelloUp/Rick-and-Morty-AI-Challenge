"""Note repository for database operations."""

from datetime import datetime
from typing import List, Optional

from src.models import Note
from src.utils import DatabaseError
from .base import BaseRepository


class NoteRepository(BaseRepository):
    """Repository for note database operations."""

    def create(self, character_id: int, character_name: str, note: str) -> int:
        """
        Create a new note.

        Args:
            character_id: ID of the character
            character_name: Name of the character
            note: Note content

        Returns:
            ID of created note

        Raises:
            DatabaseError: If creation fails
        """
        try:
            query = """
                INSERT INTO character_notes (character_id, character_name, note)
                VALUES (?, ?, ?)
            """
            note_id = self.db.execute(query, (character_id, character_name, note))
            return note_id
        except Exception as e:
            raise DatabaseError(f"Failed to create note: {str(e)}")

    def get_by_character_id(self, character_id: int) -> List[Note]:
        """
        Get all notes for a character.

        Args:
            character_id: ID of the character

        Returns:
            List of notes for the character
        """
        try:
            query = """
                SELECT * FROM character_notes
                WHERE character_id = ?
                ORDER BY created_at DESC
            """
            rows = self.db.execute(query, (character_id,), fetch_all=True)

            return [
                Note.from_dict(dict(row))
                for row in (rows or [])
            ]
        except Exception as e:
            raise DatabaseError(f"Failed to fetch notes: {str(e)}")

    def update(self, note_id: int, note: str) -> bool:
        """
        Update an existing note.

        Args:
            note_id: ID of the note to update
            note: New note content

        Returns:
            True if updated, False if note not found

        Raises:
            DatabaseError: If update fails
        """
        try:
            query = """
                UPDATE character_notes
                SET note = ?, updated_at = ?
                WHERE id = ?
            """
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (note, datetime.now(), note_id))
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseError(f"Failed to update note: {str(e)}")

    def delete(self, note_id: int) -> bool:
        """
        Delete a note.

        Args:
            note_id: ID of the note to delete

        Returns:
            True if deleted, False if note not found

        Raises:
            DatabaseError: If deletion fails
        """
        try:
            query = "DELETE FROM character_notes WHERE id = ?"
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (note_id,))
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseError(f"Failed to delete note: {str(e)}")

    def get_by_id(self, note_id: int) -> Optional[Note]:
        """
        Get a specific note by ID.

        Args:
            note_id: ID of the note

        Returns:
            Note if found, None otherwise
        """
        try:
            query = "SELECT * FROM character_notes WHERE id = ?"
            row = self.db.execute(query, (note_id,), fetch_one=True)

            if row:
                return Note.from_dict(dict(row))
            return None
        except Exception as e:
            raise DatabaseError(f"Failed to fetch note: {str(e)}")
