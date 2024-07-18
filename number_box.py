import tkinter as tk

class NumberBox:
    def __init__(self, canvas: tk.Canvas, font, num_boxes: int, canvas_width: int, canvas_height: int, ran_gen, ) -> None:
        self.canvas = canvas
        self.ran_gen = ran_gen
        self.num_boxes = num_boxes
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.padding = self.canvas_width//100
        print(f"padding = {self.padding}")

        self.canvas_text = canvas.create_text(0,0, text = ran_gen.generate_number(), fill = "black", font = font)
        # TODO: Create rectangle object
        num_padding = 1 + (num_boxes - 2)
        #width = num_padding*padding_width + (num_boxes-2)*width_boxes
        self.rectangle_width = (self.canvas_width - (self.padding*num_padding))/(num_boxes - 2)
        self.rectangle_height = self.canvas_height//2
        border_width = self.canvas_width//150
        self.canvas_rectangle = canvas.create_rectangle(0,0, self.rectangle_width, self.rectangle_height, fill="white", outline = "black", width = border_width)
        
        self.min_x = -self.rectangle_width/2

    def place_number(self, posx: float, posy: float) -> None:
        """
        Places the middle of the number box at (posx, posy)
        """
        self.posx = posx
        self.posy = posy
        #Text is placed in middle
        self.canvas.coords(self.canvas_text, posx, posy)
        #Top left corner of rectangle is placed at coordinates
        posx_rectangle = posx - self.rectangle_width/2
        posy_rectangle = posy - self.rectangle_height/2
        self.canvas.coords(self.canvas_rectangle, posx_rectangle, posy_rectangle, posx_rectangle+self.rectangle_width, posy_rectangle+self.rectangle_height)

    def move_number(self, dx):
        if self.posx > self.min_x:
            self.posx = self.posx - dx
        else:
            self.posx = self.posx + (self.num_boxes)*(self.rectangle_width + self.padding) - dx
            self.label["text"] = self.ran_gen.generate_number()
        self.canvas.coords(self.window, self.posx, self.posy)
    
    def get_width(self) -> float:
        """
        Returns the width of the number box (float)
        """
        return self.rectangle_width
    
    def get_padding(self) -> int:
        """
        Return padding value of the number box (int)
        """
        return self.padding