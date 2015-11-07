import Tkinter as tk
import ttk
import tkSimpleDialog
import os
from sqlalchemy import create_engine
from db_sync_app import App

#mysql://root:pass@192.168.0.23/hServices
#TODO#
#print out for test
#url checking
#settings file

class DB_Select_Dialog(tk.Toplevel):
    
    def __init__(self, parent, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.minsize(900,600)
        if title:
            self.title(title)
        self.parent = parent
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
        self.radio_var = tk.IntVar()
        self.radio_var.set(0)
        self.tns_var = tk.StringVar()        
        
        self.saved_constring_frame = ttk.Frame(master)
        self.saved_constring_frame.rowconfigure(1, weight=1)
        self.saved_constring_frame.columnconfigure(1, weight=1)
        self.con_label = ttk.Label(self.saved_constring_frame, text="Saved Connections") 
        self.saved_connections_list = tk.Listbox(self.saved_constring_frame, selectmode=tk.SINGLE) 
        self.save_button = ttk.Button(self.saved_constring_frame, text="Save", command=self.on_save_connection_string)
        self.delete_button = ttk.Button(self.saved_constring_frame, text="Delete", command=self.on_delete_connection_string)        
        
        self.tns_radio = ttk.Radiobutton(master, text="TNS NAMES", variable=self.radio_var, value=0, command=self.on_select_radio) 
        self.tns_frame = ttk.Frame(master)
        self.tns_select_combo = ttk.Combobox(self.tns_frame, state="readonly", values=App.get_tns_names())
        self.username_label = ttk.Label(self.tns_frame, text="User Name: ")  
        self.pass_label = ttk.Label(self.tns_frame, text="Password: ")
        self.user_name_entry = ttk.Entry(self.tns_frame)
        self.password_entry = ttk.Entry(self.tns_frame, show="*")
        
        self.constring_radio = ttk.Radiobutton(master, text="Connection String", variable=self.radio_var, value=1, command=self.on_select_radio)
        self.constring_entry = ttk.Entry(master)
        
        self.button_frame = ttk.Frame(master)
        self.ok_button = ttk.Button(self.button_frame, text="OK", command=self.ok)
        self.test_button = ttk.Button(self.button_frame, text="Test", command=self.validate)
        self.cancel_button = ttk.Button(self.button_frame, text="Cancel", command = self.cancel)
        
        self.tns_radio.invoke()
        self.saved_connections_list.bind("<Double-1>", self.on_list_double_click)
        master.rowconfigure(4, weight=1)
        master.columnconfigure(0, weight=1)
        indent_pad = 25
        
        #grid into saved constring frame
        self.con_label.             grid(row=0, column=0, padx=x_pad, pady=y_pad, sticky=tk.S+tk.W)
        self.saved_connections_list.grid(row=1, column=0, columnspan=2, padx=x_pad, pady=y_pad, sticky=tk.N+tk.S+tk.E+tk.W)
        self.save_button.           grid(row=2, column=0)
        self.delete_button.         grid(row=2, column=1)
        
        #grid into tns_frame
        self.tns_select_combo.      grid(row=1, column=1, columnspan=4, padx=x_pad, pady=y_pad, sticky=tk.N+tk.W+tk.E)
        self.username_label.        grid(row=2, column=1, padx=x_pad, pady=y_pad, sticky=tk.E)
        self.user_name_entry.       grid(row=2, column=2, padx=x_pad, pady=y_pad, sticky=tk.W)
        self.pass_label.            grid(row=2, column=3, padx=x_pad, pady=y_pad, sticky=tk.W)
        self.password_entry.        grid(row=2, column=4, padx=x_pad, pady=y_pad, sticky=tk.W)
        
        #grid buttons
        self.ok_button.             grid(row=0, column=1, padx=x_pad, pady=y_pad, sticky=tk.N+tk.E)
        self.test_button.           grid(row=0, column=2, padx=x_pad, pady=y_pad, sticky=tk.N+tk.E)
        self.cancel_button.         grid(row=0, column=3, padx=x_pad, pady=y_pad, sticky=tk.N+tk.E)

        
        #grid into Window
        self.tns_radio.             grid(row=0, column=1, padx=x_pad, pady=y_pad, sticky=tk.W)
        self.tns_frame.             grid(row=1, column=1, padx=x_pad, pady=y_pad)
        self.constring_radio.       grid(row=2, column=1, padx=x_pad, pady=y_pad, sticky=tk.N+tk.W)
        self.constring_entry.       grid(row=3, column=1, padx=x_pad * 2, pady=y_pad, sticky=tk.N+tk.E+tk.W)
        self.button_frame.          grid(row=4, column=1, sticky=tk.N+tk.E)
        self.saved_constring_frame. grid(row=0, column=0, rowspan=5 ,sticky=tk.N+tk.S+tk.E+tk.W)
        
        

    def on_select_radio(self, event=None):
        if self.radio_var.get() == 0:
            self.tns_select_combo.configure(state="active")
            self.user_name_entry.configure(state="active")
            self.password_entry.configure(state="active")
            self.constring_entry.configure(state="disabled")
        else:
            self.tns_select_combo.configure(state="disabled")
            self.user_name_entry.configure(state="disabled")
            self.password_entry.configure(state="disabled")
            self.constring_entry.configure(state="active")
    
    def on_save_connection_string(self, event=None):
        con_string,_,_ = self.parse_connection_string()
        self.saved_connections_list.insert(0,con_string)
        
    def on_delete_connection_string(self, event=None):
        if self.saved_connections_list.curselection():
            self.saved_connections_list.delete(self.saved_connections_list.curselection())
        
    def on_list_double_click(self, event=None):
        passwrd = tkSimpleDialog.askstring("Password", "Enter Password: ", show='*')
        if passwrd is not None:
            con_string = self.saved_connections_list.get(tk.ACTIVE).replace("*****", passwrd)
            self.constring_radio.invoke()
            self.constring_entry.delete(0, tk.END)
            self.constring_entry.insert(0, con_string)
        
        
    def parse_connection_string(self):
        con_string = ""
        user_name = ""
        password = ""
        if self.radio_var.get() == 0:
            user_name = self.user_name_entry.get()
            password = self.password_entry.get()
            con_string = "oracle+cx_oracle://" + user_name + ":" + "*****" + "@" + self.tns_select_combo.get()
        else:
            con_string = self.constring_entry.get()
            con_parts = con_string.split(":")
            
            user_name = con_parts[1][2:]
            password = con_parts[2][:con_parts[2].find("@")]
            
            con_parts[2] = "*****" + con_parts[2][con_parts[2].find("@"):]
            con_string = ":".join(con_parts)
            
        return con_string, user_name, password
        
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
        con_string, user_name, password = self.parse_connection_string()
        con_string = con_string.replace("*****", password)
        engine = create_engine(con_string)
        return engine.connect()

    def apply(self):
        con_string, user_name, passwrd = self.parse_connection_string()
        self.result = con_string.replace("*****", passwrd)