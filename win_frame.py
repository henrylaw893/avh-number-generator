import tkinter as tk

class WinFrame(tk.Frame):
    def __init__(self, controller: tk.Frame, winning_number:str) -> None:
        tk.Frame.__init__(self, controller)

        #self.configure(relwidth )