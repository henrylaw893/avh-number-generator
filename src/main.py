import os, sys
from ctypes import windll, byref, create_unicode_buffer, create_string_buffer

from generator_app import GeneratorApp
from start_page import StartPage
from generation_page import GenerationPage

FR_PRIVATE  = 0x10
FR_NOT_ENUM = 0x20

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def loadfont(fontpath, private=True, enumerable=False):
    """
    Makes fonts located in file `fontpath` available to the font system.

    `private`     if True, other processes cannot see this font, and this
                  font will be unloaded when the process dies
    `enumerable`  if True, this font will appear when enumerating fonts

    """
    # This function was taken from
    # https://github.com/ifwe/digsby/blob/f5fe00244744aa131e07f09348d10563f3d8fa99/digsby/src/gui/native/win/winfonts.py#L15
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

def main():
    #Load the font
    font_filepath = resource_path("../data/Poppins.ttf")
    loadfont(font_filepath)

    #Create fonts
    fonts = dict()
    fonts["title"] = ("Poppins", 40, "bold")
    fonts["start_page"] = ("Poppins", 22)
    fonts["instruction"] = ("Poppins", 12)
    
    #Set colour of the app's background
    background_colour = "#253556"

    #Create an app
    app = GeneratorApp()

    #Create each page
    start_page = StartPage(parent=app.frame, app=app, fonts=fonts, 
                           background_colour=background_colour)
    generation_page = GenerationPage(parent=app.frame, app=app, start_page=start_page, 
                                        background_colour=background_colour)

    #Add each page to the app
    app.add_frame(start_page, "StartPage")
    app.add_frame(generation_page, "GenerationPage")

    #Show the start page
    app.show_frame("StartPage")

    # Driver Code
    app.mainloop()

if __name__ == "__main__" :
    main()
    