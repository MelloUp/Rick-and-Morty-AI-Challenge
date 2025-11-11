"""Location data models."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .character import Character


@dataclass(frozen=True)
class Location:
    """Location data model."""

    id: int
    name: str
    type: str
    dimension: str
    residents: List[str] = field(default_factory=list)
    url: str = ""
    created: str = ""
    residents_details: Optional[List[Character]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any], residents_details: Optional[List[Character]] = None) -> "Location":
        """
        Create Location from dictionary.

        Args:
            data: Dictionary containing location data
            residents_details: Optional list of character details

        Returns:
            Location instance
        """
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            dimension=data["dimension"],
            residents=data.get("residents", []),
            url=data.get("url", ""),
            created=data.get("created", ""),
            residents_details=residents_details
        )

    def to_dict(self, include_residents: bool = True) -> Dict[str, Any]:
        """
        Convert to dictionary.

        Args:
            include_residents: Whether to include resident details

        Returns:
            Dictionary representation
        """
        result = {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "dimension": self.dimension,
            "residents": self.residents,
            "url": self.url,
            "created": self.created
        }

        if include_residents and self.residents_details is not None:
            result["residents_details"] = [
                char.to_dict() for char in self.residents_details
            ]

        return result

    @property
    def resident_count(self) -> int:
        """Get number of residents."""
        return len(self.residents)

    def get_summary_context(self) -> Dict[str, Any]:
        """Get context for AI summary generation."""
        return {
            "name": self.name,
            "type": self.type,
            "dimension": self.dimension,
            "resident_count": self.resident_count
        }
