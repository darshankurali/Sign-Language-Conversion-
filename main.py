#main.py
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk  
from sign_to_text_and_voice import Application
import vts2

is_exiting = False

def run_voice_to_sign():
    global is_exiting
    root.destroy()  # Close the current UI

    if not is_exiting:  # Only run Application if not exiting
        vts2.func()
        open_main_ui()  # Reopen the main UI

def run_sign_to_text():
    global is_exiting
    root.destroy()  # Close the current UI

    if not is_exiting:  # Only run Application if not exiting
        app = Application()  # Create an instance of Application
        app.run()  # Start the Application
        open_main_ui()  # Reopen the main UI

def exit_program():
    """Exit the program completely."""
    global is_exiting
    is_exiting = True  # Set the flag to indicate the program is exiting
    root.destroy()  # Destroy the current UI
    
def open_main_ui():
    
    def resize_bg(event):
        """Resize background image to fit the window dynamically."""
        new_width = event.width
        new_height = event.height
        resized_image = bg_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        updated_photo = ImageTk.PhotoImage(resized_image)
        bg_label.config(image=updated_photo)
        bg_label.image = updated_photo
        
    # Initialize the main window
    global root
    root = tk.Tk()
    root.title("Gesture and Voice Interpreter")
    root.geometry("1920x1080")  # Set the window size

    # Load and set the background image
    bg_image = Image.open("kashish.png")  # Replace with your image file path
    bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)  # Resize to fit the window
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a label for the background image
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Define custom fonts for styling
    title_font = font.Font(family="Helvetica", size=26, weight="bold")
    button_font = font.Font(family="Helvetica", size=22, weight="bold")

    # Title Label
    title_label = tk.Label(
        root,
        text="Gesture and Voice Interpreter",
        font=title_font,
        bg="#4E6984",
        fg="black",
    )
    title_label.pack(pady=30)  # Add spacing above and below the label

    # Instruction Label
    instruction_label = tk.Label(
        root,
        text="Select an option below:",
        font=("Helvetica", 20),
        bg="#4E6984",
        fg="black",
    )
    instruction_label.pack(pady=10)

    def on_enter(e):
        e.widget.config(bg="#c0c0c0", fg="white")  # Darken background, change text color to white

    def on_leave(e):
        e.widget.config(bg="#e0e0e0", fg="black")  # Restore original background and text color

    # Buttons for each option
    button1 = tk.Button(
        root,
        text="Sign Language to Text and Voice",
        command=run_sign_to_text,
        font=button_font,
        bg="#e0e0e0",  # Light gray background
        fg="black",
        activebackground="#c0c0c0",  # Slightly darker gray for active state
        activeforeground="black",
        bd=2,  # Add a border for a defined look
        highlightthickness=2,  # Add button outline
        highlightbackground="#808080",  # Gray outline color
    )
    button1.bind("<Enter>", on_enter)  # Bind hover event
    button1.bind("<Leave>", on_leave)  # Bind leave event
    #button1.place(x=50, y=150)
    button1.pack(pady=15)


    button2 = tk.Button(
        root,
        text="Voice to Sign Language",
        command=run_voice_to_sign,
        font=button_font,
        bg="#e0e0e0",  # Light gray background
        fg="black",
        activebackground="#c0c0c0",  # Slightly darker gray for active state
        activeforeground="black",
        bd=2,  # Add a border for a defined look
        highlightthickness=2,  # Add button outline
        highlightbackground="#808080",  # Gray outline color
    )
    button2.bind("<Enter>", on_enter)  # Bind hover event
    button2.bind("<Leave>", on_leave)  # Bind leave event
    button2.pack(pady=15)


    button_exit = tk.Button(
        root,
        text="Exit",
        command=exit_program,
        font=button_font,
        bg="#e0e0e0",  # Light gray background
        fg="black",
        activebackground="#c0c0c0",  # Slightly darker gray for active state
        activeforeground="black",
        bd=2,  # Add a border for a defined look
        highlightthickness=2,  # Add button outline
        highlightbackground="#808080",  # Gray outline color
    )
    button_exit.bind("<Enter>", on_enter)  # Bind hover event
    button_exit.bind("<Leave>", on_leave)  # Bind leave event
    button_exit.pack(pady=30)


    # Start the Tkinter event loop TF_ENABLE_ONEDNN_OPTScl
    root.mainloop()

open_main_ui()