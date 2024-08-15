"""
This module defines the graphical user interface for a random number generation application.

The module includes classes and functions responsible for setting up the main window, handling 
events, performing animations, and displaying the winning number. The `GenerationPage` class 
is the core of the application, managing the user interactions and visual elements during the 
random number generation process. The `WinWindow` class is used to display the winning number 
in a dedicated window.

Typical usage example:

    app = tk.Tk()
    start_page = StartPage(app)
    gen_page = GenerationPage(parent_frame, app, start_page, "#253556")
    gen_page.setup()
    app.mainloop()
"""
import os
import sys

from csv import reader
import tkinter as tk
from tkinter.font import Font
from time import time
from PIL import ImageTk
from PIL import Image

from number_box import NumberBox
from random_generator import RandomGenerator
from start_page import StartPage

def resource_path(relative_path):
    """Get the absolute path to a resource, ensuring compatibility with PyInstaller.

    Args:
        relative_path (str): The relative path to the resource.

    Returns:
        str: The absolute path to the resource.
    """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class GenerationPage(tk.Frame):
    """A page in the application responsible for generating and displaying random numbers.

    This page handles the main number generation animation, the user interface layout, and interactions such as key presses.

    Attributes:
        start_page (StartPage): Reference to the StartPage for retrieving settings and data.
        app (tk.Tk): The main application instance.
        run_idle_animation (bool): Indicates whether the idle animation should be running.
        space_times_pressed (int): Counter for the number of times the space bar has been pressed.
        background_colour (str): Background color for the page.
        prev_screen_width (int): Previous screen width before resizing.
        prev_screen_height (int): Previous screen height before resizing.
    """

    def __init__(self, parent: tk.Frame, app: tk.Tk, start_page: StartPage, background_colour: str):
        """Initialises a GenerationPage instance that will be shown when generating a random number

        Args:
            parent: a tk.Frame instance that will be the parent of the StartPage
            app: a tk.Tk app instance that will be used to quit the program
            start_page: a StartPage instance that the GenerationPage will return to and get blacklist from
            background_colour: a str that represents the desired background colour (e.g. #253556)
        """
        tk.Frame.__init__(self, parent)
        self.start_page = start_page
        self.app = app
        self.run_idle_animation = True
        self.space_times_pressed = 0
        self.background_colour = background_colour
        self.prev_screen_width = self.app.winfo_screenwidth()
        self.prev_screen_height = self.app.winfo_screenheight()
        
        #Pre-setup background set
        self["bg"] = background_colour

        #Action controllers
        def leftKey(event):
            app.show_frame("StartPage")

        self.bind("<Left>",leftKey)

        def escapeKey(event):
            app.destroy()

        def stop_idle(event):
            self.run_idle_animation = False

        def start_idle(event):
            self.run_idle_animation = True
            self.idle_animation()            

        self.bind("<Escape>",escapeKey)

        self.bind("<space>",self.space_pressed)

        self.bind("<Right>", start_idle)

        self.bind("<Down>",stop_idle)

        self.bind("<Configure>", self.on_resize)

    def setup(self):
        """Sets up the graphical layout and animations for the generation page.

        This function configures the canvases, creates the number display boxes,
        initializes the pointer, and starts the idle animation.
        """
        self.screen_height = self.app.winfo_screenheight()
        self.screen_width = self.app.winfo_screenwidth()

        filepath = resource_path("../blacklist.csv")
        blacklist = self.get_blacklist(filepath)
        self.ran_gen = RandomGenerator(1,self.start_page.member_num_input,blacklist)

        #Creating base frames
        #Sizing
        top_canvas_height = self.screen_height/4.5
        number_canvas_height = self.screen_height/2.5
        bottom_canvas_height = self.screen_height - top_canvas_height - number_canvas_height

        #creation
        top_canvas = tk.Canvas(self, height = top_canvas_height, width = self.screen_width, borderwidth=0, highlightthickness=0)
        number_canvas = tk.Canvas(self, height = number_canvas_height, width = self.screen_width, borderwidth=0, highlightthickness=0)
        bottom_canvas = tk.Canvas(self, height = bottom_canvas_height, width = self.screen_width, borderwidth=0, highlightthickness=0)

        #placement
        top_canvas.pack()
        number_canvas.pack()
        bottom_canvas.pack()

        #Creating number frames
        #setting dimensions
        num_boxes = 7
        self.numbers = []
        self.number_font = Font(family = "Segoe")
        self.number_font["size"] = -(int((self.screen_width/(num_boxes-2))/2.5))
        
        for _ in range(num_boxes):
            self.numbers.append(NumberBox(number_canvas, self.number_font, num_boxes, self.screen_width, number_canvas_height, self.ran_gen))
        
        #setting dimensions
        self.number_box_width = self.numbers[0].get_width()
        padding = self.numbers[0].get_padding()

        #Placing in initial positions
        posx = -self.number_box_width
        posy = number_canvas_height/2
        for number in self.numbers:
            number.place_number(posx, posy)
            posx = posx + self.number_box_width + padding

        #Creating pointer
        triangle_width = self.screen_width//15
        triangle_height = self.screen_height//15
        triangle_posy = number_canvas_height//10
        x0 = self.screen_width/2 - triangle_width//2
        y0 = triangle_posy
        x1 = self.screen_width/2 + triangle_width//2
        y1 = triangle_posy
        x2 = self.screen_width/2
        y2 = triangle_posy + triangle_height

        points = [x0,y0,x1,y1,x2,y2]
        
        self.pointer_line = number_canvas.create_polygon(points,
        width= self.screen_width//200, outline = "black", fill = "white")

        #backgrounds
        top_canvas["bg"] = self.background_colour
        number_canvas["bg"] = self.background_colour
        bottom_canvas["bg"] = self.background_colour

        #Logo
        avh_logo_filepath = resource_path("../data/avh_logo_png.png")
        avh_logo = Image.open(avh_logo_filepath)
        avh_logo = avh_logo.resize((int(self.screen_width/2), int(bottom_canvas_height/1.2)))
        avh_logo_width, avh_logo_height = avh_logo.size

        avh_logo_ypos = bottom_canvas_height/2.2

        avh_logo_outline_offset = self.screen_width//250
        bottom_canvas.create_rectangle(self.screen_width/2 - avh_logo_width/2 - avh_logo_outline_offset, 
                                       avh_logo_ypos - avh_logo_height/2 - avh_logo_outline_offset,
                                       self.screen_width/2 + avh_logo_width/2 + avh_logo_outline_offset, 
                                       avh_logo_ypos + avh_logo_height/2 + avh_logo_outline_offset,
                                       fill = "black")
        self.avh_logo_image_tk = ImageTk.PhotoImage(avh_logo)
        bottom_canvas.create_image(self.screen_width/2, avh_logo_ypos, image=self.avh_logo_image_tk)

        #Top text
        club17_font = tk.font.Font(self.app,font = "Poppins")
        club17_font["size"] = int(self.screen_height//10)
        outline_offset = self.screen_width//250
        
        # Create outline text items
        outline_positions = [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]

        for dx, dy in outline_positions:
            top_canvas.create_text(self.screen_width / 2 + dx, top_canvas_height / 1.5 + dy, text="Club17 Member Draw", font=club17_font, fill="black")
        
        top_canvas.create_text(self.screen_width/2,top_canvas_height/1.5, 
                                text="Club17 Member Draw", font = club17_font, fill="white")
        
        self.idle_animation()

    def on_resize(self, event):
        """Handles the resize event to adjust the layout of the GenerationPage.

        This function is triggered whenever the window is resized and updates the 
        screen dimensions stored in the page.

        Args:
            event (tk.Event): The resize event triggered by the window manager.
        """
        # Get new width and height
        new_width = self.app.winfo_screenwidth()
        new_height = self.app.winfo_screenheight()

        #Check if the event was actually a resize
        if (new_width != self.prev_screen_width) | (new_height != self.prev_screen_height):
            print("screen resized")
            print(f"width: {self.app.winfo_screenwidth()}, height: {self.app.winfo_screenheight()}")

    def space_pressed(self, event):
        """Handles the space key press event to control the number generation animation.

        The first press starts the animation, and the second press stops it and resets the state.

        Args:
            event (tk.Event): The key press event triggered by the space bar.
        """
        if self.space_times_pressed == 0:
            self.run_idle_animation = False
            self.startTime = time()
            self.run_normal_animation()
            self.space_times_pressed += 1
        elif self.space_times_pressed == 1:
            #Close winning window, bring back to idle animation
            self.win_window.hide()
            self.win_window = None
            self.run_idle_animation = True
            self.idle_animation()
            self.space_times_pressed = 0

    def get_blacklist(self, filepath: str) -> list:
        """Reads and returns the blacklist from a CSV file.

        Args:
            filepath (str): The file path to the blacklist CSV.

        Returns:
            list: A list of blacklisted numbers.
        """
        # Get the directory path of the current script (__file__)
        script_dir = os.path.dirname(sys.argv[0])

        # Construct the path to excel_data.csv relative to the script's directory
        csv_file_path = os.path.join(script_dir, filepath)
        with open(csv_file_path, newline='') as blacklist_csv_file:
            blacklist_reader = reader(blacklist_csv_file)
            blacklist_list = []
            for row in blacklist_reader:
                for number_string in row:
                    if number_string != "":
                        blacklist_list.append(int(number_string))
        return blacklist_list

    def run_normal_animation(self):
        """Performs the main number generation animation.

        The animation runs in a loop, updating the positions of the number boxes to simulate spinning.
        """
        timeStart = time()
        elapsedTime = timeStart - self.startTime
        dx = 150*pow(2,-0.5*(elapsedTime)) - 1.8
        desired_frame_duration = 16
        if dx > 0:
            for number in self.numbers:
                    number.move_number(dx)
            elapsedTimeFrames = (time() - timeStart)*1000
            sleepTime = round(max(1,(desired_frame_duration-elapsedTimeFrames)))
            self.after(sleepTime,self.run_normal_animation)
        else:
            self.check_final_pos()
        
    def idle_animation(self):
        """Runs the idle animation, making number boxes move slowly.

        The idle animation is a low-speed movement of the number boxes, creating a dynamic effect when the user is not interacting.
        """
        timeStart = time()
        desired_frame_duration = 16
        for number in self.numbers:
                number.move_number(1)
        if self.run_idle_animation:
            elapsedTime = (time() - timeStart)*1000
            sleepTime = round(max(1,(desired_frame_duration-elapsedTime)))
            self.after(sleepTime,self.idle_animation)

    def check_final_pos(self):
        """Check the final position of the pointer in relation to the number boxes.

        This function determines whether the pointer is aligned with any number box at the end 
        of the animation. If aligned, it identifies the winning number and proceeds to display it; 
        otherwise, it continues the animation until alignment is achieved.
        """
        self.pointer_x = self.screen_width//2
        valid_end = False
        for number_box in self.numbers:
            x_pos = int(number_box.get_xpos())
            val_range = range(x_pos,x_pos + int(self.number_box_width))
            if self.pointer_x in val_range:
                valid_end = True
                winning_number = number_box
        if not valid_end:
            self.after(16, self.run_joiner_animation)
        else:
            winning_number = winning_number.get_number_as_str()
            self.after(1000, self.show_winner_window(winning_number))
    
    def run_joiner_animation(self):
        """Run the joiner animation for the number boxes.

        This function animates the movement of the number boxes until one is aligned with the 
        pointer. It checks the final position of the pointer in each iteration to determine 
        if the animation should continue or stop.
        """
        for number_object in self.numbers:
            number_object.move_number(1)
        self.after(16,self.check_final_pos)
    
    def show_winner_window(self, winning_number: str):
        """Display the winner window with the winning number.

        This function creates a new window that displays the winning number 
        in a prominently styled manner.

        Args:
            winning_number (str): The number that has won the draw.
        """
        winning_font = tk.font.Font(self.app,font = "Poppins")
        winning_font["size"] = int(self.screen_height/5.5)
        border_width = self.screen_width//45
        self.win_window = WinWindow(self, font = winning_font, borderwidth=border_width, relief="solid")
        self.win_window.show_winner(winning_number=winning_number)

class WinWindow:
    """A window to display the winning number in the number draw.

    The WinWindow class is responsible for creating and managing the display
    of the winning number in a separate frame.

    Attributes:
        frame (tk.Frame): The frame that contains the winner label.
        label (tk.Label): The label that displays the winning number.
    """

    def __init__(self, controller: tk.Frame, font, borderwidth: int, relief: str) -> None:
        """Initialize the WinWindow instance.

        Args:
            controller (tk.Frame): The parent frame that controls this window.
            font (tk.font.Font): The font used for displaying the winning number.
            borderwidth (int): The width of the border around the window frame.
            relief (str): The type of border relief (e.g., "solid").
        """
        self.frame = tk.Frame(controller, borderwidth=borderwidth, relief=relief)
        self.label = tk.Label(self.frame, font=font)

    def show_winner(self, winning_number: str):
        """Display the winning number in the window.

        This function updates the label to show the winning number and 
        places the window in the center of the screen.

        Args:
            winning_number (str): The number that has won the draw.
        """
        self.label["text"] = winning_number
        self.frame.place(relx = 0.5, rely = 0.45, anchor = "center", relheight= 0.6, relwidth = 0.9)
        self.label.place(relx = 0.5, rely = 0.5, anchor = "center")

    def hide(self):
        """Hide the winner window.

        This function hides the window by removing the frame and label from the screen.
        """
        self.frame.place_forget()
        self.label.place_forget()
