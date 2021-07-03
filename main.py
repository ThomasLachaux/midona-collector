from dotenv import load_dotenv
load_dotenv()

from os import environ

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from collectors import flood

# for data in flood.collect():
#   print(data)

client = InfluxDBClient(url=environ.get("INFLUXDB_URL"), token=environ.get("INFLUXDB_TOKEN"))

write_api = client.write_api(write_options=SYNCHRONOUS)

for data in flood.collect():
  print(data)
  write_api.write(environ.get("INFLUXDB_BUCKET"), environ.get("INFLUXDB_ORG"), data)
