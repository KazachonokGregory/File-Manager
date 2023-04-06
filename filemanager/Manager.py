import os
import subprocess
import shutil
import tempfile
from CommandManager import CommandManager
import copy

def copy_contents(src, dest):
    for name in os.listdir(src):
        path = os.path.join(src, name)
        if os.path.isdir(path):
            new_path = os.path.join(dest, name)
            shutil.copytree(path, new_path)
        else:
            new_path = dest
            shutil.copy(path, new_path)

def clean(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            pass

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
        copy_contents(self.cur_directory, self.buffer)

    def __call__(self):
        try:
            copy_contents(self.copy_buffer, self.cur_directory)
        except Exception as e:
            self.undo()
            raise e

    def __del__(self):
        self.buffer.cleanup()

    def undo(self):
        clean(cur_directory)
        copy_contents(self.buffer, cur_directory)

class Manager:
    def __init__(self):
        self.cur_directory = os.getcwd()
        self.copy_buffer = tempfile.TemporaryDirectory()
        self.undo_manager = CommandManager()

    def __del__(self):
        self.copy_buffer.cleanup()

    def get_abs(self, name):
        return os.path.normpath(os.path.join(self.cur_directory, name))

    def get_list(self):
        to_append = [".."] if os.path.dirname(self.cur_directory) != self.cur_directory else []
        return to_append + sorted(os.listdir(self.cur_directory))

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
        subprocess.call((path))

    def make_folder(self):
        num = 1
        while True:
            try:
                name = "New folder " + str(num)
                path = self.get_abs(name)
                self.undo_manager.do(MakeFolder(path))
                return name
            except:
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
        self.clean(self.copy_buffer.name)
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

    
