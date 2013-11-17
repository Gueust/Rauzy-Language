r"""
A Model contains both a library and an object description using that library.

Loading a model from a file::

  >>> from modeling.model import *
  >>> loaded_model = Model.load('examples/car.model')

Saving a model from a file::

  >>> from modeling.model import *
  >>> loaded_model = Model.load('examples/car.model')
  >>> loaded_model.set_lib_path('car_lib.lib')
  >>> loaded_model.set_obj_path('car_bis.model')
  >>> loaded_model.save()

"""

import os, json, collections
from .core import *
from .library import *

class Model:

  def __init__(self):
    self.lib = Library()
    self.lib_path = None
    self.obj = None
    self.model_name = None

  def set_lib_path(self, lib_path: str):
    """Set the name for the library file in order to be saved.

    It is not needed to set the library path if the library is empty."""
    self.lib_path = lib_path

  def set_obj_path(self, obj_path: str):
    """Set the name of the object file in order to be saved"""
    self.model_name = obj_path

  @staticmethod
  def load(file):
    """Parse a file as a json object representing a model (i.e. a root object)"""
    json_data = open(file)
    json_model = json.load(json_data)

    resulting_model = Model()
    rlt_library = resulting_model.lib.dic_rlt
    obj_library = resulting_model.lib.dic_obj

    # Build the library
    lib_file = core._library(json_model)
    if lib_file is not None:
      try:
        directory_path = os.path.dirname(file)
        location = open(os.path.join(directory_path, lib_file))
      except IOError as err:
        raise IOError(format(err) + " \n The library path must be relative to the model file")

      # We load the library using ordered dictionaries
      json_lib = json.load(location)
      resulting_model.lib .load(json_lib)

    json_obj = load_json(file)
    resulting_model.obj = Object.new(json_obj, resulting_model.lib)
    resulting_model.model_name = os.path.basename(file)

    return resulting_model

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