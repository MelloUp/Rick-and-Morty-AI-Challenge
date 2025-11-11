"""Database migrations and schema initialization."""

from typing import List
from .connection import DatabaseConnection


class Migration:
    """Base class for database migrations."""

    @staticmethod
    def get_statements() -> List[str]:
        """Get SQL statements for this migration."""
        raise NotImplementedError


class CreateCharacterNotesTable(Migration):
    """Create character_notes table."""

    @staticmethod
    def get_statements() -> List[str]:
        return [
            """
            CREATE TABLE IF NOT EXISTS character_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL,
                character_name TEXT NOT NULL,
                note TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_character_notes_character_id
            ON character_notes(character_id)
            """
        ]


class CreateAPICacheTable(Migration):
    """Create api_cache table."""

    @staticmethod
    def get_statements() -> List[str]:
        return [
            """
            CREATE TABLE IF NOT EXISTS api_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cache_key TEXT UNIQUE NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_api_cache_key
            ON api_cache(cache_key)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_api_cache_expires
            ON api_cache(expires_at)
            """
        ]


class CreateCharacterEmbeddingsTable(Migration):
    """Create character_embeddings table."""

    @staticmethod
    def get_statements() -> List[str]:
        return [
            """
            CREATE TABLE IF NOT EXISTS character_embeddings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER UNIQUE NOT NULL,
                character_name TEXT NOT NULL,
                embedding TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_character_embeddings_character_id
            ON character_embeddings(character_id)
            """
        ]


def init_database(db: DatabaseConnection) -> None:
    """
    Initialize database with all migrations.

    Args:
        db: DatabaseConnection instance
    """
    migrations = [
        CreateCharacterNotesTable,
        CreateAPICacheTable,
        CreateCharacterEmbeddingsTable
    ]

    with db.get_connection() as conn:
        cursor = conn.cursor()

        for migration_class in migrations:
            migration = migration_class()
            for statement in migration.get_statements():
                cursor.execute(statement)

        conn.commit()
