r"""
The library module manages the library of a model. It allows to load, save and
modify a library. In particular, loading a library needs to solve the
dependencies due to the inheritance between objetcs or relations.

Example of the initialization and the addition of an object class::

  >>> from modeling.library import *
  >>> rlt = core.Relation()
  >>> rlt.set_directional(True);
  >>> rlt.add_property("Importance", 'High')
  >>> lib = Library()
  >>> lib.add_rlt_class("Depends On", rlt)
  >>> print(lib)
"""

import json, collections, copy
from . import core
from .typechecker import *


class Dependency:
  """Represent a node of a dependency graph.

  It is only used internally by the library class and the implementation is not detailed here."""

  """depends_on is the set of the names of the elements that are needed for this element.
  used_by is the set of names of the elements that depends on the current element."""
  @debug_typecheck
  def __init__(self, name: str, element):
    """__init__(name, element)

    Initialise a dependency named `name` and containing `element`."""
    self.name = name
    self.element = element
    self.depends_on = set()
    self.used_by = set()

  def _get_dict(self):
    result = collections.OrderedDict()
    result["nature"] = "library"
    result["objects"] = self._build_obj()
    result["relations"] = self._build_rlt()
    return result

  def __repr__(self):
    result = 'Dependency: ' + self.name + '\n' + \
             'Depends on: ' + str(self.depends_on) + '\n' + \
             'Used by : ' + str(self.used_by) + '\n'
    return result

  def has_no_dependency(self):
    """has_no_dependency()
    Return true if and only if the node does not depend on any other node."""
    """Return true if and only if depends_on is empty"""
    return len(self.depends_on) == 0

class Dependency_graph:
  """A dependency graph containing dependencies."""
  def __init__(self):
    self.graph = {}

  @debug_typecheck
  def add_class(self, name: str, dep: Dependency):
    """add_class(name, dep)
    Add the dependency `dep` with the name `name` in the graph."""
    if name in self.graph:
      raise Exception(name + " is already present as a class")
    self.graph[name] = dep

  @debug_typecheck
  def remove_class(self, name: str):
    """remove_class(name)
    Remove the dependecy attached to the name `name`."""
    del graph[name]

  @debug_typecheck
  def add_dependency(self, name1: str, name2: str):
    """add_dependency(name1, name2)
    Store that `name1` is dependent of `name2`.
    """
    self.graph[name1].depends_on.add(name2)
    self.graph[name2].used_by.add(name1)

  @debug_typecheck
  def remove_dependencies(self, name: str, ordered_dict: (collections.OrderedDict)):
    """remove_dependencies(name, ordered_dict)
    Remove the dependencies on the element named name.

    It adds in ordered_dict the elements, the last dependency of which is name."""
    if name not in self.graph:
      return

    el = self.graph[name]
    if len(el.used_by) == 0:
      return
    else:
      other_element = self.graph[el.used_by.pop()]
      other_element.depends_on.remove(el.name)
      if len(other_element.depends_on) == 0:
        ordered_dict[other_element.name] = other_element.element
        del self.graph[other_element.name]
        self.remove_dependencies(other_element.name, ordered_dict)

  @debug_typecheck
  def build(self) -> (collections.OrderedDict):
    """build()
    Return an ordered dictionnary of the elements in a valid order.

    The order respect the dependency chains: no element is inserted before all
    its dependencies have been inserted."""
    no_dependency = collections.OrderedDict()
    copy_graph = dict(self.graph)
    for name, node in copy_graph.items():
      # The element may have been already removed
      if name not in self.graph:
        continue

      if node.has_no_dependency():
        # We add the element that has no dependency in the no dependency list
        no_dependency[node.name] = node.element
        # And we remove this element in the elements that were depending on it
        self.remove_dependencies(node.name, no_dependency)
        # And we remove it in the graph
        del self.graph[name]

    if len(self.graph) == 0:
      self.graph = copy_graph
      return no_dependency
    else:
      raise SystemError("The chain dependency contains cycles ! Aborting.")


class Library:
  """Abstraction of a library storing object and relation classes."""
  def __init__(self):
    self.dic_obj = collections.OrderedDict()
    self.dic_rlt = collections.OrderedDict()

  @typecheck
  def add_obj_class(self, name: str, obj: (core.Object) ):
    """add_obj_class(name, obj)
    Add the object class `obj' in the library with the name `name`."""
    if name in self.dic_obj:
      print("The object class ", name, " is already present in the library.")
    else
      self.dic_obj[name] = obj
  
  @typecheck
  def add_rlt_class(self, name: str, rlt: (core.Relation) ):
    """add_rlt_class(name, rlt)
    Add the relation class `rlt` in the library" with the name `name`."""
    if name in self.dic_obj:
      print("The relation class ", name, " is already preset in the library.")
    else
      self.dic_rlt[name] = rlt

  @typecheck
  def rm_obj_class(self, name: str):
    """rm_obj_class(name)
    Remove the definition of an object class associated to `name` in the library."""
    del self.dic_obj[name]
  
  @typecheck
  def rm_rlt_class(self, name: str):
    """rm_rlt_class(name)
    Remove the definition of a relation class associated to `name` in the library."""
    del self.dic_rlt[name]
  
  def get_obj(self, name: str):
    """get_obj(name)
    Return the object associated with `name`"""
    return self.dic_obj[name]
      
  def get_rlt(self, name: str):
    """get_rlt(name)
    Return the library associated with `name`"""
    return self.dic_rlt[name]
  
  def _get_dict(self):
    """Return a dictionary representing the library."""
    result = collections.OrderedDict()
    result["nature"] = "library"
    result["objects"] = self.dic_obj
    result["relations"] = self.dic_rlt
    return result

  def __repr__(self):
    class ComplexEncoder(json.JSONEncoder):
      def default(self, obj):
        if isinstance(obj, core.Object):
          return obj._get_dict()
        if isinstance(obj, core.Relation):
          return obj._get_dict()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

    return json.dumps(self._get_dict(), cls=ComplexEncoder, indent=1)

  @typecheck
  def save(self, lib_path: str):
    """save(lib_path)
    Save the library as a json string into a file with path is `lib_path`."""
    library_file = open(lib_path, mode='w')
    library_file.write(str(self))

  @typecheck
  def instanciate_obj(self, class_name: str):
    """instanciate_obj(class_name)
    Returns an instance of `class_name` present in library.

    The extends field is set to the class_name and all attributes are copied"""
    try:
      res = copy.deepcopy(self.dic_obj[class_name])
      res.set_extends(class_name)
      return res
    except KeyError:
      print(class_name + " does not exist in the library.")

  @typecheck
  def instanciate_rlt(self, class_name: str):
    """instanciate_rlt(class_name)
    Return an instance of `class_name` present in library.

    The extends field is set to the class_name and all attributes are copied"""
    try:
      res = copy.deepcopy(self.dic_rlt[class_name])
      res.set_extends(class_name)
      return res
    except KeyError:
      print(class_name + " does not exist in the library.")

  @debug_typecheck
  def _load_relations(self, json_rlt_lib):
    """Add into the library the relation classes corresponding to the json data.

    The fromSet and toSet are set to empty.
    If a relation class, its propeties replace the one of its parent"""
    graph = Dependency_graph()
    # We add all the relations in the graph
    for key, rlt in json_rlt_lib.items():
      graph.add_class(key, Dependency(key, rlt))

    # We add the dependencies between the relations
    for key, rlt in json_rlt_lib.items():
      ext = core._extends(rlt)
      if ext is not None:
        graph.add_dependency(key, ext)

    ordered_rlt = graph.build()

    for key, rlt in ordered_rlt.items():
      rauzy_rlt = core.Relation.new(rlt, self)
      rauzy_rlt.fromSet = {}
      rauzy_rlt.toSet = {}
      self.dic_rlt[key] = rauzy_rlt

  @debug_typecheck
  def _load_objects(self, json_obj_lib):
    graph = Dependency_graph()
    # We add all the objects in the graph
    for key, obj in json_obj_lib.items():
      graph.add_class(key, Dependency(key, obj))

    # We add the dependencies between the objects
    # They come from the extends field and the extends field of the
    # contained objects
    for key, obj in json_obj_lib.items():
      ext = core._extends(obj)
      if ext is not None:
        graph.add_dependency(key, ext)
      contained_obj = core._objects(obj)
      if contained_obj is not None:
        for name, value in contained_obj.items():
          ext = core._extends(value)
          if ext is not None:
            graph.add_dependency(key, ext)

    ordered_obj = graph.build()

    for key, obj in ordered_obj.items():
      self.dic_obj[key] = core.Object.new(obj, self)

  def load(self, json_lib):
    """load(json_lib)
    Load a library from the json data.

    If information is already present in the library, the new classes will be added."""
    if core._nature(json_lib) != "library":
      raise Exception("This is not a valid dictionary")

    ## We load relations
    if "relations" in json_lib:
      self._load_relations(json_lib["relations"])

    # We load objects
    if "objects" in json_lib:
      self._load_objects(json_lib["objects"])

if __name__ == "__main__":
  print("Testing library module")
  rlt1 = core.Relation()
  rlt1.set_directional(True);
  rlt1.add_property("Importance", 'High')
  ## print("Relation", rlt1)
  lib = Library()
  lib.add_rlt_class("Depends On", rlt1)
  ## print("Lib", lib)
  rlt2 = core.Relation.new("Depends On", lib)
  rlt2.add_property("Mutual", "True")
  rlt2.set_directional(False)
  rlt2.set_extends("Depends On")
  lib.add_rlt_class("Mutual dependency", rlt2)
  # We put the dependent relation at the beginning
  del lib.dic_rlt["Depends On"]
  lib.add_rlt_class("Depends On", rlt1)

  obj = core.Object()
  obj.add_property("Nature", "Evil")

  obj2 = core.Object()
  obj2.set_extends("Human")
  obj2.add_property("Nature", "Good")

  lib.add_obj_class("Human", obj)
  lib.add_obj_class("SuperHero", obj2)
  print("Library", lib)

  #instance = lib.instanciate_obj("Class One")
  #print("Instance of the class 'Class One'", instance)
  #obj.add_property("Added", "Option")
  #print("Modification of the parent object", obj)
  #print("The instanciation is not modified", instance)
  #instance.add_property("Test", "42")
  #print("Modification of the instance", instance)
  #print("The object is not modified", obj)

  new_lib = Library()
  new_lib.load(json.loads(str(lib)))
  print("Loaded library from current lib", new_lib)
