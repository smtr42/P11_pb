"""Configuration module for the FavoriteCart app."""

from django.apps import AppConfig


class FavoritecartConfig(AppConfig):
    """Main config data structure for the favoritecart app."""

    name = 'favoritecart'

    def ready(self):
        """Initializations to be performed with the app is ready."""
        try:
            from . import signals
        except ImportError:
            pass
