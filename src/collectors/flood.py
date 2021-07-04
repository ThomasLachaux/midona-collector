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

  tags = {}

  for torrent in json_data.values():
    tags_list = torrent['tags']

    # Set the tag to untagged as default
    tag = 'untagged'
    # If a tag exists, use first
    if len(tags_list) > 0:
      tag = tags_list[0]

    # Create the key tags if it does not exists
    tags.setdefault(tag, {'count': 0, 'download': 0, 'upload': 0})

    tags[tag]['count'] += 1
    tags[tag]['upload'] += torrent['upTotal']
    tags[tag]['download'] += torrent['bytesDone']


  total = {'count': 0, 'upload': 0, 'download': 0}
  for tag, torrent in tags.items():
    total['count'] += torrent['count']
    yield f'flood,tag={tag} count={torrent["count"]}'

    total['upload'] += torrent['upload']
    yield f'flood,tag={tag} upload={torrent["upload"]}'

    total['download'] += torrent['download']
    yield f'flood,tag={tag} download={torrent["download"]}'

  yield f'flood,tag=total count={total["count"]}' 
  yield f'flood,tag=total upload={total["upload"]}' 
  yield f'flood,tag=total download={total["download"]}' 