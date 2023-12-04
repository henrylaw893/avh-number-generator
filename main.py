import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image  

from random_generator import RandomGenerator
from stack_adt import ArrayStack

window = tk.Tk()
avh_logo = Image.open("avh_black_logo.jpg")
#avh_logo = avh_logo.resize((150, 100))
avh_logo_image_tk = ImageTk.PhotoImage(avh_logo)

logo = ttk.Label(image=avh_logo_image_tk)
#place picture
logo.pack()

window.mainloop()
