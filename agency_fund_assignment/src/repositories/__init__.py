"""Repository pattern for data access."""

from .note_repository import NoteRepository
from .cache_repository import CacheRepository
from .embedding_repository import EmbeddingRepository

__all__ = [
    "NoteRepository",
    "CacheRepository",
    "EmbeddingRepository"
]
