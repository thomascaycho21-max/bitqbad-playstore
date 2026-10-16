"""Modulo Store: catalogo de apps."""
from .models import App
from .repository import StoreRepository

__all__ = ["App", "StoreRepository"]
