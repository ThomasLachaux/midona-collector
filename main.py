from dotenv import load_dotenv
load_dotenv()

import pkgutil
import collectors
import logging as logger

from os import environ
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

logger.basicConfig(format='%(asctime)s %(module)s %(levelname)s %(message)s', level=logger.DEBUG)

client = InfluxDBClient(url=environ.get("INFLUXDB_URL"), token=environ.get("INFLUXDB_TOKEN"))
api = client.write_api(write_options=SYNCHRONOUS)

for importer, module_name, ispkg in pkgutil.iter_modules(collectors.__path__, f'{collectors.__name__}.'):
  logger.info(f'Collect with {module_name}')
  collector = __import__(module_name, fromlist=[None])

  for data in collector.collect():
    logger.debug(data)
    api.write(environ.get("INFLUXDB_BUCKET"), environ.get("INFLUXDB_ORG"), data)