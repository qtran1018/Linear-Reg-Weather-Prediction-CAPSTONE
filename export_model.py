import linear_model_maker
import joblib
import os
import tkinter as tk
from tkinter import messagebox

def show_message(popup_message):
    # Create a Tk root widget
    root = tk.Tk()
    # Hide the root window
    root.withdraw()
    # Display a message box
    messagebox.showinfo(
        title="Information",
        message=popup_message
    )

def export_model(save_loc,data_loc):
    location = save_loc
    model = linear_model_maker.make_model(data_loc)
    filepath = os.path.join(location,'weather_model.pkl')
    joblib.dump(model,filepath)
    show_message("Model has been saved.")