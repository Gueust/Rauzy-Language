import os, json
from library import Library
from core import _library

class Model:
  def __init__(self):
    self.lib = None
    self.lib_path = None
    self.obj = None
    self.model_name = None

  def save(self):
    if self.model_name is None:
      raise Exception("You have not specified the name of the model file")

    obj_file = open(self.model_name, mode='w')
    # We get the dictionary representation of the object
    json_obj = self.obj._get_dict()
    # We add the library parameter in the root object
    json_obj["library"] = self.lib_path
    # We save the json representation in the file
    obj_file.write(json.dumps(json_obj, indent=1))

    if self.lib is not None and self.lib_path is None:
      #TODO: make a default name for it
      raise Exception("You are using a library without any name for it")
    if self.lib is not None:
      library_file = open(self.lib_path,mode='w')
      library_file.write(str(self.lib))


def parse_model(file):
  """Parse a file as a json object representing a model (i.e. a root object)"""
  json_data = open(file)
  json_model = json.load(json_data)
  lib_file = _library(json_model)
  #TODO: define precisely the path of the library with respect to path

  obj_library = {}
  rlt_library = {}

  # Build the library
  if lib_file is not None:
    try:
      directory_path = os.path.dirname(file)
      location = open(os.path.join(directory_path, lib_file))
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
