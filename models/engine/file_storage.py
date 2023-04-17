#!/usr/bin/python3
"""Defines a class to manage file storage for airBnB clone"""
import json

class FileStorage:
    """serializes instances to a JSON file and deserializes JSON file to instances"""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returs the dictionary __objects"""
        return FileStorage.__objects
    def new(self, obj):
        """sets in __objects the obj with <obj class name>.id"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id:obj})
    def save(self):
        """serializes __objects to the JSON file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)
    def reload(self):
        """deserializes the JSON file to __objects(only if the JSON file to __objects exist)"""
        from models.base_model import BaseModel
        classes = {
                     'BaseModel': BaseModel
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass
        
        
