import logging as logger
from influxdb_client.client.write_api import SYNCHRONOUS
logger.basicConfig(format='%(levelname)s %(module)s %(message)s', level=logger.DEBUG)

from os import environ
from influxdb_client import InfluxDBClient
from healthchecks import Healthcheck

healthcheck = Healthcheck(environ.get('HEALTHCHECKS_URL'))
healthcheck.start()


with InfluxDBClient(url=environ.get("INFLUXDB_URL"), token=environ.get("INFLUXDB_TOKEN")) as client:
  # Load bucket in a variable to avoid useless calls
  bucket = environ.get("INFLUXDB_BUCKET")
  org = environ.get("INFLUXDB_ORG")
  
  with client.write_api(write_options=SYNCHRONOUS) as api:

    for collector_name in environ.get('COLLECTORS').split(','):
      logger.info(f'Collect with {collector_name}')

      collector = __import__(f'collectors.{collector_name}', fromlist=[None])
      api.write(bucket, org, list(collector.collect()))

healthcheck.stop()
