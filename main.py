import json
from pprint import pprint


class Object:
  """Abstract Rauzy object"""
  def __init__(self):
    self.extends = None
    self.objects = {}
    self.relations = {}
    self.properties = {}

  def add_object(name, obj):
    self.objects[name] = obj

  def add_relation(name, relation):
    self.relations[name] = relation

  def add_property(key, value):
    self.properties[key] = value

class Relation:
  """Abstract Rauzy relation"""
  def __init__(self):
    self.extends = None
    self.fromSet = {}
    self.toSet = {}
    self.directional = None
    self.properties = {}

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
