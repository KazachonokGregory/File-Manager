import os
import shutil

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
