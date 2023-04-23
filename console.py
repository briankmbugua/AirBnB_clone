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
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partion(' ')[0]
        
        if not c_name:
            print("** class name missing **")
            return
        
        if c_name not in HBNBCommand.classes:
            print("**  class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return
        
        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found")
    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <classname> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partiton(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]
        if not c_name:
            print("** class name missing **")
            return
        
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        
        if not c_id:
            print("** instance id missing **")
            return
        
        key = c_name + "." + c_id

        try:
            del(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")
    
    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroy an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")
    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0] #removes possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorge__objects.items():
                if k.split('.')[0] == args:
                    print_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <ClassName\n")
    
    def do_update(self, args):
        """Updates a certain object with new info"""
        c_name = c_id = att_name = att_val = kwargs = ''

        #isolate cls from id/args, ex (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        else: # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes: # class name invalid
            print("** class doesn't exist **")
            return
        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            c_id = args[0]
        else: # id not present
            print("** instance id missing **")
            return
        
        # generate key from class and id
        key = c_name + "." + c_id

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return
        # first determine if kwargs or args
        
    

if __name__ == '__main__':
    HBNBCommand().cmdloop()
