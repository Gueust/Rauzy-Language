#TODO: 
# - Build a dependency graph in addition to the dictionaries for objects.
# - Ensure that this graph has no cycle
# - List the objects in a correct order according to the decendency chain
# - Do a loading and saving function

class Dependency:
  """Represent a node of a dependency graph

  depends_on is the set of objects that are needed for this object.
  used_by is the set of objects that depends on the current object"""
  def __init__(self, element):
    self.element = element
    self.depends_on = set()
    self.used_by = set()

  def has_no_dependency(self):
    """Returns true if and only if depends_on is empty"""
    return len(self.depends_on) == 0

  def remove_dependencies(self, ordered_dict):
    """"Removes the dependency self and returns in ordered_dict the non dependent objects"""
    if len(self.used_by) == 0:
      return
    else:
      new_element = self.used_by.pop()
      new_element.depends_on.remove(self.element)
      if len(new_element.depends_on) == 0:
        ordered_dict[new_element.element] = new_element
      self.remove_dependencies(ordered_dict)

class Dependency_graph:
  """A dependency graph containing dependencies"""
  def __init__(self):
    self.graph = {}

  def add_class(self, name, dep):
    if name in self.graph:
      raise Exception(name + " is already present as a class")
    self.graph[name] = dep

  def remove_class(self, name):
    del graph[name]

  def add_dependency(self, name1, name2):
    """Stores that name1 is dependent of name2"""
    self.graph[name1].depend_on.add(name2)
    self.graph[name2].used_by.add(name1)

  def build(self):
    """Returns an ordered dictionnary of the elements in a valid order

    The order respect the dependency chains: no element is inserted before all
    its dependencies have been inserted."""
    def remove_element(self, name):
      result = collections.OrderedDict()
      for used in element.used_by:
        el = self.graph[used]
        el.depends_on.remove(name)
        if el.has_no_dependency():
          result[used] = el

          result.extends()
    no_dependency = collections.OrderedDict()
    for name, node in self.graph:
      if node.has_no_dependency():
        # We add the element that has no dependency in the no dependency list
        no_dependency.append(node)
        # And we remove it in the graph
        del self.graph[name]
        # And we remove this element in the elements that were depending on it
        node.remove_dependencies(no_dependency)

    if len(self.graph) == 0:
      return no_dependency
    else:
      raise SystemError("The chain dependency contains cycles ! Aborting.")


class Library:
  def __init__(self):
    self.dic_obj = {}
    self.dic_rlt = {}

  def _build_rlt(self):
    """Returns a valid list of (class_name, class_relation)

    Returns a list of pair (class_name, element) in an order valid with the dependency chain.
    The list of pair is implemented using an ordered dictionnary."""
    graph = Dependency_graph
    # We add all the relations in the graph
    for key, rlt in self.dic_rlt:
      graph.add_class(key, rlt)

    # We add the dependencies between the relations
    for key, rlt in self.dic_rlt:
      if rlt.extends is not None:
        graph.add_dependency(key, rlt.extends)

    return graph.build()

  def _build_obj(self):
    """Returns a valid list of (class_name, class_object)

    Returns a list of pair (class_name, element) in an order valid with the dependency chain.
    The list of pair is implemented using an ordered dictionnary."""
    graph = Dependency_graph
    # We add all the objects in the graph
    for key, obj in self.dic_obj:
      graph.add_class(key, obj)

    # We add the dependencies between the objects
    for key, obj in self.dic_obj:
      if obj.extends is not None:
        graph.add_dependency(key, obj.extends)
        #TODO: add all dependencies due to the objects list
        for contained_obj in obj.objects:
          if contained_obj.extends is not None:
            graph.add_dependency(key, contained_obj.extends)

    return graph.build()