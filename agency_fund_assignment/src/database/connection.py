"""Database connection management."""

import sqlite3
from contextlib import contextmanager
from typing import Generator, Optional
from functools import lru_cache

from src.config import get_config


class DatabaseConnection:
    """Database connection manager."""

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize database connection.

        Args:
            db_path: Optional custom database path
        """
        self.db_path = db_path or get_config().database.path

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """
        Context manager for database connections.

        Yields:
            sqlite3.Connection: Database connection

        Example:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM notes")
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def execute(
        self,
        query: str,
        params: tuple = (),
        fetch_one: bool = False,
        fetch_all: bool = False
    ):
        """
        Execute a query with automatic connection management.

        Args:
            query: SQL query to execute
            params: Query parameters
            fetch_one: Return single row
            fetch_all: Return all rows

        Returns:
            Query result or None
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)

            if fetch_one:
                return cursor.fetchone()
            if fetch_all:
                return cursor.fetchall()

            return cursor.lastrowid


@lru_cache(maxsize=1)
def get_db_connection(db_path: Optional[str] = None) -> DatabaseConnection:
    """
    Get database connection singleton.

    Args:
        db_path: Optional custom database path

    Returns:
        DatabaseConnection instance
    """
    return DatabaseConnection(db_path)
