import tkinter as tk
import tkinter.messagebox as msgbox
from Manager import Manager

class FileListBox(tk.Listbox):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.edit_item = None
        self.manager = Manager()
        self.address_line = tk.Label(master)
        self.prev_edit = None
        self.refresh()

        self.bind("<Button-1>", self.on_click)
        self.bind("<Double-1>", self.go_to)
        self.bind("<Return>", self.on_enter)

    def on_click(self, event):
        self.edit_item = self.index(f"@{event.x},{event.y}")

    def on_enter(self, event):
        if not self.curselection():
            return
        self.edit_item = self.curselection()[0]
        self.go_to(event)

    def refresh(self):
        files = self.manager.get_list()
        super().delete(0, tk.END)
        for file in files:
            self.insert(tk.END, file)
        self.select_set(0)
        self.address_line.config(text=self.manager.get_abs(""))
        self.address_line.pack()

        self.focus_set()

    def go_to(self, event):
        self.manager.go_to(self.get(self.edit_item))
        self.refresh()

    def make_folder(self):
        name = self.manager.make_folder()
        self.refresh()
        self.edit_item = self.manager.get_list().index(name)
        self.insert(0, "New folder")
        self.edit_item = 0
        try:
            self.rename()
        except:
            super().delete(0)
            self.refresh()
            return

        name = self.get(0)
        try:
            self.manager.make_folder(name)
        except:
            msgbox.showerror("Error", "Couldn't make folder")
        self.refresh()

    def delete(self):
        agree = msgbox.askyesno("Warning", "Are you sure you want to delete these?")
        if not agree:
            return
        for item in self.curselection():
            self.manager.delete(self.get(item))
        self.refresh()

    def copy(self):
        to_copy = []
        for item in self.curselection():
            to_copy.append(self.get(item))
        self.manager.copy(to_copy)

    def paste(self):
        self.manager.paste()
        self.refresh()

    def rename(self):
        if not self.edit_item:
            return
        index = self.edit_item
        text = self.get(index)
        print(index)
        y0 = self.bbox(index)[1]
        entry = tk.Entry(self, borderwidth=0, highlightthickness=1)
        entry.focus_set()
        try:
            entry.grab_set()
        except:
            return
        entry.bind("<Return>", self.accept_edit)
        entry.bind("<Escape>", self.cancel_edit)

        entry.insert(0, text)
        entry.selection_from(0)
        entry.selection_to("end")
        entry.place(relx=0, y=y0, relwidth=1, width=-1)

    def cancel_edit(self, event):
        event.widget.destroy()

    def accept_edit(self, event):
        new_data = event.widget.get()
        old_data = self.get(self.edit_item)
        try:
            self.manager.rename(old_data, new_data)
        except Exception as e:
            msgbox.showerror("Error", "Couldn't rename")
        event.widget.destroy()
        self.refresh()
