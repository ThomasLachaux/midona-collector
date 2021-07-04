import requests
import logging

from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class Healthcheck():
  def __init__(self, url):
      if url:
        self.url = url
      else:
        logger.warn('No healtcheck url provided, the script will continue anyway')

  def start(self):
    if hasattr(self, 'url'):
      response = requests.get(urljoin(f'{self.url}/', 'start'))
      response.raise_for_status()

  def stop(self):
    if hasattr(self, 'url'):
      response = requests.get(self.url)
      response.raise_for_status()