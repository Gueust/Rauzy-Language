from library import Library
from core import _library

class Model:
  def __init__(self, obj, lib):
    self.lib = lib
    self.obj = obj

def parse_model(path):
  """Parse a file as a json object representing a model (i.e. a root object)"""
  lib_file = _library(obj)
  #TODO: define precisely the path of the library with respect to path

  obj_library = {}
  rlt_library = {}

  # Build the library
  if lib_file is not None:
    try:
      location = open(lib_file)
    except IOError as err:
      raise IOError(format(err) + " \n The library path must be relative to the model file")
  
    # We load the library using ordered dictionaries
    json_lib = json.load(location, object_pairs_hook=collections.OrderedDict())
    # Implement the loading of the library: first the relations, then the objects
    if "relations" in json_lib:
      for relation_class, relation in json_lib["relations"]:
        rlt_library[relation_class] = parse_relation(relation, lib=True)
    if "objects" in json_lib:
      for obj_class, object in json_lib["objects"]:
        obj_library[obj_class] = parse_object(object, obj_library, rlt_library)
  
  obj = load_json(path)
  return parse_object(obj, obj_library, rlt_library)
