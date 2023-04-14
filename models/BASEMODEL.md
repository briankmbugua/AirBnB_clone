# BaseModel
Write a class BaseModel that defines all common attributes/methods for other classes
## public instance atrributes
- models/base_model.py
- Public instance atrributes this attributes will be contained in all the objects created from this base_model class
  - id this should be a string use uuid.uuid4() for this it must be converted to a string
  - created_at:datetime - assing with the current datetime when an instance is created
## Public instance methods
- save(self): updates the public instance attribute updated_at with the current datetime
- to_dict(self): returns a dictionary containing all keys/values of __dict__ of the instance __dict__ atrribute is a dictionary that stores an objects attributes.It contains all the attributes and their values defined for the object.When an attribute is set for an instance of a class, it is stored in the __dict__ attribute of the instance.When an attribute is accessed python first checks the instance's __dict__ and if the attribute is not found it looks in the class __dict__ and if it is not there it looks in the parent classes __dict__ and if not there it looks in the parent class __dict__ recursively untill it reaches the top of the class hierarchy.
  - by using self.__dict__, only instance attributes set will be returned
  - a key __class__ must be added to this dictionary with the class name of the object
  - created_at and updated_at must be converted to string object in ISO format you can use isoformat() of the datetime object
  - this method is the first piece in serialization/deserialization process

# Create BaseModel from dictionary
*args and **kwargs are special syntax in python that allow you to pass a variable number of arguments to a function
*args is used to pass a variable number of non-keyword arguments to a function.When you use *args in a function defination, it allows the function to accept any number of positional arguments which are then passed as a tuple
```python
def my_function(*args):
    for arg in args:
        print(arg)
my_function(1,2,3)
output
1
2
2
```
**kwargs is used to pass a variable number of keyword arguments to a function.
Kwargs object is essentially a dictionary so you can use the standard dictionary methods to access and manipulate it's contents.
```python
def my_function(**kwargs):
    for key, value in kwargs.items():
        print(key, value)
my_function(name='john',age=30,city='New york')
```
- use *args, **kwargs arguments for the constructor of a BaseModel
- *args won't be used
- if kwargs is not empty:
  - Each key of this dictionary is an attribute name __class__ from kwargs is the only one that should not be added as an attribute thus delete it from the kwargs dictionary del kwargs['key'] where key is the specific key you want to remove in this case they key is __class__ this is because the key will be added to the dictionary.
  - each value of this dictionary is the value of this attribute name
  - created_at and updated_at are strings in this dictionary, but inside the BaseModel instance they are datetime object.you have to convert this strings into datetime objects
- otherwise
  - creat id and created_at as you did previously(new instance)
  # code
```python
  """This module has a base class for all models"""
import uuid
from datetime import datetime
class BaseModel:
    """The base class for all models"""
    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs: # if a dictionary containing keyword arguments is not passed
         self.id = str(uuid.uuid4()) # create a unique id
         self.created_at = datetime.now() # the time it was created
         self.updated_at = datetime.now() # the time it was updated
        else: # if a dictionary containing keyword arguments is passed
           kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f') # convert the update_at string from the passed dictionary to a datetime object using strptime(string parse time) since to_dict method expects a datetime object to convert it to a string

           kwargs['created_at'] = datetime.strptime(kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f') # convert the created_at string from the passed dictionary to a datetime object using strptime(string parse time) since to_dict method expects a datetime object to convert it to a string

           del kwargs['__class__'] # delete the __class__ key from the passed dictionary since it will be added back in the do_dict() method
           self.__dict__.update(kwargs) # the finally update the dictionary __dict__ is a dictionary representation of the object
    
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
```

# testing the model
```python
my_model = BaseModel() # create a new instance of the BaseModel class
my_model.name = "My_First_Model"
my_model.my_number = 89
print(my_model.id)
print(my_model)
print(type(my_model.created_at))
print("--")
my_model_json = my_model.to_dict() # converted the new instance created above to a dictionary
print(my_model_json)
print("JSON of my_model:")
for key in my_model_json.keys():
    print("\t{}: ({}) - {}".format(key, type(my_model_json[key]), my_model_json[key]))

print("--")
my_new_model = BaseModel(**my_model_json) #pass the dictionary created in my_model.to_dict() as a variable keyword argument to the BaseModel class **kwargs this will make the else part of the BaseModel to be used
print(my_new_model.id)
print(my_new_model)
print(type(my_new_model.created_at))

print("--")
print(my_model is my_new_model) # check whether the two models are the same since they are not it should return false
```