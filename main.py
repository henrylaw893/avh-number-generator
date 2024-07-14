import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from PIL import ImageTk, Image  
import time
from threading import Thread

from random_generator import RandomGenerator
from stack_adt import ArrayStack

#LARGEFONT = tk.font(family = "Verdana", size = 35)
TITLEFONT = ("Poppins", 40, "bold")
STARTPAGEFONT = ("Poppins", 22)
INSTRUCTIONFONT = ("Poppins", 12)
STARTCOLOUR = "#253556"
GENBACKGROUND = "#253555"

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp 
    def __init__(self, *args, **kwargs): 
		
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        #resizing, centering
        self.title("Arcadia Village Hotel Draw")
        #self.eval('tk::PlaceWindow . center')
        self.attributes('-fullscreen',True)
        #Setting background
        #self.configure(bg = "black")
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True) 

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

        start_frame = StartPage(container,self)
        page1_frame = Page1(container, self, start_frame)
        
        self.frames[StartPage] = start_frame
        self.frames[Page1] = page1_frame
        start_frame.grid(row = 0, column = 0, sticky ="nsew")
        page1_frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
    def show_frame(self, next_frame):
        frame = self.frames[next_frame]
        frame.focus_set()
        frame.tkraise()

# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        
        self.member_num_input = 0
        self.blacklist_list = []
        def get_blacklist_list(member_num_input, blacklist_input) -> list:
            #test member number is an integer
            try:
                self.member_num_input = int(str(member_num_input))
            except:
                member_num_input_label = ttk.Label(self, font = STARTPAGEFONT, text ="Invalid member number input!")
                member_num_input_label.pack()
                self.focus_set()
                return
            
            blacklist_list = []
            blacklist_stack = ArrayStack(len(blacklist_input))
            for char in blacklist_input:
                if char == ",":
                    num = ""
                    while not blacklist_stack.is_empty():
                        num = blacklist_stack.pop() + num
                    blacklist_list.append(int(num))
                elif char ==" ":
                    continue
                else:
                    try:
                        num = int(char)
                        blacklist_stack.push(char)
                    except ValueError:
                        blacklist_input_label = ttk.Label(self, font = STARTPAGEFONT, text ="Invalid member number input!")
                        blacklist_input_label.pack()
                        self.focus_set()
                        return
            num = ""
            while not blacklist_stack.is_empty():
                num = blacklist_stack.pop() + num
            blacklist_list.append(int(num))
            self.blacklist_list = blacklist_list
            print(self.blacklist_list)
            controller.show_frame(Page1)
        
        #create frame
        tk.Frame.__init__(self, parent)
        
          

        #grid configuration
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure([0,1,2,3],weight = 1)
        
        #Create base frames
        top_frame = tk.Frame(self, width=700, height = 200)
        top_frame.grid(row = 0, column = 0)
        centre_frame = tk.Frame(self, width = 800, height = 650)
        centre_frame.grid(row = 1, column = 0)
        

        #Import picture
        avh_logo = Image.open("avh_black_logo.jpg")
        avh_logo = avh_logo.resize((500, 225))
        self.avh_logo_image_tk = ImageTk.PhotoImage(avh_logo)
        logo = ttk.Label(self, image=self.avh_logo_image_tk)
        #place picture
        logo.grid(row=2,column = 0)

        #Member number label and entry
        member_num_lbl = ttk.Label(centre_frame, font = STARTPAGEFONT, text ="Please input the current highest member number below")
        member_num_lbl.pack(pady = 10)

        member_num_entry = ttk.Entry(centre_frame, font = STARTPAGEFONT, width = 10)
        member_num_entry.insert(0,"600")
        member_num_entry.pack(pady = 10)
        

        blacklist_lbl = ttk.Label(centre_frame, font = STARTPAGEFONT, text ="Please input the numbers you would NOT like to be drawn\nInput example: 1,2,3,4,5", justify = "center")
        blacklist_lbl.pack(pady = 20)
        
        blacklist_entry = ttk.Entry(centre_frame, font = STARTPAGEFONT, width = 20)
        blacklist_entry.insert(0,"1,17,22,600")
        blacklist_entry.pack(pady = 10)

        #next page button button
        onto_generation_button = ttk.Button(centre_frame, text ="Onto generation", 
        command=lambda : get_blacklist_list(member_num_entry.get(),blacklist_entry.get()))
        onto_generation_button.pack(pady = 30, ipadx = 40, ipady = 20, side = "bottom")

        #quit button
        quit_button = ttk.Button(self, text = "Quit", command = lambda : controller.destroy())
        quit_button.grid(row = 3, column = 0)

        #Title
        title_label = tk.Label(top_frame, font = TITLEFONT, text = "Arcadia Village Hotel\nClub17 Member Draw", justify = "center")
        title_label.pack(fill = tk.BOTH, expand = 1)

        #Instructions
        width = 275
        height = 450
        instruction_frame = tk.LabelFrame(self, 
        width = width, height = height, relief = "raised", borderwidth=8)
        instruction_frame.place(relx = 0.754, rely = 0.29)
        # instruction_frame_x = instruction_frame.winfo_rootx()
        # instruction_frame_y = instruction_frame.winfo_rooty()
        
        # canvas = tk.Canvas(self, width = width, height = height)
        # canvas.place(x = instruction_frame_x,y = instruction_frame_y)
        # instruction_background = canvas.create_rectangle(instruction_frame_x, instruction_frame_y, instruction_frame_x + width, instruction_frame_y - height, fill = "black")
        # #instruction_background.place()

        instruction_title = tk.Label(instruction_frame, font = STARTPAGEFONT, text = "Instructions", justify = "center")
        instruction_title.pack(side = "top")

        instruction_text = tk.Label(instruction_frame, font = INSTRUCTIONFONT, text = "Press escape key to close program." +
        "\nEnter information and then press generate button\nto proceed to the generation screen.\n" +
        "Plug in HDMI adapter once on generation screen.\n" + 
        "Press enter on the next screen to generate number.\nPress the left arrow key to return to this page.")
        instruction_text.pack()
        # instruction_frame.tkraise()

        #Change style``
        self.style = ttk.Style(self)
        self.style.configure("TButton", font = STARTPAGEFONT)   
        
        #Background

        #Arrowkeys
        def escapeKey(event):
            controller.destroy()

        self.bind("<Escape>",escapeKey)

        
    
    #Function to store the blacklist information
    

		


# second window frame page1 
class Page1(tk.Frame):
	
    def __init__(self, parent, controller, start_page):

        tk.Frame.__init__(self, parent)

        self.start_page = start_page
        self.controller = controller
        self.run_idle_animation = True

        def return_button_click(event):
            controller.show_frame(StartPage)

        def generate_button_click(event):
            ran_gen = RandomGenerator(1,start_page.member_num_input,start_page.blacklist_list)
            number = ttk.Label(self, text=str(int(ran_gen.generate_number())))
            number.grid(row = 0, column = 0)
            self.focus_set()

        
        #Pre-setup background set
        self["bg"] = GENBACKGROUND
        
        #num0 = tk.Frame()


        #Action controllers
        def leftKey(event):
            controller.show_frame(StartPage)
            print("leftkey pressed")

        self.bind("<Left>",leftKey)

        def escapeKey(event):
            controller.destroy()

        def stop_idle(event):
            self.idle_animation = ~self.idle_animation

        self.bind("<Escape>",escapeKey)

        self.bind("<Return>",generate_button_click)

        self.bind("<space>",self.setup)

        self.bind("<Right>", self.idle_animation_loop)

        self.bind("<Down>",stop_idle)

    def setup(self, event):
        self.screen_height = self.controller.winfo_screenheight()
        self.screen_width = self.controller.winfo_screenwidth()

        self.ran_gen = RandomGenerator(1,self.start_page.member_num_input,self.start_page.blacklist_list)

        #Creating base frames
        #Sizing
        top_frame_height = self.screen_height/4.5
        number_frame_controller_height = self.screen_height/2.5
        bottom_frame_height = self.screen_height - top_frame_height - number_frame_controller_height

        #creation
        top_frame = tk.Frame(self, height = top_frame_height, width = self.screen_width)
        number_frame_controller = tk.Frame(self, height = number_frame_controller_height, width = self.screen_width)
        bottom_frame = tk.Frame(self, height = bottom_frame_height, width = self.screen_width)

        #placement
        top_frame.pack()
        number_frame_controller.pack()
        bottom_frame.pack()

        #Creating number frames
        #setting dimensions
        num_frames = 7
        padding = 0
        self.number_frame_width = self.screen_width/(num_frames-1) - padding #2 extra frames at the start and end
        self.number_frame_height = number_frame_controller_height - padding
        
        #Create number frames
        self.number_frames = []
        posx = 0 - self.number_frame_width
        number_font = tk.font.Font(self.controller,font = "Poppins")
        number_font["size"] = -(int((self.number_frame_width)/2.5))
        for i in range(num_frames):
            self.number_frames.append(NumberFrame(number_frame_controller, posx, self.number_frame_width, self.number_frame_height, self.ran_gen, number_font, num_frames,1))
            posx += self.number_frame_width

        #pointer
        # self.pointer_line = tk.Frame(number_frame_controller, width = self.screen_width//110, height = number_frame_controller_height/2,
        # borderwidth= self.screen_width//400, relief = "solid")
        # self.pointer_line.place(relx = 0.5, rely = 0.5, anchor = "center")

        #backgrounds
        top_frame["bg"] = GENBACKGROUND
        number_frame_controller["bg"] = GENBACKGROUND
        bottom_frame["bg"] = GENBACKGROUND

        #Logo
        avh_logo = Image.open("avh_logo_png.png")
        avh_logo = avh_logo.resize((550, 250))
        self.avh_logo_image_tk = ImageTk.PhotoImage(avh_logo)
        logo = ttk.Label(bottom_frame, image=self.avh_logo_image_tk)
        logo.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.idle_animation()
    
    def idle_animation(self):  
        #Move number frames
        self.speed = 3
        self.sleep_time = 1
        self.min_x = 0 - self.number_frame_width
        self.posy = self.number_frame_height
        self.last_frame = self.number_frames[-1]
        #self.posx_last_frame = self.number_frames[self.last_frame][1]
        #while self.run_idle_animation:
            #calculate new positions
    def idle_animation_loop(self, *args):
        for frame in self.number_frames:
            Thread(target = frame.idle_animation).start()
        
        # timestart = time.time()
        # for frame in self.number_frames:
        #     new_posx = frame.posx - self.speed
        #     if new_posx < self.min_x:
        #         new_posx = self.last_frame.posx + self.number_frame_width
        #         self.last_frame = frame
        #         print("teleported")
        #     frame.place(x = new_posx, y = 0)
        #     frame.posx = new_posx
        # timeend = time.time()
        # timetaken = (timeend - timestart)*1000
        # print(timetaken)
        # self.speed -= 0.0005
        # if self.speed > 0:
        #     self.after(int(1-timetaken), self.idle_animation_loop)

                    
    
    def idle_position(self, time):
        speed = -10 #negative for left
        return time*speed
            
class NumberFrame(tk.Frame):
    def __init__(self, controller, start_pos, width, height, ran_gen, font, num_frames, speed):
        tk.Frame.__init__(self, controller)

        self.configure(height = height, width = width, bg = GENBACKGROUND)

        self.posx = start_pos

        self.place(x = self.posx, y = 0)

        self.font = font
        
        self.ran_gen = ran_gen

        self.min_x = -width

        self.width = width

        self.num_frames = num_frames

        self.speed = 5

        self.number = tk.Label(self, text=self.ran_gen.generate_number())
        self.number["font"] = self.font
        self.number.place(rely = 0.5, relx = 0.5, anchor = "center")
        self.number.configure(borderwidth=width//35, relief = "ridge")

    def idle_animation(self):
        new_posx = self.posx - self.speed
        if new_posx < self.min_x:
            print(f"old: {new_posx}")
            new_posx = new_posx + self.width*(self.num_frames)
            print("moved")
            print(f"new: {new_posx}")
        self.place(x = new_posx, y = 0)
        self.posx = new_posx
        self.speed -= 0.001
        if self.speed > 0:
            self.after(1, self.idle_animation)


    def run_animation(self, speed):
        pass
        




# third window frame page2
class Page2(tk.Frame): 
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text ="Page 2", font = LARGEFONT)
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text ="Page 1",
                            command = lambda : controller.show_frame(Page1))

        # putting the button in its place by 
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text ="Startpage",
                            command = lambda : controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.grid(row = 2, column = 1, padx = 10, pady = 10)

# Driver Code
app = tkinterApp()
app.mainloop()
