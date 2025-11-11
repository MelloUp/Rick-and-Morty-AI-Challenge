"""Character data models."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass(frozen=True)
class CharacterOrigin:
    """Character origin information."""

    name: str
    url: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CharacterOrigin":
        """Create from dictionary."""
        return cls(
            name=data.get("name", ""),
            url=data.get("url", "")
        )


@dataclass(frozen=True)
class CharacterLocation:
    """Character location information."""

    name: str
    url: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CharacterLocation":
        """Create from dictionary."""
        return cls(
            name=data.get("name", ""),
            url=data.get("url", "")
        )


@dataclass(frozen=True)
class Character:
    """Character data model."""

    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin: CharacterOrigin
    location: CharacterLocation
    image: str
    episode: List[str] = field(default_factory=list)
    url: str = ""
    created: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Character":
        """
        Create Character from dictionary.

        Args:
            data: Dictionary containing character data

        Returns:
            Character instance
        """
        return cls(
            id=data["id"],
            name=data["name"],
            status=data["status"],
            species=data["species"],
            type=data.get("type", ""),
            gender=data["gender"],
            origin=CharacterOrigin.from_dict(data["origin"]),
            location=CharacterLocation.from_dict(data["location"]),
            image=data["image"],
            episode=data.get("episode", []),
            url=data.get("url", ""),
            created=data.get("created", "")
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "species": self.species,
            "type": self.type,
            "gender": self.gender,
            "origin": {
                "name": self.origin.name,
                "url": self.origin.url
            },
            "location": {
                "name": self.location.name,
                "url": self.location.url
            },
            "image": self.image,
            "episode": self.episode,
            "url": self.url,
            "created": self.created
        }

    def get_description(self) -> str:
        """Get comprehensive description for embedding generation."""
        parts = [
            f"Name: {self.name}",
            f"Status: {self.status}",
            f"Species: {self.species}",
        ]

        if self.type:
            parts.append(f"Type: {self.type}")

        parts.extend([
            f"Gender: {self.gender}",
            f"Origin: {self.origin.name}",
            f"Current Location: {self.location.name}",
        ])

        return ". ".join(parts)
