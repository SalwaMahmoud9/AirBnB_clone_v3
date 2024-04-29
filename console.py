#!/usr/bin/python3
"""Console."""
import cmd
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """HBNBCommand"""

    prompt = '(hbnb) '

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def precmd(self, line):
        """ HBNBCommand """
        _cmd = _cls = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:
            pline = line[:]

            _cls = pline[:pline.find('.')]

            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                pline = pline.partition(', ')

                _id = pline[0].replace('\"', '')

                pline = pline[2].strip()
                if pline:
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """HBNBCommand"""
        return stop

    def postloop(self):
        """HBNBCommand"""
        # print()

    def do_quit(self, command):
        """HBNBCommand"""
        return True

    def do_create(self, args):
        """HBNBCommand"""
        params = self.__validateArgs(args)
        if type(params) != dict:
            return
        try:
            new_instance = HBNBCommand.classes[args.split()[0]](**params)
            new_instance.save()
            print(new_instance.id)
        except Exception:
            pass

    def do_EOF(self, arg):
        """ HBNBCommand """
        print()
        return True

    def emptyline(self):
        """HBNBCommand"""
        pass

    def __validateArgs(self, args):
        """HBNBCommand"""
        if not args:
            return print("** class name missing **")
        args = args.split()
        if args[0] not in self.classes:
            return print("** class doesn't exist **")
        params = {}
        for arg in args[1:]:
            param = arg.split('=')
            if len(param) == 2:
                value = param[1]
                if value[0] == '"' and value[-1] == '"':
                    params[param[0]] = value.replace('_', ' ').strip('"')
                elif value.isnumeric():
                    params[param[0]] = int(value)
                else:
                    try:
                        if float(value):
                            params[param[0]] = float(value)
                    except Exception:
                        pass
        return params

    def do_show(self, args):
        """HBNBCommand"""
        new = args.partition(" ")
        current_name = new[0]
        current_id = new[2]
        if current_id and ' ' in current_id:
            current_id = current_id.partition(' ')[0]
        if not current_name:
            return print("** class name missing **")
        if current_name not in HBNBCommand.classes:
            return print("** class doesn't exist **")
        if not current_id:
            return print("** instance id missing **")
        objs = storage.all(current_name).values()
        obj = [v for v in objs if v.id == current_id]
        if len(obj) == 0:
            print("** no instance found **")
        else:
            print(obj[0])

    def do_destroy(self, args):
        """HBNBCommand"""
        new = args.partition(" ")
        current_name = new[0]
        current_id = new[2]
        if current_id and ' ' in current_id:
            current_id = current_id.partition(' ')[0]
        if not current_name:
            return print("** class name missing **")
        if current_name not in HBNBCommand.classes:
            return print("** class doesn't exist **")
        if not current_id:
            return print("** instance id missing **")
        objs = storage.all(current_name).values()
        obj = [v for v in objs if v.id == current_id]
        print("** no instance found **") if len(obj) == 0 else obj[0].delete()

    def do_all(self, args):
        """HBNBCommand"""
        cls = None
        if args:
            cls = args.split(' ')[0]
            if cls not in HBNBCommand.classes:
                return print("** class doesn't exist **")
        from models import storage
        objs = storage.all(cls)
        print([str(v) for v in objs.values()])

    def do_count(self, args):
        """HBNBCommand"""
        if args not in self.classes:
            return print("** class doesn't exist **")
        print(len(storage.all(args).values()))

    def do_update(self, args):
        """HBNBCommand"""
        current_name = ''
        current_id = ''
        attr_name = ''
        attr_val = ''
        kwargs = ''

        args = args.partition(" ")
        if args[0]:
            current_name = args[0]
        else:
            print("** class name missing **")
            return
        if current_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        args = args[2].partition(" ")
        if args[0]:
            current_id = args[0]
        else:
            print("** instance id missing **")
            return

        key = current_name + "." + current_id

        if key not in storage.all(current_name):
            print("** no instance found **")
            return

        if '{' in args[2] and '}' in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:
            args = args[2]
            if args and args[0] == '\"':
                second_quote = args.find('\"', 1)
                attr_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(' ')

            if not attr_name and args[0] != ' ':
                attr_name = args[0]
            if args[2] and args[2][0] == '\"':
                attr_val = args[2][1:args[2].find('\"', 1)]

            if not attr_val and args[2]:
                attr_val = args[2].partition(' ')[0]

            args = [attr_name, attr_val]

        new_dict = storage.all(current_name)[key]

        for i, attr_name in enumerate(args):
            if (i % 2 == 0):
                attr_val = args[i + 1]
                if not attr_name:
                    print("** attribute name missing **")
                    return
                if not attr_val:
                    print("** value missing **")
                    return
                if attr_name in HBNBCommand.types:
                    attr_val = HBNBCommand.types[attr_name](attr_val)

                new_dict.__dict__.update({attr_name: attr_val})

        new_dict.save()

    def help_update(self):
        """ HBNBCommand """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")

    def help_all(self):
        """HBNBCommand"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def help_count(self):
        """HBNBCommand"""
        print("Usage: count <class_name>")

    def help_destroy(self):
        """HBNBCommand"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def help_show(self):
        """HBNBCommand"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def help_create(self):
        """HBNBCommand"""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def help_quit(self):
        """HBNBCommand"""
        print("Exits the program with formatting\n")

    def help_EOF(self):
        """HBNBCommand"""
        print("Exits the program without formatting\n")


if __name__ == "__main__":
    """ main """
    HBNBCommand().cmdloop()
