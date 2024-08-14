import tkinter as tk

class WinWindow:
    """Summary of class here.

    Longer class information...
    Longer class information...

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, controller: tk.Frame, font, borderwidth: int, relief: str) -> None:
        self.frame = tk.Frame(controller, borderwidth=borderwidth, relief=relief)
        self.label = tk.Label(self.frame, font=font)

    def show_winner(self, winning_number: str):
        self.label["text"] = winning_number
        self.frame.place(relx = 0.5, rely = 0.45, anchor = "center", relheight= 0.6, relwidth = 0.9)
        self.label.place(relx = 0.5, rely = 0.5, anchor = "center")

    def hide(self):
        self.frame.place_forget()
        self.label.place_forget()
