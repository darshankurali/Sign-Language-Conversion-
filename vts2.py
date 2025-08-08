import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
import threading
import string
import os


class ImageLabel(tk.Label):
    """A label that displays images and plays them if they are GIFs."""
    def __init__(self, master=None, frame_delay=100, **kwargs):
        super().__init__(master, **kwargs)
        self.frames = []  # Store frames of the GIF
        self.frame_index = 0  # Keep track of the current frame
        self.running = False  # Track if animation is running
        self.frame_delay = frame_delay  # Fixed frame delay in milliseconds

    def load(self, im):
        """Load a GIF and prepare for animation."""
        if isinstance(im, str):
            im = Image.open(im)
        self.frames = []

        try:
            while True:
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(len(self.frames))  # Move to the next frame
        except EOFError:
            pass

        if self.frames:
            self.config(image=self.frames[0])
        self.frame_index = 0
        self.running = True

        if len(self.frames) > 1:
            self.next_frame()

    def unload(self):
        """Stop the animation and clear the image."""
        self.running = False
        self.config(image=None)
        self.frames = []
        self.frame_index = 0

    def next_frame(self):
        """Show the next frame at a fixed speed."""
        if not self.running or not self.frames:
            return

        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.config(image=self.frames[self.frame_index])
        self.after(self.frame_delay, self.next_frame)  # Use consistent frame delay


def func():
    gif_folder = "ISL_Gifs"  # Folder containing all GIFs
    previous_inputs = []
    is_listening = threading.Event()  # Event to track if recognition is in progress
    listening_flag = False  # Flag to track listening status

    # Preload GIFs into memory
    preloaded_gifs = {
        os.path.splitext(f)[0]: os.path.join(gif_folder, f)
        for f in os.listdir(gif_folder) if f.endswith('.gif')
    }

    # Tkinter GUI Setup
    root = tk.Tk()
    root.title("Voice to Sign Language Interpreter")
    root.geometry("1900x1080")
    root.configure(bg="lightblue")

    # Labels for "Say something", "I am listening", and "You said"
    status_label = tk.Label(root, text="Say Something..", font=("Helvetica", 18), bg="lightblue")
    status_label.place(x=20, y=20)

    said_label = tk.Label(root, text="You said: ", font=("Helvetica", 16), bg="lightblue", wraplength=350, justify="left")
    said_label.place(x=20, y=100)

    # Frame for GIFs (vertical arrangement)
    gif_frame = tk.Frame(root, bg="lightblue")
    gif_frame.place(x=400, y=50, width=1000, height=800)

    displayed_gifs = []  # List to track displayed GIF widgets

    def update_history(text, gif_available=True):
        """Update the previous inputs display."""
        if not gif_available:
            text = f"{text} (No GIF available)"  # Append feedback for missing GIF
        previous_inputs.append(text)  # Add new input to the list
        if len(previous_inputs) > 15:  # Keep the last 15 entries
            previous_inputs.pop(0)
        # Display all previous inputs
        said_label.config(text="You said:\n" + "\n".join(previous_inputs))

    def unload_all_gifs():
        """Unload all GIFs at the same time."""
        for gif_label in displayed_gifs:
            gif_label.unload()
        displayed_gifs.clear()  # Clear the list of displayed GIFs

    def display_gifs_in_batches(matched_phrases):
        """Display GIFs in batches of 2 with a delay of 2 seconds."""
        def show_batch(batch):
            # Clear previous GIFs
            for widget in gif_frame.winfo_children():
                widget.destroy()
            displayed_gifs.clear()  # Reset displayed GIFs

            # Display each GIF in the current batch
            for idx, (phrase, gif_path) in enumerate(batch):
                row_frame = tk.Frame(gif_frame, bg="lightblue")  # Create a row for each GIF
                row_frame.pack(fill="both", pady=10)

                gif_label = ImageLabel(row_frame, frame_delay=100, bg="lightblue")
                gif_label.pack(side="top", padx=10)
                gif_label.load(gif_path)
                displayed_gifs.append(gif_label)

            # Schedule unloading of all GIFs after two cycles
            root.after(len(displayed_gifs) * 4000, unload_all_gifs)

        # Process batches of 2 GIFs
        for i in range(0, len(matched_phrases), 2):
            batch = matched_phrases[i:i + 2]
            root.after(i * 2000, lambda b=batch: show_batch(b))  # Schedule batch display

    def process_audio():
        """Process audio input and update UI."""
        nonlocal is_listening, listening_flag
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                status_label.config(text="I am listening...")
                root.update_idletasks()

                # Adjust for ambient noise with reduced duration
                r.adjust_for_ambient_noise(source, duration=0.5)

                # Listen with a shorter timeout and phrase time limit
                audio = r.listen(source, timeout=10, phrase_time_limit=10)

                # Recognize speech
                text = r.recognize_google(audio).lower()
                text = text.translate(str.maketrans('', '', string.punctuation))

                phrases = text.split()
                print(f"Recognized Phrases: {phrases}")

                # Match phrases to preloaded GIFs
                matched_phrases = []
                i = 0
                while i < len(phrases):
                    matched = False
                    for j in range(len(phrases), i, -1):
                        combined_phrase = " ".join(phrases[i:j])
                        gif_path = preloaded_gifs.get(combined_phrase)
                        if gif_path:
                            matched_phrases.append((combined_phrase, gif_path))
                            i = j
                            matched = True
                            break
                    if not matched:
                        i += 1

                # Display matched GIFs or show "not found" feedback
                if matched_phrases:
                    display_gifs_in_batches(matched_phrases)
                    for phrase, _ in matched_phrases:
                        update_history(phrase, gif_available=True)
                else:
                    update_history(text, gif_available=False)

        except sr.UnknownValueError:
            update_history("Could not understand (retry)")

        except sr.WaitTimeoutError:
            update_history("No speech detected. Please try again.", gif_available=False)

        except Exception as e:
            update_history(f"Error: {str(e)}", gif_available=False)

        finally:
            is_listening.clear()
            status_label.config(text="Say Something..")
            listen_button.config(text="Start Listening")  # Ensure button resets

    def toggle_listening():
        """Toggle listening when the button is clicked."""
        nonlocal listening_flag
        if listening_flag:
            listening_flag = False
            status_label.config(text="Stopped listening.")
            is_listening.clear()  # Stop listening
            listen_button.config(text="Start Listening")  # Update button text
        else:
            listening_flag = True
            is_listening.set()  # Start listening
            threading.Thread(target=process_audio, daemon=True).start()
            listen_button.config(text="Stop Listening")  # Update button text

    # Button to toggle listening
    listen_button = tk.Button(
        root,
        text="Start Listening",
        font=("Helvetica", 16),
        bg="#4CAF50",
        fg="white",
        command=toggle_listening,  # Call toggle_listening when button is clicked
    )
    listen_button.place(x=10, y=700)

    root.mainloop()


# Run the function
#func()
