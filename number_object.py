import tkinter as tk
import time

class NumberObject:
    def __init__(self, canvas: tk.Canvas, font :tk.font.Font, num_frames: int, ran_gen) -> None:
        self.canvas = canvas
        self.canvas_text = canvas.create_text(0,0, text = ran_gen.generate_number(), fill = "black", font = font)
        self.label = tk.Label(canvas,text = ran_gen.generate_number(), relief = "raised", borderwidth= 8)
        
        self.ran_gen = ran_gen
        self.num_frames = num_frames
        self.screen_width = canvas.winfo_screenwidth()
        self.run_idle_animation = True
        self.window = canvas.create_window(0,0, window=self.label)

        #set font
        self.label["font"] = font

        self.width = self.label.winfo_reqwidth()
        self.min_x = -self.width/2

        self.padding = ((self.screen_width - self.width*(num_frames-2))/(num_frames - 1))

    def place_number(self, posx, posy):
        self.posx = posx
        self.posy = posy
        self.canvas.coords(self.window, posx, posy)

    def move_number(self, dx):
        if self.posx > self.min_x:
            self.posx = self.posx - dx
        else:
            self.posx = self.posx + (self.num_frames)*(self.width + self.padding) - dx
            self.label["text"] = self.ran_gen.generate_number()
        self.canvas.coords(self.window, self.posx, self.posy)

    def idle_animation(self) -> None:
        new_posx = self.posx - self.speed_idle
        if new_posx < self.min_x:
            new_posx = new_posx + (self.screen_width + self.width)
            #update text
            self["text"] = self.ran_gen.generate_number()
        self.posx = new_posx
        self.place(x = self.posx, rely = 0.5, anchor = "w")
        if self.speed_initial > 0 and self.run_idle_animation:
            self.after(1, self.idle_animation)
    
    def begin_normal_animation(self, start_time):
        self.start_time = start_time
        self.speed = self.speed_initial
    
    def normal_animation(self) -> None:
        self.speed = (self.speed_initial)*(2.718 ** (-self.k*(time.time() - self.start_time))) - 0.2
        new_posx = self.posx - self.speed
        if new_posx < self.min_x:
            new_posx = new_posx + (self.screen_width + self.width)
            self.place(x = self.posx, rely = 0.5, anchor = "w")
            #update text
            self["text"] = self.ran_gen.generate_number()
        else:
            self.place(x = self.posx, rely = 0.5, anchor = "w")
        self.posx = new_posx

    def joiner_animation(self) -> None:
        new_posx = self.posx - self.speed
        if new_posx < self.min_x:
            new_posx = new_posx + (self.screen_width + self.width)
            self.place(x = self.posx, rely = 0.5, anchor = "w")
            #update text
            self["text"] = self.ran_gen.generate_number()
        else:
            self.place(x = self.posx, rely = 0.5, anchor = "w")
        self.posx = new_posx
        self.speed -= 0.01