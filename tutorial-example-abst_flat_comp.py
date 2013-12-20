from modeling.model import *
from modeling.library import *
from modeling.core import *

#Create three objects: car, bike and ferrari
car = Object()
bike = Object()
fleet = Object()
ferrari = Object()
camry = Object()

#Set camry and ferrari extends to car
ferrari.set_extends("car")
camry.set_extends("car")

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

#Add sub-objects to fleet
fleet.add_object("camry1", camry)
fleet.add_object("ferrari1", ferrari)

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

#Add properties to fleet
fleet.add_property("owner", "santa claus")
fleet.add_property("location", "north pole")

#Add properties to ferrari
ferrari.add_property("style", "flashy")
ferrari.add_property("speed", "fast")

#Add properties to camry
camry.add_property("style", "family")
camry.add_property("speed", "normal")

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
print("\n"+"PRINT OBJECT [car]:")
print(car)

#Remove object wheel from car and property material from tire
print("\n"+"REMOVE OBJECT & PROPERTY [wheel1 from car, material from tire]:")
car.remove_object("wheel1")
tire.remove_property("material")
print(car)

#Lookup object standard-bolt  
print("\n"+"LOOKUP OBJECT [standard-bolt in car]:")
print(car.lookup_obj_parent("standard-bolt")) 
print(car.lookup_obj("standard-bolt")) 

#Abstract car object to level 1 - will remove any objects beyond the specified level
print("\n"+"ABSTRACTION [fleet]:")
print(fleet.abst_obj(1))

#Flatten ferrari object - all sub-objects will be represented as paths in the properties group of the root object
print("\n"+"FLATTENING [fleet]:")
print(fleet.flatten())

#Compare a bike to a car - objects and properties are compared and sorted into 3 groups: only in bike, only in car and differing values
print("\n"+"COMPARISON [bike = self, car = obj]:")
bike.compare(car)

#Compare a fleet to a camry - objects and properties are compared and sorted into 3 groups: only in fleet, only in camry and differing values
print("\n"+"COMPARISON [fleet = self, camry = obj]:")
fleet.compare(camry)

#Compare a fleet to a camry accounting also for extended objects
print("\n"+"COMPARISON [fleet = self, camry = obj]:")
fleet.compare_with_extends(camry, model.lib)