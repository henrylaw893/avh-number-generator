"""
This module contains the number box that is used to display the animated numbers
"""

import tkinter as tk

class NumberBox:
    """A class to create and animate a number box on a tkinter canvas.

    The `NumberBox` class handles the graphical representation of a number within 
    a rectangular box on a tkinter canvas. The number box can be placed at specific 
    coordinates, moved across the canvas, and its properties can be queried.

    Attributes:
        canvas (tk.Canvas): The canvas on which the number box is drawn.
        font: The font used to display the number inside the box.
        ran_gen: An instance of a random number generator to provide the numbers.
        num_boxes (int): The total number of boxes to display in the animation.
        canvas_width (int): The width of the canvas in pixels.
        canvas_height (int): The height of the canvas in pixels.
        padding (int): The padding between boxes in pixels.
        rectangle_width (float): The calculated width of the rectangle box.
        rectangle_height (float): The calculated height of the rectangle box.
        canvas_rectangle: The rectangle object drawn on the canvas.
        box_width (float): The total width of the box including the border.
        box_height (float): The total height of the box including the border.
        min_x (float): The minimum x-coordinate the box can move to before 
                       resetting.
        canvas_text: The text object that displays the number inside the box.
        text_height (float): The height of the text inside the box.
        text_width (float): The width of the text inside the box.
        inner_padding (float): The padding between the text and the box border.
    """

    def __init__(self, canvas: tk.Canvas, font, num_boxes: int, canvas_width: int, canvas_height: int, ran_gen, ) -> None:
        """Initializes the NumberBox with the provided canvas, font, and parameters.

        Args:
            canvas (tk.Canvas): The canvas on which to draw the number box.
            font: The font used for displaying the number.
            num_boxes (int): The number of boxes in the animation.
            canvas_width (int): The width of the canvas.
            canvas_height (int): The height of the canvas.
            ran_gen: An instance of a random number generator.
        """
        self.canvas = canvas
        self.font = font
        self.ran_gen = ran_gen
        self.num_boxes = num_boxes
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.padding = self.canvas_width//100

        # TODO: Create rectangle object
        num_padding = 1 + (num_boxes - 2)
        #width =  + (num_boxes-2)*(width_boxes)
        #width - borderwidth*(num_boxes-2) - num_padding*padding_width =  (num_boxes-2)*(width_boxes)
        border_width = self.canvas_width//150
        self.rectangle_width = (self.canvas_width - border_width*(num_boxes - 2)- (self.padding*num_padding))/(num_boxes - 2)
        self.rectangle_height = self.canvas_height//2
        self.canvas_rectangle = canvas.create_rectangle(0,0, self.rectangle_width, self.rectangle_height, fill="white", outline = "black", width = border_width)
        
        self.box_width = self.rectangle_width + border_width
        self.box_height = self.rectangle_height + border_width

        self.min_x = -self.box_width

        self.canvas_text = canvas.create_text(0,0, text = ran_gen.generate_number(), fill = "black", font = font)

        
        # TODO: Use a command like this to get the width and height of a box
        text_bound_box = self.canvas.bbox(self.canvas_text)
        self.text_height = text_bound_box[3] - text_bound_box[1]
        self.text_width = text_bound_box[2] - text_bound_box[0]

        self.inner_padding = (self.box_width-self.text_width)/2

    def place_number(self, posx: float, posy: float) -> None:
        """Places the number box at the specified coordinates.

        This method positions the top left corner of the rectangle and 
        the text within it at the given coordinates.

        Args:
            posx (float): The x-coordinate for the middle left side of the number box.
            posy (float): The y-coordinate for the middle left side of the number box.
        """
        #Top left corner of rectangle is placed at coordinates
        self.posx_rectangle = posx
        self.posy_rectangle = posy - self.box_height/2
        self.canvas.moveto(self.canvas_rectangle, self.posx_rectangle, self.posy_rectangle)
        #Text is placed top left
        self.posx_text = posx + self.text_width/2 + self.inner_padding
        self.posy_text = posy
        self.canvas.coords(self.canvas_text, self.posx_text, self.posy_text)

    def move_number(self, dx):
        """Moves the number box horizontally by the specified distance.

        If the box moves beyond the left edge of the canvas, it resets 
        to the right side and displays a new number.

        Args:
            dx (float): The distance to move the box horizontally.
        """
        if self.posx_rectangle > self.min_x:
            self.canvas.move(self.canvas_text, -dx, 0)
            self.canvas.move(self.canvas_rectangle, -dx, 0)
            self.posx_rectangle -= dx
        else:
            self.canvas.itemconfig(self.canvas_text, text=self.ran_gen.generate_number())
            self.canvas.move(self.canvas_text, (self.num_boxes)*(self.box_width + self.padding) - dx, 0)
            self.canvas.move(self.canvas_rectangle, (self.num_boxes)*(self.box_width + self.padding) - dx, 0)
            self.posx_rectangle += (self.num_boxes)*(self.box_width + self.padding) - dx
                
    def get_width(self) -> float:
        """Returns the width of the number box.

        Returns:
            float: The width of the box including the border.
        """
        return self.box_width
    
    def get_padding(self) -> int:
        """Returns the padding between boxes.

        Returns:
            int: The padding value in pixels.
        """
        return self.padding

    def get_number_as_str(self) -> str:
        """Returns the current number displayed in the box.

        Returns:
            str: The number currently displayed in the box as a string.
        """
        return self.canvas.itemcget(self.canvas_text, "text")
    
    def get_xpos(self) -> float:
        """Returns the current x-coordinate of the number box.

        Returns:
            float: The x-coordinate of the left side of the rectangle.
        """
        return self.posx_rectangle