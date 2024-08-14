import os
import sys
import tkinter as tk
from typing import Dict
from PIL import ImageTk, Image  


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class StartPage(tk.Frame):
    """A frame that is the start page that will be displayed upon execution

    The page provides a text input to set the highest number to be drawn
    It also contains text instructions on how to use the generator
    """

    def __init__(self, parent: tk.Frame, app: tk.Tk, fonts: Dict[str,tuple]):
        """Initializes the instance based on spam preference.

        Args:
            parent: a tk.Frame instance that will be the parent of the StartPage
            app: a tk.Tk app instance that dwill be used to quit the program
            fonts: a dictionary that contains tuples of font information in 
                tk.Font format ("name", size, other specifiers)
        """
        self.app = app
        self.member_num_input = 0
        
        #create frame
        tk.Frame.__init__(self, parent)
        
        #grid configuration
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure([0,1,2,3],weight = 1)
        
        #Create base frames
        top_canvas = tk.Frame(self, width=700, height = 200)
        top_canvas.grid(row = 0, column = 0)
        centre_frame = tk.Frame(self, width = 800, height = 650)
        centre_frame.grid(row = 1, column = 0)
        
        #Import picture
        avh_logo_black = resource_path("../data/avh_black_logo.jpg")
        avh_logo = Image.open(avh_logo_black)
        avh_logo = avh_logo.resize((500, 225))
        self.avh_logo_image_tk = ImageTk.PhotoImage(avh_logo)
        logo = tk.Label(self, image=self.avh_logo_image_tk)
        #place picture
        logo.grid(row=2,column = 0)

        #Member number label and entry
        member_num_lbl = tk.Label(centre_frame, font = fonts["start_page"], text ="Please input the current highest member number below")
        member_num_lbl.pack(pady = 10)

        member_num_entry = tk.Entry(centre_frame, font = fonts["start_page"], width = 10)
        # TODO: Automate this so that it saves to a file and reads that each time so number is always correct
        member_num_entry.insert(0,"600")
        member_num_entry.pack(pady = 10)
        
        #next page button button
        onto_generation_button = tk.Button(centre_frame, text ="Draw Number", 
            command=lambda : self.next_page(member_num_entry.get()))
        onto_generation_button.pack(pady = 30, ipadx = 40, ipady = 20, side = "bottom")

        #quit button
        quit_button = tk.Button(self, text = "Quit", command = lambda : app.destroy())
        quit_button.grid(row = 3, column = 0)

        #Title
        title_label = tk.Label(top_canvas, font = fonts["title"], text = "Arcadia Village Hotel\nClub17 Member Draw", justify = "center")
        title_label.pack(fill = tk.BOTH, expand = 1)

        #Instructions
        width = 275
        height = 450
        instruction_frame = tk.LabelFrame(self, 
        width = width, height = height, relief = "raised", borderwidth=8)
        instruction_frame.place(relx = 0.65, rely = 0.35)

        instruction_title = tk.Label(instruction_frame, font = fonts["start_page"], text = "Instructions", justify = "center")
        instruction_title.pack(side = "top")

        instruction_text = tk.Label(instruction_frame, font = fonts["instruction"], text = "Press escape key to close program." +
        "\nEnter information and then press generate button\nto proceed to the generation screen.\n" +
        "Plug in HDMI adapter once on generation screen.\n" + 
        "Press space on the next screen to show numbers scrolling\nPress space again to roll for a number\nPress space again after to reset to scrolling.")
        instruction_text.pack()

        # #Change style
        # self.style = tk.Style(self)
        # self.style.configure("TButton", font = fonts["start_page"])   

        #Arrowkeys
        def escapeKey(event):
            app.destroy()

        self.bind("<Escape>",escapeKey)
    
    def next_page(self, member_num_entry: str):
        self.member_num_input = int(member_num_entry)
        self.app.show_frame("GenerationPage")  