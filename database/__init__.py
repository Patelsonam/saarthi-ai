"""
Database module for SaarthiAI
"""

from .db_utils import get_db_connection, init_db

__all__ = ['get_db_connection', 'init_db']