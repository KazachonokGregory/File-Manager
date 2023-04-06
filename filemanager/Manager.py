import os
import subprocess
import shutil
import tempfile
from UndoManager import UndoManager
from natsort import os_sorted
from Utilities import *
from Operations import *

class Manager:
    def __init__(self):
        self.cur_directory = os.getcwd()
        self.copy_buffer = tempfile.TemporaryDirectory()
        self.undo_manager = UndoManager()

    def __del__(self):
        self.copy_buffer.cleanup()

    def get_abs(self, name):
        return os.path.normpath(os.path.join(self.cur_directory, name))
    
    def is_folder(self, name):
        return os.path.isdir(self.get_abs(name))

    def get_list(self):
        to_append = [".."] if os.path.dirname(self.cur_directory) != self.cur_directory else []
        folders = []
        files = []
        for name in os.listdir(self.cur_directory):
            if self.is_folder(name):
                folders.append(name)
            else:
                files.append(name)
        return to_append + os_sorted(folders) + os_sorted(files)

    def undo(self):
        self.undo_manager.undo()

    def redo(self):
        self.undo_manager.redo()

    def go_to(self, name):
        if not name:
            return
        path = self.get_abs(name)
        if os.path.isdir(path):
            self.undo_manager.do(OpenPath(self, path))
        else:
            subprocess.call(('xdg-open', path))

    def execute(self, name):
        path = self.get_abs(name)
        subprocess.call(path)

    def make_something(self, isdir : bool):
        num = 1
        generic_name = "folder" if isdir else "file"
        while True:
            try:
                name = "New {something} ".format(something=generic_name) + str(num)
                path = self.get_abs(name)
                operation = MakeFolder(path) if isdir else MakeFile(path)
                self.undo_manager.do(operation)
                return name
            except FileExistsError:
                num += 1

    def delete(self, name):
        if not name or name == "..":
            return
        path = self.get_abs(name)
        if os.path.isdir(path):
            self.undo_manager.do(DeleteFolder(path, name))
        else:
            self.undo_manager.do(DeleteFile(path, name))

    def rename(self, old_name, new_name):
        old_path = self.get_abs(old_name)
        new_path = self.get_abs(new_name)
        self.undo_manager.do(Rename(old_path, new_path))

    def copy(self, to_copy):
        clean(self.copy_buffer.name)
        for name in to_copy:
            if name == "..":
                continue
            path = self.get_abs(name)
            if os.path.isdir(path):
                new_path = os.path.join(self.copy_buffer.name, name)
                shutil.copytree(path, new_path)
            else:
                new_path = self.copy_buffer.name
                shutil.copy(path, new_path)

    def paste(self):
        self.undo_manager.do(Paste(self.cur_directory, self.copy_buffer))

    def ascend(self):
        self.cur_directory = self.get_abs("..")

    
