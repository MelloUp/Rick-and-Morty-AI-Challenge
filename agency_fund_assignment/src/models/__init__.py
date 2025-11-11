"""Data models for the application."""

from .character import Character, CharacterOrigin, CharacterLocation
from .location import Location
from .note import Note

__all__ = [
    "Character",
    "CharacterOrigin",
    "CharacterLocation",
    "Location",
    "Note"
]
