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
                im.seek(len(self.frames))
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
        self.after(self.frame_delay, self.next_frame)

def func():
    gif_folder = "ISL_Gifs"  # Folder containing GIFs
    letter_folder = "ISL_letters"  # Folder containing JPG images for letters
    previous_inputs = []
    is_listening = threading.Event()
    listening_flag = False

    # Preload GIFs
    preloaded_gifs = {
        os.path.splitext(f)[0]: os.path.join(gif_folder, f)
        for f in os.listdir(gif_folder) if f.endswith('.gif')
    }

    # Preload letter images
    preloaded_letters = {
        letter: os.path.join(letter_folder, f"{letter}.jpg")
        for letter in string.ascii_lowercase
    }

    root = tk.Tk()
    root.title("Voice to Sign Language Interpreter")
    root.geometry("1900x1080")
    root.configure(bg="lightblue")

    status_label = tk.Label(root, text="Say Something..", font=("Helvetica", 18), bg="lightblue")
    status_label.place(x=20, y=20)

    said_label = tk.Label(root, text="You said: ", font=("Helvetica", 16), bg="lightblue", wraplength=350, justify="left")
    said_label.place(x=20, y=100)

    gif_frame = tk.Frame(root, bg="lightblue")
    gif_frame.place(x=400, y=50, width=1000, height=800)

    displayed_elements = []  # Store displayed elements (GIFs and letter images)

    def update_history(text):
        """Update the previous inputs display."""
        previous_inputs.append(text)
        if len(previous_inputs) > 15:
            previous_inputs.pop(0)
        said_label.config(text="You said:\n" + "\n".join(previous_inputs))

    def clear_display():
        """Remove all previous displayed elements (GIFs and letter images)."""
        for widget in gif_frame.winfo_children():
            widget.destroy()
        displayed_elements.clear()

    def display_gifs_and_letters_in_batches(ordered_content, index=0):
        """Display two elements at a time (GIFs or letter images), then replace them after a delay."""
        if index >= len(ordered_content):
            return  # Stop if all content is displayed

        # Clear previous display
        clear_display()

        # Show the next batch of 2 elements
        batch = ordered_content[index:index + 2]
        for item in batch:
            if isinstance(item, tuple):  # GIF case
                gif_label = ImageLabel(gif_frame, frame_delay=100, bg="lightblue")
                gif_label.pack(side="top", padx=10, pady=10)
                gif_label.load(item[1])
                displayed_elements.append(gif_label)
            else:  # Letter images case (display word as a row of letters)
                word_frame = tk.Frame(gif_frame, bg="lightblue")
                word_frame.pack(side="top", pady=10)

                # Display the word as a label
                word_label = tk.Label(word_frame, text=item, font=("Helvetica", 16), bg="lightblue")
                word_label.pack(side="top", pady=5)
                
                # Display each letter in the word
                for letter in item:
                    if letter in preloaded_letters:
                        letter_img = Image.open(preloaded_letters[letter])
                        letter_img = letter_img.resize((50, 50))  # Resize letter images
                        letter_photo = ImageTk.PhotoImage(letter_img)
                        letter_label = tk.Label(word_frame, image=letter_photo, bg="lightblue")
                        letter_label.image = letter_photo  # Keep reference
                        letter_label.pack(side="left", padx=2)
                        displayed_elements.append(letter_label)

        # Schedule next batch after 3 seconds
        root.after(3000, lambda: display_gifs_and_letters_in_batches(ordered_content, index + 2))

        # If it's the last batch, schedule the end display removal after an additional delay (e.g., 5 seconds)
        if index + 2 >= len(ordered_content):
            root.after(5000, clear_display)

    def process_audio():
        nonlocal is_listening, listening_flag
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                status_label.config(text="I am listening...")
                root.update_idletasks()
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
                text = r.recognize_google(audio).lower()
                text = text.translate(str.maketrans('', '', string.punctuation))
                print(f"Recognized Text: {text}")
                update_history(text)
                phrases = text.split()

                ordered_content = []
                i = 0
                while i < len(phrases):
                    matched = False
                    for j in range(len(phrases), i, -1):
                        combined_phrase = " ".join(phrases[i:j])
                        gif_path = preloaded_gifs.get(combined_phrase)
                        if gif_path:
                            ordered_content.append((combined_phrase, gif_path))  # Store GIFs
                            i = j
                            matched = True
                            break
                    if not matched:
                        ordered_content.append(phrases[i])  # Store words as letter images
                        i += 1
                
                # Display GIFs and letter images in batches of 2
                display_gifs_and_letters_in_batches(ordered_content)

        except sr.UnknownValueError:
            update_history("Could not understand (retry)")
        except sr.WaitTimeoutError:
            update_history("No speech detected. Please try again.")
        except Exception as e:
            update_history(f"Error: {str(e)}")
        finally:
            is_listening.clear()
            status_label.config(text="Say Something..")
            listen_button.config(text="Start Listening")

    def toggle_listening():
        nonlocal listening_flag
        if listening_flag:
            listening_flag = False
            status_label.config(text="Stopped listening.")
            is_listening.clear()
            listen_button.config(text="Start Listening")
        else:
            listening_flag = True
            is_listening.set()
            threading.Thread(target=process_audio, daemon=True).start()
            listen_button.config(text="Stop Listening")

    listen_button = tk.Button(
        root,
        text="Start Listening",
        font=("Helvetica", 16),
        bg="#4CAF50",
        fg="white",
        command=toggle_listening,
    )
    listen_button.place(x=10, y=700)
    root.mainloop()

# Uncomment this to run
func()
