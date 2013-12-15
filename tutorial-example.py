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

# Adding Users and Presentation Layer and their relation
root.add_object("Users", Object())
root.add_object("Presentation_Layer", presentation_layer)
r = Relation()
root.add_relation("Users->Presentation_Layer", r)
r.set_extends("default")
r.add_to("Presentation_Layer")
r.add_from("Users")

# Adding External Systems and Services Layer
root.add_object("External Systems", Object())
services = Object()
services.add_object("Service Interfaces", Object())
services.add_object("Message Types", Object())
root.add_object("Services Layer", services)
r = Relation()
root.add_relation("External Systems->Services Layer", r)
r.set_extends("default")
r.add_to("Services Layer")
r.add_from("External Systems")

# Adding Cross Security sub-system
cross = Object()
cross.add_object("Security", Object())
cross.add_object("Operational Management", Object())
cross.add_object("Communication", Object())
root.add_object("Cross Cutting", cross)

# Adding Business layer sub-system
business = Object()
business.add_object("Application Facade", Object())
business.add_object("Business Workflow", Object())
business.add_object("Business Components", Object())
business.add_object("Business Entities", Object())
r = Relation()
business.add_relation("Inner1", r)
r.set_extends("default")
r.add_to("Business Workflow")
r.add_from("Application Facade")
r = Relation()
business.add_relation("Inner2", r)
r.set_extends("default")
r.add_to("Business Components")
r.add_from("Application Facade")
r = Relation()
business.add_relation("Inner3", r)
r.set_extends("default")
r.add_to("Business Workflow")
r.add_from("Business Entities")


# Adding Data Layer
data = Object()
data.add_object("Data Access", Object())
data.add_object("Service Agents", Object())
root.add_object("Data Layer", data)

#Adding Data Sources  and External Services
root.add_object("Data Sources", Object())
root.add_object("External Services", Object())

# Adding all the remaining relations


