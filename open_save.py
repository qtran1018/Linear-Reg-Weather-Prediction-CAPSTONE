import tkinter as tk
from tkinter import filedialog

# def show_notification(title, message):
#     notification.notify(
#         title=title,
#         message=message,
#         app_name='My App',
#         timeout=10  # Duration in seconds
#     )

def open_file_csv():
    # Create a Tk root widget
    root = tk.Tk()
    # Hide the root window
    root.withdraw()
    # Open file dialog and get the file path
    file_path = filedialog.askopenfilename(
        title = "Select a CSV file",
        filetypes = (("CSV", "*.csv"),)
    )
    # Read and print the contents of the file (if needed)
    if file_path:
        print(file_path)
        return file_path 

def open_file_model():
    # Create a Tk root widget
    root = tk.Tk()
    # Hide the root window
    root.withdraw()
    # Open file dialog and get the file path
    file_path = filedialog.askopenfilename(
        title = "Select a model file",
        filetypes = (("PKL", "*.pkl"),)
    )
    # Read and print the contents of the file (if needed)
    if file_path:
        return file_path 

def save_file():
    # Create a Tk root widget
    root = tk.Tk()
    # Hide the root window
    root.withdraw()
    # Open save file dialog and get the file path
    folder_path = filedialog.askdirectory(
        title = "Select a folder to save to",
    )
    # Write content to the selected file (if needed)
    if folder_path:
        return folder_path
