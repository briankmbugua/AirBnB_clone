import cmd
import sys
from models.base_model import BaseModel
class HBNBCommand(cmd.Cmd):
    """functionality for the airbnclone console"""
    prompt = '(hbnb) ' if sys.__stdin__.isatty () else ''
    classes = {
        'BaseModel': BaseModel
    }