from django.apps import AppConfig
from django.conf import settings
import threading
import os
import time


class BlockchainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blockchain'

    def ready(self):

        def delayed_bootstrap():

            time.sleep(5)  # Give server time to finish loading
            from .network import bootstrap

            BOOTSTRAP_NODES = [
                "http://127.0.0.1:8000",
                "http://127.0.0.1:8001",
                "http://127.0.0.1:8002"
            ]
            SELF_URL = os.getenv("SELF_URL", "http://127.0.0.1:8000")  # Adjust per instance
            bootstrap(BOOTSTRAP_NODES, SELF_URL)

        threading.Thread(target=delayed_bootstrap).start()