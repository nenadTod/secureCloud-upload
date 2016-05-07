from Tkinter import *
from gui import Gui
from controller import Controller
from model import Model

root = Tk()
view = Gui(root)
model = Model(view)
control = Controller(model)
root.mainloop()

