from modeling.model import *
from modeling.library import *
from modeling.core import *


# Creation of the library and creation of a default relation
lib = Library()
default_relation = Relation()
default_relation.set_directional(True)
default_relation.add_property("style", "dotted")
lib.add_rlt_class("default", default_relation)

# Creation of the root object
root = Object()

# Creation of the inner objects
presentation_layer = Object()
presentation_layer.add_object("User Interface", Object())
presentation_layer.add_object("Presentation Logic", Object())

# Adding Users, Presentation Layer and their relation
root.add_object("Users", Object())
root.add_object("Presentation Layer", presentation_layer)
r = Relation()
root.add_relation("Users->Presentation Layer", r)
r.set_extends("default")
r.add_from("Users")
r.add_to("Presentation Layer")


# Adding External Systems, Services Layer and their relation
root.add_object("External Systems", Object())
services = Object()
services.add_object("Service Interfaces", Object())
services.add_object("Message Types", Object())
root.add_object("Services Layer", services)
r = Relation()
root.add_relation("External Systems->Services Layer", r)
r.set_extends("default")
r.add_from("External Systems")
r.add_to("Services Layer")

# Adding Cross Security sub-system
cross = Object()
cross.add_object("Security", Object())
cross.add_object("Operational Management", Object())
cross.add_object("Communication", Object())
cross.add_property("Abstraction", "Important")
root.add_object("Cross Cutting", cross)

# Adding Business layer sub-system
business = Object()
business.add_object("Application Facade", Object())
business.add_object("Business Workflow", Object())
business.add_object("Business Components", Object())
business.add_object("Business Entities", Object())
business.add_property("Abstraction", "Important")
r = Relation()
business.add_relation("Inner1", r)
r.set_extends("default")
r.add_from("Application Facade")
r.add_to("Business Workflow")
r = Relation()
business.add_relation("Inner2", r)
r.set_extends("default")
r.add_from("Application Facade")
r.add_to("Business Components")

r = Relation()
business.add_relation("Inner3", r)
r.set_extends("default")
r.add_from("Application Facade")
r.add_to("Business Entities")

root.add_object("Business Layer", business)

# Adding Data Layer, Data Sources, External Services and their relations
data = Object()
data.add_object("Data Access", Object())
data.add_object("Service Agents", Object())
root.add_object("Data Layer", data)

root.add_object("Data Sources", Object())
root.add_object("External Services", Object())

r = Relation()
root.add_relation("Data Layer->Data Sources", r)
r.set_extends("default")
r.add_from("Data Layer")
r.add_to("Data Sources")

r = Relation()
root.add_relation("Data Layer->Data Sources", r)
r.set_extends("default")
r.add_from("Data Layer")
r.add_to("External Services")

# Adding all the remaining relations
r = Relation()
root.add_relation("Business Layer->Data Layer", r)
r.set_extends("default")
r.add_from("Business Layer")
r.add_to("Data Layer")

# Relations comming from Data Layer
r = Relation()
root.add_relation("Data Layer->Cross Cutting", r)
r.set_extends("default")
r.add_from("Data Layer")
r.add_to("Cross Cutting")

# Relations comming from Services Layer
r = Relation()
root.add_relation("Services Layer->Cross Cutting", r)
r.set_extends("default")
r.add_from("Services Layer")
r.add_to("Cross Cutting")

r = Relation()
root.add_relation("Services Layer->Business Layer", r)
r.set_extends("default")
r.add_from("Services Layer")
r.add_to("Business Layer")

# Relations comming from Presentation Layer
r = Relation()
root.add_relation("Presentation Layer->Cross Cutting", r)
r.set_extends("default")
r.add_from("Presentation Layer")
r.add_to("Cross Cutting")

r = Relation()
root.add_relation("Presentation Layer->Business Layer", r)
r.set_extends("default")
r.add_from("Presentation Layer")
r.add_to("Business Layer")

# Printing the model
#print(root)

# Abstraction using levels
print("Abstraction using levels")
print(root.abst_obj(1))

# Abstraction using key => value property
print()
print("Abstraction using property")
print(root.keyword_abstraction("Abstraction", "Important"))

# Saving the model
model = Model()
model.set_obj(root)
model.set_lib(lib)
model.set_lib_path('tutorial-example-lib.lib')
model.set_obj_path('tutorial-example-model.model')
model.save()
