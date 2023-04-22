#!/usr/bin/python3
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
class HBNBCommand(cmd.Cmd):
    """functionality for the airbnclone console"""
    prompt = '(hbnb) ' if sys.__stdin__.isatty () else ''
    classes = {
        'BaseModel': BaseModel
    }
    def do_quit(self, command):
        """Method to exit the HBNB console"""
        exit()
    def help_quit(self):
        """print the help document for quit"""
        print("Exists the program with formattinh\n")
    def do_E0F(self, arg):
        """Handles EOF to exit the program"""
        print()
        exit()
    def help_EOF(self, arg):
        """Hnadles EOF to exit program"""
        print("Exit the program without formatting\n")
    def emptyline(self):
        """Overrides the empty line method of CMD"""
        pass
    def do_create(self, args):
        """Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        elif args not in HBNBCommand.classes:
            print("** class dosen't exist **")
            return
        new_instance = HBNBCommand.classes[args]()
        storage.save()
        print(new_instance.id)
        storage.save()
    def help_create(self):
        """Help information for the create method"""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")
    def do_show(self, args):
        """Method to show an individual object """
        new = args.partition(" ")
if __name__ == '__main__':
    HBNBCommand().cmdloop()
