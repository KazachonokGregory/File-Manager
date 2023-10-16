import config
from tkinter import messagebox as msgbox

"""
stores information about each type of operation: bindings, icons etc.
"""
class OperationsInfo:
    def __init__(self, master):
        listbox = master.files_listbox
        self.commands = {
            "New folder": listbox.make_folder,
            "Copy": listbox.copy,
            "Paste": listbox.paste,
            "Rename": listbox.rename,
            "Delete": listbox.delete,
            "Cut": listbox.cut,
            "Execute": listbox.execute,
            "Undo": listbox.undo,
            "Redo": listbox.redo,
            "New file": listbox.make_file,
            "Open": listbox.on_enter
        }

        for name, command in self.commands.items():
            self.commands[name] = self.exception_handler(command, name)

        self.icon_files = {
            "New folder": "new-folder.png",
            "Copy": "copy.png",
            "Paste": "paste.png",
            "Rename": "rename.png",
            "Delete": "delete.png",
            "Cut": "cut.png",
            "Execute": "execute.png",
            "Undo": "undo.png",
            "Redo": "redo.png",
            "New file": "new-file.png",
            "Open": "open.png"
        }
        self.bindings = {
            "New folder": "<Control-n>",
            "Copy": "<Control-c>",
            "Paste": "<Control-v>",
            "Rename": "r",
            "Delete": "<Delete>",
            "Cut": "<Control-x>",
            "Execute": "x",
            "Undo": "<Control-z>",
            "Redo": "<Control-r>",
        }
        self.button_names = ["Undo", "Redo", "Open", "New file", "New folder", "Copy", "Paste", "Rename", "Delete", "Cut", "Execute"] 
        self.menu_names = ["Open", "Rename", "Delete", "Copy", "Cut", "Execute"] 


    def exception_handler(self, func, name):
        def exception_handler_decorator(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exception:
                msgbox.showerror("Error", "{name} failed:\n{exception}".format(name=name, exception=exception))
        return exception_handler_decorator

