import os
import shutil
import tempfile
from Utilities import *

"""
these classes implement the operations on the lowest level. They are required by the UndoManager
"""

class OpenPath:
    def __init__(self, master, new_path):
        self.old_path = master.cur_directory
        self.master = master
        self.new_path = new_path

    def __call__(self):
        self.master.cur_directory = self.new_path

    def undo(self):
        self.master.cur_directory = self.old_path

class Rename:
    def __init__(self, old_name, new_name):
        self.new_name = new_name
        self.old_name = old_name

    def __call__(self):
        os.rename(self.old_name, self.new_name)
        
    def undo(self):
        os.rename(self.new_name, self.old_name)

class MakeFolder:
    def __init__(self, path):
        self.path = path

    def __call__(self):
        os.mkdir(self.path)

    def undo(self):
        shutil.rmtree(self.path)

class MakeFile:
    def __init__(self, path):
        self.path = path

    def __call__(self):
        if os.path.isfile(self.path):
            raise FileExistsError
        with open(self.path, 'a'):
            os.utime(self.path, None)

    def undo(self):
        os.remove(self.path)

class DeleteFolder:
    def __init__(self, path, name):
        self.name = name
        self.path = path
        self.buffer = tempfile.TemporaryDirectory()
        self.new_path = os.path.join(self.buffer.name, self.name)

    def __call__(self):
        try:
            shutil.copytree(self.path, self.new_path)
        except:
            pass
        shutil.rmtree(self.path)

    def __del__(self):
        self.buffer.cleanup()

    def undo(self):
        shutil.copytree(self.new_path, self.path)

class DeleteFile:
    def __init__(self, path, name):
        self.path = path
        self.buffer = tempfile.TemporaryDirectory()
        self.new_path = os.path.join(self.buffer.name, name)

    def __call__(self):
        try:
            shutil.copy(self.path, self.buffer.name)
        except:
            pass
        os.remove(self.path)

    def __del__(self):
        self.buffer.cleanup()

    def undo(self):
        shutil.copy(self.new_path, self.path)

"""
inefficient
"""
class Paste:
    def __init__(self, cur_directory, copy_buffer):
        self.cur_directory = cur_directory
        self.buffer = tempfile.TemporaryDirectory()
        self.copy_buffer = copy_buffer
        copy_contents(self.cur_directory, self.buffer.name)

    def __call__(self):
        try:
            copy_contents(self.copy_buffer.name, self.cur_directory)
        except Exception as e:
            self.undo()
            raise e

    def __del__(self):
        self.buffer.cleanup()

    def undo(self):
        clean(self.cur_directory)
        copy_contents(self.buffer.name, self.cur_directory)
