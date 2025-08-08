import cv2
import numpy as np
import pytesseract
import pyautogui
import tkinter as tk
from tkinter import Canvas, Button, Frame

# Configure Tesseract OCR path (update this path for your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class VirtualHandwritingKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Handwriting Keyboard")
        self.root.geometry("600x400")
        
        self.canvas = Canvas(self.root, bg="white", width=400, height=150)
        self.canvas.pack(pady=20)
        
        self.button_frame = Frame(self.root)
        self.button_frame.pack()
        
        self.clear_button = Button(self.button_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=0, padx=5)
        
        self.recognize_button = Button(self.button_frame, text="Recognize & Type", command=self.recognize_and_type)
        self.recognize_button.grid(row=0, column=1, padx=5)
        
        self.keyboard_frame = Frame(self.root)
        self.keyboard_frame.pack()
        
        self.create_keyboard()
        
        self.canvas.bind("<B1-Motion>", self.draw)
        
        self.image = np.ones((150, 400, 3), dtype=np.uint8) * 255
    
    def create_keyboard(self):
        keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Space']
        ]
        
        for r, row in enumerate(keys):
            for c, key in enumerate(row):
                btn = Button(self.keyboard_frame, text=key, width=5, height=2, command=lambda k=key: self.type_key(k))
                btn.grid(row=r, column=c, padx=2, pady=2)
    
    def type_key(self, key):
        if key == "Space":
            pyautogui.write(" ", interval=0.05)
        else:
            pyautogui.write(key.lower(), interval=0.05)
    
    def draw(self, event):
        x, y = event.x, event.y
        self.canvas.create_oval(x, y, x+5, y+5, fill='black', width=2)
        cv2.circle(self.image, (x, y), 2, (0, 0, 0), -1)
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = np.ones((150, 400, 3), dtype=np.uint8) * 255
    
    def recognize_and_type(self):
        filename = "handwriting.png"
        cv2.imwrite(filename, self.image)
        text = pytesseract.image_to_string(cv2.imread(filename), config='--psm 6')
        text = ''.join(filter(lambda x: x.isalnum() or x.isspace(), text))
        pyautogui.write(text.strip(), interval=0.05)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = VirtualHandwritingKeyboard(root)
    root.mainloop()