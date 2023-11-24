import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
from db import get_medication_db
from db import get_current_user_email
from db import create_request
from db import get_requests

class RequestRobotPage:
    def __init__(self, root, switch_frame):
        self.root = root
        self.mainframe = tk.Frame(self.root, bg='#333333')
        self.mainframe.pack(expand=True, fill='both')
        self.current_page = 'Request Robot'


        # Navigation Bar-------------------------------------------------------------------------- 
        navbar_frame = tk.Frame(self.mainframe, background='#a0a9de')
        navbar_frame.pack(fill='x')

        buttons = ['Home', 'Request Robot', 'Pending Requests', 'Feedback', 'Config']
        self.nav_buttons = []
        for button_text in buttons:
            button = tk.Button(navbar_frame, text=button_text, command=lambda text=button_text: self.button_click(text, switch_frame), bg='#a0a9de', bd=0)
            button.config(height=4) 
            button.pack(side='left', fill='both', expand=True)
            self.nav_buttons.append(button)
            button.bind("<Enter>", self.on_button_hover)  # hover event
            button.bind("<Leave>", self.on_button_leave)  # leave event
            
        # Update button colors
        for button in self.nav_buttons:
            if button.cget('text') == self.current_page:
                button['background'] = '#8c94c6'
            else:
                button['background'] = '#a0a9de'
                
        # Page Content--------------------------------------------------------------------------
        left_frame = tk.Frame(self.mainframe, width=300, background='#333333')
        left_frame.pack(fill='y', side='left', pady=(100,40), padx=(40,0),expand=True)

        right_frame = tk.Frame(self.mainframe, background='white', width=400)
        right_frame.pack(fill='both', expand=True, side='right', pady=40, padx=40)

        select_destination_label = tk.Label(left_frame, text="Select Destination", background='#333333', foreground='white')
        select_destination_label.grid(row=0,column=0,padx=10, pady=5, sticky='w')

        options = ['Room 1', 'Room 2', 'Room 3'] #todo: hier durch die Orte aus der Datenbank ergänzen.
        self.selected_option = tk.StringVar()
        location_dropdown = ttk.OptionMenu(left_frame, self.selected_option, *options)
        location_dropdown.grid(row=1,column=0,padx=10, sticky='w')

        medication_label = tk.Label(left_frame, text="Select Medication", background='#333333', foreground='white')
        medication_label.grid(row=2,column=0,padx=10, pady=10, sticky='w')

        medication_names, _ = get_medication_db()  # Fetch medication names from the database
        self.medication_var = tk.StringVar()
        self.medication_entry = ttk.OptionMenu(left_frame, self.medication_var,*medication_names)
        self.medication_entry.grid(row=3, column=0, padx=10,sticky='w')

        quantity_label = tk.Label(left_frame, text="Enter Medication Quantity", background='#333333', foreground='white')
        quantity_label.grid(row=4,column=0,padx=10, pady=10, sticky='w')

        self.quantity_entry = ttk.Entry(left_frame, width=24)
        self.quantity_entry.grid(row=5,column=0,padx=10, sticky='w')

        patient_label = tk.Label(left_frame, text="Enter Patient Name", background='#333333', foreground='white')
        patient_label.grid(row=6,column=0,padx=10, pady=10, sticky='w')

        self.patient_entry = ttk.Entry(left_frame, width=24)
        self.patient_entry.grid(row=7,column=0,padx=10, sticky='w')

        confirm_button = tk.Button(left_frame, text="Confirm", background='#4C4273', relief='flat', foreground='white', command=self.show_messagebox, width=15)
        confirm_button.grid(row=8,column=0,padx=10, pady=20, sticky='w')

        #map
        # add map

    def button_click(self, button_text, switch_frame):
        if button_text == 'Request Robot':
            switch_frame('Request Robot')
        elif button_text == 'Home':
            switch_frame('Home')
        elif button_text == 'Pending Requests':
            switch_frame('Pending Requests')      
        elif button_text == "Confirm":
            pass
    
    def on_button_hover(self, event):
        event.widget['background'] = '#8c94c6' 

    def on_button_leave(self, event):
        event.widget['background'] = '#a0a9de' 
        
    def show_messagebox(self):
        destination = self.selected_option.get()
        medication_name = self.medication_var.get()
        medication_quantity = self.quantity_entry.get()
        patient_name = self.patient_entry.get()
        
        # Check if any entry fields are empty
        if not destination or not medication_name or not medication_quantity:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        # who requested?
        else:
            current_user_name = get_current_user_email().split('@')[0]
            
            message = f"Destination: {destination}\nMedication Name: {medication_name}\nMedication Quantity: {medication_quantity}\nPatient Name: {patient_name}\nRequest from user: {current_user_name}"
            
            # create request in db
            create_request(destination,medication_name,medication_quantity,patient_name)
            print(get_requests)
            
            messagebox.showinfo("Confirmation", message)
            
            # clear fields
            self.selected_option.set('')
            self.medication_var.set('')
            self.quantity_entry.delete(0, tk.END)
            self.patient_entry.delete(0, tk.END)
