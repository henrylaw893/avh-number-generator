"""
# TODO:
what does canvas.move do? is it better than .moveto?
figure out how to get the width and height of numbers as text
use width and height of numbers as text to improve relative positioning (.configureitem probably/canvas.itemcget)
    need to figure out the right option to use
am I using .moveto correctly?
fix winner selection function
"""


import tkinter as tk

class NumberBox:
    def __init__(self, canvas: tk.Canvas, font, num_boxes: int, canvas_width: int, canvas_height: int, ran_gen, ) -> None:
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
        """
        Places the middle left side of the number box at (posx, posy)
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
        """
        Returns the width of the number box (float)
        """
        return self.box_width
    
    def get_padding(self) -> int:
        """
        Return padding value of the number box (int)
        """
        return self.padding

    def get_number_as_str(self) -> str:
        """
        Return current number being displayed by number box
        """
        return self.canvas.itemcget(self.canvas_text, "text")
    
    def get_xpos(self) -> float:
        """
        Returns the current x position of the left side of the rectangle
        """
        return self.posx_rectangle