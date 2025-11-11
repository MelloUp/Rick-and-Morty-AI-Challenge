"""Base repository class."""

from abc import ABC
from src.database.connection import DatabaseConnection


class BaseRepository(ABC):
    """Base class for all repositories."""

    def __init__(self, db: DatabaseConnection):
        """
        Initialize repository.

        Args:
            db: DatabaseConnection instance
        """
        self.db = db
