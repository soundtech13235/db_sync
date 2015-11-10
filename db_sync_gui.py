import Tkinter as tk
import ttk
import ConfigParser, os
from db_select_dialog import DB_Select_Dialog
from db_sync_app import App
class GUI(ttk.Frame):
    x_pad = 5
    y_pad = 5
    def __init__(self, root_window):
        ttk.Frame.__init__(self, root_window)
        self.config = self.open_config()
        connection_dialog = DB_Select_Dialog(root_window, self.config)
        self.app = App(connection_dialog.result)
        self.master = root_window
        self.master.minsize(900,500)
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.gridDBSelect()
        self.gridEditArea()
        self.gridButtons()
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def gridDBSelect(self):
        self.side_bar = ttk.Frame(self, borderwidth=1, relief=tk.GROOVE)
        self.side_bar.rowconfigure(1, weight=1)
 
        db_names = self.app.get_tns_names()
        
        ttk.Label(self.side_bar, text="Database Alias:").grid(row=0,column=0)
        self.db_combobox = ttk.Combobox(self.side_bar, values=db_names, state="readonly")
        self.db_combobox.grid(row=0, column=1, sticky=tk.E+tk.W, padx = self.x_pad, pady = self.y_pad)
            
        self.db_objects_treeview = ttk.Treeview(self.side_bar)
        self.db_objects_treeview.bind("<<TreeviewSelect>>", self.on_tree_click)
        tables = self.app.get_table_objects()
        for table in tables:
            self.db_objects_treeview.insert("", 1, text=table)
        
        self.db_objects_treeview.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S, padx = self.x_pad, pady = self.y_pad)
        self.side_bar.grid(row=0, column=0, rowspan=1, sticky=tk.N+tk.S+tk.W, padx = self.x_pad, pady = self.y_pad)
        
    def open_config(self):
        config = ConfigParser.ConfigParser()
        with open('config.cfg', 'rb') as file:
            config.readfp(file)
        
        if not config.has_section("connections"):
            config.add_section("connections")
        if not config.has_option("connections", "saved"):
            config.set("connections", "saved", "")
        return config
        
    def gridEditArea(self):
        self.ddl_text = tk.Text(self, relief=tk.GROOVE)
        self.ddl_text.grid(row=0, column=1, sticky=tk.N+tk.S+tk.W+tk.E, padx = self.x_pad, pady = self.y_pad)
        
    def gridButtons(self):
        self.quit = ttk.Button(self, text='Quit', command=self.on_close)
        self.quit.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
    def on_tree_click(self, event):
        clicked_item = self.db_objects_treeview.focus()
        
        if self.db_objects_treeview.get_children(clicked_item):
            pass
        else:
            text = self.app.get_ddl(self.db_objects_treeview.item(clicked_item, "text"))
            self.ddl_text.delete("0.0", tk.END)
            self.ddl_text.insert("0.0", text)
        
    def run(self):
        self.master.mainloop()       
        
    def on_close(self):
        with open('config.cfg','wb') as file:
            self.config.write(file)
        self.master.destroy()
        