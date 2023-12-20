import tkinter as tk
from tkinter import ttk
from db import get_requests_with_status_delivering, get_requests_with_status_delivered, get_current_user_email, update_request_status_to_delivered
from tkinter import messagebox

class FeedbackPage:
    def __init__(self, root, switch_frame):
        self.root = root
        self.mainframe = tk.Frame(self.root, bg='#333333')
        self.mainframe.pack(expand=True, fill='both')
        self.mainframe.columnconfigure(0, weight=1)
        self.switch_frame = switch_frame
        self.current_page = 'Feedback'

        # update every 5 seconds
        self.root.after(5000, self.update_feedback)

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
        self.left_frame = tk.Frame(self.mainframe, width=350, height=400, background='#333333')
        self.right_frame = tk.Frame(self.mainframe)

        self.update_feedback()
        
    # Methods -------------------------------------------------------------------------- 
        
    def update_feedback(self):
        # Get requests for the current user
        active_requests = get_request_delivering_for_current_user()
        finished_requests = get_request_delivered_for_current_user()

        # Remove the existing left frame content
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Create the widgets outside the if condition
            
        # manually set status to delivered
        self.test_button = tk.Button(self.left_frame, text="set status to delivered", background='yellow', relief='flat', foreground='black', width=20, command=lambda: test(self,active_requests[0]))
        self.test_button.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.select_title_label = tk.Label(self.left_frame, text="Order Summary", background='#333333', foreground='white')
        self.select_title_label.config(font=("TkDefaultFont", 12, "bold"))
        
        self.medication_label = tk.Label(self.left_frame, text="Medication", background='#333333', foreground='white')
        self.quantity_label = tk.Label(self.left_frame, text="Quantity", background='#333333', foreground='white')
        self.location_label = tk.Label(self.left_frame, text="Location", background='#333333', foreground='white')
        self.patient_label = tk.Label(self.left_frame, text="Patient", background='#333333', foreground='white')
        self.status_label = tk.Label(self.left_frame, text="Status: currently delivering..", background='#333333', foreground='white')

        self.order_received_button = tk.Button(self.left_frame, text="Order received", background='#4C4273', relief='flat', foreground='white', width=15, command=lambda: self.show_messagebox())
        self.order_missing_button = tk.Button(self.left_frame, text="Order missing", background='#E83C3C', relief='flat', foreground='white', width=15)

        if active_requests:
            # populate the left frame with current_order
            self.select_title_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
            self.medication_label.grid(row=1,column=0,padx=10, pady=(5,0), sticky='w')
            self.quantity_label.grid(row=2,column=0,padx=10, pady=(5,0), sticky='w')
            self.location_label.grid(row=3,column=0,padx=10, pady=(5,0), sticky='w')
            self.patient_label.grid(row=4,column=0,padx=10, pady=(5,0), sticky='w')
            self.status_label.grid(row=5,column=0,padx=10, pady=30, sticky='w')
            
            update_labels(self,active_requests[0])

                 
        elif finished_requests:
            self.select_title_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
            self.medication_label.grid(row=1,column=0,padx=10, pady=(5,0), sticky='w')
            self.quantity_label.grid(row=2,column=0,padx=10, pady=(5,0), sticky='w')
            self.location_label.grid(row=3,column=0,padx=10, pady=(5,0), sticky='w')
            self.patient_label.grid(row=4,column=0,padx=10, pady=(5,0), sticky='w')
            self.status_label.grid(row=5,column=0,padx=10, pady=30, sticky='w')

            self.order_received_button.grid(row=6,column=0,padx=10, pady=(5,0), sticky='w')
            self.order_missing_button.grid(row=7,column=0,padx=10, pady=(5,0), sticky='w')
            self.status_label.config(text='Status: delivered')

            update_labels(self,finished_requests[0])

        # if no requests are being worked on
        else:
            empty_label = tk.Label(self.left_frame, text="None of your orders are currently delivering.", background='#333333', foreground='white')
            empty_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
                        
        self.left_frame.pack(fill='both', side='left', pady=60, padx=(60, 0))

        # next update after 5 seconds
        self.root.after(5000, self.update_feedback)

    def button_click(button_text, switch_frame):
                if button_text == 'Request Robot':
                    switch_frame('Request Robot')
                elif button_text == 'Home':
                    switch_frame('Home')
                elif button_text == 'Pending Requests':
                    switch_frame('Pending Requests')     
                elif button_text == 'Feedback':
                    switch_frame('Feedback')   
                elif button_text == "Confirm":
                    pass
            
    def on_button_hover(self, event):
            event.widget['background'] = '#8c94c6' 

    def on_button_leave(self, event):
            event.widget['background'] = '#a0a9de' 

    def show_messagebox(self):
        self.switch_frame("Home")   
        messagebox.showinfo("Confirmation", "Order delivered successfully.")


def test(self, request):
        update_request_status_to_delivered(request)

def get_request_delivering_for_current_user():
        current_user = get_current_user_email()
        user_requests_delivering = get_requests_with_status_delivering(current_user)
        return user_requests_delivering

def get_request_delivered_for_current_user():
        current_user = get_current_user_email()
        user_requests_delivered = get_requests_with_status_delivered(current_user)
        return user_requests_delivered

                
def update_labels(self, request):
                self.medication_label["text"] = f"{request.med_name}"
                self.quantity_label["text"] = f"{request.quantity}"
                self.location_label["text"] = f"{request.location}"
                self.patient_label["text"] = f"{request.patientName}"
                    
                # show currently processed order



        