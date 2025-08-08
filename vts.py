import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
from itertools import count
import threading
import string

# Define the ImageLabel class for GIF animation
class ImageLabel(tk.Label):
    """A label that displays images and plays them if they are GIFs."""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

# Speech-to-text function with UI
def func():
    # Create a list of available GIF keywords
    isl_gif = ['address', 'ahemdabad', 'all', 'any question', 'any questions', 'are you angry', 'are you busy', 'assam', 'august', 'banana', 'banaras', 'banglore', 'be careful', 'beautiful', 'best friends', 'bestfriends', 'brave', 'breakfast', 'bridge', 'bye', 'can i borrow that', 'cat', 'christmas', 'church', 'cilinic', 'dasara', 'december', 'did you finish homework', 'dinner', 'do you have money', 'do you want something to drink', 'do you watch TV', 'dont worry', 'eager', 'eat', 'enjoy', 'every day', 'every week', 'excited', 'flower is beautiful', 'friday', 'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'grapes', 'hello', 'hindu', 'hour', 'hungry', 'hyderabad', 'i am a clerk', 'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont know', 'i dont understand', 'i go to a theatre', 'i had to say something but I forgot', 'i know', 'i like pink colour', 'i love to shop', 'i understand', 'job', 'july', 'june', 'karnataka', 'kerala', 'krishna', 'lets go for lunch', 'love', 'lunch', 'mango', 'may', 'mile', 'monday', 'mumbai', 'nagpur', 'nice to meet you', 'no', 'open the door', 'pakistan', 'please call me later', 'please repeat', 'please wait for sometime', 'police station', 'post office', 'pune', 'punjab', 'relieved', 'saturday', 'second', 'seriously', 'shall I help you', 'shall we go together tommorow', 'shop', 'shy', 'sign language interpreter', 'sit down', 'stand up', 'sunday', 'take care', 'temple', 'there was traffic jam', 'thirsty', 'thursday', 'today', 'toilet', 'tomato', 'tomorrow', 'tuesday', 'usa', 'village', 'wednesday', 'weekend', 'what are you doing', 'what is the problem', 'what is the weather like', 'what is todays date', 'what is your father do', 'what is your mobile number', 'what is your name', 'whats for lunch', 'whats up', 'whats wrong', 'where is the bathroom', 'where is the police station', 'you are wrong']  # Example GIFs

    # List to store recognized phrases
    previous_inputs = []
    is_listening = threading.Event()  # Event to track if recognition is in progress

    # Tkinter GUI Setup
    root = tk.Tk()
    root.title("Voice to Sign Language Interpreter")
    root.geometry("1900x1080")
    root.configure(bg="lightblue")

    # Labels for "Say something", "I am listening", and "You said"
    status_label = tk.Label(root, text="Say something...", font=("Helvetica", 18), bg="lightblue")
    status_label.place(x=20, y=20)

    said_label = tk.Label(root, text="You said: ", font=("Helvetica", 16), bg="lightblue", wraplength=350, justify="left")
    said_label.place(x=20, y=100)

    # Image/GIF Display Area
    gif_label = ImageLabel(root, bg="lightblue")
    gif_label.place(x=400, y=150, width=800, height=800)

    def update_history(text, gif_available=True):
        """Update the previous inputs display."""
        if not gif_available:
            text = f"{text} (No GIF available)"  # Append feedback for missing GIF
        previous_inputs.append(text)  # Add new input to the list
        if len(previous_inputs) > 15:  # Keep the last 15 entries
            previous_inputs.pop(0)
        # Display all previous inputs
        said_label.config(text="You said:\n" + "\n".join(previous_inputs))

    def process_audio():
        """Process audio input and update UI."""
        nonlocal is_listening
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                status_label.config(text="I am listening...")
                root.update_idletasks()
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

                # Recognize speech
                text = r.recognize_google(audio).lower()
                for c in string.punctuation:
                    text = text.replace(c, "")

                # Display the corresponding GIF or feedback
                if text in ["bye", "goodbye", "bye-bye", "bye bye"]:
                    gif_path = 'ISL_Gifs/bye.gif'  # Ensure the 'bye.gif' file exists
                    gif_label.load(gif_path)
                    status_label.config(text="Goodbye!")
                    update_history(text, gif_available=True)
                    root.update()  # Update the interface to display changes
                    root.after(4000, root.destroy)  # Wait 4 seconds, then close
                    return

                if text in isl_gif:
                    gif_path = f'ISL_Gifs/{text}.gif'  # Adjust path as needed
                    gif_label.load(gif_path)
                    update_history(text, gif_available=True)
                else:
                    gif_label.unload()  # Clear any displayed GIF
                    update_history(text, gif_available=False)  # No GIF available feedback

        except sr.UnknownValueError:
            update_history("Could not understand (retry)")
            gif_label.unload()

        except Exception as e:
            update_history(f"Error: {str(e)}", gif_available=False)
            gif_label.unload()

        finally:
            is_listening.clear()  # Indicate that listening is complete
            status_label.config(text="Say something...")

    def listen_and_process():
        """Trigger audio processing only if not already listening."""
        if not is_listening.is_set():
            is_listening.set()  # Mark that recognition is in progress
            threading.Thread(target=process_audio, daemon=True).start()

        # Schedule the next check after 2 seconds
        root.after(2000, listen_and_process)

    # Start listening after 2 seconds
    root.after(2000, listen_and_process)
    root.mainloop()

# Run the function
#func()
