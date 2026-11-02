"""SQLite-backed persistence for the continuous simulation."""
from .store import CheckpointStore, SCHEMA_VERSION  # noqa: F401

__all__ = ["CheckpointStore", "SCHEMA_VERSION"]
