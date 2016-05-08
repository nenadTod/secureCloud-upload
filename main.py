from Tkinter import *
from gui import Gui
from controller import Controller
from model import Model

root = Tk()
model = Model()
control = Controller(root, model)
view = Gui(root, control, model)
model.set_view(view)

root.mainloop()

