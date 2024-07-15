import tkinter as tk
import time

class NumberObject(tk.Label):
    def __init__(self, controller, font, num_frames, ran_gen) -> None:
        tk.Label.__init__(self, controller)
        self.ran_gen = ran_gen
        self.num_frames = num_frames
        self.screen_width = controller.winfo_screenwidth()
        self.run_idle_animation = True

        #Set number
        self.configure(text = ran_gen.generate_number(), relief = "raised", borderwidth= 8)

        #set font
        self["font"] = font

        self.width = self.winfo_reqwidth()
        self.speed_idle = 0.1
        self.speed_initial = 15
        self.k = 0.25

    def place_number(self, posx):
        self.posx = posx
        self.min_x = -self.width
        self.place(x = posx, rely = 0.5, anchor = "w")

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