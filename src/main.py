import logging as logger
logger.basicConfig(format='%(levelname)s %(module)s %(message)s', level=logger.DEBUG)

from os import environ
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from healthchecks import Healthcheck

healthcheck = Healthcheck(environ.get('HEALTHCHECKS_URL'))
healthcheck.start()


client = InfluxDBClient(url=environ.get("INFLUXDB_URL"), token=environ.get("INFLUXDB_TOKEN"))
api = client.write_api(write_options=SYNCHRONOUS)

for collector_name in environ.get('COLLECTORS').split(','):
  logger.info(f'Collect with {collector_name}')

  collector = __import__(f'collectors.{collector_name}', fromlist=[None])

  for data in collector.collect():
    api.write(environ.get("INFLUXDB_BUCKET"), environ.get("INFLUXDB_ORG"), data)
    logger.debug(data)


healthcheck.stop()
