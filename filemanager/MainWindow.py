import tkinter as tk
from FileListBox import FileListBox

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("File Manager")
        self.geometry("720x540")
        self.resizable(True, True)
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True)

        self.create_listbox()
        self.create_buttons()

    def create_listbox(self):
        self.files_listbox = FileListBox(self.main_frame, selectmode=tk.MULTIPLE)
        self.files_listbox.pack()

    def create_buttons(self):
        self.new_folder_button = tk.Button(self.main_frame, text="Create Folder", command=self.files_listbox.make_folder)
        self.new_folder_button.pack()
        
        self.delete_button = tk.Button(self.main_frame, text="Delete", command=self.files_listbox.delete)
        self.delete_button.pack()

        self.rename_button = tk.Button(self.main_frame, text="Rename", command=self.files_listbox.rename)
        self.rename_button.pack()
        
