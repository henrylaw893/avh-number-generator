"""
This module defines a tkinter frame that is used as the start frame for the Random Number Generator.

The frame allows the user to input the highest number they want to be drawn
"""
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

    def __init__(self, parent: tk.Frame, app: tk.Tk, fonts: Dict[str,tuple], background_colour: str):
        """Initializes the instance based on spam preference.

        Args:
            parent: a tk.Frame instance that will be the parent of the StartPage
            app: a tk.Tk app instance that dwill be used to quit the program
            fonts: a dictionary that contains tuples of font information in 
                tk.Font format ("name", size, other specifiers)
            background_colour: a str that represents the desired background colour (e.g. #253556)
        """
        self.app = app
        self.member_num_input = 0
        
        #create frame
        tk.Frame.__init__(self, parent)

        #Get screen height and width
        self.screen_height = self.app.winfo_screenheight()
        self.screen_width = self.app.winfo_screenwidth()
        
        #grid configuration
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure([0,1,2,3],weight = 1)
        self["bg"] = background_colour
        
        #Set canvas sizing
        top_canvas_height = self.screen_height/4.5
        lower_top_canvas_height = self.screen_height/12
        centre_canvas_height = self.screen_height/2.5
        bottom_canvas_height = self.screen_height - top_canvas_height - centre_canvas_height
        
        #Create canvasses
        top_canvas = tk.Canvas(self, width=self.screen_width, height=top_canvas_height, bg=background_colour, borderwidth=0, highlightthickness=0)
        lower_top_canvas = tk.Canvas(self, width=self.screen_width, height=lower_top_canvas_height, bg=background_colour, borderwidth=0, highlightthickness=0)
        centre_canvas = tk.Canvas(self, width=self.screen_width, height=centre_canvas_height, bg=background_colour, borderwidth=0, highlightthickness=0)
        bottom_canvas = tk.Canvas(self, height = bottom_canvas_height, width = self.screen_width, bg=background_colour, borderwidth=0, highlightthickness=0)
        
        #Place canvasses
        top_canvas.pack()
        lower_top_canvas.pack()
        centre_canvas.pack()
        bottom_canvas.pack()

        #Title
        #Top text
        club17_font = tk.font.Font(self.app,font = fonts["title"])
        club17_font["size"] = int(self.screen_height//10)
        outline_offset = self.screen_width//250
        
        # Create outline text items
        outline_positions = [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]

        for dx, dy in outline_positions:
            top_canvas.create_text(self.screen_width / 2 + dx, top_canvas_height / 1.5 + dy, text="Club17 Member Draw", font=club17_font, fill="black")
        
        top_canvas.create_text(self.screen_width/2,top_canvas_height/1.5, 
                                text="Club17 Member Draw", font = club17_font, fill="white")
        
        # Creating Input text 
        # Create outline text items
        input_text_xpos = self.screen_width / 2
        input_text_ypos = lower_top_canvas_height / 2

        outline_offset = 2
        outline_positions = [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]

        for dx, dy in outline_positions:
            lower_top_canvas.create_text(input_text_xpos + dx, input_text_ypos + dy, text="Please input the current highest member number below", font=fonts["start_page"], fill="black")
        
        lower_top_canvas.create_text(input_text_xpos, input_text_ypos, 
                                    text="Please input the current highest member number below", 
                                    font = fonts["start_page"], fill="white")

        member_num_entry = tk.Entry(centre_canvas, font = fonts["start_page"], width = 10)
        # TODO: Automate this so that it saves to a file and reads that each time so number is always correct
        member_num_entry.insert(0,"600")
        member_num_entry.pack()
        
        #next page button 
        onto_generation_button = tk.Button(centre_canvas, text ="Draw Number", font = fonts["start_page"],
            command=lambda : self.next_page(member_num_entry.get()))
        onto_generation_button.pack(pady = 30, ipadx = 40, ipady = 20, side = "bottom")

        #Instructions
        width = 275
        height = 450
        instruction_frame = tk.LabelFrame(self, 
        width = width, height = height, relief = "raised", borderwidth=8)
        instruction_frame.place(relx = 0.65, rely = 0.29)

        instruction_title = tk.Label(instruction_frame, font = fonts["start_page"], text = "Instructions", justify = "center")
        instruction_title.pack(side = "top")

        instruction_text = tk.Label(instruction_frame, font = fonts["instruction"], text = 
                                    "Press escape key to close program.\n" +
                                    "Enter information and then press Draw Number\n" + 
                                    "Press space on the next screen to show numbers scrolling\n" +
                                    "Press space again to roll for a number\n" +
                                    "Press space again after to reset\n" +
                                    "Left arrowkey to go back")
        instruction_text.pack()

        #Import picture
        avh_logo_black = resource_path("../data/avh_black_logo.jpg")
        avh_logo = Image.open(avh_logo_black)
        avh_logo = avh_logo.resize((600, 325))
        self.avh_logo_image_tk = ImageTk.PhotoImage(avh_logo)

        #Place picture
        avh_logo_x = self.screen_width/2
        avh_logo_y = bottom_canvas_height/3
        bottom_canvas.create_image(avh_logo_x, avh_logo_y, image=self.avh_logo_image_tk)

        #quit button
        quit_button = tk.Button(bottom_canvas, text = "Quit", font = fonts["start_page"], command = lambda : app.destroy())
        
        quit_button_x = self.screen_width//2 - quit_button.winfo_reqwidth()/2
        quit_button_y = bottom_canvas_height//1.25
        quit_button.place(x = quit_button_x ,y = quit_button_y)

        #Arrowkeys
        def escapeKey(event):
            app.destroy()

        self.bind("<Escape>", escapeKey)
    
    def next_page(self, member_num_entry: str):
        self.member_num_input = int(member_num_entry)
        self.app.frames["GenerationPage"].setup()
        self.app.show_frame("GenerationPage")
