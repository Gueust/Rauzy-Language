import json
from pprint import pprint

import inspect

def _function_name():
  """Returns the name of the function that calls this one"""
  return inspect.stack()[1][3]

def _get_value(obj, key):
  """Returns the value associated to key in obj.
  
  If the value does not exist or is empty, it returns None"""
  if key not in obj:
    return None
  if obj[key] == "":
    return None
  else:
    return obj[key]

# Functions to get the attributes associated to keys in dictionaries
def _nature(obj):
  return _get_value(obj, "nature")

def _extends(obj):
  return _get_value(obj, "extends")

def _objects(obj):
  return _get_value(obj, "objects")

def _relations(obj):
  return _get_value(obj, "relations")

def _properties(obj):
  return _get_value(obj, "properties")

def _fromSet(obj):
  return _get_value(obj, "from")

def _toSet(obj):
  return _get_value(obj, "to")

def _directional(obj):
  if "directional" not in obj:
    return None
  else:
    return obj["directional"]



class Object:
  """Abstract Rauzy object"""
  def __init__(self):
    self.extends = None
    self.objects = {}
    self.relations = {}
    self.properties = {}

  def __repr__(self):
    return "extends: " + self.extends.__str__() + "\n" + \
           "objects: " + str(self.objects) + "\n" + \
           "relations: " + self.relations.__str__() + "\n" + \
           "properties: " + self.properties.__str__() + "\n"

  def add_object(self, name, obj):
    if not isinstance(name, str):
      raise TypeError(_function_name() + " first argument must be a string")
    if name == "":
      raise TypeError(_function_name() + " first argument must be a non empty string")
    if not isinstance(obj, Object):
      raise TypeError(_function_name() + " second argument must be an Object")
    self.objects[name] = obj

  def add_relation(self, name, relation):
    if not isinstance(name, str):
      raise TypeError(_function_name() + " first argument must be a string")
    if name == "":
      raise TypeError(_function_name() + " first argument must be a non empty string")
    if not isinstance(obj, Relation):
      raise TypeError(_function_name() + " second argument must be a Relation")
    self.relations[name] = relation

  def add_property(self, key, value):
    if not isinstance(key, str):
      raise TypeError(_function_name() + " first argument must be a string")
    if key == "":
      raise TypeError(_function_name() + " first argument must be a non empty string")
    if not isinstance(value,str):
      raise TypeError(_function_name() + " second argument must be a string")
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
  a = Object()
  b = Object()
  a.add_object("name", b)
  pprint(a)
  print(a)
