#!/usr/bin/python3
"""
File storage

"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


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
        return FileStorage.__objects

    def new(self, obj):
        """
        save in self.__objects each object created

        Args:
            obj
        Returns:
            None

        """
        ocname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(ocname, obj.id)] = obj

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
        odict = FileStorage.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

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
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o[ "__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
