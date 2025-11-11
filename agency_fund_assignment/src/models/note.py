"""Note data models."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass(frozen=True)
class Note:
    """Character note data model."""

    id: int
    character_id: int
    character_name: str
    note: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Note":
        """
        Create Note from dictionary.

        Args:
            data: Dictionary containing note data

        Returns:
            Note instance
        """
        return cls(
            id=data["id"],
            character_id=data["character_id"],
            character_name=data["character_name"],
            note=data["note"],
            created_at=cls._parse_datetime(data.get("created_at")),
            updated_at=cls._parse_datetime(data.get("updated_at"))
        )

    @staticmethod
    def _parse_datetime(dt_str: Optional[str]) -> datetime:
        """Parse datetime string."""
        if not dt_str:
            return datetime.now()

        try:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "character_id": self.character_id,
            "character_name": self.character_name,
            "note": self.note,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def create(
        cls,
        id: int,
        character_id: int,
        character_name: str,
        note: str
    ) -> "Note":
        """
        Create a new note with current timestamp.

        Args:
            id: Note ID
            character_id: Character ID
            character_name: Character name
            note: Note content

        Returns:
            Note instance
        """
        now = datetime.now()
        return cls(
            id=id,
            character_id=character_id,
            character_name=character_name,
            note=note,
            created_at=now,
            updated_at=now
        )
