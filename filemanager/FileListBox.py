import tkinter as tk
import tkinter.messagebox as msgbox
from Manager import Manager

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
        self.bind("<Control-c>", self.copy)
        self.bind("<Control-v>", self.paste)
        self.bind("r", self.rename)
        self.bind("l", self.on_enter)
        self.bind("h", self.ascend)

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
        index = self.index(f"@{event.x},{event.y}")
        self.edit_item = index

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

    def refresh(self):
        files = self.manager.get_list()
        super().delete(0, tk.END)
        for file in files:
            self.insert(tk.END, file)
#            self.itemconfig(tk.END, background="#00ffff") 📁
        self.select_set(0)
        self.address_line.config(text=self.manager.get_abs(""))

        self.focus_set()
        self.see(self.edit_item)

    def go_to(self, event=None):
        self.manager.go_to(self.get(self.edit_item))
        self.edit_item = 0
        self.refresh()

    def execute(self, event=None):
        try:
            self.manager.execute(self.get(self.edit_item))
        except Exception as e:
            msgbox.showerror("Error", "Can't execute: {exception}".format(exception=e))


    def make_folder(self, event=None):
        name = self.manager.make_folder()
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
        try:
            self.manager.paste()
            self.refresh()
        except Exception as e:
            msgbox.showinfo("Error", "Can't paste: {exception}".format(e))

    def rename(self, event=None):
        if not self.edit_item:
            return
        index = self.edit_item
        text = self.get(index)
        y0 = self.bbox(index)[1]
        entry = tk.Entry(self, borderwidth=0, highlightthickness=0)
        entry.config(font=self.master.master.font) # awful
        entry.config(bg=self.master.master.bg_color)
        entry.config(fg=self.master.master.text_color)
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
        try:
            self.manager.rename(old_data, new_data)
        except Exception as e:
            msgbox.showerror("Error", "Couldn't rename")
        event.widget.destroy()
#        self.edit_item = 0 #self.manager.get_list().index(new_data)
        self.refresh()
