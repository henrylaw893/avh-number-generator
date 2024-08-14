"""A one-line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.

Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""

import tkinter as tk

class GeneratorApp(tk.Tk):
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, *args, **kwargs):
        """Creates an instance of 

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

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

    def add_frame(self, frame: tk.Frame):
        """Adds a frame into the app instance that acts like a page
        
        Args:
            frame: a tk.Frame instance that will act as a page
        """
        self.frames[frame] = frame
        frame.grid(row = 0, column = 0, sticky ="nsew")

    def show_frame(self, frame: tk.Frame):
        """Displays the specified frame on the app
        
        Args:
            frame: the tk.Frame instance that will be displayed
        """
        display_frame = self.frames[frame]
        display_frame.focus_set()
        display_frame.tkraise()
