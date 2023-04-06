import tkinter as tk
import config
from PIL import Image
from OperationsInfo import OperationsInfo
from FileListBox import FileListBox
from ToolTip import CreateToolTip
from PopupMenu import PopupMenu

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("File Manager")
        self.geometry("500x400")
        self.configure(bg=config.primary_color)
        self.resizable(True, True)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="top", anchor='w', fill='x', pady=5)
        self.button_frame.config(bg=config.primary_color)
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side="top", fill="both", expand=True, pady=5)
        self.main_frame.config(bg=config.primary_color)

        self.create_listbox()

        self.oper_info = OperationsInfo(self)

        self.create_buttons()
        self.create_popup_menu()

    def create_buttons(self):
        for name, key in self.oper_info.bindings.items():
            self.bind(key, self.oper_info.commands[name])

        self.buttons = dict()
        self.icons = dict()
        self.ttps = dict() # hovering tips
        path_prefix = config.icon_path_prefix # prefix of relative paths to the icons
        for name in self.oper_info.button_names:
            self.buttons[name] = tk.Button(self.button_frame, command=self.oper_info.commands[name])
            self.icons[name] = tk.PhotoImage(file=path_prefix + self.oper_info.icon_files[name])
            self.buttons[name].config(image=self.icons[name], bg=config.primary_color)
            self.buttons[name].config(relief=tk.RAISED, highlightthickness=0, bd=0)
            self.buttons[name].config(activebackground=config.neutral_color)
            self.buttons[name].pack(side='left', padx=5)
            self.ttps[name] = CreateToolTip(self.buttons[name], name, config.font)

    def create_popup_menu(self):
        self.menu = PopupMenu(self, tearoff = 0, font=config.font, bg=config.menu_color)
        for name in self.oper_info.menu_names:
            self.menu.add_command(label = name, command=self.oper_info.commands[name])
        self.menu.bind("<FocusOut>", self.menu.popup_remove)
        self.files_listbox.bind("<Button-3>", self.menu.popup, add='+')

    def create_listbox(self):
        self.files_listbox = FileListBox(
                self.main_frame, selectmode=tk.EXTENDED, relief=tk.FLAT,
                bd=0, bg=config.primary_color, fg=config.second_color, highlightcolor=config.primary_color,
                selectbackground=config.third_color,
                font=(config.font, 12, 'bold'))
        self.files_listbox.address_line.config(
                bg=config.primary_color, fg=config.second_color, font=(config.font, 9),
                anchor = 'w')
        self.files_listbox.address_line.pack(fill='x')
        self.files_listbox.pack(side=tk.TOP, padx=20, pady=10, fill='both', expand=True)

