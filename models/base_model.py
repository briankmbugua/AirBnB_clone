#!/usr/bin/python3
"""This module has a base class for all models"""
import uuid
from datetime import datetime
class BaseModel:
    """The base class for all models"""
    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs: # if a dictionary containing keyword arguments is not passed
         self.id = str(uuid.uuid4())
         self.created_at = datetime.now()
         self.updated_at = datetime.now()
        else: # if a dictionary containing keyword arguments is passed
           kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')

           kwargs['created_at'] = datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')


           del kwargs['__class__']
           self.__dict__.update(kwargs)
    
    def save(self):
        """ updates the public instance attribute updated_at with the current datetime"""
        self.updated_at = datetime.now()
    def to_dict(self):
        """This converts the instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                           (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

my_model = BaseModel()
my_model.name = "My_First_Model"
my_model.my_number = 89
print(my_model.id)
print(my_model)
print(type(my_model.created_at))
print("--")
my_model_json = my_model.to_dict()
print(my_model_json)
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

print("--")
my_new_model = BaseModel(**my_model_json)
print(my_new_model.id)
print(my_new_model)
print(type(my_new_model.created_at))

print("--")
print(my_model is my_new_model)


