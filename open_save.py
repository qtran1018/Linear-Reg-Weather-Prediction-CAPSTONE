import tkinter as tk
from tkinter import filedialog

def open_file():
    # Create a Tk root widget
    opener  = tk.Tk()
    # Hide the root window
    opener.withdraw()
    # Open file dialog and get the file path
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("CSV", "*.csv"), ("All files", "*.*"))
    )
    # Read and print the contents of the file (if needed)
    if file_path:
        print(file_path)
        return file_path 

def save_file(b):
    # Create a Tk root widget
    root = tk.Tk()
    # Hide the root window
    root.withdraw()
    # Open save file dialog and get the file path
    file_path = filedialog.asksaveasfilename(
        title="Save file as",
        defaultextension=".pkl",
        filetypes=(("Pickle files", "*.pkl"), ("All files", "*.*"))
    )
    # Print the file path (for demonstration purposes)
    print(f"File will be saved at: {file_path}")

    # Write content to the selected file (if needed)
    if file_path:
        with open(file_path, 'w') as file:
            content = "Hello, this is a sample text to be saved in the file."
            file.write(content)
            print("File saved successfully.")
