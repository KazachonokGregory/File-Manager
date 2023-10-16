import tkinter as tk
from Manager import Manager
import tkinter.messagebox as msgbox
import config

"""
implements the logic behind the displayed list of files (the interface)
"""
class FileListBox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.edit_item = 0
        self.manager = Manager()
        self.address_line = tk.Label(master)
        self.bind_keys();
        self.refresh()
    
    def bind_keys(self):
        self.bind("<Button-1>", self.on_click)
        self.bind("<Button-3>", self.on_click, add='+')
        self.bind("<Double-1>", self.go_to)
        self.bind("<Return>", self.on_enter)

    def undo(self, event=None):
        try:
            self.manager.undo()
        except:
            pass
        self.refresh()

    def redo(self, event=None):
        try:
            self.manager.redo()
        except:
            pass
        self.refresh()

    def ascend(self, event=None):
        self.manager.ascend()
        self.refresh()

    def on_click(self, event):
        self.edit_item = self.index(f"@{event.x},{event.y}")

    def on_right_click(self, event):
        index = self.index(f"@{event.x},{event.y}")
        self.select_clear(0, tk.END)
        self.selection_set(index)
        self.edit_item = index

    def on_enter(self, event=None):
        if not self.curselection():
            return
        self.edit_item = self.curselection()[0]
        self.go_to(event)
        self.select_clear(0, tk.END)
        self.select_set(self.edit_item)

    def refresh(self):
        names = self.manager.get_list()
        super().delete(0, tk.END)
        for name in names:
            self.insert(tk.END, name)
            if self.manager.is_folder(name):
                self.itemconfig(tk.END, fg=config.folder_color)
        self.select_set(self.edit_item)
        self.address_line.config(text=self.manager.get_abs(""))

        self.focus_set()
        self.see(self.edit_item)

    def go_to(self, event=None):
        path = self.get(self.edit_item)
        is_folder = self.manager.is_folder(path)
        self.manager.go_to(path)
        if is_folder:
            self.refresh()
            self.edit_item = 0

    def execute(self, event=None):
        self.manager.execute(self.get(self.edit_item))

    def make_file(self, event=None):
        self.make_something(isdir=False)

    def make_folder(self, event=None):
        self.make_something(isdir=True)

    """
    creates either a directory or a file
    """
    def make_something(self, isdir: bool):
        name = self.manager.make_something(isdir)
        self.refresh()
        self.edit_item = self.get(0, tk.END).index(name)
        self.see(self.edit_item)
        self.rename()
        self.refresh()

    def cut(self, event=None):
        self.copy(event)
        self.delete(event)

    def delete(self, event=None):
        agree = msgbox.askyesno("Warning", "Are you sure you want to delete these?")
        if not agree:
            return
        for item in self.curselection():
            self.manager.delete(self.get(item))
        self.refresh()

    def copy(self, event=None):
        to_copy = []
        for item in self.curselection():
            to_copy.append(self.get(item))
        self.manager.copy(to_copy)

    def paste(self, event=None):
        self.manager.paste()
        self.refresh()

    def rename(self, event=None):
        if not self.edit_item:
            return
        index = self.edit_item
        self.see(index)
        text = self.get(index)
        y0 = self.bbox(index)[1]
        entry = tk.Entry(self, borderwidth=0, highlightthickness=0)
        entry.config(font=self.cget('font'))
        entry.config(bg=config.bright_color)
        entry.config(fg=config.second_color)
        entry.config(insertbackground=config.second_color)
        entry.config(selectbackground=config.second_color)
        entry.config(selectforeground=config.bright_color)
        entry.bind("<Return>", self.accept_edit)
        entry.bind("<Escape>", self.cancel_edit)

        entry.insert(0, text)
        entry.selection_from(0)
        entry.selection_to("end")
        entry.place(relx=0, y=y0, relwidth=1, width=-1)
        entry.focus_set()
        entry.grab_set()

    def cancel_edit(self, event):
        event.widget.destroy()

    def accept_edit(self, event):
        new_data = event.widget.get()
        old_data = self.get(self.edit_item)
        self.manager.rename(old_data, new_data)
        event.widget.destroy()
        self.refresh()
