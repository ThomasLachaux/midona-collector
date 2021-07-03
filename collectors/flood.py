from os import environ
import requests
import json

base_url = environ.get('FLOOD_API_URL')

def connect():
  username = environ.get('FLOOD_USERNAME')
  password = environ.get('FLOOD_PASSWORD')

  response = requests.post(f'{base_url}/auth/authenticate', data={'username': username, 'password': password})
  response.raise_for_status()

  return response.cookies['jwt']

def retreive_data(token):
  jar = requests.cookies.RequestsCookieJar()
  jar.set('jwt', token)

  # Retreive response as a Server Event
  response =  requests.get(f'{base_url}/activity-stream', cookies=jar, stream=True)
  generator = response.iter_lines()

  while True:
    line = next(generator).decode('utf-8')

    # Wait to get the event TORRENT_LIST_FULL_UPDATE
    if line == 'event:TORRENT_LIST_FULL_UPDATE':
        # Retreive the data
        data = next(generator).decode('utf-8')
        # Remove the data: header
        data = data[5:]

        # Close the response as we don't need it
        response.close()

        return json.loads(data)
        

def collect():
  token = connect()
  json_data = retreive_data(token)

  count = 0
  download = 0
  upload = 0

  for torrent_id, torrent in json_data.items():
    upload += torrent['upTotal']
    download += torrent['bytesDone']
    count += 1

  print(count)
  print(upload / 1024 ** 3)
  print(download / 1024 ** 3)
