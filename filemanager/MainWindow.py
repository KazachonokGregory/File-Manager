import tkinter as tk
from FileListBox import FileListBox
from PIL import Image, ImageTk
from ToolTip import CreateToolTip

class MainWindow(tk.Tk):

    bg_color = '#33001a'
    text_color = 'white'
    font = "Fixedsys"

    def __init__(self):
        super().__init__()

        self.title("File Manager")
        self.geometry("500x400")
        self.configure(bg=self.bg_color)
        self.resizable(True, True)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="top", anchor='w', fill='x')
        self.button_frame.config(bg=self.bg_color)
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True, pady=5)
        self.main_frame.config(bg=self.bg_color)

        self.create_listbox()
        self.create_dicts()
        self.create_buttons()
        self.create_popup_menu()

    def create_dicts(self):
        self.commands = {
            "New folder": self.files_listbox.make_folder,
            "Copy": self.files_listbox.copy,
            "Paste": self.files_listbox.paste,
            "Rename": self.files_listbox.rename,
            "Delete": self.files_listbox.delete,
            "Cut": self.files_listbox.cut,
            "Open": self.files_listbox.go_to,
            "Execute": self.files_listbox.execute,
            "Undo": self.files_listbox.undo,
            "Redo": self.files_listbox.redo
        }
        self.icon_files = {
            "New folder": "../stuff/new-folder.png",
            "Copy": "../stuff/copy.png",
            "Paste": "../stuff/paste.png",
            "Rename": "../stuff/rename.png",
            "Delete": "../stuff/delete.png",
            "Cut": "../stuff/cut.png",
            "Execute": "../stuff/execute.png",
            "Undo": "../stuff/undo.png",
            "Redo": "../stuff/redo.png"
        }
        self.button_names = ["Undo", "Redo", "New folder", "Copy", "Paste", "Rename", "Delete", "Cut", "Execute"] 
        self.menu_names = ["Rename", "Delete", "Copy", "Cut", "Execute"] 

    def popup(self, event):
        self.event = event
        try:
            self.menu.post(event.x_root, event.y_root)
            self.menu.focus_set()
        finally:
            self.menu.grab_release()

    def popup_remove(self, event):
        self.menu.unpost()

    def create_popup_menu(self):
        self.menu = tk.Menu(self, tearoff = 0, font=self.font, bg="#ffffff")
        for name in self.menu_names:
            self.menu.add_command(label = name, command=self.commands[name])
        self.menu.bind("<FocusOut>", self.popup_remove)
        self.files_listbox.bind("<Button-3>", self.popup, add='+')

    def create_listbox(self):
        self.files_listbox = FileListBox(
                self.main_frame, selectmode=tk.EXTENDED, relief=tk.FLAT,
                bd=0, bg=self.bg_color, fg=self.text_color, highlightcolor=self.bg_color,
                highlightbackground=self.text_color, font=self.font)
        self.files_listbox.address_line.config(
                bg=self.bg_color, fg=self.text_color, font=(self.font, 9))
        self.files_listbox.address_line.pack(side=tk.TOP, anchor='nw')
        self.files_listbox.pack(side=tk.TOP, padx=20, pady=10, fill='both', expand=True)

    def create_buttons(self):
        self.buttons = dict()
        self.icons = dict()
        self.ttps = dict() # hovering tips

        for name in self.button_names:
            self.buttons[name] = tk.Button(self.button_frame, command=self.commands[name])
            self.icons[name] = tk.PhotoImage(file=self.icon_files[name])
            self.buttons[name].config(image=self.icons[name], bg=self.bg_color)
            self.buttons[name].config(relief=tk.RAISED, highlightthickness=0, bd=0)
            self.buttons[name].config(activebackground=self.text_color)
            self.buttons[name].pack(side='left', padx=5)
            self.ttps[name] = CreateToolTip(self.buttons[name], name, self.font)
