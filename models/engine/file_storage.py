#!/usr/bin/python3
"""
File storage

"""
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {'BaseModel': BaseModel, 'User': User, 'Place': Place,
           'State': State, 'City': City, 'Amenity': Amenity,
           'Review': Review}


class FileStorage:
    """
    FileStorage gets the new objects created using Basemodel or
    another class that inherits from BaseModel, and save this new
    objects in a file.json.
    in order to save the objects and upload them when we start to
    run again the program
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """
        all return the dictionary of objects
        Args:
            None
        Returns:
            the dictionary of objects
        """
        return self.__objects

    def new(self, obj):
        """
        save in self.__objects each object created

        Args:
            obj
        Returns:
            None

        """
        self.__objects[obj.__class__.__name__ + "." + obj.id] = obj

    def save(self):
        """
        save in file the serialized dictionary of objects
        we have to change a dictionary of objects into
        a dictionary of dictionaries using method .to_dict()
        Save the result in file.json
        Args:
            None

        Returns:
            None
        """
        new = {}
        for elem in self.__objects:
            new[elem] = self.__objects[elem].to_dict()
        with open(self.__file_path, 'w') as fd:
            json.dump(new, fd)

    def reload(self):
        """
        load the Json from file and gets the dictionary of dictionaries
        and the turn into a dictionary of objects and save it in
        self.__objects

        Args:
            None

        Returns:
            None
        """
        if os.path.exists(self.__file_path) is True:
            with open(self.__file_path, 'r') as fd:
                var = json.load(fd)
                for elem in var:
                    aux = classes[var[elem]['__class__']]
                    self.__objects[elem] = aux(**(var[elem]))

