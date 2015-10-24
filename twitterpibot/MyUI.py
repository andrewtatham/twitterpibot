try:
    from tkinter import Tk
except ImportError:
    from Tkinter import Tk

top = Tk()


def Start():
    top.mainloop()


def Close():
    top.quit()
