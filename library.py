import json, collections, core
# - Build a dependency graph in addition to the dictionaries for objects.
# - Ensure that this graph has no cycle
# - List the objects in a correct order according to the decendency chain
# - Do a loading and saving function
from typechecker import *


class Dependency:
  """Represent a node of a dependency graph

  depends_on is the set of the names of the elements that are needed for this element.
  used_by is the set of names of the elements that depends on the current element."""
  @typecheck
  def __init__(self, name: str, element):
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
    """Returns true if and only if depends_on is empty"""
    return len(self.depends_on) == 0

class Dependency_graph:
  """A dependency graph containing dependencies"""
  def __init__(self):
    self.graph = {}

  @typecheck
  def add_class(self, name: str, dep: Dependency):
    if name in self.graph:
      raise Exception(name + " is already present as a class")
    self.graph[name] = dep

  @typecheck
  def remove_class(self, name: str):
    del graph[name]

  @typecheck
  def add_dependency(self, name1: str, name2: str):
    """Stores that name1 is dependent of name2"""
    self.graph[name1].depend_on.add(name2)
    self.graph[name2].used_by.add(name1)

  @typecheck
  def remove_dependencies(self, name: str, ordered_dict: (collections.OrderedDict)):
    """"Removes the dependencies on the element named name

    It adds in ordered_dict the elements, the last dependency of which is name."""
    el = self.graph[name]
    if len(el.used_by) == 0:
      return
    else:
      other_element = el.used_by.pop()
      other_element.depends_on.remove(el.name)
      if len(other_element.depends_on) == 0:
        ordered_dict[other_element.name] = other_element.element
        del self.graph[other_element.name]
        self.remove_dependencies(other_element.name, ordered_dict)

  @typecheck
  def build(self) -> (collections.OrderedDict):
    """Returns an ordered dictionnary of the elements in a valid order

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
  def __init__(self):
    self.dic_obj = {}
    self.dic_rlt = {}

  # TODO:
  # done? add_obj_class(self, name, obj) 
  # done? add_rlt_class(self, name, rlt)
  # done? rm_obj_class(self, name)
  # done? rm_rlt_class(self, name)
  
  # rename_obj_class(self, current_name, new_name)
  # rename_rlt_class(self, current_name, new_name)
  
  # question: error with the @typecheck?
  
  def add_obj_class(self, name, obj):
    self.dic_obj[name] = obj
  
  def add_rlt_class(self, name, rlt):
    self.dic_rlt[name] = rlt
    
  def rm_obj_class(self, name):
    del self.dic_obj[name]
  
  def rm_rlt_class(self, name):
    del self.dic_rlt[name]
  
  def _get_dict(self):
    result = collections.OrderedDict()
    result["nature"] = "library"
    result["objects"] = self._build_obj()
    result["relations"] = self._build_rlt()
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
    library_file = open(lib_path, mode='w')
    library_file.write(str(self))

  @typecheck
  def instanciate_obj(self, class_name: str):
    """Returns an instance of class_name present in library"""
    return deepcopy(dic_obj[class_name])

  @typecheck
  def instanciate_rlt(self, name: str):
    """Returns an instance of class_name present in library"""
    return deepcopy(dic_rlt[class_name])

  @typecheck
  def _build_rlt(self) -> (collections.OrderedDict):
    """Returns a valid list of (class_name, class_relation)

    Returns a list of pair (class_name, element) in an order valid with the dependency chain.
    The list of pair is implemented using an ordered dictionnary."""
    graph = Dependency_graph()
    # We add all the relations in the graph
    for key, rlt in self.dic_rlt:
      graph.add_class(key, Dependency(key, rlt))

    # We add the dependencies between the relations
    for key, rlt in self.dic_rlt:
      if rlt.extends is not None:
        graph.add_dependency(key, rlt.extends)

    return graph.build()

  @typecheck
  def _build_obj(self) -> (collections.OrderedDict):
    """Returns a valid list of (class_name, class_object)

    Returns a list of pair (class_name, element) in an order valid with the dependency chain.
    The list of pair is implemented using an ordered dictionnary."""
    graph = Dependency_graph()
    # We add all the objects in the graph
    for key, obj in self.dic_obj.items():
      graph.add_class(key, Dependency(key, obj))

    # We add the dependencies between the objects
    for key, obj in self.dic_obj.items():
      if obj.extends is not None:
        # We take into account the inheritance system
        graph.add_dependency(key, obj.extends)
        # We add all dependencies due to the objects list
        for contained_obj in obj.objects.values():
          if contained_obj.extends is not None:
            graph.add_dependency(key, contained_obj.extends)

    return graph.build()

