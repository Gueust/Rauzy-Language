from modeling.model import *
from modeling.library import *
from modeling.core import *

#Create three objects: car, bike and citroen
car = Object()
bike = Object()
ferrari = Object()

#Set ferrari extends to car
ferrari.set_extends("car")

#Create sub-objects: wheel, frame, tire, rim, bolt
wheel = Object()
frame = Object()
tire = Object()
rim = Object()
bolt = Object()

#Add sub-objects to car
car.add_object("wheel1", wheel)
car.add_object("wheel2", wheel)
car.add_object("wheel3", wheel)
car.add_object("wheel4", wheel)

#Add sub-objects to bike
bike.add_object("wheel1", wheel)
bike.add_object("wheel2", wheel)
bike.add_object("frame1", frame)

#Add sub-objects to wheel, rim
wheel.add_object("tire1", tire)
wheel.add_object("rim1", rim)
rim.add_object("standard-bolt", bolt)

#Add properties to car
car.add_property("size", "big")
car.add_property("color", "blue")

#Add properties to bike
bike.add_property("size", "medium")
bike.add_property("color", "blue")

#Add properties to ferrari
car.add_property("style", "flashy")
car.add_property("speed", "fast")

#Add properties to tire, bolt
tire.add_property("material", "rubber")
bolt.add_property("material", "iron")

#Add objects to library
model = Model()
model.obj = car
model.lib_path = "car.lib"
model.lib.dic_obj["wheel"] = wheel
model.lib.dic_obj["car"] = car
model.model_name = "examples/car.model"
model.save()

#Print object
print("\n"+"PRINT OBJECT:")
print(car)

#Remove object wheel from car and property material from tire
print("\n"+"REMOVE OBJECT & PROPERTY:")
car.remove_object("wheel1")
tire.remove_property("material")
print(car)

#Lookup object standard-bolt  
print("\n"+"LOOKUP OBJECT:")
print(car.lookup_obj_parent("standard-bolt")) 
print(car.lookup_obj("standard-bolt")) 

#Abstract car object to level 1 - will remove any objects beyond the specified level
print("\n"+"ABSTRACTION:")
print(car.abst_obj(1))

#Flatten car object - all sub-objects will be represented as paths in the properties group of the root object
print("\n"+"FLATTENING:")
print(car.flatten())

#Flatten car object - compares a flatten versus flatten_with_extends, which will add objects and properties of all objects with extends
print("\n"+"FLATTENING WITH CONSIDERATION FOR EXTENDS:")
print(ferrari.flatten())
print(ferrari.flatten_with_extends(model.lib))

#Compare a bike to a car - objects and properties are compared and sorted into 3 groups: only in bike, only in car and differing values
print("\n"+"COMPARISON:")
bike.compare(car)