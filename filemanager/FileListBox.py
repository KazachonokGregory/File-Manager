import tkinter as tk
from Manager import Manager

class FileListBox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master_frame = master

        self.edit_item = None
        self.manager = Manager()
        self.refresh()

        self.bind("<Button-1>", self.on_click)
        self.bind("<Double-1>", self.go_to)

    def popup(self, message):
        top = tk.Toplevel(self.master_frame)
        tk.Label(top, text=message).place(x=150,y=80)

    def on_click(self, event):
        self.edit_item = self.index(f"@{event.x},{event.y}")

    def refresh(self):
        files = self.manager.get_list()
        super().delete(0, tk.END)
        for file in files:
            self.insert(tk.END, file)

    def go_to(self, event):
        self.manager.go_to(self.get(self.edit_item))
        self.refresh()

    def make_folder(self):
        name = self.manager.make_folder()
        self.refresh()
        self.edit_item = self.manager.get_list().index(name)
        self.rename()
        self.refresh()

    def delete(self):
        self.popup("Aand their gone")
        for item in self.curselection():
            self.manager.delete(self.get(item))
        self.refresh()

    def rename(self):
        if not self.edit_item:
            return
        index = self.edit_item
        text = self.get(index)
        y0 = self.bbox(index)[1]
        entry = tk.Entry(self, borderwidth=0, highlightthickness=1)
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
