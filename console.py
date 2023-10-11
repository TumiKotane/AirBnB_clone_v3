#!/usr/bin/python3
""" console """

import cmd
from datatime import datetime
from models
from models.city import City
from models.base_model import BaseModel
from models.amenity import Amenity
from models.state import State
from models.review import Review
from models.place import Place
from models.user import User
import shlex # for splitting the line along spaces except in double quotes

classes = {"BaseModel": Basemodel, "User": User, "State": State, "City": City, "Amenity": Amenity, "Place": Place, "Review": Review}

class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = ' (hbnb) '

    def do_EOF(self, arg):
        """ Exits console """
        return True

    def emptyline(self):
        """ Overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def _key_value_parser(self, args):
        """ Creates a dictionary from a list of strings """
        new_dict = {}
        for arg in args:
            if "=" in arg:
                kvp = arg.split('=', 1)
                key = kvp[0]
                value = kvp[1]
                if value[0] == value[-1] == '"':
                    value = shlex.split(value)[0].replace('_', ' ')
                else:
                    try:
                        value = int(value)
                    except:
                        try:
                            value = float(value)
                        except:
                            continue
                new_dict[key] = value
        return new_dict

    def do_create(self, arg):
        """ Creates a new instance of a class """
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            new_dict = self._key_value_parser(args[1:])
            instance = classes[args[0]](*new_dict)
        else:
            print("** class dosen't exist **")
            return False
        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """ Print an instance as a string based on the class and id """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """ Delets an instance based on the class and id """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """ Prints string representations of instances """
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        elif args[0] in classes:
            obj_dict = models.storage.all(classes[args[0])
        else:
            print("** class doesn't exist **")
            return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key])
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, arg):
    """ Updates an instance based on the class name, id, attribute & value """
    args = shlex.split(arg)
    integers = ["number_rooms", "number_bathrooms", "max_guest",
                "price_by_night"]
    floats = ["latitude", "longitude"]
    if len(args) == 0:
        print("** class name missing **")
    else:
        try:
            eval(str(linr[0]))
        except:
            print("** class doesn't exist **")
            return
        if len(line) == 1:
            print("** instance id missing **")
        else:
                objects = models.storage.all()
                key = str(line[0]) + "." + str(line[1])
                if key not in objects:
                    print("** no instance found **")
                else:
                    if len(line) == 2:
                        print("** attribute name missing **")
                    else:
                        if len(line) == 3:
                            print("** value missing **")
                        else:
                            setattr(objects[key], line[2], line[3])
                            models.storage.save()

    def do_count(self, args):
        """Count the number of type of class - Usage: count <classname>"""
        cont = 0
        objects = models.storage.all()
        new = {}
        for elem in objects:
            new[elem] = objects[elem].to_dict()
        for elem in new:
            if (args == new[elem]['__class__']):
                cont = cont + 1
        print(cont)

     def default(self, args):
        """ Handle alternative command representations """
        first = args.split('.')
        if len(first) > 1:
            class_name = first[0]
            methods = first[1]
            first[1] = first[1].replace('(', '&(')
            second = first[1].split('&')
            comando = class_name

            if methods == "all()":
                self.do_all(comando)
            elif methods == "count()":
                self.do_count(comando)
            else:
                methods = second[0]
                elems = second[1]
                elems = elems.replace('(', '')
                elems = elems.replace(')', '')
                elems = elems.replace('{', '"{')
                elems = elems.replace('}', '}"')
                third = shlex.split(elems)
                if not third:
                    id = ' '
                    third.append(id)
                 else:
                    for i in range(len(third)):
                        third[i] = third[i].replace(',', ' ')
                        third[i] = third[i].strip()
                    id = third[0]
                comando = comando + ' ' + id
                comando = comando.replace('\"', '')
                if methods == "show" and len(third) == 1:
                    self.do_show(comando)
                elif methods == "destroy" and len(third) == 1:
                    self.do_destroy(comando)
                elif methods == "update":
                    x = len(third)
                    if x > 1 and third[1][0] == '{' and third[1][-1] == '}':
                        third[1] = third[1].replace('{', '')
                        third[1] = third[1].replace('}', '')
                        third[1] = third[1].replace(': ', ':')
                        sub = shlex.split(third[1], ', ')
                        new = []
                        for ele in sub:
                            sub2 = ele.split(':')
                            if len(sub2) < 2:
                                sub2.append('')
                            new.append(tuple(sub2))
                        dicti = dict(new)
                        print(dicti)
                        for key in dicti:
                            new_comand = comando + ' '
                            new_comand += str(key)
                            new_comand = new_comand.replace('\"', '')
                            new_comand = new_comand.replace('\'', '')
                            new_comand += ' \"' + str(dicti[key]) + '\"'
                            self.do_update(new_comand)
                    else:
                        for i in range(1, len(third)):
                            if i == 1:
                                comando = comando + ' ' + third[i]
                            if i == 2:
                                comando = comando + ' '
                                comando += '\"' + third[i] + '\"'
                        self.do_update(comando)
                else:
                    return cmd.Cmd.default(self, args)
            else:
                return cmd.Cmd.default(self, args)

    if __name__ == '__main__':
        """ Main """
        HBNBHCommand().cmdloop()
