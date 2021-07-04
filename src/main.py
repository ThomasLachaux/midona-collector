import logging as logger
logger.basicConfig(format='%(asctime)s %(levelname)s %(module)s %(message)s', level=logger.DEBUG)

import pkgutil
import collectors

from os import environ
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from healthchecks import Healthcheck

healthcheck = Healthcheck(environ.get('HEALTHCHECKS_URL'))
healthcheck.start()


client = InfluxDBClient(url=environ.get("INFLUXDB_URL"), token=environ.get("INFLUXDB_TOKEN"))
api = client.write_api(write_options=SYNCHRONOUS)

for importer, module_name, ispkg in pkgutil.iter_modules(collectors.__path__, f'{collectors.__name__}.'):
  logger.info(f'Collect with {module_name}')
  collector = __import__(module_name, fromlist=[None])

  for data in collector.collect():
    api.write(environ.get("INFLUXDB_BUCKET"), environ.get("INFLUXDB_ORG"), data)
    logger.debug(data)

healthcheck.stop()