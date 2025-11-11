"""Cache repository for API response caching."""

import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from src.utils import DatabaseError
from .base import BaseRepository


class CacheRepository(BaseRepository):
    """Repository for caching API responses."""

    def get(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Get cached data by key.

        Args:
            cache_key: Cache key

        Returns:
            Cached data if found and not expired, None otherwise
        """
        try:
            query = """
                SELECT data FROM api_cache
                WHERE cache_key = ?
                AND (expires_at IS NULL OR expires_at > ?)
            """
            row = self.db.execute(
                query,
                (cache_key, datetime.now()),
                fetch_one=True
            )

            if row:
                return json.loads(row['data'])
            return None
        except Exception as e:
            # Don't raise error for cache misses
            print(f"Cache fetch error: {e}")
            return None

    def set(
        self,
        cache_key: str,
        data: Dict[str, Any],
        ttl_minutes: int = 60
    ) -> None:
        """
        Set cache data with expiration.

        Args:
            cache_key: Cache key
            data: Data to cache
            ttl_minutes: Time to live in minutes

        Raises:
            DatabaseError: If cache set fails
        """
        try:
            expires_at = datetime.now() + timedelta(minutes=ttl_minutes)
            query = """
                INSERT OR REPLACE INTO api_cache (cache_key, data, expires_at)
                VALUES (?, ?, ?)
            """
            self.db.execute(
                query,
                (cache_key, json.dumps(data), expires_at)
            )
        except Exception as e:
            raise DatabaseError(f"Failed to set cache: {str(e)}")

    def delete(self, cache_key: str) -> bool:
        """
        Delete cached data.

        Args:
            cache_key: Cache key

        Returns:
            True if deleted, False otherwise
        """
        try:
            query = "DELETE FROM api_cache WHERE cache_key = ?"
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (cache_key,))
                return cursor.rowcount > 0
        except Exception as e:
            raise DatabaseError(f"Failed to delete cache: {str(e)}")

    def clear_expired(self) -> int:
        """
        Clear all expired cache entries.

        Returns:
            Number of entries deleted
        """
        try:
            query = """
                DELETE FROM api_cache
                WHERE expires_at IS NOT NULL AND expires_at < ?
            """
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (datetime.now(),))
                return cursor.rowcount
        except Exception as e:
            raise DatabaseError(f"Failed to clear expired cache: {str(e)}")

    def clear_all(self) -> None:
        """Clear all cache entries."""
        try:
            query = "DELETE FROM api_cache"
            self.db.execute(query)
        except Exception as e:
            raise DatabaseError(f"Failed to clear cache: {str(e)}")
