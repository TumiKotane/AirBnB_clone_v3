#!/usr/bin/python3
"""
Parent class BaseModel
"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """
    Defines the common attributes of new objects
    """
    def __init__(self, *args, **kwargs):
        """
        Class constructor
        """
        if kwargs is not None and len(kwargs) != 0:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        setattr(self, key, datetime.strptime(
                            value, "%Y-%m-%dT%H:%M:%S.%f"))
                    else:
                        setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
        Returns specific info
        """
        className = "[" + self.__class__.__name__ + "] "
        classId = "(" + self.id + ") "
        classDict = str(self.__dict__)
        return className + classId + classDict

    def save(self):
        """
        Saves the object
        """
        value = datetime.now()
        setattr(self, 'updated_at', value)
        models.storage.save()

    def to_dict(self):
        """
        Gets the __dict__ and add the key __class__
        """
        new = {}
        var = self.__dict__
        for elem in var:
            if elem == 'created_at' or elem == 'updated_at':
                new[elem] = var[elem].isoformat()
            else:
                new[elem] = var[elem]
        new['__class__'] = self.__class__.__name__
        return (new)
