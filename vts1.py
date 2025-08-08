import tkinter as tk
from PIL import Image, ImageTk
import speech_recognition as sr
from itertools import count
import threading
import string

class ImageLabel(tk.Label):
    """A label that displays images and plays them if they are GIFs."""
    def load(self, im, fixed_delay=100):
        """Load a GIF with a fixed frame delay for uniform speed."""
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        
        try:
            # Extract frames from the GIF
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass  # End of frames

        # Override the delay value for a consistent playback speed
        self.delay = fixed_delay  # Set a fixed delay (100ms) for all GIFs

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        """Unload the current GIF and clear the display."""
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        """Display the next frame with a fixed delay."""
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)  # Use the fixed delay for all frames



def func():
    isl_gif =['address', 'ahemdabad', 'all', 'any question', 'any questions', 'are you angry', 'are you busy', 'assam', 'august', 'banana', 'banaras', 'banglore', 'be careful', 'beautiful', 'best friends', 'bestfriends', 'brave', 'breakfast', 'bridge', 'bye', 'can i borrow that', 'cat', 'christmas', 'church', 'cilinic', 'dasara', 'december', 'did you finish homework', 'dinner', 'do you have money', 'do you want something to drink', 'do you watch TV', 'dont worry', 'eager', 'eat', 'enjoy', 'every day', 'every week', 'excited', 'flower is beautiful', 'friday', 'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'grapes', 'hello', 'hindu', 'hour', 'how are you doing', 'how are you', 'hungry', 'hyderabad', 'i am a clerk', 'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont know', 'i dont understand', 'i go to a theatre', 'i had to say something but I forgot', 'i know', 'i like pink colour', 'i love to shop', 'i understand', 'job', 'july', 'june', 'karnataka', 'kerala', 'krishna', 'lets go for lunch', 'love', 'lunch', 'mango', 'may', 'mile', 'monday', 'mumbai', 'nagpur', 'nice to meet you', 'no', 'open the door', 'pakistan', 'please call me later', 'please repeat', 'please wait for sometime', 'police station', 'post office', 'pune', 'punjab', 'relieved', 'saturday', 'second', 'seriously', 'shall I help you', 'shall we go together tommorow', 'shop', 'shy', 'sign language interpreter', 'sit down', 'stand up', 'sunday', 'take care', 'temple', 'there was traffic jam', 'thirsty', 'thursday', 'today', 'toilet', 'tomato', 'tomorrow', 'tuesday', 'usa', 'village', 'wednesday', 'weekend', 'what are you doing', 'what is the problem', 'what is the weather like', 'what is todays date', 'what is your father do', 'what is your mobile number', 'what is your name', 'what time is it', 'what', 'whats for lunch', 'whats up', 'whats wrong', 'where is the bathroom', 'where is the police station', 'you are wrong']  # Add more keywords as needed
    previous_inputs = []
    is_listening = threading.Event()

    root = tk.Tk()
    root.title("Voice to Sign Language Interpreter")
    root.geometry("1000x600")
    root.configure(bg="lightblue")

    # Labels for status and history
    status_label = tk.Label(root, text="Say something...", font=("Helvetica", 18), bg="lightblue", anchor="w", justify="left")
    status_label.place(x=20, y=20, width=400)

    said_label = tk.Label(root, text="You said: ", font=("Helvetica", 16), bg="lightblue", wraplength=350, anchor="w", justify="left")
    said_label.place(x=20, y=60, width=400)

    gif_label = ImageLabel(root, bg="lightblue")
    gif_label.place(x=450, y=50, width=500, height=500)

    def update_history(text, gif_available=True):
        if not gif_available:
            text = f"{text} (No GIF available)"
        previous_inputs.append(text)
        if len(previous_inputs) > 15:
            previous_inputs.pop(0)
        said_label.config(text="You said:\n" + "\n".join(previous_inputs))
        

    def process_audio():
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                status_label.config(text="Listening...")
                r.dynamic_energy_threshold = True
                r.energy_threshold = 300
                audio = r.listen(source, timeout=1, phrase_time_limit=2)
                text = r.recognize_google(audio).lower()
                text = text.translate(str.maketrans('', '', string.punctuation))

                gif_path = f'ISL_Gifs/{text}.gif'
                if text in isl_gif:
                    try:
                        gif_label.load(gif_path, fixed_delay=100)  # Force uniform speed for all GIFs
                        update_history(text)
                    except FileNotFoundError:
                        gif_label.unload()
                        update_history(f"{text} (GIF missing)", gif_available=False)
                else:
                    gif_label.unload()
                    update_history(text, gif_available=False)
        except sr.WaitTimeoutError:
            update_history("Listening timeout. Please try again.", gif_available=False)
        except sr.UnknownValueError:
            update_history("Could not understand. Please try again.", gif_available=False)
        except Exception as e:
            update_history(f"Error: {str(e)}", gif_available=False)
        finally:
            is_listening.clear()
            status_label.config(text="Say something...")
            if is_listening.is_set():  # Restart listening if still active
                threading.Thread(target=process_audio, daemon=True).start()

    def toggle_listening():
        if is_listening.is_set():
            # Stop Listening
            is_listening.clear()
            start_stop_button.config(text="Start Listening")
            status_label.config(text="Listening stopped.")
        else:
            # Start Listening
            is_listening.set()
            start_stop_button.config(text="Stop Listening")
            threading.Thread(target=process_audio, daemon=True).start()

    # Start/Stop Button
    start_stop_button = tk.Button(root, text="Start Listening", font=("Helvetica", 16), command=toggle_listening)
    start_stop_button.place(x=20, y=700, width=200)

    root.mainloop()

func()
