import requests
from loguru import logger

from urllib.parse import urljoin


class Healthcheck:
    def __init__(self, url):
        if url:
            self.url = url
        else:
            logger.warning(
                "No healtcheck url provided, the script will continue anyway"
            )

    def start(self):
        if hasattr(self, "url"):
            response = requests.get(urljoin(f"{self.url}/", "start"))
            response.raise_for_status()

    def stop(self):
        if hasattr(self, "url"):
            response = requests.get(self.url)
            response.raise_for_status()
