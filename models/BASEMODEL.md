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

# Store first object
Now we can rectrate BaseModel from another one using a dictionary representation
```python
<class 'BaseModel'> -> to_dict() -> <class 'dict'> -> <class 'BaseModel'>
```
This is greate but it is still not persistent:every time you launch the program, you don't restore all the objects created before...The first way you will see here is to save these objects to a file.
Writting the dictionary representation to a file won't be relevant:
- python dosen't know how to convert a string to a dictionary (easily)
- it is not human readable
- Using the file with another program in python or other language will be hard.
so you will convert the dictionary representation to a JSON String.In this format human can read and all programming languages have a JSON reader and writer.
Now the flow of serialization-deserialization will be
```python
<class 'BaseModel'> -> to_dict() -> <class 'dict'> -> JSON dump -> <class 'str'> -> FILE -> <class 'str'> -> JSON load -> <class 'dict'> -> <class 'BaseModel'>
```
- simple python data structure:Dictionaries, arrays, number and string ```python{'12':{'numbers' [1,2,3], 'name': "john"}}```
- JSON string representation: String representing a simple data structure in JSON format ```json python{"12":{"numbers": [1,2,3], "name": "john"}}''```
## FileStorage class
```python
class FileStorage:
    """serializes instances to a JSON file and deserializes JSON file to instances"""
    __file_path = 'file.json' # path to the json file
    __objects = {} # an empty __objects dictionary

    def all(self):
        """Returs the dictionary __objects"""
        return FileStorage.__objects # returns the dictionary object

    def new(self, obj):
        """sets in __objects the obj with <obj class name>.id"""
        """The new() method takes an object, converts it to a dictionary representation using its to_dict() method, constructs a unique key using the object's class name and id, and then adds the resulting key-value pair to the __objects dictionary using the update() method. So the __objects dictionary stores all the objects in the FileStorage instance, and each object is associated with a unique key that identifies its class name and id."""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id:obj})
        """This method takes an obj as an argument and adds it to the __objects dictionary by setting the key value pair tp obj_class_name.id: obj
        self.all().update(...) -> this retrieves the entire dictioanary ob objects by calling 'all() method and then updates it with new object
        {obj.to_dict()['__class__'] + '.' + obj.id: obj} -> this creates a new dictionary with a single key-value pair.The key is a string concantation of the objects's class name obtained from its to_dict() method and its unique id.The value is the object itself.By default obj.to_dict() returns a dictionary representation of the object, which includes __class__ attribute as one of its keys.Therefore we use the [__class__] key to access the objects class name
        In summary the new method takes an object, converts it to dictionary representation using its to_dict() method, constructs a unique key using the class name and id and the adds the resulting key valie pair to the __objects dictionary using the update() method.
        """
    def save(self):
        """serializes __objects to the JSON file"""
        with open(FileStorage.__file_path, 'w') as f:#open the __file_path file for writting using the 'with' statement
            temp = {} # creates a temporary dictionary and copies the content of the __objects dictionary to 'temp' using the update() method this is dome to avoid modifying the original __objects dictionary
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
                 # iterates through the temp dictionary using a for loop and converts each value which is an object to a dictionary representation using to_dict() method defined in the basemodel class,The resulting dictionary is stored back in temp with the same key.
            json.dump(temp, f) # finally uses the json.dump method to write the contents of the temp dictionary to the file handle f
            #save writes the serialized objects to a JSON file
    def reload(self):
        """deserializes the JSON file to __objects(only if the JSON file to __objects exist)"""
        from models.base_model import BaseModel # imports the basemodel class this is necessar beceuse the deserialized objects are constructed as instances of the appropriate subclass of 'BaseModel'
        classes = {
                     'BaseModel': BaseModel
                  } #the methods then creates a dictionary classes that maps the corresponding class objects.Currently there is only one mapping from the string 'BaseModel' to the 'BaseModel' class.
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
                    #Open the json file in the __file_path for reading using the with statement, if file is not found the exception is caught and ignored if the file is found
        except FileNotFoundError:
            pass
```