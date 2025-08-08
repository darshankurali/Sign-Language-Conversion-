import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import string
import threading
import json
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import *
import os
import Levenshtein

class VirtualSigner(ShowBase):
    def __init__(self, parent_frame):
        ShowBase.__init__(self)
        self.parent_frame = parent_frame
        self.setup_3d_environment()
        self.load_character()
        self.load_gesture_map()
        self.current_animation = None
        self.animation_queue = []

    def setup_3d_environment(self):
        self.disableMouse()
        self.win = self.open_window()
        self.win.set_clear_color((0.9, 0.9, 0.9, 1))
        self.graphicsEngine.open_windows[0].setParentWindow(int(self.parent_frame.winfo_id()))
        self.cam.setPos(0, -5, 1.5)
        
    def load_character(self):
        self.character = self.loader.loadModel("models/young_male_character.glb")
        self.character.reparentTo(self.render)
        self.character.setScale(0.8)
        self.character.setH(180)
        
        # Load animations
        self.animations = {
            'idle': self.character.actorAnim('idle'),
            **{chr(c): self.load_letter_animation(chr(c)) for c in range(97, 123)},
            **self.load_word_animations()
        }

    def load_letter_animation(self, letter):
        path = f"animations/letters/{letter}.bam"
        return self.loader.loadAnimation(path) if os.path.exists(path) else None

    def load_word_animations(self):
        word_anims = {}
        for word in os.listdir("animations/words"):
            if word.endswith('.bam'):
                word_anims[word[:-4]] = self.loader.loadAnimation(f"animations/words/{word}")
        return word_anims

    def load_gesture_map(self):
        with open("config/gesture_map.json") as f:
            self.gesture_map = json.load(f)

    def find_closest_gesture(self, text):
        words = text.split()
        gestures = []
        for word in words:
            if word in self.animations:
                gestures.append(word)
            else:
                closest = max(self.gesture_map.keys(), 
                            key=lambda x: Levenshtein.ratio(word, x))
                if Levenshtein.ratio(word, closest) > 0.7:
                    gestures.extend(self.gesture_map[closest])
                else:
                    gestures.extend(list(word))
        return gestures

    def play_gesture_sequence(self, text):
        gestures = self.find_closest_gesture(text.lower())
        self.animation_queue.extend(gestures)
        if not self.current_animation:
            self.play_next_gesture()

    def play_next_gesture(self):
        if self.animation_queue:
            gesture = self.animation_queue.pop(0)
            anim = self.animations.get(gesture, self.animations['idle'])
            
            if self.current_animation:
                self.current_anim.stop()
                
            anim.start()
            self.current_animation = anim
            self.accept_once(anim.getAnimControl().getAnimDoneEvent(), 
                           self.play_next_gesture)
        else:
            self.current_animation = None
            self.animations['idle'].loop()

class SignLanguageApp:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
        self.setup_voice_engine()
        self.setup_virtual_signer()

    def setup_ui(self):
        self.root.title("AI Sign Language Interpreter")
        self.root.geometry("1400x800")
        
        # 3D View Frame
        self.p3d_frame = ttk.Frame(self.root, width=800, height=600)
        self.p3d_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
        
        # Control Panel
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=0, column=0, sticky='nw')
        
        self.status_label = ttk.Label(control_frame, text="Status: Ready", font=('Helvetica', 12))
        self.status_label.pack(pady=10)
        
        self.btn_listen = ttk.Button(control_frame, text="Start Listening", command=self.toggle_listening)
        self.btn_listen.pack(pady=5)
        
        self.txt_output = tk.Text(control_frame, width=40, height=15, wrap=tk.WORD)
        self.txt_output.pack(pady=10)

    def setup_virtual_signer(self):
        self.signer = VirtualSigner(self.p3d_frame)

    def setup_voice_engine(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.listening = False
        self.audio_thread = None

    def toggle_listening(self):
        self.listening = not self.listening
        if self.listening:
            self.btn_listen.config(text="Stop Listening")
            self.status_label.config(text="Status: Listening...")
            self.audio_thread = threading.Thread(target=self.listen_loop, daemon=True)
            self.audio_thread.start()
        else:
            self.btn_listen.config(text="Start Listening")
            self.status_label.config(text="Status: Ready")

    def listen_loop(self):
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.listening:
                try:
                    audio = self.recognizer.listen(source, timeout=2, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio).lower()
                    text = text.translate(str.maketrans('', '', string.punctuation))
                    self.process_text(text)
                except (sr.UnknownValueError, sr.WaitTimeoutError):
                    continue

    def process_text(self, text):
        self.root.after(0, self.update_output, text)
        self.root.after(0, self.signer.play_gesture_sequence, text)

    def update_output(self, text):
        self.txt_output.insert('end', f"You: {text}\n")
        self.txt_output.see('end')

if __name__ == "__main__":
    root = tk.Tk()
    app = SignLanguageApp(root)
    root.mainloop()