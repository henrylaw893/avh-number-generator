import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
from PIL import ImageTk, Image  
import time
from threading import Thread
from csv import reader
import os, sys
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer
FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

from random_generator import RandomGenerator
from stack_adt import ArrayStack
from number_box import NumberBox
from win_window import WinWindow

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def loadfont(fontpath, private=True, enumerable=False):
    '''
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    See https://msdn.microsoft.com/en-us/library/dd183327(VS.85).aspx

    '''
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
    # This function is written for Python 2.x. For 3.x, you
    # have to convert the isinstance checks to bytes and str
    if isinstance(fontpath, str):
        pathbuf = create_unicode_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExW
    elif isinstance(fontpath, bytes):
        pathbuf = create_string_buffer(fontpath)
        AddFontResourceEx = windll.gdi32.AddFontResourceExA
    else:
        raise TypeError('fontpath must be of type str or unicode')

    flags = (FR_PRIVATE if private else 0) | (FR_NOT_ENUM if not enumerable else 0)
    numFontsAdded = AddFontResourceEx(byref(pathbuf), flags, 0)
    return bool(numFontsAdded)

#Load the font
font_filepath = resource_path("./data/Poppins.ttf")
loadfont(font_filepath)

#LARGEFONT = tk.font(family = "Verdana", size = 35)
TITLEFONT = ("Poppins", 40, "bold")
STARTPAGEFONT = ("Poppins", 22)
INSTRUCTIONFONT = ("Poppins", 12)
STARTCOLOUR = "#253556"
GENBACKGROUND = "#253556"

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
        page1_frame = GenerationPage(container, self, start_frame)
        
        self.frames[StartPage] = start_frame
        self.frames[GenerationPage] = page1_frame
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
        
        self.controller = controller
        self.member_num_input = 0
        
        #create frame
        tk.Frame.__init__(self, parent)
        
        #grid configuration
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure([0,1,2,3],weight = 1)
        
        #Create base frames
        top_canvas = tk.Frame(self, width=700, height = 200)
        top_canvas.grid(row = 0, column = 0)
        centre_frame = tk.Frame(self, width = 800, height = 650)
        centre_frame.grid(row = 1, column = 0)
        

        #Import picture
        avh_logo_black = resource_path("./data/avh_black_logo.jpg")
        avh_logo = Image.open(avh_logo_black)
        avh_logo = avh_logo.resize((500, 225))
        self.avh_logo_image_tk = ImageTk.PhotoImage(avh_logo)
        logo = ttk.Label(self, image=self.avh_logo_image_tk)
        #place picture
        logo.grid(row=2,column = 0)

        #Member number label and entry
        member_num_lbl = ttk.Label(centre_frame, font = STARTPAGEFONT, text ="Please input the current highest member number below")
        member_num_lbl.pack(pady = 10)

        member_num_entry = ttk.Entry(centre_frame, font = STARTPAGEFONT, width = 10)
        # TODO: Automate this so that it saves to a file and reads that each time so number is always correct
        member_num_entry.insert(0,"600")
        member_num_entry.pack(pady = 10)
        
       

        #next page button button
        onto_generation_button = ttk.Button(centre_frame, text ="Draw Number", 
        command=lambda : self.next_page(member_num_entry.get()))
        onto_generation_button.pack(pady = 30, ipadx = 40, ipady = 20, side = "bottom")

        #quit button
        quit_button = ttk.Button(self, text = "Quit", command = lambda : controller.destroy())
        quit_button.grid(row = 3, column = 0)

        #Title
        title_label = tk.Label(top_canvas, font = TITLEFONT, text = "Arcadia Village Hotel\nClub17 Member Draw", justify = "center")
        title_label.pack(fill = tk.BOTH, expand = 1)

        #Instructions
        width = 275
        height = 450
        instruction_frame = tk.LabelFrame(self, 
        width = width, height = height, relief = "raised", borderwidth=8)
        instruction_frame.place(relx = 0.7, rely = 0.4)
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
        "Press space on the next screen to generate number.\nPress the left arrow key to return to this page.")
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

     #Next page generation function
    def next_page(self, member_num_entry: str):
        self.member_num_input = int(member_num_entry)
        self.controller.show_frame(GenerationPage)    

class GenerationPage(tk.Frame):
    def __init__(self, parent, controller, start_page):
        tk.Frame.__init__(self, parent)
        self.start_page = start_page
        self.controller = controller
        self.run_idle_animation = True
        self.space_times_pressed = 0

        def return_button_click(event):
            controller.show_frame(StartPage)
        
        #Pre-setup background set
        self["bg"] = GENBACKGROUND

        #Action controllers
        def leftKey(event):
            controller.show_frame(StartPage)

        self.bind("<Left>",leftKey)

        def escapeKey(event):
            controller.destroy()

        def stop_idle(event):
            self.run_idle_animation = False

        # TODO: Call move function on number object
        def start_idle(event):
            self.run_idle_animation = True
            self.idle_animation()            

        self.bind("<Escape>",escapeKey)

        self.bind("<space>",self.space_pressed)

        self.bind("<Right>", start_idle)

        self.bind("<Down>",stop_idle)

    def setup(self, event):
        self.screen_height = self.controller.winfo_screenheight()
        self.screen_width = self.controller.winfo_screenwidth()

        filepath = resource_path("./data/blacklist.csv")
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
        self.number_font = tk.font.Font(self.controller,font = "Segoe")
        self.number_font["size"] = -(int((self.screen_width/(num_boxes-2))/2.5))
        
        for i in range(num_boxes):
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
        #self.pointer_window = number_canvas.create_window(self.screen_width//2, number_canvas_height//7, window=self.pointer_line)        

        #backgrounds
        top_canvas["bg"] = GENBACKGROUND
        number_canvas["bg"] = GENBACKGROUND
        bottom_canvas["bg"] = GENBACKGROUND

        #Logo
        avh_logo_filepath = resource_path("./data/avh_logo_png.png")
        avh_logo = Image.open(avh_logo_filepath)
        avh_logo = avh_logo.resize((int(self.screen_width/2), int(bottom_canvas_height/1)))
        avh_logo_width, avh_logo_height = avh_logo.size

        avh_logo_outline_offset = self.screen_width//50
        bottom_canvas.create_rectangle(self.screen_width/2 - avh_logo_width/2 - avh_logo_outline_offset, 
                                       bottom_canvas_height/2.5 + avh_logo_height/2 + avh_logo_outline_offset +100,
                                       self.screen_width/2 + avh_logo_width/2 + avh_logo_outline_offset, 
                                       bottom_canvas_height/2.5 - avh_logo_height/2 - avh_logo_outline_offset,
                                       fill = "black")
        self.avh_logo_image_tk = ImageTk.PhotoImage(avh_logo)
        bottom_canvas.create_image(self.screen_width/2, bottom_canvas_height/2.5, image=self.avh_logo_image_tk)

        #Top text
        club17_font = tk.font.Font(self.controller,font = "Poppins")
        club17_font["size"] = int(self.screen_height//10)
        outline_offset = self.screen_width//250
        # Create outline text items
        outline_positions = [(-outline_offset, 0), (outline_offset, 0), (0, -outline_offset), (0, outline_offset)]

        for dx, dy in outline_positions:
            top_canvas.create_text(self.screen_width / 2 + dx, top_canvas_height / 1.5 + dy, text="Club17 Member Draw", font=club17_font, fill="black")
        #club17_text = tk.Text(top_canvas, font = club17_font, bg = GENBACKGROUND, fg="white")
        
        club17_text = top_canvas.create_text(self.screen_width/2,top_canvas_height/1.5, 
                                             text="Club17 Member Draw", font = club17_font, fill="white")
        
        self.idle_animation()

    def space_pressed(self, event):
        if self.space_times_pressed == 0:
            self.setup(event)
            self.space_times_pressed += 1
        elif self.space_times_pressed == 1:
            self.run_idle_animation = False
            self.startTime = time.time()
            self.run_normal_animation()
            self.space_times_pressed += 1
        elif self.space_times_pressed == 2:
            #Close winning window, bring back to idle animation
            self.win_window.hide()
            self.win_window = None
            self.run_idle_animation = True
            self.idle_animation()
            self.space_times_pressed = 1

    def get_blacklist(self, filepath: str) -> list:
        """
        hi
        """
        # Get the directory path of the current script (__file__)
        script_dir = os.path.dirname(sys.argv[0])

        # Construct the path to excel_data.csv relative to the script's directory
        csv_file_path = os.path.join(script_dir, 'blacklist.csv')
        with open(csv_file_path, newline='') as blacklist_csv_file:
            blacklist_reader = reader(blacklist_csv_file)
            blacklist_list = []
            for row in blacklist_reader:
                for number_string in row:
                    if number_string != "":
                        blacklist_list.append(int(number_string))
        return blacklist_list

    def run_normal_animation(self):
        timeStart = time.time()
        elapsedTime = timeStart - self.startTime
        dx = 150*pow(2,-0.5*(elapsedTime)) - 1.8
        #print(f"Elapsed time: {elapsedTime}, dx: {dx}")
        desired_frame_duration = 16
        if dx > 0:
            for number in self.numbers:
                    number.move_number(dx)
            elapsedTimeFrames = (time.time() - timeStart)*1000
            #print(elapsedTime)
            sleepTime = round(max(1,(desired_frame_duration-elapsedTimeFrames)))
            #print(f"Sleeptime: {sleepTime}")
            self.after(sleepTime,self.run_normal_animation)
        else:
            self.check_final_pos()
        
    def idle_animation(self):
        timeStart = time.time()
        desired_frame_duration = 16
        for number in self.numbers:
                number.move_number(1)
        if self.run_idle_animation:
            elapsedTime = (time.time() - timeStart)*1000
            sleepTime = round(max(1,(desired_frame_duration-elapsedTime)))
            self.after(sleepTime,self.idle_animation)

    def check_final_pos(self):
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
        for number_object in self.numbers:
            number_object.move_number(1)
        self.after(16,self.check_final_pos)
    
    def show_winner_window(self, winning_number: str):
        #Create winning frame
        winning_font = tk.font.Font(self.controller,font = "Poppins")
        winning_font["size"] = int(self.screen_height/5.5)
        border_width = self.screen_width//45
        self.win_window = WinWindow(self, font = winning_font, borderwidth=border_width, relief="solid")
        self.win_window.show_winner(winning_number=winning_number)

# Driver Code
app = tkinterApp()
app.mainloop()