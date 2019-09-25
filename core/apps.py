from django.apps import AppConfig
from connectingkerala.db import setup_connection


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Set MongoDB connections
        setup_connection()
