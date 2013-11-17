import os, json, collections
from . import core
from .library import Library

class Model:

  def __init__(self):
    self.lib = Library()
    self.lib_path = None
    self.obj = None
    self.model_name = None

  def save(self, indentation=1):
    """Saves the model into an object file and a library file.

    The object must be non empty (i.e. not None).
    The model must have a name (i.e. model_name not None).
    The library can be empty and in that case it is not saved.
    If the library is not empty, lib_path must not be None."""
    if self.obj is None:
      raise Exception("The model does not contain any object. \
                      Put an object in Model.obj")

    if self.model_name is None:
      raise Exception("You have not specified the name of the model file. \
                      Put the name in Model.model_name")

    obj_file = open(self.model_name, mode='w')
    # We get the dictionary representation of the object
    json_obj = self.obj._get_dict()
    # We add the library parameter in the root object
    json_obj["library"] = self.lib_path
    # We save the json representation into the file
    obj_file.write(json.dumps(json_obj, indent=indentation))

    if self.lib is not None and self.lib_path is None:
      #TODO: make a default name for it
      raise Exception("You are using a library without any name for it")
    if self.lib is not None:
      self.lib.save(os.path.join(os.path.dirname(self.model_name), self.lib_path))

def load(file):
  """Parse a file as a json object representing a model (i.e. a root object)"""
  json_data = open(file)
  json_model = json.load(json_data)

  resulting_model = Model()
  rlt_library = resulting_model.lib.dic_rlt
  obj_library = resulting_model.lib.dic_obj

  # Build the library
  lib_file = _library(json_model)
  if lib_file is not None:
    try:
      directory_path = os.path.dirname(file)
      location = open(os.path.join(directory_path, lib_file))
      print("localisation of the library file " + location)
    except IOError as err:
      raise IOError(format(err) + " \n The library path must be relative to the model file")
  
    # We load the library using ordered dictionaries
    json_lib = json.load(location, object_pairs_hook=collections.OrderedDict())
    # Implement the loading of the library: first the relations, then the objects
    #TODO : modify this part in order to load any library
    if "relations" in json_lib:
      for relation_class, relation in json_lib["relations"]:
        rlt_library[relation_class] = parse_relation(relation, resulting_model.lib, is_lib=True)
    if "objects" in json_lib:
      for obj_class, object in json_lib["objects"]:
        obj_library[obj_class] = parse_object(object, resulting_model.lib, is_lib=True)
  
  json_obj = load_json(path)
  resulting_model.obj = parse_object(obj, resulting_model)
  resulting_model.model_name = os.path.basename(file)

  return resulting_model

if __name__ == "__main__":
  print("Testing model module")
  car = core.Object()
  wheel = core.Object()
  car.add_object("wheel1", wheel)
  car.add_object("wheel2", wheel)
  car.add_property("size", "big")
  car.add_property("color", "blue")
  print(car)

  model = Model()
  model.obj = car
  model.lib_path = "car.lib"
  model.lib.dic_obj["wheel"] = wheel
  model.model_name = "examples/car.model"
  model.save()