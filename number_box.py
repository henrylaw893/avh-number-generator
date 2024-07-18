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
        print(f"padding = {self.padding}")

        # TODO: Create rectangle object
        num_padding = 1 + (num_boxes - 2)
        #width = num_padding*padding_width + (num_boxes-2)*width_boxes
        self.rectangle_width = (self.canvas_width - (self.padding*num_padding))/(num_boxes - 2)
        self.rectangle_height = self.canvas_height//2
        border_width = self.canvas_width//150
        self.canvas_rectangle = canvas.create_rectangle(0,0, self.rectangle_width, self.rectangle_height, fill="white", outline = "black", width = border_width)
        
        self.min_x = -self.rectangle_width/2

        self.canvas_text = canvas.create_text(0,0, text = ran_gen.generate_number(), fill = "black", font = font)

        self.inner_padding = self.rectangle_width/20
        # TODO: Use a command like this to get the width and height of a box
        self.text_height = 130
        self.text_width = 100
        #print(self.canvas.itemcget(self.canvas_text, "text"))
        #print(self.canvas.itemconfigure(self.canvas_text))


    def place_number(self, posx: float, posy: float) -> None:
        """
        Places the middle left side of the number box at (posx, posy)
        """
        #Top left corner of rectangle is placed at coordinates
        self.posx_rectangle = posx
        self.posy_rectangle = posy - self.rectangle_height/2
        self.canvas.moveto(self.canvas_rectangle, self.posx_rectangle, self.posy_rectangle)
        #Text is placed top left
        self.posx_text = posx + self.inner_padding
        self.posy_text = posy - self.text_height/2
        self.canvas.moveto(self.canvas_text, self.posx_text, self.posy_text)

    def move_number(self, dx):
        if self.posx_rectangle > self.min_x:
            self.posx_rectangle = self.posx_rectangle - dx
            self.posx_text = self.posx_text - dx
        else:
            self.posx_rectangle = self.posx_rectangle + (self.num_boxes)*(self.rectangle_width + self.padding) - dx
            self.posx_text = self.posx_text + (self.num_boxes)*(self.rectangle_width + self.padding) - dx
            #self.canvas_text = self.canvas.create_text(self.posx, self.posy, text = self.ran_gen.generate_number(), fill = "black", font = self.font)
        self.canvas.moveto(self.canvas_text, self.posx_text, self.posy_text)
        self.canvas.moveto(self.canvas_rectangle, self.posx_rectangle, self.posy_rectangle)
    
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

    def get_number_as_str(self) -> str:
        """
        Return current number being displayed by number box
        """
        return self.canvas.itemcget(self.canvas_text, "text")