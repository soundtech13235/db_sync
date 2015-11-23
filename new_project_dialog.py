import Tkinter as tk
import ttk
import tkSimpleDialog
import os



class NewProjectDialog(tk.Toplevel):
    
    def __init__(self, parent, config, title = None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.minsize(900,600)
        if title:
            self.title(title)
        self.parent = parent
        self.config = config
        self.result = None
        body = ttk.Frame(self)
        self.initial_focus = self.construct_body(body)
        body.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.grab_set()
        if not self.initial_focus:
            self.initial_focus = self
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))                         
        self.initial_focus.focus_set()
        self.wait_window(self)

    # construction hooks

    def construct_body(self, master):
        x_pad = 5
        y_pad = 5

    
    def load_config(self, list_box):
        pass
            
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return
        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    def validate(self):    
        return 1

    def apply(self):
        pass