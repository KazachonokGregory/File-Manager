import os
import subprocess
import shutil
import tempfile

class Manager:
    def __init__(self):
        self.cur_directory = os.getcwd()
        self.copy_buffer = tempfile.TemporaryDirectory()

    def __del__(self):
        self.copy_buffer.cleanup()

    def get_abs(self, name):
        return os.path.normpath(os.path.join(self.cur_directory, name))

    def get_list(self):
        to_append = [".."] if os.path.dirname(self.cur_directory) != self.cur_directory else []
        return to_append + sorted(os.listdir(self.cur_directory))

    def go_to(self, name):
        if not name:
            return
        path = self.get_abs(name)
        if os.path.isdir(path):
            self.cur_directory = path
        elif os.access(path, os.X_OK):
            subprocess.call((path))
        else:
            subprocess.call(('xdg-open', path))

    def make_folder(self):
        num = 1
        while True:
            try:
                name = "New folder " + str(num)
                os.mkdir(self.get_abs(name))
                return name
            except:
                num += 1

    def delete(self, name):
        if not name or name == "..":
            return
        path = self.get_abs(name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def rename(self, old_name, new_name):
        old_path = self.get_abs(old_name)
        new_path = self.get_abs(new_name)
        os.rename(old_path, new_path)

    def clean(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

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
        print("copy", path, new_path)
        print(os.listdir(self.copy_buffer.name))

    def paste(self):
        print(os.listdir(self.copy_buffer.name))
        for name in os.listdir(self.copy_buffer.name):
            path = os.path.join(self.copy_buffer.name, name)
            if os.path.isdir(path):
                new_path = self.get_abs(name)
                shutil.copytree(path, new_path)
            else:
                new_path = self.cur_directory
                shutil.move(path, new_path)
            print("print", path, new_path)
    
