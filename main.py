from Tkinter import *
from gui import Gui
from controller import Controller
from model import Model

root = Tk()
model = Model()
control = Controller(model)
view = Gui(root, control, model)
control.view = view
model.view = view

root.mainloop()

