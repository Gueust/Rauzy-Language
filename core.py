# Import built-in modules
import json, collections
from pprint import pprint
from copy import deepcopy

# Import user modules
from typechecker import *

import inspect
def _function_name():
  """Returns the name of the function that calls this one"""
  return inspect.stack()[1][3]

@debug_typecheck
def _get_value(obj, key: str):
  """Returns the value associated to key in obj.
  
  Obj is supposed to be a dictionnary.
  If the value does not exist or is empty, it returns None."""
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
  return _get_value(obj, "directional")

def _library(obj):
  return _get_value(obj, "library")

# Used to define Relation for the type checking. It will be overridden latter.
class Relation:
  pass

class Object:
  """Abstract Rauzy object"""
  def __init__(self):
    self.extends = None
    self.objects = {}
    self.relations = {}
    self.properties = {}

  @staticmethod
  def new(json_obj, library):
    """Returns an Object representation of the json object"""
    ext = _extends(json_obj)
    if ext is None:
      obj = Object()
    else:
      obj = library.instanciate_obj(ext)

      list_objects = _objects(json_obj)
      if list_objects is not None:
        for name, tmp_obj in list_objects.items():
          obj.objects[name] = Object.new(tmp_obj, library)

      relations = _relations(json_obj)
      if relations is not None:
        for name, rlt in relations.items():
          obj.relations[name] = Relation.new(rlt)

    properties = _properties(json_obj)
    if properties is not None:
      obj.properties.update(properties)

    return obj

  #TODO: look at the difference between __str__ and __repr__
  def __repr__(self):
    return json.dumps(self._get_dict(), indent=1)

  def _get_dict(self):
    result = collections.OrderedDict()
    result["nature"] = "object"
    if self.extends is not None:
      result["extends"] = self.extends
    result["objects"] = {}
    for key, value in self.objects.items():
      result["objects"][key] = value._get_dict()
    result["relations"] = {}
    for key, value in self.relations.items():
      result["relation"][key] = value._get_dict()
    result["properties"] = self.properties
    return result

  @typecheck
  def set_extends(self, name: str):
    """Set the extends field of the object"""
    self.extends = name

  @typecheck
  def add_object(self, name: str, obj):
    if self.extends is not None:
      #TODO: modify the type of the error
      raise TypeError("Illegal call of " + _function_name() + " on an objects extending " + str(self.extends))
    if name == "":
      raise TypeError(_function_name() + " first argument must be a non empty string")
    if not isinstance(obj, Object):
      raise TypeError(_function_name() + " second argument must be an Object")
    self.objects[name] = obj
    
  @typecheck
  def remove_object(self, name: str):
    del self.objects[name]

  @typecheck
  def add_relation(self, name: str, relation: Relation):
    ##TODO: illegal call if extends is not None
    if name == "":
      raise TypeError(_function_name() + " first argument must be a non empty string")
    self.relations[name] = relation

  @typecheck
  def remove_relation(self, name: str):
    del self.relations[name]

  @typecheck
  def add_property(self, key: str, value: str):
    if not isinstance(key, str):
      raise TypeError(_function_name() + " first argument must be a string")
    if key == "":
      raise TypeError(_function_name() + " first argument must be a non empty string")
    if not isinstance(value,str):
      raise TypeError(_function_name() + " second argument must be a string")
    self.properties[key] = value
  
  @typecheck
  def remove_property(self, key: str):
    if key == "":
      raise TypeError(_function_name() + " first argument must be a non empty string")
    del self.properties[key]
    
  def lookup_obj_parent(self, name: str):
    if name in self.objects:
      return self
    else:
      res = None
      for key in self.objects.keys():
        obj = self.objects[key]
        if res==None and len(obj.objects)>0:
          res = obj.lookup_obj_parent(name)
        else:
          pass
      return res

  def lookup_obj(self, name: str):
    return self.lookup_obj_parent(name).objects[name]

# TODO: consider in the fromSet and toSet the name: rauzy obj linked
class Relation:
  """Abstract Rauzy relation"""
  def __init__(self):
    self.extends = None
    self.fromSet = {}
    self.toSet = {}
    self.directional = None
    self.properties = {}

  @staticmethod
  def new(json_rlt, library):
    """Returns a relation representation of the json relation """
    ext = _extends(json_rlt)
    if ext is None:
      rlt = Relation()
      toSet = _toSet(json_rlt)
      if toSet is not None:
        rlt.toSet = toSet
      fromSet = _fromSet(json_rlt)
      if fromSet is not None:
        rlt.fromSet = fromSet
    else:
      rlt = library.instanciate_rlt(ext)

    directional = _directional(json_rlt)
    if directional is not None:
      rlt.directional = directional

    properties = _properties(json_rlt)
    if properties is not None:
      rlt.properties.update(properties)

    return rlt

  def __repr__(self):
    return json.dumps(self._get_dict(), indent=1)

  def _get_dict(self):
    result = collections.OrderedDict()
    result["nature"] = "relation"
    if self.extends is not None:
      result["extends"] = self.extends
    result["from"] = {}
    for key, value in self.fromSet.items():
      result["from"][key] = value._get_dict()
    result["to"] = {}
    for key, value in self.toSet.items():
      result["to"][key] = value._get_dict()
    result["directional"] = self.directional
    result["properties"] = self.properties
    return result

  @typecheck
  def add_property(self, key: str, value: str):
    self.properties[key] = value

  @typecheck
  def set_directional(self, value: bool):
    self.directional = value

  @typecheck
  def set_extends(self, name: str):
    """Set the extends field of the relation"""
    self.extends = name
  ## TODO: rm_property, set_directional, add_from, add_to, rm_from, rm_to

def parse_object(obj, libraryn, is_lib=False):
  """Parse a json object and return the Rauzy object

  obj must be a dictionary"""
  nature = _nature(obj)
  if nature != "object":
    raise Exception("It is not an object :", nature)

  extends = _extends(obj)
  if extends is not None:
    object = library.instanciate_obj(extends)
  else:
    object = Object()

    contained_objs = _contained_objects(obj)
    for name, contained_obj in contained_objs:
      object.objects[name] = parse_object(contained_obj)

    relations = _relations(obj)
    for name, relation in relations:
      object.relations[name] = parse_relation(relation)

  properties = _properties(obj)
  for key, value in properties:
    # check that value is a string
    object.properties[name] = value

def parse_relation(rlt, library, is_lib=False):
  """Parse a json object representing a Rauzy relation and returns the
  corresponding Rauzy relation"""
  nature = _nature(rlt)
  if nature != "relation":
    raise Exception("It is not a relation")
  extends = _extends(rlt)
  if extends is not None:
    relation = library.instanciate_rlt(extends)
  else:
    relation = Relation()
    # If it is a relation of the library, there is no from and to sets
    if is_lib:
      fromSet = _fromSet(rlt)
      for name, contained_obj in fromSet:
        relation.fromSet[name] = parse_object(contained_obj)

      toSet = _toSet(obj)
      for name, contained_obj in toSet:
        relation.toSet[name] = parse_object(contained_obj)

  properties = _properties(obj)
  for key, value in properties:
    #TODO: check that value is a string
    relation.properties[name] = value

@typecheck
def load_json(file: str, debug = False):
  """Open a file and parse it as json"""
  json_data = open(file)
  data = json.load(json_data)
  if debug :
    pprint(data)
  json_data.close()
  return data

#test ground
if __name__ == "__main__":
  print("Testing library module")
  car = Object()
  wheel = Object()
  tire = Object()
  bolt = Object()
  contains = Relation()
  car.add_object("wheel1", wheel)
  car.add_object("wheel2", wheel)
  wheel.add_object("tire1", tire)
  wheel.add_object("bolt1", bolt)
  wheel.add_object("bolt2", bolt)
  car.add_property("size", "big")
  car.add_property("color", "blue")
  bolt.add_property("material", "iron")
  print(car.lookup_obj_parent("bolt1"))
  print(car.lookup_obj("bolt1"))
  
  
  car.remove_object("wheel1")
  car.remove_property("size")
  car.remove_property("color")
  print(car)