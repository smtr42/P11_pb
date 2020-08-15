"""Configuration module for the FavoriteCart app."""

from django.apps import AppConfig


class <built-in method title of str object at 0x10fa36930>Config(AppConfig):
    """Main config data structure for the favoritecart app."""

    name = 'favoritecart'

    def ready(self):
        """Initializations to be performed with the app is ready."""
        try:
            from . import signals
        except ImportError:
            pass
