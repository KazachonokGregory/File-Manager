import tkinter as tk

class PopupMenu(tk.Menu):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def popup(self, event):
        self.event = event
        try:
            self.post(event.x_root, event.y_root)
            self.focus_set()
        finally:
            self.grab_release()

    def popup_remove(self, event):
        self.unpost()

