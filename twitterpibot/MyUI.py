try:
    from tkinter import Tk
except ImportError:
    from Tkinter import Tk

_top = Tk()


def start():
    _top.mainloop()


def close():
    _top.quit()
