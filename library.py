#TODO: 
# - Build a dependency graph in addition to the dictionaries for objects.
# - Ensure that this graph has no cycle
# - List the objects in a correct order according to the decendency chain
# - Do a loading and saving function

class Library:
  def __init__(self):
    self.dic_obj = {}
    self.dic_rlt = {}

