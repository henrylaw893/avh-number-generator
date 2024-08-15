"""
This module defines the main application structure for a tkinter-based random number 
generation program.

The module includes the `GeneratorApp` class, which is the main application window 
that manages different frames (or pages) within the application. The class provides 
methods to add frames and switch between them, enabling a multi-page user interface.

Typical usage example:

    app = GeneratorApp()
    app.add_frame(start_page_frame, "StartPage")
    app.show_frame("StartPage")
    app.mainloop()
"""
import tkinter as tk

class GeneratorApp(tk.Tk):
    """The main application class for managing frames in a tkinter-based GUI.

    The `GeneratorApp` class inherits from `tk.Tk` and provides functionality 
    to manage multiple frames (pages) within the application, handle fullscreen 
    mode, and control the layout and switching of different frames.

    Attributes:
        frame (tk.Frame): The main container frame for all the child frames.
        frames (dict): A dictionary mapping frame names (str) to their corresponding 
                       `tk.Frame` instances, used for switching between pages.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the GeneratorApp instance.

        This method sets up the main window, enables fullscreen mode, and 
        initializes the container frame where all other frames will be added.

        Args:
            *args: Variable length argument list for passing to the tk.Tk initializer.
            **kwargs: Arbitrary keyword arguments for passing to the tk.Tk initializer.
        """
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        #resizing, centering
        self.title("Arcadia Village Hotel Draw")
        self.attributes('-fullscreen',True)

        # creating a main frame that will contain everything
        self.frame = tk.Frame(self)
        self.frame.pack(side = "top", fill = "both", expand = True)

        self.frame.grid_rowconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

    def add_frame(self, frame: tk.Frame, name: str):
        """Adds a frame into the app instance that acts like a page

        Args:
            frame (tk.Frame): The frame instance to add to the application.
            name (str): The name associated with the frame, used for reference.
        """
        self.frames[name] = frame
        frame.grid(row = 0, column = 0, sticky ="nsew")

    def show_frame(self, name: str):
        """Displays the specified frame on the app
        
        Args:
            name (str): a string that references the frame to be displayed
        """
        display_frame = self.frames[name]
        display_frame.focus_set()
        display_frame.tkraise()
