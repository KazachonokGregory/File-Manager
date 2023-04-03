import os
import subprocess
import shutil

class Manager:
    def __init__(self):
        self.cur_directory = os.getcwd()

    def get_abs(self, name):
        return os.path.normpath(os.path.join(self.cur_directory, name))

    def get_list(self):
        to_append = [".."] if os.path.dirname(self.cur_directory) != self.cur_directory else []
        return to_append + sorted(os.listdir(self.cur_directory))

    def go_to(self, name):
        if not name:
            return
        path = self.get_abs(name)
        print(path)
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

