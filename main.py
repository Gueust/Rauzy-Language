import json
from pprint import pprint

def load_json(file, debug = False):
  """Open a file and parse it as json."""
  json_data = open(file)
  data = json.load(json_data)
  if debug :
    pprint(data)
  json_data.close()
  return data

if __name__ == '__main__':
  data = load_json('example.json', True)
  pprint(data["maps"][0]["id"])
  pprint(data["masks"]["id"])
  pprint(data["om_points"])
